# -*- coding: utf-8 -*-
import socket,re
import xml.etree.ElementTree as ETree
from threading import Thread
from random import randint
from time import sleep
import urllib
import urllib2
import glob
import sys
import ctypes
import webbrowser

class LBot(Thread):
	sockXat = None
	me = {'id': None, 'regname': None, 'name': None, 'homepage': None, 'avatar': None, 'married': '1'}
	copiedUser = {}
	allowedUsers = ['6006006', '885544817', '1337873972']
	chat = {'id': None, 'name': None}
	users = []
	
	"""BOT PGO SETTINGS - Feel free to edit these!
	The AutoLure function determines if you renew lures after they run out.
	PGL is a list of Pokemon the bot should chase @ xat.com/PGO
	Chasing refers to what the bot should chase, values include: all, shinies, megas, list, none. 
	Chasing all *can* cause the bot to be signed off after 5 attempts 
	You'll be forced to reload the page or do xat's anti-bot verification."""
	pgo = {'bottingPgo': True, 'autoLure': True, 'chasingPgo': True, 'pgl': ['Infernape', 'Rayquaza'], 'chasing': 'all'}
	pgo['pgl'] = [x.lower() for x in pgo['pgl']]
	pgoGo = None
			
	def writeData(self,data,Socket):
		if '\0' in data:
			Socket.send(data)
		else:
			Socket.send(data+'\0')
			
	def getID(self, regname):
		if (regname.isdigit()):
			return regname
		else:
			for u in self.users:
				if u['reg'].lower() == regname.lower():
					return u['id']
					
	def getReg(self, id):
		if (id.isdigit() == False):
			return id
		else:
			for u in self.users:
				if u['id'] == id:
					return u['reg']
					
	def getFName(self, uID):
		for user in self.users:
			if uID == user['id']:
				try:
					if user['name'][0] == '$':
						uName = user['name'][1:].encode('utf-8')
						return uName
					else:
						uName = user['name'].encode('utf-8')
						return uName
				except:
					uName = user['name'].encode('utf-8')
					return uName
					
	def getName(self, uID):
		for user in self.users:
			if uID == user['id']:
				try:
					if user['name'][0] == '$':
						uName = user['name'][1:].encode('utf-8').split('##',1)[0]
						return uName
					else:
						uName = user['name'].encode('utf-8').split('##',1)[0]
						return uName
				except:
					uName = user['name'].encode('utf-8').split('##',1)[0]
					return uName
					
	def getAvi(self, uID):
		for user in self.users:
			if uID == user['id']:
				return user['avatar']
				
	def getHP(self, uID):
		for user in self.users:
			if uID == user['id']:
				return user['page']
				
	def getRelationship(self, uID):
		for user in self.users:
			if uID == user['id']:
				return user['married']
				
	def getChatID(self, cName):
		url = "https://api.mundosmilies.com/chatinfo.php?chat=" + cName
		opener = urllib2.build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		f = opener.open(url).read()
		json_data = json.loads(f)
		if json_data['status'] != 'OK':
			return False
		return json_data['chatid']

	def getChatName(self, cID):
		url = "https://api.mundosmilies.com/chatinfo.php?chat=xat" + cID
		opener = urllib2.build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		f = opener.open(url).read()
		json_data = json.loads(f)
		if json_data['status'] != 'OK':
			return False
		return json_data['name']
		
	def sendClient(self, msg, user="help", type="main", target="none"):
		if user == "help":
			user = "0"
		else:
			user = self.me['id']
			
		if type == "main":
			self.Socket.send('<m t="'+msg+'" u="'+user+'" />\0')
		elif type == "pc":
			self.Socket.send('<p u="'+target+'" t="'+msg+'" s="2" d="'+user+'" />\0')
		elif type == "pm":
			self.Socket.send('<p u="'+target+'" t="'+msg+'" d="'+user+'" />\0')
			
	def sendXat(self, msg, type="main", target="none"):
		user = self.me['id']
			
		if type == "main":
			self.Socket.send('<m t="([C]) '+msg+'" u="'+user+'" />\0')
			self.sockXat.send('<m t="'+msg+'" u="'+user+'" />\0')
		elif type == "pc":
			self.Socket.send('<p u="'+target+'" t="([C]) '+msg+'" s="2" d="'+user+'" />\0')
			self.sockXat.send('<p u="'+target+'" t="'+msg+'" s="2" d="'+user+'" />\0')
		elif type == "pm":
			self.Socket.send('<p u="'+target+'" t="([C]) '+msg+'" d="'+user+'" />\0')
			self.sockXat.send('<p u="'+target+'" t="'+msg+'" d="'+user+'" />\0')
			
	def isOnline(self, id):
		found = False
		for user in self.users:
			if id == user['id']:
				found = True
		return found
		
	def isStaff(self, id):
		found = False
		for u in self.staff:
			if id == u['id']:
				found = True
		return found
		
	def isRegged(self, id):
		found = True
		for user in self.users:
			if id == user['reg']:
				found = False
		return found
		
	def sendcmd(self, txt):
		"""This function manages your xat client's commands.
		The cc variable is your command
		The cmdArgs variable is your arguments
		Example: @google how to program in python
		cc: google
		cmdArgs[1]: how to program in python
		When searching for all arguments, use cmdArgs[1]
		When searching for a specific argument use cmdArgs[1].split(' ')[index]
		"""
		cc = txt[0]
		cmdArgs = txt
		
		if cc == "google":
			"""Untested code, translated from my discord bot, may work, may not.
			If you want to use it you need to get your Google API Key & App ID
			Your daily calls will be limited
			https://developers.google.com/custom-search/json-api/v1/using_rest
			The link above should explain everything you need to know."""
			try:
				search = cmdArgs[1]
				opener = urllib2.build_opener()
				opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
				f = opener.open("https://www.googleapis.com/customsearch/v1?key=API_KEY&cx=CX_ID&q=" + search.replace(' ', '+')).read()
				json_data = json.loads(f)
				search_results = json_data['items']
				formatted = [[s['title']] + " - " + (s['link']) for s in search_results[:3]]
				for result in formatted:
					self.sendClient(result)
					sleep(0.5)
			except:
				self.sendClient("Please include a search query")
		
		elif cc == "yt" or cc == "youtube":
			try:
				ytSearch = cmdArgs[1]
				ytSearch = ytSearch.replace(' ', '+')
				youtubeData = urllib2.urlopen('http://www.youtube.com/results?q='+ ytSearch).read()
				ytSearch = re.findall(r'\/watch\?v=\w+',youtubeData)
				ytArray = []
				counter = 0
				for vid in ytSearch:
					if vid in ytArray:
						pass
					else:
						ytArray.append(vid)
				for vid in ytArray[1:4]:
				   url = "https://www.youtube.com/" + vid
				   opener = urllib2.build_opener()
				   opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
				   f = opener.open(url)
				   title = str(f.read()).split('<title>')[1].split('</title>')[0]
				   self.sendClient(title.split('- YouTube ')[0] + ' : https://www.youtube.com/'+vid)
				   sleep(0.5)
			except:
				self.sendClient("Please include a video title to search.")
				
			"""IMPROVED YOUTUBE COMMAND
			Grabbing videos this way is much quicker and more accurate 
			However you need a Google API Key & your daily calls are limited
			https://developers.google.com/youtube/v3/docs/search/list
			The link above should explain everything you need to know
			
			f = opener.open('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q='+ ytSearch + '&key=API_KEY').read()
			json_data = json.loads(f)
			for x in range(0, 3):
				vLink = json_data['items'][x]['snippet']['title'] + " - https://youtube.com/watch?v=" + json_data['items'][x]['id']['videoId']
				self.sendClient(vLink, 'help')"""
				
		elif cc == "broadcast":
			"""Can be improved should you decide to use
			the previously provided code for the youtube command
			Otherwise this works fine."""
			ytSearch = cmdArgs[1]
			ytSearch = ytSearch.replace(' ','+')
			youtubeData = urllib2.urlopen('http://www.youtube.com/results?q=%s' % ytSearch).read()
			ytSearch = re.findall(r'\/watch\?v=\w+',youtubeData)
			ytArray = []
			for vid in ytSearch:
				if vid in ytArray:
					pass
				else:
					ytArray.append(vid)
			for vid in ytArray[0:1]:
				broadcast = vid.split('/watch?v=')[1]
				self.sockXat.send('<x i="10001" u="'+self.me['id']+'" t="b'+broadcast+'" />\0')
				self.Socket.send('<x i="10001" u="'+self.me['id']+'" t="b'+broadcast+'" />\0')
				
		elif cc == 'commands':
			if user != 0:
				self.sendXat("http://client.lejonathan.com/free", "pc", user)
			else:
				webbrowser.open("http://client.lejonathan.com/free")
				
		elif cc == "slo":
			self.sendClient("PGO Slots command sent")
			for x in range(0,3):
				self.sendXat("!pgo slots")
				sleep(1)
				
		elif cc == "lureup":
			self.sendClient("- Lure bought & used -")
			self.sendXat("!pgo buy lure")
			self.sendXat("!pgo use lure")
			
		elif cc == "users":
			all = []
			unreg = 0
			reg = 0
			for u in self.users:
				all.append(u['reg'])
				if self.isRegged(u['id']) == False:
					unreg += 1
				else:
					reg += 1
			print "- Online users: " + ', '.join(all) + " -"
			total = len(self.users)
			if user != 0:
				self.sendXat('Users online: ' + str(total) + ' | ' + str(unreg) + " Toon(s) ; " + str(reg) + " Registered.")
			else:
				self.sendClient('Users online: ' + str(total) + ' | ' + str(unreg) + " Toon(s) ; " + str(reg) + " Registered.")
			
		elif cc == "allow":
			try:
				target = cmdArgs[1]
				if self.getID(target) not in self.allowedUsers:
					self.allowedUsers.append(self.getID(target))
					self.sendClient("User: "+target+" added to allow list.")
				else:
					self.sendClient("User: "+target+" is already in allow list.")
			except:
				self.sendClient("Usage: @allow USER_ID")
				
		elif cc == "disallow":
			try:
				target = cmdArgs[1]
				if self.getID(target) in self.allowedUsers:
					self.allowedUsers.remove(self.getID(target))
					self.sendClient("User: "+target+" removed from allow list.")
				else:
					self.sendClient("User: "+target+" not found in allow list.")
			except:
				self.sendClient("Usage: @disallow USER_ID")
				
		elif cc == "pgo":
			if not self.pgo['bottingPgo']:
				self.sendClient("Botting PGO, turned [ON].")
				self.pgo['bottingPgo'] = True
			else:
				self.sendClient("Botting PGO, turned [OFF].")
				self.pgo['bottingPgo'] = False
				
		elif cc == "pgolure":
			if not self.pgo['autoLure']:
				self.sendClient("Luring PGO, turned [ON].")
				self.pgo['autoLure'] = True
			else:
				self.sendClient("Luring PGO, turned [OFF].")
				self.pgo['autoLure'] = False
				
	def chat(self):
		"""CLIENT MESSAGES
		Here lies all of the data you send to xat.
		The client can intercept the data and modify it accordingly if needed.
		Since this is a developer-friendly version of the client
		you will be receiving raw data packets to your console window.
		If you instead want formatted & readable outputs, find a way to implement this code piece:
		print("["+self.chat['name']+"][" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "][" + self.getReg(self.me['id']) + "]: " + text.encode('utf-8')) """
		while 1:
			try:
				data = self.Socket.recv(1024)
			except:
				self.sockXat.close()
			if len(data) > 0:
				if data.startswith('<f'):
					self.sockXat.send(data)
					print data
				else:
					try:
						print data
						data = data.strip(chr(0))
						xml = ETree.fromstring(data)
						
						"""Quick Packet run-down so you know what you should be looking for:
						'm': Regular xat message | 'p': PC/PM | 'z': Tickle/Click
						The tags inside of those packets should be self explanatory."""
						if xml.tag == 'm':
							text = xml.attrib['t']
							if text[0:1] == '@':
								self.sendcmd(text[1:].split(' ', 1))
							else:
								self.sockXat.send(data+"\0")
						else:
							self.sockXat.send(data+"\0")
					except Exception,e:
							print e
	Socket = None
	
	def __init__(self,Socket):
		sockXat = None
		me = {'id': None, 'regname': None, 'name': None, 'homepage': None, 'avatar': None, 'married': '1'}
		copiedUser = {}
		allowedUsers = ['6006006', '885544817']
		chat = {'id': None, 'name': None}
		users = []
		pgo = {'bottingPgo': True, 'autoLure': True, 'chasingPgo': True, 'pgl': ['Infernape', 'Rayquaza'], 'chasing': 'all'}
		Thread.__init__(self)
		self.Socket = Socket
			
	def run(self):
		while 1:
			data = self.Socket.recv(1024)
			if len(data) > 0:
				print data
				if '<policy-file-request/>' in data:
					self.Socket.send('<cross-domain-policy><allow-access-from domain="*" to-ports="12345" /></cross-domain-policy>\0')
				if '<y' in data:
					self.chat['id'] = ETree.fromstring(data.strip(chr(0))).attrib['r']
					self.chat['name'] = self.getChatName(self.chat['id'])
					sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
					sock.connect(('fwdelb00-1964376362.us-east-1.elb.amazonaws.com',10001))
					sock.send(data)
					self.Socket.send(sock.recv(1024))
					data = self.Socket.recv(1024)
					sock.send(data)
					try:
						self.me['id'] = ETree.fromstring(data.strip(chr(0))).attrib['u']
						self.me['regname'] = ETree.fromstring(data.strip(chr(0))).attrib['N']
						self.me['name'] = ETree.fromstring(data.strip(chr(0))).attrib['n'].encode('utf-8')
						self.me['homepage'] = ETree.fromstring(data.strip(chr(0))).attrib['h'].encode('utf-8')
						self.me['avatar'] = ETree.fromstring(data.strip(chr(0))).attrib['a']
						if 'd2' in ETree.fromstring(data.strip(chr(0))).attrib:
							self.me['married'] = ETree.fromstring(data.strip(chr(0))).attrib['d2']
							
						exists = False
						for u in self.users:
							if u['id'] == id:
								exists = True
						if not exists:
							self.users.append({'id': self.me['id'] , 'reg': self.me['regname'], 'name': self.me['name'], 'page': self.me['homepage'], 'avatar': self.me['avatar'], 'married': self.me['married'], 'isDunced': False, 'powers': []})
					except Exception, e:
						print e
						
					self.Socket.send(sock.recv(1024))
					dataX = ''
					while 1:
						data = sock.recv(1024)
						dataX += data
						if len(data) > 0:
							if '<done />' in dataX or '<done  />' in dataX:
								print(dataX)
								self.Socket.send(dataX)
								print '.:{[Client Loaded on ' + self.chat['name'] + " (" + self.chat['id'] + ")]}:."
								break
					while 1:
						"""After the initial load packets have been sent, the client filters through it
						In order to find any information that can be of use.
						Packet logic from above applies > 'm': Regular xat message (If chat saves past messages) | 'u': Online xat user"""
						packets = dataX.split('\0')
						for packet in packets:
							try:
								xml = ETree.fromstring(packet)
								if xml.tag == 'u':
									regname = "Unregistered"
									married = "1"
									id = xml.attrib['u'].split('_')[0]
									uName = xml.attrib['n'].encode('utf-8')
									uPage = xml.attrib['h'].encode('utf-8')
									uAvi = xml.attrib['a']
									powers = []
									
									if 'N' in xml.attrib:
										regname = xml.attrib['N']
										
										if 'd2' in xml.attrib:
											married = xml.attrib['d2']
											
										for e in range(0,21):
											p = "p"+str(e)
											if p in xml.attrib:
												powers.append(xml.attrib[p])
											else:
												pass
									
									self.users.append({'id': id, 'reg': regname, 'name': uName, 'page': uPage, 'avatar': uAvi, 'married': married, 'isDunced': False, 'powers': powers})
							except Exception,e: print e
						break
						
					self.sendClient("- Client Enabled")
					self.sockXat = sock
					
					"""PGO CHASING FUNCTION
					It checks if there's already a chat in memory, 
					If there is, it returns your account to xat.com/PGO to await a next catch"""
					if self.pgoGo != "" and self.chatName.lower() == self.pgoGo.lower():
						self.sockXat.send('<p u="23232323" t="!pgo catch '+str(randint(0,100))+'" s="2" d="'+self.me['id']+'" />\0')
						self.sockXat.send('<m t="/go PGO" u="'+self.me['id']+'" />\0')
						
					thredad_chat = Thread(target=self.chat,args=[])
					thredad_chat.start()
					while 1:
						"""Data sent from xat to your client is processed here.
						Packet logic from above applies > 
						'm': Regular xat message | 'p': PC/PM | 'u': Online xat user | 'l': user disconnect | 'z': Click/Tickle"""
						data = sock.recv(1024)
						if len(data) > 0:
							print data
							self.Socket.send(data)
							try:
								data = data.strip(chr(0))
								xml = ETree.fromstring(data)
								if xml.tag == 'l':
									u = xml.attrib['u'].split('_')[0]
									for user in self.users:
										if u == user['id']:
											self.users.remove(user)
								if xml.tag == 'u':
									try:
										regname = "Unregistered"
										married = "1"
										id = xml.attrib['u'].split('_')[0]
										uName = xml.attrib['n'].encode('utf-8')
										uPage = xml.attrib['h'].encode('utf-8')
										uAvi = xml.attrib['a']
										powers = []
										
										if 'N' in xml.attrib:
											regname = xml.attrib['N']
											
											if 'd2' in xml.attrib:
												married = xml.attrib['d2']
												
											for e in range(0,21):
												p = "p"+str(e)
												if p in xml.attrib:
													powers.append(xml.attrib[p])
												else:
													pass
										
										self.users.append({'id': id, 'reg': regname, 'name': uName, 'page': uPage, 'avatar': uAvi, 'married': married, 'isDunced': False, 'powers': powers})
									except Exception,e:print e
								if xml.tag == 'm':
									user = xml.attrib['u'].split('_')[0]
									text = xml.attrib['t']
									cText = xml.attrib['t'].lower()
									cmd = text[1:].split(' ', 1)
									
									"""PGO BOTTING
									Below is how your client will respond to the FEXBot's Pokemon Spawning"""
									if user == '23232323':
										if text.startswith('[LURE] A wild ') or text.startswith('A wild '):
											if self.pgo['bottingPgo']:
												sleep(randint(0,10))
												self.sendXat("!pgo catch", pc, user)
												
												if self.pgo['autoLure'] and not text.startswith('A wild '):
													pTimer = randint(60, 120)
													sleep(pTimer)
													self.sendXat("!pgo buy lure")
													self.sendXat("!pgo use lure")
										
										"""PGO CHASING
										Basic logic to follow when awaiting Pokémon to fetch"""
										if self.pgo['chasingPgo']:
											chasing = self.pgo['chasing']
											def go(c):
												self.pgoGo = c
												self.sendXat("/go " + c)
												
											if cText.find("#ping") != -1 or cText.find("#sword") != -1 or cText.find("#lasersword") != -1:
												chat = text.split('://xat.com/')[1].split(' -')[0]
												spawned = text.split('- ')[1].split(' |')[0]
												if chasing.lower() in ["selected", "list"]:
													if spawned.lower() in self.pgo['pgl'] or spawned.startswith("(dmd)"):
														print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
														go(chat)
												elif chasing.lower() in ["shinies", "shiny"]:
													if spawned.startswith("(dmd)"):
														print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
														go(chat)
												elif chasing.lower() in ["megas", "mega"]:
													if spawned.startswith("Mega") or spawned.startswith("(dmd)"):
														print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
														go(chat)
												elif chasing.lower() == "all":
													print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
													go(chat)
													
									else:
										if user in self.allowedUsers:
											if text[0:1] in ['@', '~']:
												try:
													"""Here are custom commands you're okay with letting people call, using your client"""
													if cmd[0] == 'say':
														bypass = ['6006006'] # List of users who can bypass the ! ignore
														if cmdArgs[1].startswith('!'):
															if user != '6006006':
																return
														self.sendXat(cmdArgs[1])
														
													if cmd[0] == 'broadcast':
														ytSearch = cmdArgs[1]
														ytSearch = ytSearch.replace(' ','+')
														youtubeData = urllib2.urlopen('http://www.youtube.com/results?q=%s' % ytSearch).read()
														ytSearch = re.findall(r'\/watch\?v=\w+',youtubeData)
														ytArray = []
														for vid in ytSearch:
															if vid in ytArray:
																	pass
															else:
																	ytArray.append(vid)
														for vid in ytArray[0:1]:
															broadcast = vid.split('/watch?v=')[1]
															self.sockXat.send('<x i="10001" u="'+self.me['id']+'" t="b'+broadcast+'" />\0')
															self.Socket.send('<x i="10001" u="'+self.me['id']+'" t="b'+broadcast+'" />\0')
															print broadcast
															
												except Exception,e1: print e1
							except Exception,e: print e
