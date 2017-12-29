import json
from asyncio import coroutine

import requests as re
from abc import ABCMeta, abstractmethod, abstractproperty
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, TracebackFuture, HTTPResponse
from tornado.gen import Task
from tornado.ioloop import IOLoop


class Exchange(metaclass=ABCMeta):
    def __init__(self):
        pass

    def _request(self):
        raise NotImplementedError

    def get_tickers(self):
        raise NotImplementedError

    @coroutine
    def sleep(self):
        yield Task(IOLoop.instance().add_timeout,
                   IOLoop.instance().time() + 5)


class BitStamp(Exchange, object):
    def __init__(self):
        super().__init__()
        self.api = 'https://www.bitstamp.net/api'
        self.tickers = '/v2/ticker/'
        self.currencies = ['eth', 'btc', 'xrp', 'bch']
        self.base_value = 'usd'

    def _process_response(self, resp: HTTPResponse):
        print(resp.body)

    def _request(self, path: str=None, method: str=None, body: str=None) -> TracebackFuture:
        client = AsyncHTTPClient()
        request = HTTPRequest(
            url=self.api + path,
            method=method,
            body=body,
        )
        return client.fetch(
            request=request,
            callback=lambda resp: self._process_response(resp)
        )

    @coroutine
    def get_tickers(self, pair: str='btcusd'):
        path = "{}/{}{}".format(self.tickers, pair, self.base_value)
        return self._request(path=path, method='GET')

    @coroutine
    def run(self):
        for currency in self.currencies:
            yield self.get_tickers(pair=currency)
        yield self.sleep()


class BitFinex(Exchange, object):
    def __init__(self):
        super().__init__()
        self.api = 'https://api.bitfinex.com'
        self.tickers = '/v2/tickers?symbols='
        self.currencies = ['eth', 'btc', 'xrp', 'bch', 'dsh']
        self.base_value = 'usd'

    def _process_response(self, resp: HTTPResponse):
        print(resp.body)

    def _request(self, path: str=None, method: str=None, body: str=None) -> TracebackFuture:
        client = AsyncHTTPClient()
        request = HTTPRequest(
            url=self.api + path,
            method=method,
            body=body,
        )
        return client.fetch(
            request=request,
            callback=lambda resp: self._process_response(resp)
        )

    @coroutine
    def get_tickers(self, pair: str='btcusd'):
        path = "{}{}{}".format(self.tickers, pair, self.base_value)
        return self._request(path=path, method='GET')

    @coroutine
    def run(self):
        for currency in self.currencies:
            yield self.get_tickers(pair=currency)
        yield self.sleep()


@coroutine
def tickers():
    loaded_tickers = [
        BitStamp(),
        BitFinex()
    ]

    while True:
        for ticker in loaded_tickers:
            yield ticker.run()


if __name__ == '__main__':
    IOLoop.instance().run_sync(tickers)
