#!/usr/bin/python
import sys
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from subprocess import call
import subprocess
import commands
import re
import os
from optparse import OptionParser

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, prefix):
        ClientXMPP.__init__(self, jid, password)
	self.room = "" 
	self.prefix = prefix
	self.nick = prefix + re.sub(r'[{}]','',os.popen('dohost "show hostname"').read()).rstrip('\n')[1:]
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
	self.add_event_handler("muc::%s::got_online" % self.room,self.muc_online)
	self.add_event_handler("groupchat_invite", self.accept_invite)
	self.add_event_handler("groupchat_message", self.muc_message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
	#self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def message(self, msg):
	if "conference" not in repr(msg['from']):
            if msg['type'] in ('chat', 'normal'):
	        str = "%(body)s" % msg
                sstr = str.split(';')
                sstr.insert(0, "dohost")
                #final = ["dohost", "conf t", "show clock"]
                final = sstr
                p = subprocess.Popen(final, stdout=subprocess.PIPE)
                outj = p.stdout.read()
                #print outj
                msg.reply("Output:\n%s" % outj).send()
			
    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware 
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.
        Whenever the bot's nickname is mentioned, respond to
        the message.
        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.
        This handler will reply to messages that mention 
        the bot's nickname.
        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
	if self.prefix not in msg['mucnick']:
    	    str = "%(body)s" % msg
            sstr = str.split(';')
            sstr.insert(0, "dohost")
            final = sstr
            p = subprocess.Popen(final, stdout=subprocess.PIPE)
            outj = p.stdout.read()
            self.send_message(mto=msg['from'].bare,
		mbody="Output:\n%s" % outj,
                 mtype='groupchat')

    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are 
        handled by sending a welcome message that includes
        the user's nickname and role in the room.
        Arguments:
            presence -- The received presence stanza. See the 
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
	print "inside online"
#        if presence['muc']['nick'] != self.nick:
#            self.send_message(mto=presence['from'].bare, mbody="Hello, %s %s" % (presence['muc']['role'],presence['muc']['nick']),mtype='groupchat')
			
    def accept_invite(self, inv):
	print("Invite from %s to %s" %(inv["from"], inv["to"]))
	self.plugin['xep_0045'].joinMUC(inv["from"], self.nick, wait=True)

if __name__ == '__main__':
    userId = '<username@localhost>'
    pwd = '<password>'
    prefix = 'node-'
    xmpp = EchoBot(userId, pwd, prefix)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    xmpp.connect((<ip address>, <port example: 5222>))
    xmpp.process(block=True)

