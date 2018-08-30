无码科技开发了一个抽奖的小程序，里面有一些赞助商提供的抽奖，但是每次都要一个一个的点才能参与，很麻烦。参考了网上的一些教程，写了一个脚本，可以不用一个一个地点就可以参与抽奖。

过程的话主要是

- 抓包，分析如何获取奖品列表，分析如何提交参与抽奖。
- 模拟小程序发送的请求，参与抽奖。

抓包的话，这个就不详细讲，最近也是在摸索，等有空了出个图文教程。这里先说个结论吧。

## 获取每日抽奖的奖品

> https://lucky.nocode.com/public_lottery?page=1&size=5

用的 GET 方法请求的，需要注意的是请求的 headers , 因为无码可见会 headers 里面的一些用户信息。headers 的话可以通过抓包工具分析。

这里贴下我的代码

```python

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
        if response.status_code == 200:
            for product in response.json()['data']:
                if not product['joined'] :
                    print('find:', product['id'],product['prizes']['data'][0]['name'])
                    # yield product['id'], product['prizes']['data'][0]['name']
                    self.jioned_product(product['prizes']['data'][0]['name'], product['id'])
        else:
            print(r'请求失败,状态码为%s' % response.status_code)
```

## 参与某个奖品的抽奖

通过抓包可以知道，参与抽奖的 url 是：

> https://lucky.nocode.com/lottery/{product_id}/join

`product_id` 是这个奖品的 `id` , 可以通过获取抽奖奖品列表的时候获取。同样需要注意的是 headers ，因为里面保存了你的登录信息等。

特别说明的是，这个方法是用 `POST` 来请求的，需要注意一下。下面贴下我的代码

```python
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
        response = response.json()
        if response.get('data', False):
            print(r'抽奖成功')
        else:
            print(r'抽奖失败')
```

这里有个坑需要特别说明下，在参与抽奖的这个请求里面， `headers` 里面不能有 `content-length` ,否则会请求失败，原因未知，解决的办法就是删掉 `content-length` 。


## 获取自助福利并参与

老规矩，先上代码
```python
    def get_square_products(self, url):
        if url == "": url = 'https://lucky.nocode.com/square'
        print(url)
        req = Request('GET', url, headers=self.headers).prepare()
        response = self.session.send(req)
        if response.status_code != 200: return
        response = response.json()
        for product in response['data']:
            if not product['joined'] :
                print('find square products:', product['id'], product['prizes']['data'][0]['name'])
                # yield product['id'], product['prizes']['data'][0]['name']
                self.jioned_product(product['prizes']['data'][0]['name'], product['id'])
        nextUrl = response['links']['next']
        if nextUrl != None :
            self.get_square_products( "https://lucky.nocode.com%s" % nextUrl)
```

自助福利是分页的，所有后面有个递归调用。然后最开始的 url 是 `https://lucky.nocode.com/square`，请求这个 api 以后，会返回自助福利列表，如果有下一页的话就请求下一页的 url ，解析出来奖品后参与抽奖。