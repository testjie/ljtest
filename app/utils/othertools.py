# -*- coding:utf-8 -*-
__author__ = 'LangJin'

import os, hashlib,urllib
from flask import jsonify,make_response,session,request
from config import keys
import re

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
        username = str(username)
        if len(username) >= 5 and len(username) <= 12:
            for i in username:
                if i not in "0123456789qazwsxedcrfvtgbyhnujmikolp":
                    return "账号仅能由数字和小写字母组成！"
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
        password = str(password)
        if len(password) >= 8 and len(password) <= 16:
            for i in password:
                if i not in "0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJMIKOLP_!@#$%^&*<>?-=+|":
                    return "密码不能输入特殊字符！"
            return True
        else:
            return "密码长度必须大于等于8位，并且小于等于16位"
    else:
        return "密码不能为空！"

def checkuserinfo(username,password):
    '''
    检查用户的账号密码是否符合规范
    '''
    usernamemsg = checkusername(username)
    passwordmsg = checkpasswd(password)
    if usernamemsg == True:
        if passwordmsg == True:
            return True
        else:
            return passwordmsg
    else:
        return usernamemsg
    


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
            return "token无效，请重新登录"
    else:
        return "请先登录后再操作！"



def setcors(data=None,msg="操作成功！",status=401):
    '''
    解决跨域问题
    '''
    res = {
        "data":data,
        "msg":msg,
        "status":status
    }
    referrer = request.referrer
    parse = urllib.parse
    scheme = parse.urlsplit(referrer).scheme
    netloc = parse.urlsplit(referrer).netloc
    res = make_response(jsonify(res))
    res.headers['Access-Control-Allow-Origin'] = "{scheme}://{netloc}".format(scheme=scheme, netloc=netloc)
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    res.headers['Access-Control-Allow-Credentials'] = 'true'
    return res


def setcorsimg(data=None,msg="操作成功！",errno=401):
    '''
    解决跨域问题
    '''
    res = {
        "data":data,
        "msg":msg,
        "errno":errno
    }
    referrer = request.referrer
    parse = urllib.parse
    scheme = parse.urlsplit(referrer).scheme
    netloc = parse.urlsplit(referrer).netloc
    res = make_response(jsonify(res))
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
            if int(s) > 0:
                return True
            else:
                return "数字必须大于0"
        except ValueError:
            return "【{}】应该是数字才行！".format(s)
    else:
        return "不能为空"

def checkctype(ctype):
    '''
    检查ctype的类型对不对
    '''
    if ctype in [0,1,2,3,"0","1","2","3"]:
        return True
    else:
        return "ctype不在范围内，0教程1提问2灵感3心得体会"



def checkvalueisNone(valuelist):
    '''
    检查输入的参数是否为空
    '''
    for i in valuelist:
        if i == None or i == "":
            return "输入的参数不能有空值！"
    return True



def checkphonenum(phone):
    '''
    正则判断手机号格式
    '''
    res = re.match("^(13[0-9]|14[5|7]|15[0|1|2|3|4|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$",phone)
    if res:
        return True
    else:
        return "请输入正确的手机号！"


def checkemail(email):
    '''
    正则判断邮箱格式
    '''
    res = re.match("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",email)
    if res:
        return True
    else:
        return "请输入正确的邮箱！"

def checkvaluelen(value,num):
    '''
    校验字符串的长度是否合法
    value是校验的值，num是长度的限制
    '''
    if value != None or value != "":
        if len(value) > num:
            return "长度不能大于%s" % num
        else:
            return True
    else:
        return "不能为空哦~"


def checklistid(value):
    '''
    检查输入的值是否符合规范
    例：1,2,3,
    '''
    res = re.match("^([0-9]+,)+$",value)
    # print(res)
    if res:
        return True
    else:
        return "输入的值不符合规范，必须以数字开头逗号结尾，如1,2,3,"