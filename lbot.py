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

ctypes.windll.kernel32.SetConsoleTitleA("Free - xat Client")

reload(sys)
sys.setdefaultencoding('utf-8')

class LBot(Thread):
        userID = None
        chatName = ""
        chatID = ""
        bottingPgo = True
        autoLure = False
        chasingPgo = True
        pgl = ['Infernape', 'Rayquaza']
        chasing = "all"
        unregUsers = []
        regUsers = {}
        userPage = {}
        userName = {}
        userAva = {}
        copiedUser = {}
        sockXat = None
        allowedUsers = ['6006006', '885544817']
                
        def writeData(self,data,Socket):
                if '\0' in data:
                        Socket.send(data)
                else:
                        Socket.send(data+'\0')
        def getID(self, regname):
                if (regname.isdigit()):
                        return regname
                else:
                        for id, reg in self.regUsers.iteritems():
                                if reg.lower() == regname.lower():
                                        return id
        def getReg(self, id):
                if (id.isdigit):
                        for ids, reg in self.regUsers.iteritems():
                                if id == ids:
                                        return reg
                else:
                        return id
        def getChatName(self, cID):
            link = "http://xat.com/xat" + cID
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36')]
            f = opener.open(link)
            fID = str(f.read()).split('&GroupName=')[1].split('" title=')[0]
            return fID
        def getChat(self, cID):
            return self.getChatName(cID)
        def sendcmd(self, txt):
                cc = txt[0]
                cmdArgs = txt
                if cc == "yt" or cc == "youtube":
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
                           self.Socket.send('<m t=" ' + title.split('- YouTube ')[0] + ' : https://www.youtube.com/'+vid+'" u="0" />\0')
                           sleep(1)
                    except:
                        self.Socket.send('<m t="Please include a video title to search." u="0" />\0')
                elif cc == "broadcast":
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
                        self.sockXat.send('<x i="10001" u="'+self.userID+'" t="b'+broadcast+'" />\0')
                        self.Socket.send('<x i="10001" u="'+self.userID+'" t="b'+broadcast+'" />\0')
                        print broadcast
                elif cc == 'commands':
                    input = cmdArgs[1]
                    if user != 0:
                        self.Socket.send('<p u="'+user+'" t="https://lejon.000webhostapp.com/free.html" s="2" d="'+self.userID+'" />\0')
                        self.sockXat.send('<p u="'+user+'" t="https://lejon.000webhostapp.com/free.html" s="2" d="'+self.userID+'" />\0')
                    else:
                        webbrowser.open('https://lejon.000webhostapp.com/free.html')
                elif cc == "slo":
                    self.Socket.send('<m t="PGO Slots being run." u="0" />\0')
                    self.sockXat.send('<m t="!pgo slots" u="'+self.userID+'" />\0')
                    sleep(1)
                    self.sockXat.send('<m t="!pgo slots" u="'+self.userID+'" />\0')
                    sleep(1)
                    self.sockXat.send('<m t="!pgo slots" u="'+self.userID+'" />\0')
                elif cc == "lureup":
                    self.Socket.send('<m t="- Lure bought & used -" u="23232323" />\0')
                    self.sockXat.send('<m t="!pgo buy lure" u="'+self.userID+'" />\0')
                    self.sockXat.send('<m t="!pgo use lure" u="'+self.userID+'" />\0')
                elif cc == "users":
                    total = len(self.regUsers) + len(self.unregUsers) + 1
                    self.Socket.send('<m t="Users online: ' + str(total) + '." u="0" />\0')
                    #self.Socket.send('<m t="Registered users: %d, Unregistered users: %d" u="0" />\0'%(len(self.regUsers),len(self.unregUsers)))
                elif cc == "allow":
                    try:
                        if self.getID(cmdArgs[1]) not in self.allowedUsers:
                            self.allowedUsers.append(self.getID(cmdArgs[1]))
                            self.Socket.send('<m t="User: '+cmdArgs[1]+' added to allow list." u="0" />\0')
                        else:
                            self.Socket.send('<m t="User: '+cmdArgs[1]+' is already in allow list." u="0" />\0')
                    except:
                        self.Socket.send('<m t="Usage: @allow USERID" u="0" />\0')
                elif cc == "disallow":
                    try:
                        if self.getID(cmdArgs[1]) in self.allowedUsers:
                            self.allowedUsers.remove(self.getID(cmdArgs[1]))
                            self.Socket.send('<m t="User: '+cmdArgs[1]+' removed from allow list." u="0" />\0')
                        else:
                            self.Socket.send('<m t="User: '+cmdArgs[1]+' not found in allow list." u="0" />\0')
                    except:
                        self.Socket.send('<m t="Usage: @disallow USERID" u="0" />\0')
                elif cc == "pgo":
                    if self.bottingPgo == False:
                        self.Socket.send('<m t="Botting PGO, turned [ON]." u="0" />\0')
                        self.bottingPgo = True
                    else:
                        self.Socket.send('<m t="Botting PGO, turned [OFF]." u="0" />\0')
                        self.bottingPgo = False
                elif cc == "pgolure":
                    if self.autoLure == False:
                        self.Socket.send('<m t="Luring PGO, turned [ON]." u="0" />\0')
                        self.autoLure = True
                    else:
                        self.Socket.send('<m t="Luring PGO, turned [OFF]." u="0" />\0')
                        self.autoLure = False
        def chat(self):
                while 1:
                        data = self.Socket.recv(1024)
                        if len(data) > 0:
                                if data.startswith('<f'):
                                        self.sockXat.send(data)
                                        print data
                                else:
                                        try:
                                                print data
                                                data = data.strip(chr(0))
                                                xml = ETree.fromstring(data)
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
                self.bottingPgo = True
                self.userID = None
                self.userPage = {}
                self.userName = {}
                self.userAva = {}
                self.regUsers = {}
                self.unregUsers = []
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
                                        self.chatID = ETree.fromstring(data.strip(chr(0))).attrib['r']
                                        self.chatName = self.getChatName(self.chatID)
                                        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
                                        sock.connect(('fwdelb00-1964376362.us-east-1.elb.amazonaws.com',10001))
                                        sock.send(data)
                                        self.Socket.send(sock.recv(1024))
                                        data = self.Socket.recv(1024)
                                        sock.send(data)
                                        try:
                                                self.userID = ETree.fromstring(data.strip(chr(0))).attrib['u']
                                                print "Your ID is: " + str(self.userID)
                                        except:pass
                                        self.Socket.send(sock.recv(1024))
                                        dataX = ''
                                        while 1:
                                                data = sock.recv(1024)
                                                dataX += data
                                                if len(data) > 0:
                                                        print data
                                                        self.Socket.send(data)
                                                        if '<done  />' in data:
                                                                print 'Done!'
                                                                break
                                        while 1:
                                                packets = dataX.split('\0')
                                                for packet in packets:
                                                        try:
                                                                xml = ETree.fromstring(packet)
                                                                if xml.tag == 'u':
                                                                        if 'N' in xml.attrib:
                                                                                self.regUsers[xml.attrib['u']] = xml.attrib['N']
                                                                        else:
                                                                                self.unregUsers.append(xml.attrib['u'])
                                                                        self.userName[xml.attrib['u']] = xml.attrib['n']
                                                                        self.userAva[xml.attrib['u']] = xml.attrib['a']
                                                                        self.userPage[xml.attrib['u']] = xml.attrib['h']
                                                        except Exception,e: print e
                                                break
                                        self.Socket.send('<m t="(Ɫ) Client running on port 10101 and 12345. (Base by Lucas)" u="0" />\0')
                                        self.sockXat = sock
                                        with open('mods/go.txt', 'r') as f:
                                            go = f.readline()
                                            
                                            if go != "" and self.chatName.lower() == go.lower():
                                                newFile = open("mods/go.txt","w")
                                                newFile.write("")
                                                newFile.close()
                                                self.sockXat.send('<p u="23232323" t="!pgo catch '+str(randint(0,100))+'" s="2" d="'+self.userID+'" />\0')
                                                self.sockXat.send('<m t="/go PGO" u="'+self.userID+'" />\0')
                                            f.close()
                                        thredad_chat = Thread(target=self.chat,args=[])
                                        thredad_chat.start()
                                        while 1:
                                                data = sock.recv(1024)
                                                if len(data) > 0:
                                                        print data
                                                        self.Socket.send(data)
                                                        try:
                                                                data = data.strip(chr(0))
                                                                xml = ETree.fromstring(data)
                                                                if xml.tag == 'l':
                                                                        u = xml.attrib['u']
                                                                        if u in self.regUsers:
                                                                                del self.regUsers[u]
                                                                        else:
                                                                                self.unregUsers.remove(u)
                                                                if xml.tag == 'u':
                                                                        try:
                                                                                if 'N' in xml.attrib:
                                                                                        user = xml.attrib['u']
                                                                                        self.regUsers[xml.attrib['u']] = xml.attrib['N']
                                                                                else:
                                                                                        self.unregUsers.append(xml.attrib['u'])
                                                                        except Exception,e:print e
                                                                if xml.tag == 'm':
                                                                        user = xml.attrib['u'].split('_')[0]
                                                                        text = xml.attrib['t']
                                                                        cText = xml.attrib['t'].lower()
                                                                        cmd = text[1:].split(' ', 1)
                                                                        if user == '23232323':
                                                                                if text.startswith('[LURE] A wild '):
                                                                                        if self.bottingPgo == True:
                                                                                                sleep(5)
                                                                                                self.Socket.send('<p u="'+user+'" t="!pgo catch" s="2" d="0" />\0')
                                                                                                self.sockXat.send('<p u="'+user+'" t="!pgo catch" s="2" d="'+self.userID+'" />\0')
                                                                                elif text.startswith('A wild '):
                                                                                        if self.bottingPgo == True:
                                                                                                pTimer = randint(60, 120)
                                                                                                sleep(5)
                                                                                                self.Socket.send('<p u="'+user+'" t="!pgo catch" s="2" d="0" />\0')
                                                                                                self.sockXat.send('<p u="'+user+'" t="!pgo catch" s="2" d="'+self.userID+'" />\0')
                                                                                        if self.autoLure == True:
                                                                                                sleep(pTimer)
                                                                                                self.sockXat.send('<m t="!pgo buy lure" u="'+self.userID+'" />\0')
                                                                                                self.sockXat.send('<m t="!pgo use lure" u="'+self.userID+'" />\0')
                                                                                elif self.chasingPgo == True:
                                                                                    def go(c):
                                                                                        newFile = open("mods/go.txt","w")
                                                                                        newFile.write(c)
                                                                                        newFile.close()
                                                                                        self.sockXat.send('<m t="/go '+c+'" u="'+self.userID+'" />\0')
                                                                                    if cText.find("#ping") != -1 or cText.find("#sword") != -1 or cText.find("#lasersword") != -1:
                                                                                        chat = text.split('://xat.com/')[1].split(' -')[0]
                                                                                        spawned = text.split('- ')[1].split(' |')[0]
                                                                                        if self.chasing.lower() == "selected" or self.chasing.lower() == "list":
                                                                                            for l in self.pgl:
                                                                                                if spawned.lower() == l.text.lower() or spawned.startswith("(dmd)"):
                                                                                                    print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
                                                                                                    go(chat)
                                                                                        elif self.chasing.lower() == "shinies":
                                                                                            if spawned.startswith("(dmd)"):
                                                                                                print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
                                                                                                go(chat)
                                                                                        elif self.chasing.lower() == "megas":
                                                                                            if spawned.startswith("Mega") or spawned.startswith("(dmd)"):
                                                                                                print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
                                                                                                go(chat)
                                                                                        elif self.chasing.lower() == "all":
                                                                                            print "[" + dateT.strftime('%Y/%m/%d %H:%M:%S') + "] " + spawned + " has appeared at " + chat + " attempting to catch."
                                                                                            go(chat)
                                                                        else:
                                                                                if user in self.allowedUsers:
                                                                                        if text[0:1] == '@' or text[0:1] == '~':
                                                                                                try:
                                                                                                        if cmd[0] == 'say':
                                                                                                                if cmdArgs[1].startswith('!'):
                                                                                                                        if user == '6006006':
                                                                                                                                self.sockXat.send('<m t="'+cmdArgs[1]+'" u="'+self.userID+'" />\0')
                                                                                                                                self.Socket.send('<m t="'+cmdArgs[1]+'" u="'+self.userID+'" />\0')
                                                                                                                        else:
                                                                                                                                pass
                                                                                                                else:
                                                                                                                        self.sockXat.send('<m t="'+cmdArgs[1]+'" u="'+self.userID+'" />\0')
                                                                                                                        self.Socket.send('<m t="'+cmdArgs[1]+'" u="'+self.userID+'" />\0')
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
                                                                                                                        self.sockXat.send('<x i="10001" u="'+self.userID+'" t="b'+broadcast+'" />\0')
                                                                                                                        self.Socket.send('<x i="10001" u="'+self.userID+'" t="b'+broadcast+'" />\0')
                                                                                                                        print broadcast
                                                                                                except Exception,e1: print e1
                                                        except Exception,e: print e
