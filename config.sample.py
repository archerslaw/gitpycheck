#-*- encoding: utf-8 -*-
smtp_addr = ""        #smtp地址
smtp_port = 587       #smtp端口
smtp_account = ""     #账户
smtp_password = ""    #密码
mailList = []         #收件列表
mailSubject = ""      #邮件主题

sms_notify = False
sms_userName = ""
sms_md5Key = ""
sms_sendNum = []
sms_sendTiming = 0     #0为即时发送 1为定时发磅
sms_sendTime = ""      #定时发送的时间

cpu_warn_percent = 70  # cpu报警使用率
mem_warn_percent = 90  # 内存报警使用率
disks_warn_percent = 80  # 硬盘报警使用率
neto_warn_avg = 2048.00  # 网络流出平均值
neti_warn_avg = 1024.00  # 网络流入平均值
net_warn_established = 200 # 已建立连接报警值
net_warn_syn = 100         # 半开通连接报警值

webserver_process = ['httpd']  # 需要监控的web服务器的进程名称
database_process = ['mysql']
