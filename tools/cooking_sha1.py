# -*- coding: utf-8 -*-

import hashlib
import sys
import base64
import json
reload(sys)
sys.setdefaultencoding("utf-8")

init_secret = "foobar"  # 初始化


def cooking_sha1(strings, secret=init_secret):

    strings = (strings + secret)
    sha1 = hashlib.sha1()
    sha1.update(strings.encode('utf-8'))
    res = sha1.hexdigest()
    return res

#print (json.dumps(contents.deviceId))
