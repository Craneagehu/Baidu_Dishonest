from urllib.parse import quote

import requests

url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg=110000'



post_data = {
        'draw': '1',
        'start': '0',
        'length': '10'
}

headers = {
    'Referer': 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    #一个cookie绑定一个user-agent和ip地址
    'Cookie': '__jsluid_h=c86bc61903575ca039738e275f0fefd1; __jsl_clearance=1572934477.763|0|jAr4w4O2vUdah54hGMK5qDpLGRA%3D;'
}

response = requests.post(url,data=post_data,headers=headers)
print(response.json())





