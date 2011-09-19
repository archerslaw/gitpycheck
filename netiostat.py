#!/usr/bin/python
#coding=utf-8
#file : netiostat
#author : flynetcn

from __future__ import division
import sys
import os
import time
import signal

netcmd = '/sbin/ifconfig eth0 | grep bytes'


def getnetio(line):
    s1 = line.find('RX bytes:') + 9
    e1 = line.find(' ', s1)
    neti = line[s1:e1]
    s2 = line.find('TX bytes:') + 9
    e2 = line.find(' ', s2)
    neto = line[s2:e2]
    return (int(neti), int(neto))


def int_handler(signum, frame):
    print ""
    sys.exit()


def get_net_io():
    signal.signal(signal.SIGINT, int_handler)
    line = os.popen(netcmd).readline().strip()
    netio = getnetio(line)
    neti_start = netio[0]
    neto_start = netio[1]
    time_start = time.time()
    count = 60
    neti_list = []
    neto_list = []
    while (count > 0):
        count -= 1
        time.sleep(1)
        info = []
        line = os.popen(netcmd).readline().strip()
        netio = getnetio(line)
        info.append("网络流入总量:%.4fm, 网络流出总量:%.4fm"
                    % (netio[0] / 1024 / 1024, netio[1] / 1024 / 1024))
        time_curr = time.time()
        neti_total = netio[0] - neti_start
        neto_total = netio[1] - neto_start
        sec_total = time_curr - time_start
        neti_start = netio[0]
        neto_start = netio[1]
        time_start = time_curr

        neti_avg = neti_total / sec_total / 1024
        neti_list.append(neti_avg)

        neto_avg = neto_total / sec_total / 1024
        neto_list.append(neto_avg)

        info.append("当前网络流入速度:%.4fk/s"
                    % (neti_total / sec_total / 1024))
        info.append("当前网络流出速度:%.4fk/s"
                    % (neto_total / sec_total / 1024))
        info.append("当前网络平均流入速度:%.4fk/s"
                    % (sum(neti_list) / len(neti_list)))
        info.append("当前网络平均流出速度:%.4fk/s"
                    % (sum(neto_list) / len(neto_list)))
        #show = ", ".join(info)
        #sys.stdout.write(show+"\r")
        #sys.stdout.flush()

    #print ""

    def sort_avg(li):
        li.sort()
        li = li[1:-1]
        return li

    neti_list = sort_avg(neti_list)
    neto_list = sort_avg(neto_list)
    return  (neti_list, neto_list, (sum(neti_list) / len(neti_list)),
             (sum(neto_list) / len(neto_list)))

if __name__ == '__main__':
    print get_net_io()[3]
