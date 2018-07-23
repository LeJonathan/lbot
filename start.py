# -*- coding: utf-8 -*-
import socket
import xml.etree.ElementTree as ETree
from threading import Thread
import json, sys
from http import Http
from lbot import LBot
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
			Http(Socket2).start()
			while 1:
				s,a = Socket1.accept()
				LBot(s).start()
		except Exception,e:
			print e

if __name__ == "__main__":
	strt = Start()