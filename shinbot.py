# shinbot 0.1

import socket
import string 
import select
import os
import imp
import sys

class Bot:
	nick = ""
	ident = ""
	realname = ""
	onchannel = False
	sock = None
	active = True
	quitting = False
	def __init__(self, nick, ident, password, realname="shinDebotti"):
		self.nick = nick
		self.ident = ident
		self.realname = realname
		self.channels = []
		self.admin = None
		self.admin_password = password
		self.plugins = []

	def irc_command(self, command, arg):
		c = command + ' ' + arg + "\r\n"
		self.sock.send(c)

	def extract_nick(self, message):
		while message[-1] in string.punctuation:
			message = message[:-1]
		return message

	def write_output(self, message, target):
		print message, '\n'
		self.irc_command('PRIVMSG', target + ' :' + message)

	def check_privmsg(self, message):
		TAG_MESSAGE = 3
		TAG_TARGET = 2
		TAG_COMMAND = 1
		TAG_HOST = 0
		for i in range(0, len(message)):
			message[i] = message[i].lstrip(':')
		print "received ", message
		host = message[TAG_HOST]
		sender = message[TAG_HOST].split('!')[0]
		target = message[TAG_TARGET]
		# only privmsg
		if target not in self.channels:
			# admin commands
			if host == self.admin:
				if "join" == message[TAG_MESSAGE]:
					channel = message[-1]
					if not self.onchannel:
						self.irc_command('JOIN', ':'+channel)
						self.write_output("Joining " + channel, sender)
						self.onchannel = True
						self.channels.append(channel)
				elif "part" == message[TAG_MESSAGE]:
					channel = message[-1]
					if len(self.channels) > 0:
						if channel in self.channels:
							self.irc_command('PART', ':'+channel)
						else:
							self.write_output("Not on " + channel, sender)
					else:
						self.write_output("Not on channel!", sender)
				elif "quit" == message[TAG_MESSAGE]:
					self.irc_command('PRIVMSG', sender + ' :Quitting!')
					self.irc_command('QUIT', ':Bye!')
					self.quitting = True
				elif "say" == message[TAG_MESSAGE] and "in" == message[TAG_MESSAGE + 1]:
					if message[TAG_MESSAGE + 2] in self.channels:
						c = message[TAG_MESSAGE + 2] 
						m = ' '.join(message[TAG_MESSAGE + 3:])
						self.irc_command('PRIVMSG', c + ' :' + m)
				elif "reload" == message[TAG_MESSAGE]:
					pass
			# public privmmsg commands
			else:
				if "authorize" == message[TAG_MESSAGE]:
					password = message[-1]
					if self.admin_password == password:
						self.admin = host
						self.irc_command('PRIVMSG', sender + ' :Authorized ' + sender + '!')
				elif "hello" == message[TAG_MESSAGE]:
					self.irc_command('PRIVMSG', sender + ' :Hello!')
		# public channel commands
		else:
			if self.nick in self.extract_nick(message[TAG_MESSAGE]):
				for c in self.channels:
					if c in message:
						if 'rivo' in message and 'vitsi' in message:
							self.irc_command('PRIVMSG', c + ' :penis lol')
						else:
							self.irc_command('PRIVMSG', c + ' :so cool!')
			else:
				print self.plugins
				for p in self.plugins:
					try:
						response = p.run(message)
						if response:
							self.irc_command('PRIVMSG', response[0] + " :" + response[1])
					except AttributeError:
						print "Faulty plugin without run-method. <", p, ">"
						self.irc_command('PRIVMSG', sender + ' :Faulty plugin without run-method <' + p.__name__ + '>!')

	def load_plugins(self):
		plugins = []
		plugin_folder = 'plugins'
		plugin_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), plugin_folder)
		candidates = os.listdir(plugin_folder)
		for c in candidates:
			if not ".py" in c or ".pyc" in c:
				continue
			print c
			info = imp.find_module(c.split('.')[0], [plugin_folder])
			plugins.append({"name":c, "info":info})
		for p in plugins:
			self.plugins.append(imp.load_module(p['name'].split('.')[0], *p['info']))


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
					
# maybe make this a bit more flexible
if __name__ == '__main__':
	if len(sys.argv) < 6:
		print "usage:\nshinbot.py <name> <ident> <host> <port> <admin_password> (<realname>)"
		print "<realname> is optional, defaults to shinDebotti"
		sys.exit(0)
	print "loading shinbot..."
	name = sys.argv[1]
	ident = sys.argv[2]
	admin_password = sys.argv[3]
	host = sys.argv[4]
	port = sys.argv[5]
	print "name: ", name
	print "ident: ", ident
	print "connecting to ", host, ":", port
	print "your password is ", admin_password
	if len(sys.argv) == 7:
		realname = sys.argv[6]
		bot = Bot(name, ident, admin_password, realname)
	else:
		bot = Bot(name, ident, admin_password)
	bot.load_plugins()
	bot.run(host, int(port))
