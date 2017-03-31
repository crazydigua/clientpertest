#coding:gbk
import os, sys, time, re
import dpkt, pcap
from Lib import autogui
if __name__ == '__main__':
    hwnd = autogui.findWindow("#32770",'',True)

    if hwnd:
        print "sucess"
    else:
        print "fail"
