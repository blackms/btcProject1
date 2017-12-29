"""
Quick and Dirty approach to make Money
"""
import sys
from bitstamp.client import Public
from bitstamp.client import Trading
from bitstamp.client import BitstampError
from datetime import datetime
import time

import argparse

parser = argparse.ArgumentParser(prog='PoC')
parser.add_argument('--key', type=str, dest='key', action='store')
parser.add_argument('--secret', type=str, dest='secret', action='store')
parser.add_argument('--username', type=str, dest='username', action='store')
p = parser.parse_args()


def connect(key: str, secret, username) -> Trading:
    return Trading(username=username, key=key, secret=secret)


trader = connect(username=p.username, key=p.key, secret=p.secret)
public = Public()


class Balance(object):
    def __init__(self, b_trader: Trading, currency: str = 'eur'):
        self.currency = currency
        self.b_trader = b_trader

    def get_current_balance(self):
        return self.b_trader.account_balance(quote='eur')


balance = Balance(b_trader=trader)

while True:
    current_balance_eur = balance.get_current_balance()
    last_transaction = public.transactions(quote='eur')[0]
    last_transaction['datetime'] = datetime.utcfromtimestamp(
        int(last_transaction['date'])
    ).strftime('%Y-%m-%dT%H:%M:%SZ')

    print('BTC/EUR Value {}'.format(last_transaction['price']), end=' ||| ')
    my_last_transaction = trader.user_transactions(base='btc', quote='eur')[0]
    if my_last_transaction['type'] == '2':
        print("Buy at price: {}, current fee: {}, Current BTC available: {}".format(my_last_transaction['btc_eur'],
                                                                                    current_balance_eur['fee'],
                                                                                    current_balance_eur['btc_balance']
                                                                                    ), end=' '
              )
        percentage = 1
        sell_at = round(my_last_transaction['btc_eur'] + (my_last_transaction['btc_eur'] * percentage / 100), 2)
        print("Setting gain to: {}%, We want to sell at: {}. Delta: {}".format(
            percentage, sell_at, float(sell_at) - float(last_transaction['price']))
        )

        # check for the active order, if there is one matching the gain
        open_orders = trader.open_orders(quote='eur')
        match = list(filter(lambda x: float(x['price']) == float(sell_at), open_orders))
        if len(match) == 0:
            print("!!! Creating Sell Order at: {}".format(sell_at))
            amount_to_sell = float(current_balance_eur['btc_balance'])
            try:
                trader.sell_limit_order(amount=round(amount_to_sell, 8), price=sell_at, base='btc', quote='eur')
            except BitstampError as e:
                print(e)
                sys.exit(0)
    if my_last_transaction['type'] == '2':
        print("Sold at price: {}, current fee: {}, Current EUR available: {}".format(
            my_last_transaction['btc_eur'],
            current_balance_eur['fee'],
            current_balance_eur['eur_balance']
        ))

        percentage = 1
        buy_at = round(my_last_transaction['btc_eur'] - (my_last_transaction['btc_eur'] * percentage / 100), 2)
        print("Setting loss to: {}%, We want to buy at: {}".format(percentage, buy_at))

        # check for the active order, if there is one matching the gain
        open_orders = trader.open_orders(quote='eur')
        match = list(filter(lambda x: float(x['price']) == float(buy_at), open_orders))
        if len(match) == 0:
            print("!!! Creating Buy Order at: {}".format(buy_at))
            amount_to_buy = float(float(current_balance_eur['eur_available']) / buy_at)
            try:
                trader.buy_limit_order(amount=round(amount_to_buy, 8), price=buy_at, base='btc', quote='eur')
            except BitstampError as e:
                print(e)
                sys.exit(0)
    time.sleep(2)
