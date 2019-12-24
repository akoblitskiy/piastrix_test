import urllib.request
import json


def urllib_post(url, data):
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), method='POST')
    req.add_header('Content-Type', 'application/json')
    res = urllib.request.urlopen(req)
    json_str = res.read().decode('utf-8')
    return json.loads(json_str)


class Piastrix:
    currency_ids = {'eur': 978, 'usd': 840, 'rub': 643}
    shop_id = 5
    secret_key = 'SecretKey01'
    payway = 'payeer_rub'
    response = None

    def proceed_bill(self, url, data):
        json_dict = urllib_post(url, data)
        if not json_dict['result']:
            self.response = {'error': json_dict}
        self.response = {'url': json_dict['data']['url']}

    def proceed_invoice(self, url, data):
        json_dict = urllib_post(url, data)
        if not json_dict['result']:
            self.response = {'error': json_dict}
        self.response = {'url': json_dict['data']['url'], 'data': json_dict['data']['data']}
