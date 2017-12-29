from abc import abstractmethod
from asyncio import coroutine

from tornado.gen import Task
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, TracebackFuture, HTTPResponse
from tornado.ioloop import IOLoop


class Exchange(object):
    def __init__(self):
        self.base_value = None
        self.tickers = None
        self.currencies = None
        self.api = None

    @abstractmethod
    def _process_response(self, resp):
        raise NotImplementedError

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
    def sleep(self):
        yield Task(IOLoop.instance().add_timeout,
                   IOLoop.instance().time() + 5)

    @coroutine
    def run(self):
        for currency in self.currencies:
            yield self.get_tickers(pair=currency)
        yield self.sleep()


class BitStamp(Exchange):
    def __init__(self):
        super().__init__()
        self.api = 'https://www.bitstamp.net/api'
        self.tickers = 'v2/ticker/'
        self.currencies = ['eth', 'btc', 'xrp', 'bch']
        self.base_value = 'usd'

    def _process_response(self, resp: HTTPResponse):
        print(resp.body)


class BitFinex(Exchange, object):
    def __init__(self):
        super().__init__()
        self.api = 'https://api.bitfinex.com'
        self.tickers = '/v2/tickers?symbols='
        self.currencies = ['eth', 'btc', 'xrp', 'bch', 'dsh']
        self.base_value = 'usd'

    def _process_response(self, resp: HTTPResponse):
        print(resp.body)


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
