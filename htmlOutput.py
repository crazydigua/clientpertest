#coding:gbk
import sys

def writeHtmlHead(hResFile):
    body  = '<html>\r\n'
    body += '<head>\r\n'
    body += '<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />\r\n'
    body += '<title>ID化获取请求耗时结果</title>\r\n'
    body += '</head>\r\n'
    body += '<body>\r\n'
    body += '<h1 align="center">ID化获取请求耗时结果</h1>\r\n'
    hResFile.write(body)

def writeTableHead(hResFile):
    body = '<table align="center" width="60%" cellspacing="0" style="WORD-WRAP: break-word;border-left:1px solid black;border-top:1px solid black">\r\n'
    body += '<tr align="center">\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">请求</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">最长耗时(秒)</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">平均耗时(秒)</font></strong></td>\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><strong><font size="4">详细时间</font></strong></td>\r\n'
    body += '</tr>\r\n'
    hResFile.write(body)

def writeCheckItem(hResFile, urlStr, checkItem):
    averTime, maxTime, timestr = checkItem
    body = '<tr align="center">\r\n'
    body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%urlStr
    if averTime == -1:
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000>请求失败</font></td>\r\n'
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black"><font color=#FF0000></font></td>\r\n'
    else:
        if ((float(maxTime) > 2.0) and (urlStr != '打开管家首页')) or ((float(maxTime) > 10.0) and (urlStr == '打开管家首页')):
            content = '<font color=#FF0000>%s</font>'%maxTime
        else:
            content = maxTime
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%content
        if ((float(averTime) > 2.0) and (urlStr != '打开管家首页')) or ((float(averTime) > 10.0) and (urlStr == '打开管家首页')):
                content = '<font color=#FF0000>%s</font>'%averTime
        content = averTime
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n'%content
        content = timestr
        body += '<td style="border-right:1px solid black;border-bottom:1px solid black">%s</td>\r\n' % content
    body += '<tr>\r\n'
    hResFile.write(body)

def writeTableTail(hResFile):
    body = '</table>\r\n'
    hResFile.write(body)

def writeHtmlTail(hResFile):
    body = '</body>\r\n'
    body += '</html>\r\n'
    hResFile.write(body)