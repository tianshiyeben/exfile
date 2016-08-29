#!/usr/bin/env python  
#coding=utf-8
#import sys
#default_encoding = 'utf-8'
#if sys.getdefaultencoding() != default_encoding:
#    reload(sys)
#    sys.setdefaultencoding(default_encoding)
import xlwt
import MySQLdb
import sys,time, os, sched,platform

def export():
    nowdate = time.strftime('%Y-%m-%d', time.localtime(time.time()-60*60*24))
    sql = u"select id as 序号,title as 信息名称 from test  where RELEASED_DTIME like '" + nowdate + "%'"
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='cicro', charset='utf8')
    cursor = conn.cursor()
    count = cursor.execute(sql)
    print 'has %s record' % count
    if count > 0:
        # 重置游标位置
        cursor.scroll(0, mode='absolute')
        # 搜取所有结果
        results = cursor.fetchall()
        # 测试代码，print results
        # 获取MYSQL里的数据字段
        fields = cursor.description
        # 将字段写入到EXCEL新表的第一行
        wbk = xlwt.Workbook(encoding='utf-8')
        sheet = wbk.add_sheet('sheet1', cell_overwrite_ok=True)
        for ifs in range(0, len(fields)):
            sheet.write(0, ifs, fields[ifs][0])
        ics = 1
        jcs = 0
        for ics in range(1, len(results) + 1):
            for jcs in range(0, len(fields)):
                sheet.write(ics, jcs, results[ics - 1][jcs])
		#保存文件
        wbk.save('d:/' + nowdate + '.xlsx')

# 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
# 第二个参数以某种人为的方式衡量时间
schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    # 安排inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    export()


def timming_exe(cmd, inc=60):
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()

#fork后台运行进程
def createDaemon():
    # fork进程
    try:
        if os.fork() > 0: os._exit(0)
    except OSError, error:
        print 'fork #1 failed: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print 'Daemon PID %d' % pid
            os._exit(0)
    except OSError, error:
        print 'fork #2 failed: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)
    # 重定向标准IO
    sys.stdout.flush()
    sys.stderr.flush()
    si = file("/dev/null", 'r')
    so = file("/dev/null", 'a+')
    se = file("/dev/null", 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    # 在子进程中执行代码
    print("show time after 60 * 60 * 24 seconds:")
    timming_exe("echo %time%", 60 * 60 * 24)

#执行函数createDaemon
createDaemon()