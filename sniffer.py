#coding:gbk
import os, time
import json, re
from Lib import autoproc
import Logger

cLog = Logger.printLog()

g_sniffer = os.path.join(os.curdir, r'httpSniffer.py')
g_snifferLog = os.path.join(os.curdir, r'sniffer.txt')


def startSniffer(hostAdd):
    #netRefresh()
    cmd = 'python "%s" "%s"'%(g_sniffer, hostAdd)
    snifferPID = autoproc.createProcess(cmd)
    return snifferPID

def stopSniffer(snifferPID):
    print 'stop sniffer...'
    os.system(r'taskkill /F /PID %s 1> NUL 2> NUL' % str(snifferPID))

def checkSniffer(urlStr):
    global g_snifferLog
    logContent = []
    if not urlStr:
        cLog.Error('未指定需要抓取的链接地址')
        return False
    if (not g_snifferLog) or (not os.path.exists(g_snifferLog)):
        return False
    try:
        hf = open(g_snifferLog, 'r')
        logContent = hf.readlines()
    except:
        return False
    hf.close()
    if not logContent:
        return False
    find = False
    for line in logContent:
        if line.startswith('GET') and (urlStr in line):
            find = True
    if not find:
        return False
    else:
        return True

def getJsonData(urlStr, taskid = None):
    global g_snifferLog
    logContent = []
    if not urlStr:
        cLog.Error('未指定需要抓取的链接地址')
        return None
    if (not g_snifferLog) or (not os.path.exists(g_snifferLog)):
        cLog.Error('未找到抓包结果')
        return None
    try:
        hf = open(g_snifferLog, 'r')
        logContent = hf.readlines()
    except:
        cLog.Error('读取抓包内容失败')
        return None
    hf.close()
    if not logContent:
        cLog.Error('抓包内容为空')
        return None
    find = False
    for line in logContent:
        if taskid:
            taskidStr = 'taskid=%s'%str(taskid)
            if line.startswith('GET') and (urlStr in line) and (taskidStr in line):
                find = True
        else:
            if line.startswith('GET') and (urlStr in line):
                find = True
    if not find:
        cLog.Error('未抓到链接%s下的内容'%urlStr)
        return None
    jsonData = ''
    beginFind = False
    beginCatch = False
    for line in logContent:
        if len(line) == 0:
            continue
        if (not beginFind) and (not beginCatch) and re.findall('Content-Type: .*json.*', line, re.I):
            beginFind = True
            continue
        if beginFind:
            if line.startswith('{'):
                beginCatch = True
                beginFind = False
                jsonData += line.strip()
            continue
        if beginCatch:
            if len(line.strip()) == 1 and line.strip() == '0':
                beginCatch = False
            else:
                jsonData += line.strip()
            continue
    try:
        jData = json.loads(jsonData)
    except:
        cLog.Error('获取json数据失败')
        return None
    else:
        return jData

if __name__ == '__main__':
    spid = startSniffer('host safe.priv.uc.360.cn')
    time.sleep(10)
    stopSniffer(spid)
    print getJsonData('index.php?method=Privilege.getUserPrivileges')