import csv
import json
import os

from cloudshell.tg.breaking_point.flows.bp_download_test_file_flow import BPDownloadTestFileFlow
from cloudshell.tg.breaking_point.helpers.port_reservation_helper import PortReservationHelper
import re

import io
from xml.etree import ElementTree

from cloudshell.tg.breaking_point.flows.bp_load_configuration_file_flow import BPLoadConfigurationFileFlow
from cloudshell.tg.breaking_point.flows.bp_load_pcap_file_flow import BPLoadPcapFileFlow
from cloudshell.tg.breaking_point.flows.bp_results_flow import BPResultsFlow
from cloudshell.tg.breaking_point.flows.bp_statistics_flow import BPStatisticsFlow
from cloudshell.tg.breaking_point.flows.bp_test_execution_flow import BPTestExecutionFlow
from cloudshell.tg.breaking_point.helpers.bp_cs_reservation_details import BPCSReservationDetails
from cloudshell.tg.breaking_point.helpers.quali_rest_api_helper import QualiAPIHelper, create_quali_api_instance
from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestClientUnauthorizedException
from cloudshell.tg.breaking_point.runners.bp_runner import BPRunner
from cloudshell.tg.breaking_point.runners.exceptions import BPRunnerException


class BPTestRunner(BPRunner):
    def __init__(self, context, logger, api):
        """
        Test runner, hold current configuration fo specific test
        :param context:
        :param logger:
        :param api:
        """
        super(BPTestRunner, self).__init__(context, logger, api)
        self._test_id = None
        self._test_name = None

        self.__test_execution_flow = None
        self.__test_statistics_flow = None
        self.__test_results_flow = None
        self.__test_configuration_file_flow = None
        self.__download_test_file_flow = None
        self.__reservation_details = None
        self.__port_reservation_helper = None

    @BPRunner.context.setter
    def context(self, value):
        """
        Override setter for context
        :param value: 
        :return: 
        """
        BPRunner.context.fset(self, value)
        self._cs_reservation_details.context = value

    @BPRunner.logger.setter
    def logger(self, value):
        """
        Override setter for logger
        :param value: 
        :return: 
        """
        BPRunner.logger.fset(self, value)
        self._cs_reservation_details.logger = value

    @BPRunner.api.setter
    def api(self, value):
        """
        Override setter for api
        :param value: 
        :return: 
        """
        BPRunner.api.fset(self, value)
        self._cs_reservation_details.api = value

    @property
    def _test_execution_flow(self):
        """
        :return:
        :rtype: BPTestExecutionFlow
        """
        if not self.__test_execution_flow:
            self.__test_execution_flow = BPTestExecutionFlow(self._session_context_manager, self.logger)
        return self.__test_execution_flow

    @property
    def _test_statistics_flow(self):
        """
        :return:
        :rtype: BPStatisticsFlow
        """
        if not self.__test_statistics_flow:
            self.__test_statistics_flow = BPStatisticsFlow(self._session_context_manager, self.logger)
        return self.__test_statistics_flow

    @property
    def _test_results_flow(self):
        """
        :return:
        :rtype: BPResultsFlow
        """
        if not self.__test_results_flow:
            self.__test_results_flow = BPResultsFlow(self._session_context_manager, self.logger)
        return self.__test_results_flow

    @property
    def _test_configuration_file_flow(self):
        if not self.__test_configuration_file_flow:
            self.__test_configuration_file_flow = BPLoadConfigurationFileFlow(self._session_context_manager,
                                                                              self.logger)
        return self.__test_configuration_file_flow

    @property
    def _download_test_file_flow(self):
        if not self.__download_test_file_flow:
            self.__download_test_file_flow = BPDownloadTestFileFlow(self._session_context_manager,
                                                                    self.logger)
        return self.__download_test_file_flow

    @property
    def _cs_reservation_details(self):
        """
        :return:
        :rtype: BPCSReservationDetails
        """
        if not self.__reservation_details:
            self.__reservation_details = BPCSReservationDetails(self.context, self.logger, self.api)
        return self.__reservation_details

    @property
    def _resource_address(self):
        """
        Override property for resource address
        :return: 
        """
        return self._cs_reservation_details.get_chassis_address()

    @property
    def _username(self):
        """
        Override property for username
        :return: 
        """
        return self._cs_reservation_details.get_chassis_user()

    @property
    def _password(self):
        """
        Override property for password
        :return: 
        """
        return self._cs_reservation_details.get_chassis_password()

    @property
    def _port_reservation_helper(self):
        """
        Port reservation operations
        :return:
        :rtype: PortReservationHelper
        """
        if not self.__port_reservation_helper:
            self.__port_reservation_helper = PortReservationHelper(self._session_context_manager,
                                                                   self._cs_reservation_details,
                                                                   self.logger)
        return self.__port_reservation_helper

    def _get_existing_path(self, file_path):
        """
        Looking for existing path
        :return:
        :rtype: basestring
        """
        test_files_location = self._get_attribute_by_name('Test Files Location')
        search_order = [os.path.join(test_files_location or '', file_path),
                        os.path.join(test_files_location or '', self.context.reservation.reservation_id, file_path),
                        file_path]
        for path in search_order:
            if os.path.exists(path):
                return path
        raise BPRunnerException(self.__class__.__name__,
                                'File {} does not exists or "Test Files Location" attribute was not specified'.format(
                                    file_path))

    def load_configuration(self, file_path):
        """
        Upload configuration file and reserve ports
        :param file_path: 
        :return: 
        """
        file_path = self._get_existing_path(file_path)

        self._test_name = self._test_configuration_file_flow.load_configuration(file_path)
        test_model = ElementTree.parse(file_path).getroot().find('testmodel')
        network_name = test_model.get('network')
        interfaces = []
        for interface in test_model.findall('interface'):
            interfaces.append(int(interface.get('number')))
        self._port_reservation_helper.reserve_ports(network_name, interfaces)

    def load_pcap(self, file_path):
        response_file_name = BPLoadPcapFileFlow(self._session_context_manager, self.logger).load_pcap(file_path)
        self.logger.debug("Response received: " + str(response_file_name))
        file_name = file_path.split("\\")[-1].split(".")[0]
        if not re.search(response_file_name, file_name, re.IGNORECASE):
            raise BPRunnerException(self.__class__.__name__, 'Unable to load pcap file')

    def start_traffic(self, blocking):
        """
        Start traffic
        :param blocking: 
        :return: 
        """
        if not self._test_name:
            raise BPRunnerException(self.__class__.__name__, 'Load configuration first')
        self._test_id = self._test_execution_flow.start_traffic(self._test_name,
                                                                self._port_reservation_helper.group_id)
        if blocking.lower() == 'true':
            self._test_execution_flow.block_while_test_running(self._test_id)

    def stop_traffic(self):
        """
        Stop traffic
        :return: 
        """
        if not self._test_id:
            raise BPRunnerException(self.__class__.__name__, 'Test id is not defined, run the test first')
        self._test_execution_flow.stop_traffic(self._test_id)

    def get_statistics(self, view_name, output_format):
        """
        Real time statistics
        :param view_name: 
        :param output_format: 
        :return: 
        """
        if not self._test_id:
            raise BPRunnerException(self.__class__.__name__, 'Test id is not defined, run the test first')
        result = self._test_statistics_flow.get_rt_statistics(self._test_id, view_name)
        if output_format.lower() == 'json':
            statistics = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
            # print statistics
            # self.api.WriteMessageToReservationOutput(self.context.reservation.reservation_id, statistics)
        elif output_format.lower() == 'csv':
            output = io.BytesIO()
            w = csv.DictWriter(output, result.keys())
            w.writeheader()
            w.writerow(result)
            statistics = output.getvalue().strip('\r\n')

            # self.api.WriteMessageToReservationOutput(self.context.reservation.reservation_id,
            #                                          output.getvalue().strip('\r\n'))
        else:
            raise BPRunnerException(self.__class__.__name__, 'Incorrect file format, supported csv or json only')
        return statistics

    def get_results(self):
        """
        Get test result file and attache it to the reservation
        :return: 
        """
        if not self._test_id:
            raise BPRunnerException(self.__class__.__name__, 'Test id is not defined, run the test first')
        pdf_result = self._test_results_flow.get_results(self._test_id)
        quali_api_helper = create_quali_api_instance(self.context, self.logger)
        quali_api_helper.login()
        env_name = re.sub("\s+", "_", self.context.reservation.environment_name)
        test_id = re.sub("\s+", "_", self._test_id)
        file_name = "{0}_{1}.pdf".format(env_name, test_id)
        quali_api_helper.upload_file(self.context.reservation.reservation_id, file_name=file_name,
                                     file_stream=pdf_result)
        return "Please check attachments for results"

    def get_test_file(self, test_name):
        """
        Download test file from BP
        :param test_name: 
        :return: 
        """
        test_files_location = self._get_attribute_by_name('Test Files Location')

        if not test_files_location:
            raise BPRunnerException(self.__class__.__name__, "Test Files Location attribute is not defined")
        if not os.path.exists(test_files_location) or os.access(test_files_location, os.W_OK) is not True:
            raise BPRunnerException(self.__class__.__name__,
                                    'The location of the test files "{}" does not exist or is not writable'.format(
                                        test_files_location))
        reservation_files = os.path.join(test_files_location, self.context.reservation.reservation_id)
        if not os.path.exists(reservation_files):
            os.makedirs(reservation_files)
        test_file_path = os.path.join(reservation_files, test_name + '.bpt', )
        test_file_content = self._download_test_file_flow.download_test_file(test_name)
        with open(test_file_path, 'w') as f:
            f.write(test_file_content)
        return test_file_path

    def close(self):
        """
        Destroy
        :return: 
        """
        reservation_id = self.context.reservation.reservation_id
        self.logger.debug('Close session for reservation ID: '.format(reservation_id))
        self._port_reservation_helper.unreserve_ports()
