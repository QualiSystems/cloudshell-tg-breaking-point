from cloudshell.tg.ixia.breaking_point.rest_api.rest_json_client import RestJsonClient


class AutoloadActions(object):
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

    def get_ports_info(self):
        self._logger.debug('Ports info request')
        uri = '/api/v1/bps/ports'
        data = self._rest_service.request_get(uri)
        result = data.get('portReservationState')
        return result

    def get_modules_info(self):
        self._logger.debug('Modules info request ')
        uri = '/api/v1/bps/ports/chassisconfig'
        data = self._rest_service.request_get(uri)

        result = {}
        for blade_id, blade_info in data.iteritems():
            if blade_info.get('state').lower() == 'ok':
                result[blade_id] = blade_info

        return result

        # def logout(self):
        #     """
        #     Logout request
        #     :return:
        #     """
        #     self._logger.debug('Logout request')
        #     uri = '/api/v1/auth/session'
        #     self._rest_service.request_delete(uri)
