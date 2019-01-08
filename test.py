import requests
import time
# 待测试目标网页
targetUrl = "http://proxy.abuyun.com/switch-ip"
def get_proxies():
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

    for i in range(1,6):
        resp = requests.get(targetUrl, proxies=proxies)
        # print(resp.status_code)
        text = resp.text.split(',')[0]
        print('第%s次请求的IP为：%s'%(i,text))
        time.sleep(2)
 
get_proxies()
