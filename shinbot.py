# shinbot 0.1

import socket
import string 

class Bot:
	nick = ""
	ident = ""
	realname = ""
	onchannel = False
	sock = None
	active = True
	quitting = False
	def __init__(self, nick="gitaxiazzz", ident="gitaxiazzz", realname="shinDebotti"):
		self.nick = nick
		self.ident = ident
		self.realname = realname
		self.channels = []
		self.admin = None
		self.admin_password = 's44tana'

	def irc_command(self, command, arg):
		c = command + ' ' + arg + "\r\n"
		self.sock.send(c)

	def check_privmsg(self, message):
		for i in range(0, len(message)):
			message[i] = message[i].lstrip(':')
		print "received ", message
		host = message[0]
		sender = message[0].split('!')[0]
		if "authorize" in message:
			password = message[-1]
			if self.admin_password == password:
				self.admin = host
			self.irc_command('PRIVMSG', sender + ' :Authorized ' + sender + '!')
		if "hello" in message:
			self.irc_command('PRIVMSG', sender + ' :Hello!')
		if "join" in message and host == self.admin:
			channel = message[-1]
			if not self.onchannel:
				self.irc_command('JOIN', ':'+channel)
				self.irc_command('PRIVMSG', sender + ' :Joining ' + channel + '!')
				self.onchannel = True
				self.channels.append(channel)
		if "part" in message and host == self.admin:
			channel = message[-1]
			if self.onchannel:
				if channel in self.channels:
					self.irc_command('PART', ':'+channel)
				else:
					print "Not on " + channel
					self.irc_command('PRIVMSG', sender + ' :Not on ' + channel + '!')
			else:
				print "Not on a channel!"
				self.irc_command('PRIVMSG', sender + ' :Not on channel!')
		if "quit" in message and host == self.admin:
			self.irc_command('PRIVMSG', sender + ' :Quitting!')
			self.irc_command('QUIT', ':Bye!')
			self.quitting = True
		if self.nick + ":" in message:
			for c in self.channels:
				if c in message:
					if 'rivo' in message and  'vitsi' in message:
						self.irc_command('PRIVMSG', c + ' :penis lol')
					else:
						self.irc_command('PRIVMSG', c + ' :so cool!')


	def run(self, host='europe.afternet.org', port=6667):
		r = ""
		self.sock = socket.socket()
		self.sock.connect((host, port))
		self.sock.send("NICK %s\r\n" % self.nick)
		self.sock.send("USER %s %s bla :%s\r\n" % (self.ident, host, self.realname))
		while self.active:
			r = r + self.sock.recv(1024)
			lines = r.split('\n')
			r = lines.pop()
			for l in lines:
				print l
				l=string.rstrip(l)
				l=string.split(l)
				if "PRIVMSG" in l:
					self.check_privmsg(l)
				if(l[0]=="PING"):
					self.sock.send("PONG %s\r\n" % l[1])
			if self.quitting:
				self.active = False
					

if __name__ == '__main__':
	bot = Bot()
	bot.run()
