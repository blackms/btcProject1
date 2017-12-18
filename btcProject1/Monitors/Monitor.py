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

    def run(self):
        raise NotImplementedError("Method must be implemented.")


class PusherWebSocketMonitor(Monitor):
    """
    Generic class to Monitor on a single channel. Usable to listen on USD/BTC and other crypto's for
    any exchange who uses WebSocket protocol.
    """
    _pusher_key = str()
    _channel = str()
    pusher = None

    def __init__(self, name: str, pusher_key: str='de504dc5763aeef9ff52', channel: str='live_orders'):
        """
        Init method for :class:'PusherWebSocketMonitor' class.

        :param name: [str] Thread name
        :param pusher_key: [str] String representing the pusher key
        :param channel: [str] String representing the channel name to listen on
        """
        super().__init__(None, name)
        print("Initializing: {}".format(self.name))
        self.pusher_key = pusher_key
        self.channel = channel
        self.pusher = pysher.Pusher(self.pusher_key)

    @property
    def pusher_key(self):
        """
        Getter method for pusher_key
        :return: [str] Pusher key: this._pusher_key
        """
        return self._pusher_key

    @pusher_key.setter
    def pusher_key(self, value):
        """
        Setter method for pusher_key
        :param value: [str] Pusher Key
        :return: None
        """
        assert(isinstance(value, str)), TypeError("Excepted string, got: {}".format(type(value)))
        self._pusher_key = value

    @property
    def channel(self):
        """
        Getter Method for channel
        :return: [str] Channel: this._channel
        """
        return self._channel

    @channel.setter
    def channel(self, value):
        """
        Setter Method for channel
        :param value: [str] Channel ID
        :return: None
        """
        assert(isinstance(value, str)), TypeError("Excepted string, got: {}".format(type(value)))
        self._channel = value

    def _order_callback(self, data):
        """
        Json stream (string) received from the Stream.

        :param data: [str] Data received from WebSocket Stream
        :return: None
        """
        print("{}: {}".format(self.name, data))

    def _connect_handler(self, data):
        channel = self.pusher.subscribe(self.channel)
        channel.bind('order_created', self._order_callback)
        channel.bind('order_changed', self._order_callback)
        channel.bind('order_deleted', self._order_callback)

    def stop(self) -> None:
        """
        Stop the current thread using the instance of event set.
        :return: None
        """
        self.e.set()
        print("Send stop signal to thread: {}".format(self.name))

    def run(self):
        self.pusher.connection.bind('pusher:connection_established', self._connect_handler)
        self.pusher.connect()
        while not self.e.isSet():
            time.sleep(1)
