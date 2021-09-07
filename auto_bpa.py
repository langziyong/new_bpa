#!/usr/bin/python3
# coding=utf-8

import os
import execjs
import urllib.parse
import requests as req
import re
import time
import smtplib
import datetime
from email.mime.text import MIMEText
from email.utils import formataddr

os.chdir(os.path.dirname(__file__))

try:  # 打开 AES加密JS 文件
    with open("./aes.js", 'r', encoding = 'utf-8') as f:  # 打开JS文件
        aesjs = f.read()
        print("AES加密JS读取成功！")
except:
    print("AES加密JS读取失败！")


def get_aes_passwd(t):  # AES 密码加密
    aes = execjs.compile(aesjs)  # 加载JS文件
    return aes.call('Encrypt', str(t))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数


def get_chinese(t):
    a = t
    t = ''
    for i in a:
        if u'\u4e00' <= i <= u'\u9fff':
            u = i.encode('unicode_escape')
            a = '%5B' + re.search(r'(?<=\\u).+(?=\')', str(u)).group() + '%5D'
            t = t + a
        else:
            t = t + i
    return t


def login(user):
    user[2] = get_aes_passwd(user[2])
    log = "------------------报平安自动化日志------------------\n1#您的序列号为：" + str(user[0]) + '\n2#您的密码AES加密后为：' + str(user[2])  # 日志文件
    login_url = 'https://newca.zjtongji.edu.cn/cas/login?service=https%3A%2F%2Fbdmobile.zjtongji.edu.cn%3A8081%2FReportServer%3Fformlet%3Dxxkj%2Fmobile%2Fbpa%2Fbpa.frm%26op%3Dh5'
    login_headers_paper = {
        'Host':'newca.zjtongji.edu.cn',
        'Connection':'keep-alive',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache',
        'sec-ch-ua':r'"Chromium";v="88", "Google Chrome";v="88", ";Not\\A\"Brand";v="99"',
        'sec-ch-ua-mobile':'?1',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Mobile Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site':'none',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
    }
    requests_paper = req.get(url = login_url, headers = login_headers_paper)
    # print(requests_paper.headers)
    cookie_paper = re.search(r'JSESSIONID=\w+', requests_paper.headers['Set-Cookie']).group()
    # print(requests_paper.history)
    lt = re.search(r'(?<=<input type="hidden" name="lt" value=").+(?=")', requests_paper.text).group()
    execution = re.search(r'(?<=<input type="hidden" name="execution" value=").+(?=")', requests_paper.text).group()
    # print(requests_paper.text)
    print("登录页面请求成功")
    log = log + "\n3#登录页面请求成功"
    # log = log + "\nexecution=" + str(execution)
    login_headers = {
        'Host':'newca.zjtongji.edu.cn',
        'Connection':'keep-alive',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache',
        'sec-ch-ua':r'"Chromium";v="88","GoogleChrome";v="88",";Not\\A\"Brand";v="99"',
        'sec-ch-ua-mobile':'?1',
        'Upgrade-Insecure-Requests':'1',
        'Origin':'https://newca.zjtongji.edu.cn',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0(Linux;Android6.0;Nexus5Build/MRA58N)AppleWebKit/537.36(KHTML,likeGecko)Chrome/88.0.4324.182MobileSafari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Accept-Encoding':'gzip,deflate,br',
        'Accept-Language':'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
        'Cookie':cookie_paper
    }
    login_body = 'password=' + user[2] + '&username=' + user[1] + '&lt=' + urllib.parse.quote(lt, safe = '') + '&execution=' + urllib.parse.quote(execution, safe = '') + '&_eventId=submit'
    # print(login_body)
    requests = req.post(url = login_url, headers = login_headers, data = login_body, timeout = 4, verify = True)
    # print(requests.text)

    # 直接进行获取
    sessionid_cookie = re.search('JSESSIONID=\w+', requests.history[1].headers['Set-Cookie']).group()
    print("会话Cookie获取成功：" + sessionid_cookie)
    log = log + "\n4#会话Cookie获取成功：" + str(sessionid_cookie)
    # print(requests.history[1].headers['Set-Cookie'])
    sessionid = re.search('(?<=get sessionID\(\) {return \')\d+(?=\'})', requests.text).group()
    print("Sessionid获取成功：" + sessionid)
    log = log + "\n5#Sessionid获取成功：" + str(sessionid)
    # cookie = requests.history[1].headers['Location']
    # print("提交Cookie获取成功(网页内地址，存在问题)  " '%s' % cookie)
    print(time.strftime("%H:%M:%S", time.localtime()) + "用户%s学号%s成功登录" % (user[3], user[1]))

    # 标题检测暂时弃用
    '''  
    title_check = re.search(r'<title>.+</title>', requests.text).group()
    if title_check == "<title>报平安</title>":
        sessionid_cookie = re.search('JSESSIONID=\w+', requests.history[1].headers['Set-Cookie']).group()
        print("会话Cookie获取成功  " '%s' % sessionid_cookie)
        #print(requests.history[1].headers['Set-Cookie'])
        sessionid = re.search('(?<=get sessionID\(\) {return \')\d+(?=\'})', requests.text).group()
        print("Sessionid获取成功  "'%s'%sessionid)
        cookie = requests.history[1].headers['Location']
        print("提交Cookie获取成功(网页内地址，存在问题)  " '%s'%cookie)

    elif title_check == "<title>统一身份认证平台</title>":
        print("SessionID请求失败!可能是Cookie失效!")
    '''
    return {'sessionid_cookie':sessionid_cookie, 'log':log,'sessionid':sessionid}


def commit(user, sessionid_cookie, sessionid, log):
    print("开始提交数据！")
    # commit_url = 'https://bdmobile.zjtongji.edu.cn:8081/ReportServer;jsessionid='+ re.search(r'(?<=JSESSIONID=).+',sessionid_cookie).group()
    commit_url = 'https://bdmobile.zjtongji.edu.cn:8081/ReportServer'
    commit_headers = {
        'Host':'bdmobile.zjtongji.edu.cn:8081',
        'Connection':'keep-alive',
        "Content-Length":'',
        'terminal':'{"type":"mobile","os":"H5"}',
        'Origin':'https://bdmobile.zjtongji.edu.cn:8081',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
        'clienttype':'mobile/h5_5.0',
        'content-type':'application/x-www-form-urlencoded',
        'Accept':'* / *',
        'Accept-Encoding':'gzip,deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
        'Cookie':sessionid_cookie
    }
    commit_data = '''%7B%22xmlconf%22%3A%22%3C%3Fxml%20version%3D%5C%221.0%5C%22%20encoding%3D%5C%22UTF-8%5C%22%3F%3E%3CR%20xmlVersion%3D%5C%2220170720%5C%22%20releaseVersion%3D%5C%229.0.0%5C%22%20class%3D%5C%22com.fr.js.Commit2DBJavaScript%5C%22%3E%3CParameters%2F%3E%3CAttributes%20dsName%3D%5C%22sjjcpt%5C%22%20name%3D%5C%22%5B63d0%5D%5B4ea4%5D1%5C%22%2F%3E%3CDMLConfig%20class%3D%5C%22com.fr.write.config.IntelliDMLConfig%5C%22%3E%3CTable%20schema%3D%5C%22XX_SJJCPT%5C%22%20name%3D%5C%22T_XX_BPAXX%5C%22%2F%3E%3CColumnConfig%20name%3D%5C%22ACCNO%5C%22%20isKey%3D%5C%22true%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3D%24gh%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SJHM%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sjhm%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SZD%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22szd%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22MQZT%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22mqzt%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22ZTRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22ztrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22DD%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22dd%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFJTHB%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sfjthb%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFFRKS%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sffrks%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22FRKSRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22frksrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22BZ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22bz%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22GXSJ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3Dnow()%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SBRQ%5C%22%20isKey%3D%5C%22true%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sbrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTDZ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtdz%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFJTWZ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sfjtwz%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTWZRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtwzrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFJTTZ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sfjttz%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTTZRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jttzrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JCRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jcrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JCS%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jcs%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JG%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jg%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22GLFS%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22glfs%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFJY%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sfjy%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JZJG%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jzjg%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JCXXXX%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jcxxxx%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22WCN%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22wcn%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22HZJKM%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22hzjkm%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22HG%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22hg%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22QSGX%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22qsgx%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22FHSJ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22fhsj%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JCSJ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22scjcsj%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22CGDQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22CGDQ%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CCondition%20class%3D%5C%22com.fr.data.condition.ListCondition%5C%22%2F%3E%3C%2FDMLConfig%3E%3CAttributes%20dsName%3D%5C%22sjjcpt%5C%22%20name%3D%5C%22%5B63d0%5D%5B4ea4%5D2%5C%22%2F%3E%3CDMLConfig%20class%3D%5C%22com.fr.write.config.IntelliDMLConfig%5C%22%3E%3CTable%20schema%3D%5C%22XX_SJJCPT%5C%22%20name%3D%5C%22T_BPA_JTDD%5C%22%2F%3E%3CColumnConfig%20name%3D%5C%22ACCNO%5C%22%20isKey%3D%5C%22true%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3D%24gh%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SBRQ%5C%22%20isKey%3D%5C%22true%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sbrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTDD%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtdd%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTQSRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtqsrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTJSRQ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtjsrq%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTDD2%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtdd2%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTQSRQ2%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtqsrq2%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTJSRQ2%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtjsrq2%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTDD3%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtdd3%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTQSRQ3%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtqsrq3%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22JTJSRQ3%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22jtjsrq3%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CCondition%20class%3D%5C%22com.fr.data.condition.ListCondition%5C%22%2F%3E%3C%2FDMLConfig%3E%3CAttributes%20dsName%3D%5C%22sjjcpt%5C%22%20name%3D%5C%22%5B63d0%5D%5B4ea4%5D3%5C%22%2F%3E%3CDMLConfig%20class%3D%5C%22com.fr.write.config.IntelliDMLConfig%5C%22%3E%3CTable%20schema%3D%5C%22XX_SJJCPT%5C%22%20name%3D%5C%22T_XX_DGSXDY%5C%22%2F%3E%3CColumnConfig%20name%3D%5C%22XH%5C%22%20isKey%3D%5C%22true%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3D%24gh%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFCJSX%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sfsx%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFLSDW%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sfyls%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22SFDG%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22sfzg%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22DWDGSJ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22dwdgsj%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22BRDGSJ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22brdgsj%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22DGSXFH%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22aqfh%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22HJMS%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22aqyhms%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22DWMC%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22dwmc%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22DWDH%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22dwdh%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22DWSZD%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22swszd%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22GXSJ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3DNOW()%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CCondition%20class%3D%5C%22com.fr.data.condition.ListCondition%5C%22%2F%3E%3C%2FDMLConfig%3E%3CAttributes%20dsName%3D%5C%22sjjcpt%5C%22%20name%3D%5C%22%5B63d0%5D%5B4ea4%5D4%5C%22%2F%3E%3CDMLConfig%20class%3D%5C%22com.fr.write.config.IntelliDMLConfig%5C%22%3E%3CTable%20schema%3D%5C%22XX_SJJCPT%5C%22%20name%3D%5C%22T_XS_TEMP%5C%22%2F%3E%3CColumnConfig%20name%3D%5C%22XH%5C%22%20isKey%3D%5C%22true%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3D%24gh%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22RQ%5C%22%20isKey%3D%5C%22true%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3DTODAY()%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22TW1%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22tw1%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22TW2%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22WidgetName%5C%22%20class%3D%5C%22WidgetName%5C%22%3E%3CWidetName%20name%3D%5C%22tw2%5C%22%2F%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CColumnConfig%20name%3D%5C%22GXSJ%5C%22%20isKey%3D%5C%22false%5C%22%20skipUnmodified%3D%5C%22false%5C%22%3E%3CO%20t%3D%5C%22Formula%5C%22%20class%3D%5C%22Formula%5C%22%3E%3CAttributes%3E%3C!%5B5b%5DCDATA%5B5b%5D%3DNOW()%5B5d%5D%5B5d%5D%3E%3C%2FAttributes%3E%3C%2FO%3E%3C%2FColumnConfig%3E%3CCondition%20class%3D%5C%22com.fr.data.condition.ListCondition%5C%22%2F%3E%3C%2FDMLConfig%3E%3CJavaScript%20class%3D%5C%22com.fr.js.JavaScriptImpl%5C%22%3E%3CParameters%2F%3E%3CContent%3E%3C!%5B5b%5DCDATA%5B5b%5Dvar%20mqzt%3DglobalForm.getWidgetByName(%5C%22mqzt%5C%22).getValue()%3B%5Cnvar%20ztrq%3DglobalForm.getWidgetByName(%5C%22ztrq%5C%22).getValue()%3B%5Cnvar%20dd%3DglobalForm.getWidgetByName(%5C%22dd%5C%22).getValue()%3B%5Cnvar%20glfs%3DglobalForm.getWidgetByName(%5C%22glfs%5C%22).getValue()%3B%5Cnvar%20hg%3DglobalForm.getWidgetByName(%5C%22hg%5C%22).getValue()%3B%5Cnvar%20qsgx%3DglobalForm.getWidgetByName(%5C%22qsgx%5C%22).getValue()%3B%5Cnvar%20cgdq%3DglobalForm.getWidgetByName(%5C%22CGDQ%5C%22).getValue()%3B%5Cnvar%20fhsj%3DglobalForm.getWidgetByName(%5C%22fhsj%5C%22).getValue()%3B%5Cnif(mqzt%3D%3D2%26%26glfs%3D%3D'')%7B%5Cn%5CtFR.Msg.alert(%5C%22%5B9694%5D%5B79bb%5D%5B65b9%5D%5B5f0f%5D%5B4e0d%5D%5B5141%5D%5B8bb8%5D%5B4e3a%5D%5B7a7a%5D%5Bff01%5D%5C%22)%3B%5Cn%7Delse%20if(hg!%3D'9'%26%26(cgdq%3D%3D''%7C%7Cfhsj%3D%3D''))%7B%5Cn%5CtFR.Msg.alert(%5C%22%5B51fa%5D%5B56fd%5D%5B5730%5D%5B533a%5D%5B548c%5D%5B8fd4%5D%5B676d%5D%5B65f6%5D%5B95f4%5D%5B4e0d%5D%5B5141%5D%5B8bb8%5D%5B4e3a%5D%5B7a7a%5D%5Bff01%5D%5C%22)%3B%5Cn%7Delse%20if((hg.indexOf('2')%3E%3D0%7C%7Chg.indexOf('3')%3E%3D0)%26%26qsgx%3D%3D'')%7B%5Cn%5CtFR.Msg.alert(%5C%22%5B4eb2%5D%5B5c5e%5D%5B5173%5D%5B7cfb%5D%5B4e0d%5D%5B5141%5D%5B8bb8%5D%5B4e3a%5D%5B7a7a%5D%5Bff01%5D%5C%22)%3B%5Cn%7Delse%7B%20if%20(fr_submitinfo.success)%20%7B%5Cn%5Ct%2F*FR.Msg.toast('%5B63d0%5D%5B4ea4%5D%5B6210%5D%5B529f%5D')%3B*%2F%5Cn%5CtsetTimeout(function()%20%7B%5Cn%20%20%20%20%20_g('%24%7BsessionID%7D').writeReport()%3B%20%20%20%2F%2F%5B6267%5D%5B884c%5D%5B63d0%5D%5B4ea4%5D%5B5165%5D%5B5e93%5D%5B64cd%5D%5B4f5c%5D%20%5Cn%20%20%20%20%7D%2C%202000)%3B%5Cn%20%20%20%20%20%20%20%20var%20url%20%3D%20FR.cjkEncode(%5C%22%24%7BservletURL%7D%3Freportlet%3Dxxkj%2Fmobile%2Fdf%2FForm8.cpt%5C%22)%3B%20%20%5Cn%20%20%20%20FR.doHyperlinkByGet(%7B%20%20%5Cn%20%20%20%20%20%20%20%20url%3A%20url%2C%20%20%5Cn%20%20%20%20%20%20%20%20title%3A%20'%5B62a5%5D%5B5e73%5D%5B5b89%5D'%20%20%5Cn%20%20%20%20%7D)%3B%20%20%20%20%20%5Cn%7D%20else%20%7B%5Cn%5CtFR.Msg.toast('%5B63d0%5D%5B4ea4%5D%5B5931%5D%5B8d25%5D')%3B%5Cn%7D%5Cn%7D%5B5d%5D%5B5d%5D%3E%3C%2FContent%3E%3C%2FJavaScript%3E%3C%2FR%3E%22%2C%22callback%22%3A%22%3C%3Fxml%20version%3D%5C%221.0%5C%22%20encoding%3D%5C%22UTF-8%5C%22%3F%3E%3CR%20xmlVersion%3D%5C%2220170720%5C%22%20releaseVersion%3D%5C%229.0.0%5C%22%20class%3D%5C%22com.fr.js.JavaScriptImpl%5C%22%3E%3CParameters%2F%3E%3CContent%3E%3C!%5B5b%5DCDATA%5B5b%5Dvar%20mqzt%3DglobalForm.getWidgetByName(%5C%22mqzt%5C%22).getValue()%3B%5Cnvar%20ztrq%3DglobalForm.getWidgetByName(%5C%22ztrq%5C%22).getValue()%3B%5Cnvar%20dd%3DglobalForm.getWidgetByName(%5C%22dd%5C%22).getValue()%3B%5Cnvar%20glfs%3DglobalForm.getWidgetByName(%5C%22glfs%5C%22).getValue()%3B%5Cnvar%20hg%3DglobalForm.getWidgetByName(%5C%22hg%5C%22).getValue()%3B%5Cnvar%20qsgx%3DglobalForm.getWidgetByName(%5C%22qsgx%5C%22).getValue()%3B%5Cnvar%20cgdq%3DglobalForm.getWidgetByName(%5C%22CGDQ%5C%22).getValue()%3B%5Cnvar%20fhsj%3DglobalForm.getWidgetByName(%5C%22fhsj%5C%22).getValue()%3B%5Cnif(mqzt%3D%3D2%26%26glfs%3D%3D'')%7B%5Cn%5CtFR.Msg.alert(%5C%22%5B9694%5D%5B79bb%5D%5B65b9%5D%5B5f0f%5D%5B4e0d%5D%5B5141%5D%5B8bb8%5D%5B4e3a%5D%5B7a7a%5D%5Bff01%5D%5C%22)%3B%5Cn%7Delse%20if(hg!%3D'9'%26%26(cgdq%3D%3D''%7C%7Cfhsj%3D%3D''))%7B%5Cn%5CtFR.Msg.alert(%5C%22%5B51fa%5D%5B56fd%5D%5B5730%5D%5B533a%5D%5B548c%5D%5B8fd4%5D%5B676d%5D%5B65f6%5D%5B95f4%5D%5B4e0d%5D%5B5141%5D%5B8bb8%5D%5B4e3a%5D%5B7a7a%5D%5Bff01%5D%5C%22)%3B%5Cn%7Delse%20if((hg.indexOf('2')%3E%3D0%7C%7Chg.indexOf('3')%3E%3D0)%26%26qsgx%3D%3D'')%7B%5Cn%5CtFR.Msg.alert(%5C%22%5B4eb2%5D%5B5c5e%5D%5B5173%5D%5B7cfb%5D%5B4e0d%5D%5B5141%5D%5B8bb8%5D%5B4e3a%5D%5B7a7a%5D%5Bff01%5D%5C%22)%3B%5Cn%7Delse%7B%20if%20(fr_submitinfo.success)%20%7B%5Cn%5Ct%2F*FR.Msg.toast('%5B63d0%5D%5B4ea4%5D%5B6210%5D%5B529f%5D')%3B*%2F%5Cn%5CtsetTimeout(function()%20%7B%5Cn%20%20%20%20%20_g('%24%7BsessionID%7D').writeReport()%3B%20%20%20%2F%2F%5B6267%5D%5B884c%5D%5B63d0%5D%5B4ea4%5D%5B5165%5D%5B5e93%5D%5B64cd%5D%5B4f5c%5D%20%5Cn%20%20%20%20%7D%2C%202000)%3B%5Cn%20%20%20%20%20%20%20%20var%20url%20%3D%20FR.cjkEncode(%5C%22%24%7BservletURL%7D%3Freportlet%3Dxxkj%2Fmobile%2Fdf%2FForm8.cpt%5C%22)%3B%20%20%5Cn%20%20%20%20FR.doHyperlinkByGet(%7B%20%20%5Cn%20%20%20%20%20%20%20%20url%3A%20url%2C%20%20%5Cn%20%20%20%20%20%20%20%20title%3A%20'%5B62a5%5D%5B5e73%5D%5B5b89%5D'%20%20%5Cn%20%20%20%20%7D)%3B%20%20%20%20%20%5Cn%7D%20else%20%7B%5Cn%5CtFR.Msg.toast('%5B63d0%5D%5B4ea4%5D%5B5931%5D%5B8d25%5D')%3B%5Cn%7D%5Cn%7D%5B5d%5D%5B5d%5D%3E%3C%2FContent%3E%3C%2FR%3E%22%2C%22LABEL0%22%3A%22%5B59d3%5D%5B540d%5D%5Bff1a%5D%22%2C%22XM%22%3A%22''' + str(
        get_chinese(user[3])) + '''%22%2C%22LABEL1%22%3A%22%5B6240%5D%5B5728%5D%5B7cfb%5D%5Bff1a%5D%22%2C%22BM%22%3A%22''' + str(get_chinese(user[4])) + '''%22%2C%22LABEL2%22%3A%22%5B624b%5D%5B673a%5D%5B53f7%5D%5B7801%5D%5Bff1a%5D%22%2C%22SJHM%22%3A%22''' + str(user[5]) + '''%22%2C%22LABEL19%22%3A%22%5B7c4d%5D%5B8d2f%5D%5Bff1a%5D%22%2C%22JG%22%3A%22''' + str(get_chinese(user[6])) + '''%22%2C%22LABEL13%22%3A%22%5B4e0a%5D%5B62a5%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22SBRQ%22%3A%22''' + (datetime.datetime.now() + datetime.timedelta(days = 1)).strftime(
        "%Y-%m-%d") + '''%22%2C%22LABEL4%22%3A%22%5B76ee%5D%5B524d%5D%5B72b6%5D%5B6001%5D%5Bff1a%5D%22%2C%22MQZT%22%3A%221%22%2C%22LABEL25%22%3A%22%5B9694%5D%5B79bb%5D%5B65b9%5D%5B5f0f%5D%5Bff1a%5D%22%2C%22GLFS%22%3A%22%22%2C%22LABEL5%22%3A%22%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22ZTRQ%22%3A%22%22%2C%22LABEL11%22%3A%22%5B662f%5D%5B5426%5D%5B5b58%5D%5B5728%5D%5B53d1%5D%5B70ed%5D%5B6216%5D%5B54b3%5D%5B55fd%5D%5B4e4f%5D%5B529b%5D%5B7b49%5D%5B75c7%5D%5B72b6%5D%5Bff1a%5D%22%2C%22LABEL6%22%3A%22%5B5730%5D%5B70b9%5D%5Bff1a%5D%22%2C%22SFFRKS%22%3A%220%22%2C%22DD%22%3A%22%22%2C%22LABEL29%22%3A%22%5B4eca%5D%5B65e5%5D%5B4e0a%5D%5B5348%5D%5B4f53%5D%5B6e29%5D%5Bff1a%5D%22%2C%22LABEL12%22%3A%22%5B53d1%5D%5B70ed%5D%5B54b3%5D%5B55fd%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22FRKSRQ%22%3A%22%22%2C%22TW1%22%3A%22''' + str(user[9]) + '''%22%2C%22LABEL29_C%22%3A%22%5B6628%5D%5B65e5%5D%5B4e0b%5D%5B5348%5D%5B4f53%5D%5B6e29%5D%5Bff1a%5D%22%2C%22TW2%22%3A%22''' + str(
        user[10]) + '''%22%2C%22LABEL26%22%3A%22%5B662f%5D%5B5426%5D%5B5c31%5D%5B533b%5D%5Bff1a%5D%22%2C%22SFJY%22%3A%22%22%2C%22LABEL27%22%3A%22%5B5c31%5D%5B8bca%5D%5B7ed3%5D%5B679c%5D%5Bff1a%5D%22%2C%22JZJG%22%3A%22%22%2C%22LABEL3%22%3A%22%5B76ee%5D%5B524d%5D%5B5c45%5D%5B4f4f%5D%5B5730%5D%5Bff1a%5D%22%2C%22SZD%22%3A%22''' + str(get_chinese(user[7])) + '''%22%2C%22LABEL14%22%3A%22%5B5177%5D%5B4f53%5D%5B5730%5D%5B5740%5D%5Bff1a%5D%22%2C%22JTDZ%22%3A%22''' + str(get_chinese(user[
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  8])) + '''%22%2C%22LABEL30%22%3A%2214%5B65e5%5D%5B5185%5D%5B7ecf%5D%5B505c%5D%5B5730%5D(%5B676d%5D%5B5dde%5D%5B9664%5D%5B5916%5D)%5Bff1a%5D%22%2C%22SFJT%22%3A%220%22%2C%22LABEL8%22%3A%2214%5B65e5%5D%5B5185%5D%5B7ecf%5D%5B505c%5D%5B5730%5D%5B70b9%5D(%5B676d%5D%5B5dde%5D%5B9664%5D%5B5916%5D)%5Bff1a%5D%22%2C%22JTDD%22%3A%22%22%2C%22LABEL15%22%3A%22%5B7ecf%5D%5B505c%5D%5B8d77%5D%5B59cb%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22LABEL9%22%3A%22%5B8fd1%5D14%5B5929%5D%5B5185%5D%5B63a5%5D%5B89e6%5D%5B53f2%5D%5Bff1a%5D%22%2C%22JTQSRQ%22%3A%22%22%2C%22JCS%22%3A%229%22%2C%22LABEL16%22%3A%22%5B7ecf%5D%5B505c%5D%5B7ed3%5D%5B675f%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22JTJSRQ%22%3A%22%22%2C%22LABEL7%22%3A%22%5B7ecf%5D%5B505c%5D%5B5730%5D%5B70b9%5D2%5Bff1a%5D%22%2C%22JTDD2%22%3A%22%22%2C%22LABEL20%22%3A%22%5B7ecf%5D%5B505c%5D%5B8d77%5D%5B59cb%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22JTQSRQ2%22%3A%22%22%2C%22LABEL21%22%3A%22%5B7ecf%5D%5B505c%5D%5B7ed3%5D%5B675f%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22JTJSRQ2%22%3A%22%22%2C%22LABEL22%22%3A%22%5B7ecf%5D%5B505c%5D%5B5730%5D%5B70b9%5D3%5Bff1a%5D%22%2C%22JTDD3%22%3A%22%22%2C%22LABEL23%22%3A%22%5B7ecf%5D%5B505c%5D%5B8d77%5D%5B59cb%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22JTQSRQ3%22%3A%22%22%2C%22LABEL24%22%3A%22%5B7ecf%5D%5B505c%5D%5B7ed3%5D%5B675f%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22JTJSRQ3%22%3A%22%22%2C%22LABEL28%22%3A%22%5B63a5%5D%5B89e6%5D%5B8be6%5D%5B7ec6%5D%5B4fe1%5D%5B606f%5D%5Bff1a%5D%22%2C%22JCXXXX%22%3A%22%22%2C%22LABEL17%22%3A%22%5B63a5%5D%5B89e6%5D%5B65e5%5D%5B671f%5D%5Bff1a%5D%22%2C%22JCRQ%22%3A%22%22%2C%22LABEL50%22%3A%22%5B8fd1%5D14%5B5929%5D%5B5185%5D%5B63a5%5D%5B89e6%5D%5B56de%5D%5B56fd%5D%5Bff08%5D%5B5165%5D%5B5883%5D%5Bff09%5D%5B4eba%5D%5B5458%5D%5B4fe1%5D%5B606f%5D%5Bff1a%5D%22%2C%22HG%22%3A%229%22%2C%22LABEL51%22%3A%22%5B4eb2%5D%5B5c5e%5D%5B5173%5D%5B7cfb%5D%5Bff1a%5D%22%2C%22LABEL18%22%3A%22%5B5065%5D%5B5eb7%5D%5B7801%5D%5Bff1a%5D%22%2C%22QSGX%22%3A%22%22%2C%22HZJKM%22%3A%221%22%2C%22LABEL52%22%3A%22%5B51fa%5D%5B56fd%5D%5B5730%5D%5B533a%5D%5Bff1a%5D%22%2C%22CGDQ%22%3A%22%22%2C%22LABEL53%22%3A%22%5B8fd4%5D%5B676d%5D%5B65f6%5D%5B95f4%5D%5Bff1a%5D%22%2C%22FHSJ%22%3A%22%22%2C%22LABEL54%22%3A%22%5B9996%5D%5B6b21%5D%5B63a5%5D%5B89e6%5D%5B65f6%5D%5B95f4%5D%5Bff1a%5D%22%2C%22SCJCSJ%22%3A%22%22%2C%22LABEL10%22%3A%22%5B5907%5D%5B6ce8%5D%5Bff1a%5D%22%2C%22BZ%22%3A%22%22%2C%22LABEL40%22%3A%22%5B662f%5D%5B5426%5D%5B9700%5D%5B8981%5D%5B53c2%5D%5B52a0%5D%5B6bd5%5D%5B4e1a%5D%5B9876%5D%5B5c97%5D%5B5b9e%5D%5B4e60%5D%5Bff1a%5D%22%2C%22SFSX%22%3A%220%22%2C%22LABEL41%22%3A%22%5B662f%5D%5B5426%5D%5B843d%5D%5B5b9e%5D%5B5b9e%5D%5B4e60%5D%5B5355%5D%5B4f4d%5D%5Bff1a%5D%22%2C%22SFYLS%22%3A%22%22%2C%22LABEL42%22%3A%22%5B76ee%5D%5B524d%5D%5B5df2%5D%5B7ecf%5D%5B5230%5D%5B516c%5D%5B53f8%5D%5B73b0%5D%5B573a%5D%5B4e0a%5D%5B73ed%5D%5Bff08%5D%5B4e0d%5D%5B542b%5D%5B5c45%5D%5B5bb6%5D%5B529e%5D%5B516c%5D%5Bff09%5D%5Bff1a%5D%22%2C%22SFZG%22%3A%22%22%2C%22LABEL43%22%3A%22%5B5355%5D%5B4f4d%5D%5B8981%5D%5B6c42%5D%5B5230%5D%5B5c97%5D%5B65f6%5D%5B95f4%5D%5Bff1a%5D%22%2C%22DWDGSJ%22%3A%22%22%2C%22LABEL44%22%3A%22%5B672c%5D%5B4eba%5D%5B8ba1%5D%5B5212%5D%5B5230%5D%5B5c97%5D%5B65f6%5D%5B95f4%5D%5Bff1a%5D%22%2C%22LABEL45%22%3A%22%5B9876%5D%5B5c97%5D%5B5b9e%5D%5B4e60%5D%5B5b89%5D%5B5168%5D%5B9632%5D%5B62a4%5D%5B60c5%5D%5B51b5%5D%5B5b%5D%5B591a%5D%5B9009%5D%5B9898%5D%5B5d%5D%5Bff1a%5D%22%2C%22AQFH%22%3A%22%22%2C%22BRDGSJ%22%3A%22%22%2C%22LABEL46%22%3A%22%5B9876%5D%5B5c97%5D%5B5b9e%5D%5B4e60%5D%5B73af%5D%5B5883%5D%5B9632%5D%5B75ab%5D%5B5b89%5D%5B5168%5D%5B9690%5D%5B60a3%5D%5B63cf%5D%5B8ff0%5D%5Bff1a%5D%22%2C%22AQYHMS%22%3A%22%22%2C%22LABEL47%22%3A%22%5B5b9e%5D%5B4e60%5D%5B5355%5D%5B4f4d%5D%5B540d%5D%5B79f0%5D%5Bff1a%5D%22%2C%22DWMC%22%3A%22%22%2C%22LABEL48%22%3A%22%5B5b9e%5D%5B4e60%5D%5B5355%5D%5B4f4d%5D%5B8054%5D%5B7cfb%5D%5B7535%5D%5B8bdd%5D%5Bff1a%5D%22%2C%22DWDH%22%3A%22%22%2C%22LABEL49%22%3A%22%5B5b9e%5D%5B4e60%5D%5B5355%5D%5B4f4d%5D%5B6240%5D%5B5728%5D%5B5730%5D%5Bff1a%5D%22%2C%22SWSZD%22%3A%22%22%2C%22WCN%22%3A%5B5b%5D%221%22%5B5d%5D%2C%22BUTTON0%22%3A%22%5B63d0%5D%5B4ea4%5D%22%7D'''
    commit_body = '__device__=unknown&op=dbcommit&path=%2Fview%2Freport&sessionID=' + str(sessionid) + '&__parameters__=' + commit_data.encode("utf-8").decode("latin1") + '&'
    requests = req.post(url = commit_url, headers = commit_headers, data = commit_body, timeout = 4, verify = True)
    print("提交地址为：" + commit_url)
    log = log + "\n6#提交地址为：" + commit_url
    # print("提交数据为：" + commit_body)
    # log = log + "\n提交数据为："+commit_body
    log = log + "\n7#提交数据已拼接\n8#用户源数据" + str(user)
    print("↓↓↓↓↓↓↓↓↓↓POST请求响应检查点↓↓↓↓↓↓↓↓↓↓ \n如果下面行为空说明提交失败！有 'callback' 字样表示成功")
    log = log + "\n↓POST请求响应检查点↓ \n如果下面行为空说明提交失败！有 'callback' 字样表示成功\n"
    print(requests.text)
    log = log + requests.text
    print("↑↑↑↑↑↑↑↑↑↑表单数据提交完毕检查点↑↑↑↑↑↑↑")
    log = log + "\n↑表单数据提交完毕检查点↑\n如果上！面行为空说明提交失败！有 'callback' 字样表示成功"

    commit2_url = 'https://bdmobile.zjtongji.edu.cn:8081/ReportServer?reportlet=xxkj%2Fmobile%2Fdf%2FForm8.cpt&op=h5'
    commit2_headers = {
        'Host':'bdmobile.zjtongji.edu.cn:8081',
        'Connection':'keep-alive',
        'sec-ch-ua':r'"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile':'?0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User':'?1',
        'Sec-Fetch-Dest':'document',
        'Referer':'https://bdmobile.zjtongji.edu.cn:8081/ReportServer;jsessionid=' + re.search(r'(?<=JSESSIONID=).+', sessionid_cookie).group() + '?formlet=xxkj/mobile/bpa/bpa.frm&op=h5',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
        'Cookie':sessionid_cookie
    }
    requests = req.get(url = commit2_url, headers = commit2_headers)
    # print('第2次get页面 在提交之后:\n'+requests.text)
    sessionid_2 = re.search('(?<=get sessionID\(\) {return \')\d+(?=\'})', requests.text).group()
    print("Sessionid_2获取成功  "'%s' % sessionid_2)
    log = log + "\n8#Sessionid_2获取成功  "'%s' % sessionid_2

    commit_body = r'op=fs&cmd=h5_get_auth&__device__=unknown&'
    requests = req.post(url = commit_url, headers = commit_headers, data = commit_body, timeout = 4, verify = True)
    print('第3次post页面 :\n' + requests.text)
    log = log + '\n9#第3次post页面 :\n' + requests.text

    commit_body = r'__device__=unknown&op=h5_template&sessionID=' + sessionid_2 + '&cmd=firstdata&'
    requests = req.post(url = commit_url, headers = commit_headers, data = commit_body, timeout = 4, verify = True)
    print('第4次post页面 :\n' + requests.text)
    log = log + '\n10#第4次post页面 :\n' + requests.text

    commit_body = r'__device__=unknown&toVanCharts=true&op=page_content&cmd=json&sessionID=' + sessionid_2 + '&pn=1&path=&'
    requests = req.post(url = commit_url, headers = commit_headers, data = commit_body, timeout = 4, verify = True)
    print('第5次post页面省略\n')
    # log = log + '\n第5次post页面 :\n' + requests.text
    log = log + '\n11#第5次post页面 :\n' + '省略'

    commit_body = r'__device__=unknown&op=h5_manager&cmd=setting_get&'
    requests = req.post(url = commit_url, headers = commit_headers, data = commit_body, timeout = 4, verify = True)
    print('第6次post页面 :\n' + requests.text)
    log = log + '\n12#第6次post页面 :\n' + requests.text
    log = log + '\n------------------日志结束------------------'
    log = log + '\n------------------' + time.strftime("%H:%M:%S", time.localtime()) + '------------------'
    print(time.strftime("%H:%M:%S", time.localtime()) + "用户%s学号%s成功提交！" % (user[3], user[1]))
    send_mail(user, log)


def send_mail(user, log):
    my_sender = '2502164784@qq.com'  # 发件人邮箱账号
    my_pass = 'cmyscdshikxbdjgf'  # 发件人邮箱密码
    my_user = str(user[11])  # 收件人邮箱账号
    clock_time = time.strftime("%H:%M:%S", time.localtime())

    try:
        text = str(clock_time) + '主进程-消息：\n姓名：' + str(user[3]) + '  账号：' + str(user[1]) + '\n今日报平安<主进程>已提交！以下是提交数据！\n' + log
        msg = MIMEText(str(text), 'plain', 'utf-8')
        msg['From'] = formataddr(("zhaoyong_sever", my_sender))
        msg['To'] = formataddr((str(user[1]), my_user))
        msg['Subject'] = time.strftime("%Y-%m-%d", time.localtime()) + "报平安自动化<主进程>"
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
        print("邮件发送成功")
    except:
        print("邮件发送失败")


def bpa(user):
    q = login(user)
    sessionid = q['sessionid']
    sessionid_cookie = q['sessionid_cookie']
    log = q['log']
    commit(user, sessionid_cookie,sessionid, log)

