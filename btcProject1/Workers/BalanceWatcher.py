from btcProject1.Workers import Worker
from tornado.gen import Task
from asyncio import coroutine
from django.utils import timezone

from bitstamp.client import Trading


class BalanceWatcher(Worker):
    timeout = 3

    """Polls Bitstamp account balance, saves & broadcasts it on changes."""

    def __init__(self, client: Trading) -> None:
        """
        Initialize Object with Client

        NOTE: For now, I only support Bitstamp Client, a new abstract class must be
        created here.

        :param client: [Trading] client object
        """
        super(Worker, self).__init__()
        self.client = client

    @coroutine
    def work(self):
        """
        Check current account balance and saves it

        :return: None
        """
        current = yield Task(self.client.account_balance)

        try:
            latest = self.client.account_balance()[0]
        except:
            differs = True
        else:
            differs = any(getattr(latest, k) != v for k, v in current.items())

        if not differs:
            self.log.debug('no balance change')
        else:
            self.log.info('current balance differs from latest, saving, %r',
                          current)
            """self.publish(account.balances.create(
                inferred=False,
                timestamp=timezone.now(),
                **current
            )"""