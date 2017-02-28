from cloudshell.tg.breaking_point.rest_actions.rest_actions import RestActions
from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class AutoloadActions(RestActions):
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
