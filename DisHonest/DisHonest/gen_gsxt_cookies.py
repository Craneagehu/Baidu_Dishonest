from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import pickle

import requests
import re
import js2py
from redis import StrictRedis
from DisHonest.settings import REDIS_URL
from fake_useragent import UserAgent
from DisHonest.settings import COOKIES_KEY,COOKIES_PROXY_KEY,REDIS_COOKIES_KEY,COOKIE_USER_AGENT_KEY

"""
实现生成cookie的脚本

1. 创建gen_gsxt_cookies.py文件，在其中创建GenGsxtCookie的类
2 . 实现一个方法，用于把一套代理IP，User-Agent,Cookie绑定在一起的信息放到Redis的list中
    随机获取一个User-Agent
    随机获取一个代理IP
    获取request的session对象
    把User-Agent，通过请求头，设置给session对象
    把代理IP，通过proxies，设置给session对象
    使用session对象，发送请求，获取需要的cookie的信息
    把代理IP，User-Agent，Cookie放到字典中，序列化后，储存到Redis的list中
3. 实现一个run方法，用于开启多个异步来执行这个方法

注; 为了和下载器中间件交互方便，需要在settings.py中配置一些常量

"""
class GenGsxtCookie(object):

    def __init__(self):
        """
        建立Redis数据库连接
        """
        self.redis = StrictRedis.from_url(REDIS_URL)
        self.pool = Pool()

    def push_cookie_to_redis(self):
        while True:
            try:
                '''
                    2 . 实现一个方法，用于把一套代理IP，User-Agent,Cookie绑定在一起的信息放到Redis的list中
                '''
                # 2.1 随机获取一个User-Agent
                user_agent = UserAgent().random

                # 2.2 随机获取一个代理IP
                response = requests.get('http://localhost:5000/random_proxy')
                proxy = response.content.decode()

                # 2.3 获取request的session对象
                session = requests.session()

                # 2.4 把User-Agent，通过请求头，设置给session对象
                session.headers = {
                    "User-Agent":user_agent
                }
                # 2.5 把代理IP，通过proxies，设置给session对象
                session.proxies = {
                    "http": proxy
                }
                # 2.6 使用session对象，发送请求，获取需要的cookie的信息
                url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
                response = session.get(url)

                # print(response.content.decode())
                # 1. 提取script标签的js文件
                js = re.findall('<script>(.*?)</script>', response.content.decode())[0]

                # 2. 由于这种加密js，最终指向的js代码，都是在eval函数中的，所以'eval('替换为'{code=(' ,然后通过code,获取到真正的js值
                js = js.replace('eval', 'code=')
                print(js)

                # 3. 执行js代码
                # 3.1 获取执行js的环境
                context = js2py.EvalJs()
                context.execute(js)
                #print(context.code)

                # 获取生成cookie的js
                cookie_code = re.findall("document.(cookie=.*)\+';Expires", context.code)[0]

                context.execute(cookie_code)
                print(context.cookie)  # __jsl_clearance=1572941662.599|0|QkanTZPKXziECY6ig8ttOW8Lg0s%3D
                # 提取String.fromCharCode()字符串

                cookie_str = context.cookie
                cookie_str_list = re.findall('String\.fromCharCode\([^()]*\)', cookie_str)

                for str in cookie_str_list:
                    code = js2py.eval_js('var str=' + str + ';str')
                    if str in cookie_str:
                        cookie_str = cookie_str.replace(str, code)

                cookie = cookie_str.split('=')

                # 添加__jsl_clearance到session中
                session.cookies.set(cookie[0], cookie[1])
                session.get(url)
                # print(session.cookies)  #<RequestsCookieJar[<Cookie __jsl_clearance=1572942229.839|0|E%2FiZmr6ghYtZFNaZ7aUm%2FwMSWGU%3D for />, <Cookie HttpOnly for www.gsxt.gov.cn/>, <Cookie JSESSIONID=55C0212024D176415B8D809B0BF38975-n2:-1 for www.gsxt.gov.cn/>, <Cookie SECTOKEN=6918542873195186425 for www.gsxt.gov.cn/>, <Cookie __jsluid_h=830d87ca5afb1cba61d3fff73bd7472b for www.gsxt.gov.cn/>, <Cookie tlb_cookie=S172.16.12.71 for www.gsxt.gov.cn/>]>
                # 将cookieJar数据转换为字典  其实也不用转换，直接用session去请求后面的数据就行，session自带所有的cookies
                cookies = requests.utils.dict_from_cookiejar(session.cookies)

                # 2.7 把代理IP，User-Agent，Cookie放到字典中，序列化后，储存到Redis的list中
                cookies_dict = {
                    COOKIES_KEY:cookies,
                    COOKIE_USER_AGENT_KEY:user_agent,
                    COOKIES_PROXY_KEY:proxy
                }
                print(cookies_dict)
                # 序列化后，存储到Redis的list中
                self.redis.lpush(REDIS_COOKIES_KEY,pickle.dumps(cookies_dict))
                break
            except Exception as e:
                print(e)

    def run(self):
        # 3. 实现一个run方法，用于开启多个异步来执行这个方法
        for i in range(5):
            self.pool.apply_async(self.push_cookie_to_redis)
        self.pool.join()




if __name__ == '__main__':
    ggc = GenGsxtCookie()
    # ggc.push_cookie_to_redis()
    ggc.run()


