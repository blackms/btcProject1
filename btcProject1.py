import argparse

import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='btcProject1')
    parser.add_argument('--key', '-k', type=str, dest='key', action='store', help='BitStamp API Key.', required=False)
    parser.add_argument('--secret', '-s', type=str, dest='secret', action='store', help='BitStamp API Key',
                        required=False)

    p = parser.parse_args()
    from btcProject1.Monitors.Monitor import PusherWebSocketMonitor
    from btcProject1.Monitors.MonitorPool import MonitorPool

    monitorPool = MonitorPool()

    b = PusherWebSocketMonitor(name='BitStampBTC-USD', pusher_key='de504dc5763aeef9ff52')
    monitorPool.add_monitor(b)
    monitorPool[b.name].setDaemon(True)

    c = PusherWebSocketMonitor(name='BitStampXRP-USD', pusher_key='0ea60078504a5d9773ab')
    monitorPool.add_monitor(c)
    monitorPool[c.name].start()
    monitorPool[b.name].start()

    time.sleep(1)
    #monitorPool.stop_all()
