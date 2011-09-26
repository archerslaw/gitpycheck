#-*- encoding: utf-8 -*-


def constructData(data):
    """根据规则组成md5"""
    data['Content'] = data['Content'].decode("utf-8")
    data['Content'] = data['Content'].encode("gb2312")
    string = "%s" * 7  % (data["ID"],
                          data['UserName'],
                          data['Md5key'],
                          data['SendNum'],
                          data['Content'],
                          data['SendTiming'],
                          data['SendTime'])
    import hashlib
    m = hashlib.md5(string)
    data["MD5String"] = m.hexdigest()

    encode = ""
    import urllib
    for key in data:
        val = str(data[key])
        formater = "%s" * 4
        string = formater % (urllib.quote(key),
                             "=",
                             urllib.quote(val),
                             "&")
        encode += string

    return encode[:-1]


def posttohost(data):
    """提交短信到发送列队"""
    url = "http://sms.powereasy.net/MessageGate/Message.aspx"
    for num in data["sendNums"]:
        data["SendNum"] = num
        string = constructData(data)
        import urllib2
        req = urllib2.Request(url, string)
        urllib2.urlopen(req)


def getTime(formater):
    """组成短信要求的时间格式"""
    import time
    timenow = time.time()
    local = time.localtime(timenow)
    return time.strftime(formater, local)


import config
data = {}

data["ID"] = getTime("%Y%m%d%H%M%S")
data["UserName"] = config.sms_userName
data["Md5key"] = config.sms_md5Key
data["Content"] = ""
data["SendTiming"] = config.sms_sendTiming
data["SendTime"] = config.sms_sendTime
data["sendNums"] = config.sms_sendNum
