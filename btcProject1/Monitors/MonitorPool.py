import logging
from btcProject1.Monitors.Monitor import Monitor


class MonitorPool(object):
    _threadPool = {}

    def __init__(self, logger: logging=logging.Logger):
        """
        Init Constructor with logger parameter
        :param logger: [logging.Logger] instance of logger class
        """
        self.logger = logger

    def add_monitor(self, monitor: Monitor) -> None:
        """
        Add a Monitor to the Pool
        :param monitor: [Monitor] Monitor object to add
        """
        self._threadPool[monitor.name] = monitor

    def del_monitor(self, monitor: Monitor) -> None:
        """
        Remove a Monitor from the Pool
        :param monitor:
        :return: [bool] True in case of success
        """
        self._threadPool[monitor.name].stop()
        del self._threadPool[monitor.name]

    def stop_all(self):
        for t in self._threadPool:
            self._threadPool[t].stop()

    def __getitem__(self, item):
        return self._threadPool[item]
