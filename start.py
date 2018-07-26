# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ETree
import json, sys
import socket,re
import urllib
import urllib2
import glob
import ctypes
import webbrowser
import time

from threading import Thread
from random import randint
from time import sleep

from lbot import LBot

ctypes.windll.kernel32.SetConsoleTitleA("Free - xat Client")

reload(sys)
sys.setdefaultencoding('utf-8')

class Start:
	def __init__(self):
		try:
			Socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
			Socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
			Socket1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			Socket2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			Socket1.bind(('',12345))
			Socket1.listen(-1)
			Socket2.bind(('',10101))
			Socket2.listen(-1)
			print "Socket is listening.."
			while 1:
				Http(Socket2).start()
				s,a = Socket1.accept()
				print "Got connection from", a
				LBot(s).start()
		except Exception,e:
			print e
			
class Http(Thread):
	http = None
	def __init__(self,http):
		Thread.__init__(self)
		self.http = http
	def run(self):
		while 1:
			s,a = self.http.accept()
			while 1:
				httpData = s.recv(4096)
				if httpData != "":
					pass #print httpData
				if '.swf' in httpData:
					swf = urllib2.urlopen('https://www.xatech.com/web_gear/flash/chat643.swf').read()
					x200ok = 'HTTP/1.1 200 OK\r\n'
					x200ok += 'Date: ' + time.strftime("%a, %d %b %Y %H:%M:%S GMT") + '\r\n'
					x200ok += 'Content-Type: application/x-shockwave-flash\r\n'
					x200ok += 'Content-Length: '+str(len(swf))+'\r\n'
					x200ok += 'Connection: keep-alive\r\n'
					x200ok += 'Cache-Control: max-age=180\r\n'
					x200ok += 'Server: cloudflare-nginx\r\n\r\n'
					s.send(x200ok + swf)
					print '> Connection established (SWF)'
				if 'crossdomain' in httpData:
					cr = '<cross-domain-policy><allow-access-from domain="*" to-ports="12345" /></cross-domain-policy>'
					x200ok = 'HTTP/1.1 200 OK\r\n'
					x200ok += 'Date: ' + time.strftime("%a, %d %b %Y %H:%M:%S GMT") + '\r\n'
					x200ok += 'Content-Type:text/html\r\n'
					x200ok += 'Content-Length: '+str(len(cr))+'\r\n'
					x200ok += 'Connection: keep-alive\r\n'
					x200ok += 'Cache-Control: max-age=180\r\n'
					x200ok += 'Server: cloudflare-nginx\r\n\r\n'
					s.send(x200ok + cr)
					print '> Connection established (XML)'
				if 'ip2' in httpData:
					current_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT")
					ip2 = urllib2.urlopen('https://xat.com/web_gear/chat/ip2.php').read()
					ipJson = json.loads(ip2)
					ipJson['E1'] = ipJson['E0'] = [1,['127.0.0.1:12345:1']]
					ipJson = json.dumps(ipJson, sort_keys=True)
					x200ok = 'HTTP/1.1 200 OK\r\n'
					x200ok += 'Date: ' + current_date + '\r\n'
					x200ok += 'Content-Type: text/html\r\n'
					x200ok += 'Content-Length: '+str(len(ipJson))+'\r\n'
					x200ok += 'Connection: keep-alive\r\n'
					x200ok += 'Cache-Control: max-age=1800\r\n'
					x200ok += 'Server: cloudflare-nginx\r\n\r\n'
					#ipJson['F1'] = [0,["127.0.0.1:12345:1"]]
					s.send(str.lstrip(x200ok))
					s.send(ipJson)
					print '> Connection established (IP2)'

if __name__ == "__main__":
	strt = Start()
