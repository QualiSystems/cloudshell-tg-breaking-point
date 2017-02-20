from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class TestExecutionActions(object):
    def __init__(self, rest_service, logger):
        """
        Reboot actions
        :param rest_service:
        :type rest_service: RestJsonClient
        :param logger:
        :type logger: Logger
        :return:
        """
        self._rest_service = rest_service
        self._logger = logger

    def start_test(self, test_name):
        self._logger.debug('Starting test {}'.format(test_name))
        uri = '/api/v1/bps/ports/operations/reserve'
        json_data = {"modelname": test_name, "group": "1"}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        return result

    def stop_test(self, test_id):
        self._logger.debug('Unreserving ports {0} on slot {1}'.format(port_list, slot))
        uri = '/api/v1/bps/ports/operations/unreserve'
        json_data = {"slot": slot, "portList": port_list}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        return result
