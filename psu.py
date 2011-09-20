#-*- encoding: utf-8 -*-

import psutil


class PSU(object):
    """使用psutil检查服务器系统进程"""

    def __init__(self):
        """初始化"""
        self.warning_report = ""

    def check_sys_status(self):
        """获取CPU,内存，硬盘的信息"""
        func_list = [self.get_sys_cpu_info,
                     self.get_sys_mem_info,
                     self.get_sys_disks_info]
        self.get_sys_warn_info(func_list)

        """获取web服务器进程"""
        from config import webserver_process
        func_list = [self.get_process_info]
        self.get_sys_warn_info(func_list,
                               process=webserver_process,
                               connection=True)

        """获取数据库进程"""
        from config import database_process
        func_list = [self.get_process_info]
        self.get_sys_warn_info(func_list,
                               process=database_process,
                               connection=False)

        """检查网络"""
        func_list = [self.get_net_io]
        self.get_sys_warn_info(func_list)
        return self.warning_report

    def get_sys_warn_info(self, func_list, **args):
        for func in func_list:
            #print func.__name__
            msg_list = func(**args)

            if msg_list:
                for msg in msg_list:
                    '''判断报警信息'''
                    sys_warn_msg_list = ['warn_condiction',
                                              'warn_num',
                                              'warn_msg']
                    msg_dict = dict(zip(sys_warn_msg_list, msg))

                    if msg_dict['warn_condiction'] > msg_dict['warn_num']:
                        warn_msg = msg_dict['warn_msg']
                        warn_num = str(msg_dict['warn_num'])
                        self.warning_report += warn_msg + warn_num + '\n'

    def get_sys_cpu_info(self):
        """获取CPU信息"""
        from config import cpu_warn_percent
        import time
        self.cpu_percent = psutil.cpu_percent(interval=0)
        time.sleep(1)
        self.cpu_percent = psutil.cpu_percent(interval=1)

        return [self.cpu_percent, cpu_warn_percent, "CPU占用率"],

    def get_sys_mem_info(self):
        """获取MEM信息"""
        from config import mem_warn_percent
        self.mem = psutil.phymem_usage()

        return [self.mem.percent, mem_warn_percent, "内存占用率"],

    def get_sys_disks_info(self, path="/"):
        """获取硬盘信息"""
        from config import disks_warn_percent
        self.disks = psutil.disk_usage(path)

        return [self.disks.percent, disks_warn_percent, "硬盘占用率"],

    def get_process_info(self, **args):
        process_name_list = args['process']
        connection = args['connection']
        """获取特定进程的信息"""
        for process_name in process_name_list:
            p = self.get_process_by_name(process_name)
            try:
                self.get_process_io(p[0])
                pass
            except Exception, e:
                #print e
                #print "no such process"
                pass
            finally:
                if connection:
                    #print p[0].name, "connection:"
                    est, syn = self.get_process_connection(p[0])
                    self.est = est
                    self.syn = syn

                    from config import net_warn_established, net_warn_syn
                    e = [est, net_warn_established, "已建立连接"]
                    s = [syn, net_warn_syn, "半开通连接"]
                    return e, s

    def get_process_by_name(self, process_name):
        return [process for process in psutil.process_iter()
                if process_name in process.name and process.ppid == 1]

    def get_process_connection(self, process):
        "获取进程的连接数"
        ESTABLISHED = 0
        SYN_SENT = 0
        for children in process.get_children():
            try:
                for connection in children.get_connections():
                    if connection.remote_address:
                        if connection.status == 'SYN_SENT':
                            SYN_SENT += 1
                        else:
                            ESTABLISHED += 1
            except Exception, e:
                pass
        return	ESTABLISHED, SYN_SENT

    def get_process_io(self, process):
        "获取进程的I/O"
        return process.get_io_counters()

    def get_net_io(self):
        """获取网络流量信息"""
        import netiostat
        (neti_list, neto_list, neti_avg, neto_avg) = netiostat.get_net_io()
        from config import neto_warn_avg, neti_warn_avg
        self.neti_avg = neti_avg
        self.neto_avg = neto_avg

        o = [neto_avg, neto_warn_avg, "网络流出平均速度"]
        i = [neti_avg, neti_warn_avg, "网络流入平均速度"]
        return o, i

    def __str__(self):
        self.check_sys_status()
        object_str = """

        Cpus核心数目: %d
        CPU使用率: %.2f%%

        内存总数: %sMb
        内存使用率: %.2f%%

        硬盘使用率: %.2f%%

        启动时间: %s
        系统进程数目: %d

        网络流出平均速度: %.4fk/s
        网络流入平均速度: %.4fk/s

        webserver已建立连接数:%d
        webserver半开通连接数:%d

        """ % (psutil.NUM_CPUS, self.cpu_percent,
               psutil.TOTAL_PHYMEM / 1024 / 1024, self.mem.percent,
               self.disks.percent, psutil.BOOT_TIME / 60,
               len(psutil.get_pid_list()),
               self.neto_avg, self.neti_avg, self.est, self.syn)

        return object_str

if __name__ == "__main__":
    p = PSU()
    print p
