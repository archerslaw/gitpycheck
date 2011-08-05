#-*- encoding: utf-8 -*-
mailFrom = ""
mailList = []
mailPass = ""
mailSubject = ""


def fileToList(arrFilename):
    """ 读取文件到列表中 """
    arr = []
    for fileName in arrFilename:
        try:
            lines = open(fileName, 'r').readlines()
        except IOError: #如果文件不存在则创建新文件
            open(fileName, 'a').close()
            lines = ""

        arr.append(lines)
    return arr[:3], arr[-1]


def compareWithArchive(compare, archives):
    """
     未跟踪，修改和已删除的文件和已发送的邮件
     做比较返回未发送的邮件列表
    """
    mail = []
    for files in compare:
        f = []
        for single in files:
            if single not in archives:
                f.append(single)
        mail.append(f)
    return mail


def writeToArchive(array):
    """ 本次已发送的邮件列表写入到archive.log中"""
    archive = open('archive.log', 'a+')
    for arr in array:
        for string in arr:
            phpFile = string + '\n'
            archive.write(phpFile)
    archive.close()


def constructString(array, arrString):
    """ 格式化邮件内容 """
    mailString = ""

    for check in array:
        if check:
            index = array.index(check) #获取当前数组的下标
            tmpString = """%s
            %r
            """ % (arrString[index], array[index])

            mailString += tmpString + '\n'

    return mailString

arrFilename = ['add.log', 'mod.log', 'del.log', 'archive.log']
arr, archiveFiles = fileToList(arrFilename)

mails = compareWithArchive(arr, archiveFiles)
arrString = ['服务器添加了以下文件',
             '服务器修改了以下文件',
             '服务器删除了以下文件']
mailString = constructString(mails, arrString)

if mailString:
    import smtplib
    from email.MIMEText import MIMEText
    from email.MIMEMultipart import MIMEMultipart

    msg = MIMEMultipart()   #创建可包含附件的MIME对象
    msg['Subject'] = mailSubject
    msg['From'] = mailFrom
    msg['To'] = mailList

    txt = MIMEText(mailString, _charset='utf-8')
    msg.attach(txt)

    server = smtplib.SMTP('smtp.gmail.com', 587) #port 465 or 587
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(mailFrom, mailPass)

    server.sendmail(mailFrom,
                    mailList,
                    msg.as_string())
    server.close()
    writeToArchive(mails)
