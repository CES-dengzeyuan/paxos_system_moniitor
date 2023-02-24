import paramiko
import time

linux = ['219.216.64.229']


def connectHost(ip, uname='guest10', passwd='123456'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=uname, password=passwd)
    return ssh


def MainCheck():
    try:
        while True:

            for a in range(len(linux)):
                ssh = connectHost(linux[a])
                # 查询主机名称
                cmd = 'hostname'
                stdin, stdout, stderr = ssh.exec_command(cmd)
                host_name = stdout.readlines()
                host_name = host_name[0]
                # 查看当前时间
                csj = 'date +%T'
                stdin, stdout, stderr = ssh.exec_command(csj)
                curr_time = stdout.readlines()
                curr_time = curr_time[0]

                # 查看cpu使用率(取三次平均值)
                cpu = "vmstat 1 3|sed  '1d'|sed  '1d'|awk '{print $15}'"
                stdin, stdout, stderr = ssh.exec_command(cpu)
                cpu = stdout.readlines()
                print(cpu)
                cpu_usage = str(round((100 - (int(cpu[0]) + int(cpu[1]) + int(cpu[2])) / 3), 2)) + '%'

                # 查看内存使用率
                mem = "cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'"
                stdin, stdout, stderr = ssh.exec_command(mem)
                mem = stdout.readlines()
                mem_total = round(int(mem[0]) / 1024)
                mem_total_free = round(int(mem[1]) / 1024) + round(int(mem[2]) / 1024) + round(int(mem[3]) / 1024)
                mem_usage = str(round(((mem_total - mem_total_free) / mem_total) * 100, 2)) + "%"
                # print(host_name, curr_time, cpu_usage, mem_usage)
                print(curr_time)
                print(cpu_usage)
                print(mem_usage)
                time.sleep(10)
    except:
        print("连接服务器 %s 异常" % (linux[a]))


if __name__ == '__main__':
    MainCheck()
