#coding: gbk
import os, sys, time, re
import dpkt, pcap

g_outputFile = None
g_filter = ''

def writeOutput(txt):
    g_outputFile.write(txt + os.linesep)    
    g_outputFile.flush()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    g_filter = sys.argv[1]
    currentFolder = os.getcwd()    
    outPutPath = os.path.join(currentFolder,'sniffer.txt')
    g_outputFile = open(outPutPath, 'w')
    try:
        print 'Start Sniffer... %s'%g_filter
        pc= pcap.pcap()
        pc.setfilter(g_filter)
        for ts, pkt in pc:
            tem = dpkt.ethernet.Ethernet(pkt)
            txt = tem.data.data.data
            writeOutput(txt)
    except Exception, e:
        print e
        pass
    finally:
        g_outputFile.close()