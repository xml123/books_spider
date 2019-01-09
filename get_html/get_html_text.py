import datetime

import chardet
import requests
import random
from urllib import request
import time
import re
# import execjs

def get_headers():
    '''
    随机获取一个headers
    '''
    #'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    user_agents =  [
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]
    headers = {'User-Agent':random.choice(user_agents)}
    return headers

def get_dl():
    targetUrl = "http://proxy.abuyun.com/switch-ip"
    #targetUrl = "http://proxy.abuyun.com/current-ip"
    # 代理服务器
    proxyHost = "http-cla.abuyun.com"
    proxyPort = "9030"

    # 代理隧道验证信息
    proxyUser = "H1K845Z7K8BUO75C"
    proxyPass = "DF205E31552BB478"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    resp = requests.get(targetUrl, proxies=proxies)
    # print(resp.status_code)
    # print('resp',resp.text)
    ip_string = resp.text.split(',')[0]
    proxy = {
       "http":"http://%s" % ip_string
    }
    return proxy

# def executejs(html,url):
#     # 提取其中的JS加密函数
#     try:
#         __jsluid = html.headers["Set-Cookie"].split(';')[0]
#         print('__jsluid1',__jsluid)
#         #cookie1 = __jsluid

#         get_js = re.findall(r'<script>(.*?)</script>', html.text)[0].replace('eval', 'return')
#         #print('get_js',get_js)
#         resHtml = "function getClearance(){" + get_js + "};"
#         #print('resHtml',resHtml)
#         ctx = execjs.compile(resHtml)
#         #print('ctx',ctx)
#         # 一级解密结果
#         temp1 = ctx.call('getClearance')
#         #print('temp1',temp1)


#         s = 'var a' + temp1.split('document.cookie')[1].split("Path=/;'")[0]+"Path=/;';return a;"
#         s = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(url), s)
#         # print ('s',s)
#         resHtml = "function getClearance(){" + s + "};"
#         ctx = execjs.compile(resHtml)
#         # 二级解密结果
#         jsl_clearance = ctx.call('getClearance')
#         #print('jsl_clearance',jsl_clearance)

#         return jsl_clearance
#     except Exception as e:
#         print('解析cookie出错',e)
#         return ''


# def parse_cookie(string):
#     string = string.replace("document.cookie='", "")
#     clearance = string.split(';')[0]
#     return {clearance.split('=')[0]: clearance.split('=')[1]}

# 获取URL的网页HTML
def get_html_text(url):
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    # }
    headers = get_headers()
    # proxy = get_dl()
    # print('proxy',proxy)
    # 第一次访问获取动态加密的JS
    # first_html = requests.get(url,headers=headers)
    # #last_html= first_html.decode('utf-8')
    # #print('first_html',first_html)
    # # 执行JS获取Cookie
    # cookie_str = executejs(first_html,url)
    # #print('cookie_str',cookie_str)
    # # 将Cookie转换为字典格式
    # cookie = parse_cookie(cookie_str)
    # print('cookies = ',cookie)

    try:
        res = requests.get(url,headers=headers,timeout=15)
        print('code',res.status_code)
        html_bytes = res.content
        code_style = chardet.detect(html_bytes).get("encoding")
        html_text = html_bytes.decode(code_style, "ignore")
    except Exception as e:
        print(datetime.datetime.now())
        print("encoding is error")
        print(e)
        return ''
    return html_text

# 保存图片到本地
def save_img(url):
    headers = get_headers()
    t = int(time.time())
    name = '%s.jpg' % t
    try:
        path = r'/Users/xumingliang/userReact/booksApi/static/image/%s' % name
        request03 = request.Request(url,None,headers)
        response = request.urlopen(request03)
        with open (path,"wb") as f :
            f.write(response.read())   # 以二进制的方法写进本地文件中
        #request.urlretrieve(url,'/Users/xumingliang/userReact/booksApi/static/')
        return name
    except Exception as e:
        print("图片保存失败")
        print(e)
        return ''





