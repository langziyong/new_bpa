#!/usr/bin/python3
# coding=utf-8

import json

import requests as req

from auto_bpa import get_aes_passwd


def get_verify_code_tips(xh):
    url = f'https://newca.zjtongji.edu.cn/ng//out/security/getEmail?username={xh}&%22%22'
    headers = {
        'Host':'newca.zjtongji.edu.cn',
        'Connection':'keep-alive',
        'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With':'XMLHttpRequest',
        'sec-ch-ua-mobile':'?0',
        'access_token':'',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Content-Type':'application/json;charset=utf-8',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Dest':'empty',
        'Referer':'https://newca.zjtongji.edu.cn/security/start/index.html',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
    }
    try:
        r = req.get(url = url, headers = headers)
    except:
        return '获取提示请求失败'
    q = json.loads(r.text)
    return q


def send_verify_code(xh):
    tips = get_verify_code_tips(xh)
    url = 'https://newca.zjtongji.edu.cn/ng//out/security/emailCode'
    headers = {
        'Host':'newca.zjtongji.edu.cn',
        'Connection':'keep-alive',
        'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With':'XMLHttpRequest',
        'sec-ch-ua-mobile':'?0',
        'access_token':'',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Content-Type':'application/json;charset=utf-8',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Dest':'empty',
        'Referer':'https://newca.zjtongji.edu.cn/security/start/index.html',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
    }
    data = '{"username":"%s"}' % xh
    try:
        r = req.post(url = url, headers = headers, data = data)
    except:
        return '发送验证码请求失败'
    q = json.loads(r.text)
    return {'tips':tips, 'send_msg':q}


def reset_password(xh, verify, new_password):
    new_password = get_aes_passwd(new_password)
    url = 'https://newca.zjtongji.edu.cn/ng//out/security/changePwd'
    headers = {
        'Host':'newca.zjtongji.edu.cn',
        'Connection':'keep-alive',
        'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With':'XMLHttpRequest',
        'sec-ch-ua-mobile':'?0',
        'access_token':'',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Content-Type':'application/json;charset=utf-8',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Dest':'empty',
        'Referer':'https://newca.zjtongji.edu.cn/security/start/index.html',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-HK;q=0.5',
    }
    data = '{"username":"%s","validcode":"%s","password":"%s"}' % (xh, verify, new_password)
    print(data)
    try:
        r = req.post(url = url, headers = headers, data = data)
    except:
        return '修改请求失败'
    q = json.loads(r.text)
    return q
