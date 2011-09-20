#-*- encoding: utf-8 -*-


def git_to_list(pwd):
    git_command = [
    "git ls-files  -m|grep php",
    "git ls-files  -d|grep php",
    "git ls-files --exclude-standard --others |grep php"]
    git_list = []

    import os
    for command in git_command:
        git_line = pwd + command
        l = [line.strip() for line in os.popen(git_line).readlines()
             if line != '\n']
        git_list.append(l)
    return git_list


def fileToList(arrFilename):
    """ 读取文件到列表中 """
    arr = []
    for fileName in arrFilename:
        try:
            files = [lines.strip() for lines in
                 open(fileName, 'r').readlines()
                 if lines != '\n']
        except IOError:  # 如果文件不存在则创建新文件
            open(fileName, 'a').close()

        arr.append(files)

    return arr[:3], arr[-1]


def file_to_archive():
    """ 读取已存档的文件 """
    file_name = "archive.log"
    try:
        files = [lines.strip() for lines in
             open(file_name, 'r').readlines()
             if lines != '\n']
    except IOError:  # 如果文件不存在则创建新文件
        open(file_name, 'a').close()
        files = []

    return files


def compare_with_archive(compare, archives):
    """
     未跟踪，修改和已删除的文件和已发送的邮件
     做比较返回未发送的邮件列表
    """
    mail = []

    """
     files: 分别是添加，修改和删除的文件名列表
     single: 上面列表里的单个元素（文件名）
    """
    for files in compare:
        f = [single for single in files
             if single not in archives]
        mail.append(f)
    return mail


def write_to_archive(array):
    """ 本次已发送的邮件列表写入到archive.log中"""
    archive = open('archive.log', 'w+')
    array2 = [single for arr in array for single in arr]

    def stringn(string):
        return string + '\n'

    phpFile = map(stringn, array2)
    archive.writelines(phpFile)
    archive.close()


def construct_string(array, arrString):
    """ 格式化邮件内容 """
    mailString = ""

    for check in array:
        if check:
            index = array.index(check)  # 获取当前数组的下标
            tmpString = """%s
            %r
            """ % (arrString[index], array[index])

            mailString += tmpString + '\n'

    return mailString


def send_mail(mailString):
    """发送邮件"""
    import smtplib
    from email.MIMEText import MIMEText
    from email.MIMEMultipart import MIMEMultipart
    try:
        import config
    except ImportError:
        print "请拷贝config.sample.py为config.py，并进行配置"
        import sys
        sys.exit()

    msg = MIMEMultipart()   # 创建可包含附件的MIME对象
    msg['Subject'] = config.mailSubject
    msg['From'] = config.smtp_account
    msg['To'] = ",".join(config.mailList)

    txt = MIMEText(mailString, _charset='utf-8')
    msg.attach(txt)

    server = smtplib.SMTP(config.smtp_addr, config.smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.smtp_account, config.smtp_password)

    server.sendmail(config.smtp_account,
                    config.mailList,
                    msg.as_string())
    server.close()


def main():
    from config import git_dir
    pwd = 'cd ' + git_dir + ' ;'
    arr = git_to_list(pwd)
    archive_files = file_to_archive()

    mails = compare_with_archive(arr, archive_files)
    arr_mail_string = ['服务器添加了以下文件',
                       '服务器修改了以下文件',
                       '服务器删除了以下文件']
    mail_string = construct_string(mails, arr_mail_string)

    from psu import PSU
    p = PSU()
    mail_string += p.check_sys_status()

    if mail_string:
        send_mail(mail_string)
        write_to_archive(arr)

    from config import sms_notify
    if sms_notify:
        import sendsms
        sendsms.data["Content"] = mail_string
        sendsms.posttohost(sendsms.data)

if __name__ == "__main__":
    main()
