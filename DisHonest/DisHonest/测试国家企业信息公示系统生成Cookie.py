# import requests
# import re
# import js2py
#
# '''
# 获取cookie思路：
#     1. 通过前面文件分析可知：cookie必须包含三个参数(jsluid_h, __jsl_clearance, SECTOKEN=6925908179269977476)
#         url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'发送了两次请求，第一次请求效应码为521，
#        并在响应头设置 Set-Cookie: __jsluid_h=093df14baab5d165240…即通过第一次请求可以获得第一个cookie参数，并储存在session中
#
#     2. 通过第一次请求，我们可以提取响应数据中<script>标签中的内容，通过自定义的code=去替换掉<script>标签中的eval，再执行该
#         'code=....' js文件
#
#     3. 通过正则表达式提取包含'cookie='的js文件，这个就是完整的cookie的js文件，再通过执行js文件中的'document.cookie=',便得到了__jsl_clearance
#        数据
#
# '''
#
# url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
# index_url = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=21&areaid=100000&noticeTitle=&regOrg=110000'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
#
# }
#
# session = requests.session()
# session.headers = headers
# response = session.get(url)
# print(response.status_code)
# #print(response.content.decode())
# #1. 提取script标签的js文件
# js = re.findall('<script>(.*?)</script>',response.content.decode())[0]
#
# #2. 由于这种加密js，最终指向的js代码，都是在eval函数中的，所以'eval('替换为'{code=(' ,然后通过code,获取到真正的js值
# js = js.replace('eval','code=')
# #print(js)
#
# #3. 执行js代码
# #3.1 获取执行js的环境
# context = js2py.EvalJs()
# context.execute(js)
# # # print(context.code)
#
# #获取生成cookie的js
# cookie_code = re.findall("document.(cookie=.*)\+';Expires",context.code)[0]
# # print(cookie_code)
#
# context.execute(cookie_code)
# #print(context.cookie)   #__jsl_clearance=1572941662.599|0|QkanTZPKXziECY6ig8ttOW8Lg0s%3D
#
# cookie_str = context.cookie
# cookie_str_list = re.findall('String\.fromCharCode\([^()]*\)',cookie_str)
#
# for str in cookie_str_list:
#     code = js2py.eval_js('var str='+str+';str')
#     if str in cookie_str:
#         cookie_str = cookie_str.replace(str,code)
#
# cookie = cookie_str.split('=')
# #添加__jsl_clearance到session中
# session.cookies.set(cookie[0],cookie[1])
#
# session.get(url)
# # print(session.cookies)  #<RequestsCookieJar[<Cookie __jsl_clearance=1572942229.839|0|E%2FiZmr6ghYtZFNaZ7aUm%2FwMSWGU%3D for />, <Cookie HttpOnly for www.gsxt.gov.cn/>, <Cookie JSESSIONID=55C0212024D176415B8D809B0BF38975-n2:-1 for www.gsxt.gov.cn/>, <Cookie SECTOKEN=6918542873195186425 for www.gsxt.gov.cn/>, <Cookie __jsluid_h=830d87ca5afb1cba61d3fff73bd7472b for www.gsxt.gov.cn/>, <Cookie tlb_cookie=S172.16.12.71 for www.gsxt.gov.cn/>]>
# #将cookieJar数据转换为字典  其实也不用转换，直接用session去请求后面的数据就行，session自带所有的cookies
# cookies = requests.utils.dict_from_cookiejar(session.cookies)
# #print(cookies)
#
#
# post_data = {
#         # 'draw': '1',
#         'start': '0',
#         'length': '10'
# }
#
# response = session.post(index_url,data=post_data,headers=headers)  #session的post请求不用添加cookies;requests的post请求必须添加cookies
# print(response.json())

import js2py

js = "cookie=(function(){var _1p=[function(_1q){return _1q},function(_1p){return _1p},(function(){var _1q=document.createElement('div');_1q.innerHTML='<a href=\'/\'>_23</a>';_1q=_1q.firstChild.href;var _1p=_1q.match(/https?:\/\//)[0];_1q=_1q.substr(_1p.length).toLowerCase();return function(_1p){for(var _23=0;_23<_1p.length;_23++){_1p[_23]=_1q.charAt(_1p[_23])};return _1p.join('')}})(),function(_1q){return code=('String.fromCharCode('+_1q+')')}],_23=['v8d',[(-~{}+[]+[])+(-~{}-~{}+[]+[])+(-~{}-~{}+[]+[]),(7+[[]][0])+[(-~~~''<<-~~~'')+(-~~~''<<-~~~'')],[(-~~~''+[-~(+!+{})])/[-~(+!+{})]]+[[((-~~~''<<-~~~'')^-~!![][{}])]*(((-~~~''<<-~~~'')^-~!![][{}]))]],'9',[(-~{}+[]+[])+(~~[]+[[]][0])+[[((-~~~''<<-~~~'')^-~!![][{}])]*(((-~~~''<<-~~~'')^-~!![][{}]))],(7+[[]][0])+(-~{}-~{}+[]+[]),((+!+{})-~(+!+{})+[]+[])+(7+[[]][0])],'2',[(7+[[]][0])+(~~[]+[[]][0]),(7+[[]][0])+(-~{}-~{}+[]+[]),(-~{}+[]+[])+(~~[]+[[]][0])+[[((-~~~''<<-~~~'')^-~!![][{}])]*(((-~~~''<<-~~~'')^-~!![][{}]))]],[(-~{}+[]+[])+((+!+{})-~(+!+{})+[]+[])],'nAM%',(-~{}-~{}+[]+[]),[(7+[[]][0])+(~~[]+[[]][0])],'Rph',[[(-~~~''+[-~(+!+{})])/[-~(+!+{})]]+[[((-~~~''<<-~~~'')^-~!![][{}])]*(((-~~~''<<-~~~'')^-~!![][{}]))]],'%',(-~{}-~{}+[]+[]),[[(-~~~''+[-~(+!+{})])/[-~(+!+{})]]+[(-~~~''+[-~(+!+{})])/[-~(+!+{})]]],'G',[(-~~~''+[-~(+!+{})])/[-~(+!+{})]],[[3+((+!+{})+[(+!![][{}])])/[-~(+!+{})]]+[(-~~~''<<-~~~'')+(-~~~''<<-~~~'')]],'i',[[3+((+!+{})+[(+!![][{}])])/[-~(+!+{})]]+[((+!+{})+[(+!![][{}])])/[-~(+!+{})]]],'%',((+!+{})-~(+!+{})+[]+[]),'D'];for(var _1q=0;_1q<_23.length;_1q++){_23[_1q]=_1p[[1,3,1,3,1,3,2,1,0,3,1,3,1,0,3,1,0,3,1,3,1,0,1][_1q]](_23[_1q])};return _23.join('')})()"
context = js2py.EvalJs(js).execute(cookie)

print(context)


