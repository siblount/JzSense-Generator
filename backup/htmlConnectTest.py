import socket
from collections import OrderedDict
from requests import Session
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen, urlretrieve
answers = socket.getaddrinfo('https://rule34.xxx', 443)
(family, type, proto, canonname, (address, port)) = answers[0]

s = Session()
headers = OrderedDict({
    'Accept-Encoding': 'utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'authority' : 'rule34.xxx',
    'path' : "/index.php?page=post&s=view&id=4511795"
})
s.headers = headers
response = s.get(f"https://rule34.xxx/index.php?page=post&s=view&id=4511795", headers=headers, verify=False).text
x = bs(response, features="html5lib")
for x in x.find_all("div",{"class" : "link-list"}):
    print(x.sourceline)

x = urlretrieve("https://wimg.rule34.xxx//images/3978/2af9b6d59a54b2a6039ea05cb21ae160.png?4511795", "D:/a.png")
print(x)