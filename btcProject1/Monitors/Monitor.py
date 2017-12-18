from threading import Thread, Event
import logging
import pysher
import time


class Monitor(Thread):
    def __init__(self, source, name: str):
        super().__init__()
        self._source = source
        self.name = name
        self.e = Event()

    def start(self):
        self.run()

    def stop(self) -> None:
        """
        Stop the current thread using the instance of event set.
        :return: None
        """
        self.e.set()

    def run(self):
        raise NotImplementedError("Method must be implemented.")


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


class BitstampMonitorLive(Monitor):
    _pusher_key = str()
    _channel = str()
    pusher = None

    def __init__(self, name: str, pusher_key: str='de504dc5763aeef9ff52', channel: str='live_orders'):
        """
        Init method for BitStampMonitorLive class.

        :param name: [str] Thread name
        :param pusher_key: [str] String representing the pusher key
        :param channel: [str] String representing the channel name to listen on
        """
        super().__init__(None, name)
        self.pusher_key = pusher_key
        self.channel = channel
        self.pusher = pysher.Pusher(self.pusher_key)

    @property
    def pusher_key(self):
        return self._pusher_key

    @pusher_key.setter
    def pusher_key(self, value):
        assert(isinstance(value, str)), TypeError("Excepted string, got: {}".format(type(value)))
        self._pusher_key = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        assert(isinstance(value, str)), TypeError("Excepted string, got: {}".format(type(value)))
        self._channel = value

    def _order_callback(self, data):
        print(data)

    def _connect_handler(self, data):
        channel = self.pusher.subscribe(self.channel)
        channel.bind('order_created', self._order_callback)
        channel.bind('order_changed', self._order_callback)
        channel.bind('order_deleted', self._order_callback)

    def start(self) -> None:
        super(self, BitstampMonitorLive).start()

    def stop(self) -> None:
        super(self, BitstampMonitorLive).stop()

    def run(self):
        self.pusher.connection.bind('pusher:connection_established', self._connect_handler)
        self.pusher.connect()
        while not self.e.isSet():
            time.sleep(1)
