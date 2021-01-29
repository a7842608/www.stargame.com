import requests
import re


def ip_pool(targetUrl): # 需传入
    '''极光ip代理'''

    # targetUrl = targetUrl     # 请求地址
    print(targetUrl, '请求地址被调用')
    targetUrl = "http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=1&fa=0&dt=&groupid=0&fetch_key=&qty=1&time=1&port=1&format=txt&ss=1&css=&dt=&pro=&city=&usertype=6"
    # s = '{"code":0,"success":"true","msg":"","data":[{"IP":"113.64.92.50","Port":37840}]}'
    resp = requests.get(targetUrl)
    # statue = resp.status_code
    if resp.status_code != 200:
        statue = {'Code': 400, 'Message':'请求失败, ip并未返回'}
        return statue
    data = resp.text
    try:
        # s_l = re.split('\[|\]|\{|\}', s)
        s_l = re.split('\[|\]|\{|\}', data)
        n_l = [i for i in s_l if i != ""][-1]
        nn_l = n_l.split(',')
        ip_x = nn_l[0].split('"')
        nip_x = [i for i in ip_x if i !='']
        ip = nip_x[-1] # ip
        po_x = nn_l[-1].split(':')
        port = po_x[-1] # port
    except Exception as e:
        statue = {'Code': 400, 'Message':'解析失败, 返回可能为空', 'Data': e}
        return statue

    # ip_pool = ip + ':' + port
    ip_pool = {
        'IP': ip,
        # 'Port': port
    }

    print(ip_pool, 'ippond')
    return ip_pool
