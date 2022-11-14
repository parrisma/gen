import os
import logging
from rltrace.interface.TraceI import TraceI


class SimpleTrace(TraceI):

    def __init__(self,
                 session_uuid: str):
        self._session_uuid = session_uuid
        self._pid = os.getpid()
        return

    def set_log_level(self,
                      level: int) -> None:
        self.log("WARNING: call to set_log_level ignored in this implementation")
        return

    def new_session(self) -> None:
        """
        Change the session id to a different, randomly generated GUID. This allows a specific subset of trace
        traffic to be selected from the overall handler capture.
        """
        self.log("WARNING: call to new_session ignored in this implementation")
        return

    def enable_handler(self,
                       handler: logging.Handler) -> None:
        """
        Attach the handler as an additional sink.
        :param handler: The log handler to attach
        """
        self.log("WARNING: call to enable_handler ignored in this implementation")
        return

    def enable_tf_capture(self,
                          tf_logger: logging.Logger) -> None:
        """
        Disable TF logging to console direct and re-direct to experiment trace console & elastic
        :param tf_logger: The tensorflow logger
        """
        self.log("WARNING: call to enable_tf_capture ignored in this implementation")
        return

    def log(self, msg: object, level: int = None) -> None:
        self._pid = os.getpid()
        print(f'ST: {self._session_uuid} - {self._pid} - {msg}')
        return
