import requests
apikey = "b519bc995376f867"
url = "https://botcheck2-dot-surfsafe-rbl.appspot.com/DeepScan"
params = { "apikey": apikey,
           "username": "superducktoes"}

headers = {"Accept": "application/json, text/plain,",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "en-US,en;q=0.5",
           "Connection": "keep-alive",
           "Content-Length": "55",
           "Content-Type": "application/json;charset=utf-8",
           "DNT":"1",
           "Host":"botcheck2-dot-surfsafe-rbl.appspot.com",
           "Origin":"https://botcheck.me",
           "Referer":"https://botcheck.me/",
           "TE":"Trailers",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; ) Gecko/20100101 Firefox/63.0"}
r = requests.post(url, params={"apikey": apikey, "username":"superducktoes"}, headers=headers)
print(r.text)
