import time
from broker import Broker


class PriceScanner:
    def __init__(self, subaccount, market, period):
        self.market = market
        self.Broker = Broker(subaccount=subaccount)
        self.period = period

    def pprint(self, text):
        print(f'[+] {text}')

    def loop(self):
        while True:
            data = self.Broker.api_call('GET', f'/markets/{self.market}/orderbook?depth=1')
            # {'bids': [[19858.0, 0.008]], 'asks': [[19859.0, 0.1186]]}
            bid_price, bid_size = data['bids'][0][0], data['bids'][0][1]
            ask_price, ask_size = data['asks'][0][0], data['asks'][0][1]
            price = (bid_price*bid_size + ask_price*ask_size) / (bid_size + ask_size)
            self.pprint(f'{self.market} {price}')
            time.sleep(self.period)


ps = PriceScanner(subaccount='Algo#1',
                  market='BTC/USD',
                  period=60)
ps.loop()
example_market = """
{
      "name": "BTC/USD",
      "enabled": true,
      "postOnly": false,
      "priceIncrement": 1.0,
      "sizeIncrement": 0.0001,
      "minProvideSize": 0.0001,
      "last": 19882.0,
      "bid": 19880.0,
      "ask": 19881.0,
      "price": 19881.0,
      "type": "spot",
      "futureType": null,
      "baseCurrency": "BTC",
      "isEtfMarket": false,
      "quoteCurrency": "USD",
      "underlying": null,
      "restricted": false,
      "highLeverageFeeExempt": true,
      "largeOrderThreshold": 3000.0,
      "change1h": -0.01266388557806913,
      "change24h": -0.04307855217558722,
      "changeBod": -0.017300182887647668,
      "quoteVolume24h": 432826358.0407,
      "volumeUsd24h": 432826358.0407,
      "priceHigh24h": 20833.0,
      "priceLow24h": 19802.0
}
"""