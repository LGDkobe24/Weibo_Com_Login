# -*- coding: utf-8 -*-
import urllib
import base64
import rsa
import binascii

def PostEncode(userName, passWord, serverTime, nonce, pubkey, rsakv):
    "Used to generate POST data"
    encodedUserName = GetUserName(userName)#Encode username using base64
    encodedPassWord = get_pwd(passWord, serverTime, nonce, pubkey)#rsa encoding currently
    postPara = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': encodedUserName,
        'service': 'miniblog',
        'servertime': serverTime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'sp': encodedPassWord,
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv': rsakv,     
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    postData = urllib.urlencode(postPara)#Network coding
    return postData

def GetUserName(userName):
    "Used to encode user name"
    userNameTemp = urllib.quote(userName)
    userNameEncoded = base64.encodestring(userNameTemp)[:-1]
    return userNameEncoded

def get_pwd(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #Create PubKey
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #Concatenate plaintext js
    passwd = rsa.encrypt(message, key) #Encode
    passwd = binascii.b2a_hex(passwd) #Transfer into hexadecimal number
    return passwd
