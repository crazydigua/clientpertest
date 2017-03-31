  # -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import re
import time
import jieba
response = urllib2.urlopen('http://www.duowan.com/')
html = response.read()
html=unicode(html,'utf-8')
word=re.findall(ur"[\u4e00-\u9fa5]+",html)
print word
s=""
for w in word:
    s+=w
seg_list=jieba.cut(s,cut_all=False)
fenci="/ ".join(seg_list)
print fenci
file_object = open('steam', 'w')
file_object.write(fenci)
file_object.close( )