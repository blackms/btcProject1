import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='btcProject1')
    parser.add_argument('--key', '-k', type=str, dest='key', action='store', help='BitStamp API Key.', required=False)
    parser.add_argument('--secret', '-s', type=str, dest='secret', action='store', help='BitStamp API Key',
                        required=False)

    p = parser.parse_args()
    from btcProject1.Monitors.Monitor import BitstampMonitorLive
    b = BitstampMonitorLive(name='BitStampMonitorLive')
    b.run()
