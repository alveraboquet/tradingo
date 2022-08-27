import os
import json
import time
import hmac
import requests
import urllib.parse


class Broker:
    def __init__(self, subaccount='Algo#1'):
        self.base_uri = 'https://ftx.com/api'
        self.FTX_key = os.getenv('FTXkey')
        self.FTX_secret = os.getenv('FTXsecret')
        self.SUBACCOUNT = subaccount
        self.s = requests.Session()

    def pprint(self, text):
        print(f'[+] {text}')

    def api_call(self, method, url):
        self.pprint(f'{method} {url}')
        ts = int(time.time() * 1000)
        prepared = requests.Request(method, self.base_uri + url).prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        signature = hmac.new(self.FTX_secret.encode(), signature_payload, 'sha256').hexdigest()

        prepared.headers['FTX-KEY'] = self.FTX_key
        prepared.headers['FTX-SIGN'] = signature
        prepared.headers['FTX-TS'] = str(ts)
        prepared.headers['FTX-SUBACCOUNT'] = urllib.parse.quote_plus(self.SUBACCOUNT)

        response = self.s.send(prepared)
        data = json.loads(response.text)
        if not data['success']:
            self.pprint(response.text)

        return data['result']


b = Broker()
markets = b.api_call('GET', '/markets')
