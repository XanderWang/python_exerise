# /user/bin
# -*- coding: UTF-8 -*-
import time
import requests
from requests import Request, Session
import urllib3
urllib3.disable_warnings()

class NoCode:
    headers = {
        'charset': 'utf-8',
        'Accept-Encoding': 'gzip',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNjAxOTgxLCJuaWNrX25hbWUiOiJYYW5kZXIuV2FuZ-6MriIsImF2YXRhciI6Imh0dHBzOi8vd3gucWxvZ28uY24vbW1vcGVuL3ZpXzMyL1EwajRUd0dUZlRMa3ZXcjJuMXlwWUVQZUpQS3g1YjZINUNhbGhUa3VKbEJudTJuTEJTVmdSYlNsbERXYXRFYno0M0xEQWZtemRMbnVPMXlqWEUxUmd3LzEzMiIsInByb3ZpbmNlIjoiIiwiY2l0eSI6IiIsImdlbmRlciI6IjEiLCJpYXQiOjE1MzU0NjUyMDgsImV4cCI6MTUzNjA3MDAwOH0.6LbvLpbumpOOdsk_NUFBdMMS8cPT3oviQd32yY1IyC8',
        'version': '0.1.76',
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5s Plus Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x26070233) NetType/WIFI Language/zh_CN',
        'Host': 'lucky.nocode.com',
        'Connection': 'Keep-Alive'
    }

    session = Session()

    def get_daily_products(self):
        print('get daliy prodeucts')
        daliy_url = 'https://lucky.nocode.com/public_lottery?page=1&size=5'
        req = Request('GET',daliy_url, headers=self.headers).prepare()
        response = self.session.send(req)
        # response = requests.get(daliy_url, headers=self.headers, verify=False)
        # print(response.request.headers)
        if response.status_code == 200:
            for prize in response.json()['data']:
                if not prize['joined'] and r'不满足' not in prize.get('condition_error', ''):
                    print('find:', prize['id'],
                          prize['prizes']['data'][0]['name'])
                    yield prize['id'], prize['prizes']['data'][0]['name']
                    # self.jioned_product(
                    #     prize['id'], prize['prizes']['data'][0]['name'])
        else:
            print(r'请求失败,状态码为%s' % response.status_code)

    def jioned_product(self, params):
        print('start jion the product', params[1])
        url = 'https://lucky.nocode.com/lottery/%s/join' % params[0]
        datas = {
            'form_id': "%s" % int(time.time()*1000)
        }
        print('url:', url, 'datas:', datas)
        req = Request('POST',url, data=datas, headers=self.headers).prepare()
        del req.headers['content-length']
        response = self.session.send(req)
        # response = requests.post(
        #     url, data=datas, headers=self.headers, verify=False)
        # print(response)
        # print(response.request.headers)
        response = response.json()
        if response.get('data', False):
            print(r'抽奖成功')
        else:
            print(r'抽奖失败')


nocode = NoCode()

for param in nocode.get_daily_products():
    nocode.jioned_product(param)
