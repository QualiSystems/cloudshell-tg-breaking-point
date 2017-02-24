from abc import ABCMeta
from cloudshell.tg.breaking_point.rest_api.rest_session_manager import RestSessionManager


class BPFlow(object):
    __metaclass__ = ABCMeta

    def __init__(self, session_manager, logger):
        """
        :param session_manager:
        :type session_manager: RestSessionManager
        :param logger:
        :return:
        """
        self._session_manager = session_manager
        self._logger = logger
