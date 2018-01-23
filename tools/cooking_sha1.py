# -*- coding: utf-8 -*-

import hashlib
import sys
import base64
reload(sys)
sys.setdefaultencoding("utf-8")

secret_cooking3 = "foobar"  # 测试服
secret_cooking2 = ""  # 测试服


def cooking_sha1(strings, secret=secret_cooking2):

    strings = (strings + secret)
    sha1 = hashlib.sha1()
    sha1.update(strings.encode('utf-8'))
    res = sha1.hexdigest()
    return res
