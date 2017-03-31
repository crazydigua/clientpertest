#coding:gbk
import os, time
import shutil
import win32api
import json
import random
import httplib
from Lib import autoutil, autoproc, auto360
import Logger, sniffer, htmlOutput

cLog = Logger.printLog()
def getFileVersion(fileName):
    try:
        version = win32api.GetFileVersionInfo(fileName, os.sep)
        ms = version['FileVersionMS']
        ls = version['FileVersionLS']
        return '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
    except:
        return None

verFile = os.path.join(auto360.SAFE_PATH, r'Utils\360ExpClient.dll')
g_ver = getFileVersion(verFile)
g_mid = '32f079158e193a659bf85e5b4241b678'

#从uri中分离出host和location
def parseUrl(url):
    proto = url[:url.find('://')]
    index1 = url.find('://') + 3
    index2 = url.find('/', index1)
    if index2 == -1:
        return proto, url[index1:], '/'
    return proto, url[index1:index2], url[index2:]

#http请求
def doHttp(url, method, body, headers = {}, timeout = 60):
    proto, host, location = parseUrl(url)
    baseHeaders = {}
    baseHeaders['Accept']  = '*.*'
    baseHeaders['Cache-Control'] = 'no-cache'
    baseHeaders['Connection'] = 'keep-alive'
    baseHeaders['Host'] = host
    baseHeaders['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; qa_automation)'

    for k, v in headers.items():
        baseHeaders[k] = v
    conn = None
    try:
        begin = time.time()
        if proto == 'http':
            conn = httplib.HTTPConnection(host, timeout = timeout)
        else:
            conn = httplib.HTTPSConnection(host, timeout = timeout)
        conn.request(method, location, body, baseHeaders)
        res = conn.getresponse()
        end = time.time()
        baseHeaders.clear()
        for k, v in res.getheaders():
            baseHeaders[k] = v
        return res.status, baseHeaders, res.read(), end - begin
    except:
        return
    finally:
        if conn:
            autoutil.tryExcept(conn.close)

def _getRandNum():
    return str(random.randint(10000000, 99999999))

def _countGuidNum(para, key):
    para = para.replace('&', '')
    para = para + key
    return autoutil.md5(para)

##Js
def checkGetVerJS():
    global g_ver, g_mid
    body = {}
    host_url = r'http://static.360.cn/qucexp/safe/2.0/ver.js'
    ret = doHttp(host_url, 'GET', body)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = ret[2]
    t = ret[3]
    try:
        json.loads(content)
    except:
        cLog.Error('请求结果格式错误')
        return None
    else:
        cLog.Comment('请求成功')
        return (0, t)

def checkGetPercentJS():
    global g_ver, g_mid
    body = {}
    host_url = r'http://static.360.cn/qucexp/safe/2.0/percent.js'
    ret = doHttp(host_url, 'GET', body)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = ret[2]
    t = ret[3]
    try:
        json.loads(content)
    except:
        cLog.Error('请求结果格式错误')
        return None
    else:
        cLog.Comment('请求成功')
        return (0, t)

def checkGetLevelJS():
    global g_ver, g_mid
    body = {}
    host_url = r'http://static.360.cn/qucexp/safe/2.0/level.js'
    ret = doHttp(host_url, 'GET', body)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = ret[2]
    t = ret[3]
    try:
        json.loads(content)
    except:
        cLog.Error('请求结果格式错误')
        return None
    else:
        cLog.Comment('请求成功')
        return (0, t)

def checkGetMessageJS():
    global g_ver, g_mid
    body = {}
    host_url    = r'http://static.360.cn/qucexp/safe/2.0/message.js'
    ret = doHttp(host_url, 'GET', body)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = ret[2]
    t = ret[3]
    try:
        jRet = json.loads(content)
    except:
        cLog.Error('请求结果格式错误')
        return None
    else:
        md5 = jRet['md5'].decode('unicode-escape').encode('gbk')
        cLog.Comment('请求成功,message.js文件md5为："%s"'%md5)
        return (0, t)

def checkGetTaskJS():
    global g_ver, g_mid
    body = {}
    host_url    = r'http://static.360.cn/qucexp/safe/2.0/task.js'
    ret = doHttp(host_url, 'GET', body)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = ret[2]
    t = ret[3]
    try:
        jRet = json.loads(content)
    except:
        cLog.Error('请求结果格式错误')
        return None
    else:
        md5 = jRet['md5'].decode('unicode-escape').encode('gbk')
        cLog.Comment('请求成功,task.js文件md5为："%s"'%md5)
        return (0, t)

def checkGetPrivilegeJS():
    global g_ver, g_mid
    body = {}
    host_url    = r'http://static.360.cn/qucexp/safe/2.0/privilege.js'
    ret = doHttp(host_url, 'GET', body)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = ret[2]
    t = ret[3]
    try:
        jRet = json.loads(content)
    except:
        cLog.Error('请求结果格式错误')
        return None
    else:
        md5 = jRet['md5'].decode('unicode-escape').encode('gbk')
        cLog.Comment('请求成功,privilege.js文件md5为："%s"'%md5)
        return (0, t)

##Exp
def checkGetUserExp():
    global g_ver, g_mid
    qid = str(555546650)
    qc = 'u%3D360H555546650%26n%3D%26r%3D%26qid%3D555546650%26im%3D1_t00df551a583a87f4e9%26s%3D360%26src%3Dpcc_guard_safe%26t%3D1%26le%3DpTyuo2kcqKOcozpyAQOfnKMyYzAioD%3D%3D'
    tc = 's%3D0221d873d5d69a009a8eaa73381489f0%26t%3D1392107712%26a%3D1%26v%3D1.0%26lm%3D'
    body = {}
    host_url    = r'http://safe.exp.uc.360.cn/index.php'
    method = 'Exp.getUserExp'
    app    = 'safe'
    appkey = 'safe_exp_client'
    ver    = g_ver
    rand   = _getRandNum()
    mid    = g_mid
    guid   = None
    headers = {'Cookie':'Q=%s; T=%s' % (qc, tc)}
    para   = 'app=%s&appkey=%s&method=%s&mid=%s&qid=%s&rand=%s&ver=%s' % (app, appkey, method, mid, qid, rand, ver)
    guid   = _countGuidNum(para, requestConst.exp_prikey)
    if not guid:
        cLog.Error('获取请求Guid失败...')
        return None
    #cLog.Comment('获取请求Guid为：%s' % guid)

    url = host_url + '?' + para + '&' + 'guid=%s'%guid + '&' + 'qc=%s'%qc + '&' + 'tc=%s'%tc
    #cLog.Comment('请求url为：%s' % url)

    ret = doHttp(url, 'GET', body, headers)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = eval(ret[2])
    t = ret[3]
    errmsg = content['errmsg'].decode('unicode-escape').encode('gbk')
    cLog.Comment('发送请求，服务端返回结果为 ： { errno : %s , errmsg : %s } ' % (content['errno'],errmsg))
    if type(content) == dict and 'errno' in content.keys():
        return (content['errno'], t)
    return None

##Track
def checkGetUserTrack():
    global g_ver, g_mid
    trackid = '1002'
    qid = str(555546650)
    qc = 'u%3D360H555546650%26n%3D%26r%3D%26qid%3D555546650%26im%3D1_t00df551a583a87f4e9%26s%3D360%26src%3Dpcc_guard_safe%26t%3D1%26le%3DpTyuo2kcqKOcozpyAQOfnKMyYzAioD%3D%3D'
    tc = 's%3De20bb1337dc5e2582ce84736d4c7ea40%26t%3D1392110680%26a%3D1%26v%3D1.0%26lm%3D'
    body = {}
    host_url    = r'http://safe.track.uc.360.cn/index.php'
    method = 'Track.getUserTrack'
    app    = 'safe'
    appkey = 'safe_track_client'
    ver    = g_ver
    rand   = _getRandNum()
    mid    = g_mid
    guid   = None
    headers = {'Cookie':'Q=%s; T=%s' % (qc, tc)}
    para   = 'app=%s&appkey=%s&method=%s&mid=%s&qid=%s&rand=%s&trackid=%s&ver=%s' % (app, appkey, method, mid, qid, rand, trackid, ver)
    guid   = _countGuidNum(para, requestConst.trace_prikey)
    if not guid:
        cLog.Error('获取请求Guid失败...')
        return None
    #cLog.Comment('获取请求Guid为：%s' % guid)

    url = host_url + '?' + para + '&' + 'guid=%s'%guid + '&' + 'qc=%s'%qc + '&' + 'tc=%s'%tc
    #cLog.Comment('请求url为：%s' % url)

    ret = doHttp(url, 'GET', body, headers)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = eval(ret[2])
    t = ret[3]
    errmsg = content['errmsg'].decode('unicode-escape').encode('gbk')
    cLog.Comment('发送请求，服务端返回结果为 ： { errno : %s , errmsg : %s } ' % (content['errno'],errmsg))
    if type(content) == dict and 'errno' in content.keys():
        return (content['errno'], t)
    return None

##Task
def checkgetUserTasksState():
    global g_ver, g_mid
    taskids = '1002,1003,1004,1005,1006,1007,1009,1011,1012,1015,1027,1040,1069,1078,1097,1103,1106,3001,3003,3008,3009,3010,3011,3012,3013,3014,3015,3018,3021,3022,3023,3024'
    qid = str(555546650)
    qc = 'u%3D360H555546650%26n%3D%26r%3D%26qid%3D555546650%26im%3D1_t00df551a583a87f4e9%26s%3D360%26src%3Dpcc_guard_safe%26t%3D1%26le%3DpTyuo2kcqKOcozpyAQOfnKMyYzAioD%3D%3D'
    tc = 's%3D1bf3a4557b6e851ed9caf9db855618a0%26t%3D1392191200%26a%3D1%26v%3D1.0%26lm%3D'
    body = {}
    host_url = r'http://safe.task.uc.360.cn/index.php'
    method = 'Task.getUserTasksState'
    app    = 'safe'
    appkey = 'safe_task_client'
    ver    = g_ver
    rand   = _getRandNum()
    mid    = g_mid
    guid   = None
    headers = {'Cookie':'Q=%s; T=%s' % (qc, tc)}
    para   = 'app=%s&appkey=%s&method=%s&mid=%s&qid=%s&rand=%s&taskids=%s&ver=%s' % (app, appkey, method, mid, qid, rand, taskids, ver)
    guid   = _countGuidNum(para, requestConst.task_prikey)
    if not guid:
        cLog.Error('获取请求Guid失败...')
        return None
    #cLog.Comment('获取请求Guid为：%s' % guid)

    url = host_url + '?' + para + '&' + 'guid=%s'%guid + '&' + 'qc=%s'%qc + '&' + 'tc=%s'%tc
    #cLog.Comment('请求url为：%s' % url)

    ret = doHttp(url, 'GET', body, headers)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = eval(ret[2])
    t = ret[3]
    errmsg = content['errmsg'].decode('unicode-escape').encode('gbk')
    cLog.Comment('发送请求，服务端返回结果为 ： { errno : %s , errmsg : %s } ' % (content['errno'],errmsg))
    if type(content) == dict and 'errno' in content.keys():
        return (content['errno'], t)
    return None

def checkGetUserPrivileges():
    global g_ver, g_mid
    pids = '1008,1021,1039,1064,1074,1112,1113,1114,1115,1116,1117,1127,1138,1139,1140,1141,1157,1158,1159,1160,1174,1176,5001'
    qid = str(555546650)
    qc = 'u%3D360H555546650%26n%3D%26r%3D%26qid%3D555546650%26im%3D1_t00df551a583a87f4e9%26s%3D360%26src%3Dpcc_guard_safe%26t%3D1%26le%3DpTyuo2kcqKOcozpyAQOfnKMyYzAioD%3D%3D'
    tc = 's%3D1bf3a4557b6e851ed9caf9db855618a0%26t%3D1392191200%26a%3D1%26v%3D1.0%26lm%3D'
    body = {}
    host_url = r'http://safe.priv.uc.360.cn/index.php'
    method = 'Privilege.getUserPrivileges'
    app    = 'safe'
    appkey = 'safe_priv_client'
    ver    = g_ver
    rand   = _getRandNum()
    mid    = g_mid
    guid   = None
    headers = {'Cookie':'Q=%s; T=%s' % (qc, tc)}
    para   = 'app=%s&appkey=%s&method=%s&mid=%s&pids=%s&qid=%s&rand=%s&ver=%s' % (app, appkey, method, mid, pids, qid, rand, ver)
    guid   = _countGuidNum(para, requestConst.priv_prikey)
    if not guid:
        cLog.Error('获取请求Guid失败...')
        return None
    #cLog.Comment('获取请求Guid为：%s' % guid)

    url = host_url + '?' + para + '&' + 'guid=%s'%guid + '&' + 'qc=%s'%qc + '&' + 'tc=%s'%tc
    #cLog.Comment('请求url为：%s' % url)

    ret = doHttp(url, 'GET', body, headers)
    if not ret:
        cLog.Error('请求失败')
        return None
    content = eval(ret[2])
    t = ret[3]
    errmsg = content['errmsg'].decode('unicode-escape').encode('gbk')
    cLog.Comment('发送请求，服务端返回结果为 ： { errno : %s , errmsg : %s } ' % (content['errno'],errmsg))
    if type(content) == dict and 'errno' in content.keys():
        return (content['errno'], t)
    return None


def getAverageTime(tryTimes = 10):
    totalTime = 0
    maxTime = 0.0
    urlStr = '完整登陆'
    fails = 0
    timestr = ''
    for i in range(tryTimes):
        cLog.Comment('请求“%s”第%s次'%(urlStr, i+1))
        ret = checkLoginIn()
        if not ret:
            cLog.Error('请求“%s”第%s次失败'%(urlStr, i+1))
            fails += 1
            continue
        if ret[1] > maxTime:
            maxTime = ret[1]
        totalTime += ret[1]
        cLog.Pass('请求“%s”第%s次成功'%(urlStr, i+1))
        timestr = timestr + str('%0.3f'%ret[1])
        timestr = timestr + ' '
    if fails == tryTimes:
        return (-1, -1, fails)
    average = totalTime/(float(tryTimes - fails))
    print  timestr
    return ('%0.3f'%average, '%0.3f'%maxTime, timestr)

def launchSafe():
    safePath = os.path.join(auto360.SAFE_PATH, r'SoftMgr\SoftMgr.exe')
    autoproc.createProcess('%s'%safePath)

def checkLoginIn():
    auto360.closeProtect()
    autoproc.killProcessName(r'SoftMgr.exe')
    autoutil.handleTimeout(autoutil.negative, 10, autoproc.existProcessName, r'SoftMgr.exe')
    # rmdir = os.path.join(os.environ['APPDATA'], r'360Safe\safeid')
    # if os.path.exists(rmdir):
    #     shutil.rmtree(rmdir)
    #     if not autoutil.handleTimeout(autoutil.negative, 10, os.path.exists, rmdir):
    #         cLog.Error('无法删除id信息缓存文件夹')
    #         return None
    snifferID = sniffer.startSniffer('host s.360.cn')
    time.sleep(5)
    begin = time.time()
    autoutil.doInThread(launchSafe)
    if not autoutil.handleTimeout(sniffer.checkSniffer, 60, '360_softm_hot'):
        sniffer.stopSniffer(snifferID)
        return None
    end = time.time()
    sniffer.stopSniffer(snifferID)
    time.sleep(3)
    #wastetime = end -begin
    #writehtml(wastetime)
    return (0, end - begin)


def getTime(style = '%m%d%H%M'):
    return time.strftime(style, time.localtime())
def writehtml(wastetime):
    resultVerFile = os.path.join(auto360.SAFE_PATH, r'SoftMgr\SoftMgr.exe')
    version = getFileVersion(resultVerFile).split('.')[-1]
    htmlFile = os.path.abspath(r'result_%s_%s.html'%(version, getTime()))
    try:
        hHtmlFile = open(htmlFile, 'w')
    except:
        cLog.Error('创建结果文件失败')
        return False
    htmlOutput.writeHtmlHead(hHtmlFile)
    htmlOutput.writeTableHead(hHtmlFile)
    htmlOutput.writeCheckItem(hHtmlFile, '一个登录周期', wastetime);
    htmlOutput.writeTableTail(hHtmlFile)
    htmlOutput.writeHtmlTail(hHtmlFile)
    hHtmlFile.close()


def main():
    resultVerFile = os.path.join(auto360.SAFE_PATH, r'SoftMgr\SoftMgr.exe')
    version = getFileVersion(resultVerFile).split('.')[-1]
    htmlFile = os.path.abspath(r'result_%s_%s.html'%(version, getTime()))
    try:
        hHtmlFile = open(htmlFile, 'w')
    except:
        cLog.Error('创建结果文件失败')
        return False
    htmlOutput.writeHtmlHead(hHtmlFile)
    htmlOutput.writeTableHead(hHtmlFile)
    #cLog.Comment('单独校验各个请求链接')
    # #checkList = [('checkGetVerJS', 'static.360.cn/qucexp/safe/2.0/ver.js'),
    #              ('checkGetPercentJS', 'static.360.cn/qucexp/safe/2.0/percent.js'),
    #              ('checkGetLevelJS', 'static.360.cn/qucexp/safe/2.0/level.js'),
    #              ('checkGetMessageJS', 'static.360.cn/qucexp/safe/2.0/message.js'),
    #              ('checkGetTaskJS', 'static.360.cn/qucexp/safe/2.0/task.js'),
    #              ('checkGetPrivilegeJS', 'static.360.cn/qucexp/safe/2.0/privilege.js'),
    #              ('checkGetUserExp', 'safe.exp.uc.360.cn/index.php?method=Exp.getUserExp'),
    #              ('checkGetUserTrack', 'safe.track.uc.360.cn/index.php?method=Track.getUserTrack'),
    #              ('checkgetUserTasksState', 'safe.task.uc.360.cn/index.php?method=Task.getUserTasksState'),
    #              ('checkGetUserPrivileges', 'safe.priv.uc.360.cn/index.php?method=Privilege.getUserPrivileges')]
    # for checkItem, urlStr in checkList:
    #     cLog.Comment('校验请求：%s'%urlStr)
    #     htmlOutput.writeCheckItem(hHtmlFile, urlStr, getAverageTime(checkItem, urlStr))
    #cLog.Comment('校验完整登陆过程')

    htmlOutput.writeCheckItem(hHtmlFile, '打开管家首页', getAverageTime(10));
    htmlOutput.writeTableTail(hHtmlFile)
    htmlOutput.writeHtmlTail(hHtmlFile)
    hHtmlFile.close()
    auto360.closeProtect()
    autoproc.killProcessName(r'SoftMgr.exe')
    autoutil.handleTimeout(autoutil.negative, 10, autoproc.existProcessName, r'SoftMgr.exe')
    if os.path.exists(htmlFile):
        os.system(htmlFile)
    return True

if __name__ == '__main__':
    main()
