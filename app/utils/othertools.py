# -*- coding:utf-8 -*-
__author__ = 'LangJin'

import os, hashlib,urllib
from flask import jsonify,make_response,session,request



def create_token():
    '''
    生成登陆后的token，格式如下：\n
    "eca7f38788d4764959919b46c61005038cf37f68"
    '''
    return hashlib.sha1(os.urandom(64)).hexdigest()

def encryption(username,password,role):
    '''
    说明：密码的加密算法,role是角色\n
    用法:encryption("用户名","明文密码","user")
    '''
    md5 = hashlib.md5()
    md5.update(password.encode("utf8")+username.encode("utf8")+keys.get(role).encode("utf8"))
    password = md5.hexdigest()
    return password

def checkusername(username):
    '''
    检查账号是否满足用户需求
    '''
    if username != None and username != "":
        if len(username) >= 5 and len(username) <= 12:
            for i in username:
                if i not in "0123456789qazwsxedcrfvtgbyhnujmikolp":
                    return "账号仅能由数字和字母组成！"
            return True
        else:
            return "账号长度必须大于等于5位，并且小于等于12位"
    else:
        return "账号不能为空！"


def checkpasswd(password):
    '''
    检查密码是否符合规范
    '''
    if password != None and password != "":
        if len(password) >= 8 and len(password) <= 16:
            for i in username:
                if i not in "0123456789qazwsxedcrfvtgbyhnujmikolp_!@#$%^&*<>?-=+|":
                    return "密码不能输入特殊字符！"
            return True
        else:
            return "密码长度必须大于等于8位，并且小于等于16位"
    else:
        return "密码不能为空！"

def checkloginstatus(session,token):
    '''
    检查用户的登录状态
    '''
    userinfo = session.get("userinfo")
    if userinfo != None and token != None:
        tokenid = userinfo.get("token")
        if tokenid == token:
            return True
        else:
            return False
    else:
        return False



def setcors(data):
    '''
    解决跨域问题
    '''
    referrer = request.referrer
    parse = urllib.parse
    scheme = parse.urlsplit(referrer).scheme
    netloc = parse.urlsplit(referrer).netloc
    res = make_response(jsonify(data))
    res.headers['Access-Control-Allow-Origin'] = "{scheme}://{netloc}".format(scheme=scheme, netloc=netloc)
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'true'
    return res


def checkContentType(request):
    '''
    检查用户headers的状态
    '''
    contentType = request.headers.get("Content-Type")
    if contentType == "application/json":
        return True
    else:
        return "请求头必须为application/json"


def is_number(s):
    '''
    判断输入值是否是数字
    '''
    if s != None and s != "":
        try:
            int(s)
            return True
        except ValueError:
            return "仅支持输入数字"
    else:
        return "不能为空"