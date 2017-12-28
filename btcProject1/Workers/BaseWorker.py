import logging

from asyncio import coroutine
from tornado.gen import Task, IOLoop

log = logging.getLogger(__name__)


class Worker(object):
    """
    Abstract async Worker
    """
    timeout = 3

    def __init__(self):
        self.failures = 0
        self.iterations = 0
        self.reset()
        self.is_running = False
        self.should_stop = False
        self.log = log.getChild('Worker')

    @property
    def successes(self):
        return self.iterations - self.failures

    @coroutine
    def work(self):
        raise NotImplementedError

    def reset(self):
        self.is_running = False

    def stop(self):
        self.log.info('Stopping')

    def run_once(self):
        return self.run_forever(until_number_of_successes=1)

    def run_forever(self, until_number_of_successes=None):
        assert not self.is_running
        self.reset()
        self.is_running = True

        if until_number_of_successes is not None:
            self.log.info('running until %s successes',
                          until_number_of_successes)
        else:
            self.log.info('running forever')

        while not self.should_stop:
            try:
                result = yield self.work()
            except Exception as e:
                result = None
                """self.failures += 1
                if isinstance(e, bitstamp.InvalidNonceError):
                    # Anything > info would send an email.
                    self.log.info('invalid nonce', exc_info=True)
                else:
                    self.log.exception('work failed')"""
                self.log.info('will try again')
            else:
                self.log.debug('work success')
            finally:
                self.iterations += 1
            if until_number_of_successes is not None \
                    and self.successes >= until_number_of_successes:
                self.stop()
                self.is_running = False
                # Only really useful with until_number_of_successes=1
                return result
            else:
                yield self.sleep()

    @coroutine
    def sleep(self):
        self.log.debug('sleeping for %d seconds', self.timeout)
        yield Task(IOLoop.instance().add_timeout,
                   IOLoop.instance().time() + self.timeout)
        self.log.debug('woken up')



