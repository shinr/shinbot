#food.py

import urllib2 as url
from HTMLParser import HTMLParser

class Parser(HTMLParser):
	current_data = ""
	reading_data = False
	header_tag = False
	data = []
	def handle_starttag(self, tag, attrs):
		if tag == "p": 
			self.reading_data = True
			#print "<--------"
			self.current_data = ""
		if tag == "h4":
			self.header_tag = True

	def handle_endtag(self, tag):
		if tag == "p": 
			self.reading_data = False
			#print "-------->"
			if self.current_data not in self.data:
				self.data.append(self.current_data)
				
		if tag == "h4":
			self.header_tag = False

	def handle_data(self, data):
		if self.reading_data:
			if len(data) > 4:
				if not "Kcal" in data:
					if not self.header_tag:
						self.current_data += data


		
def run():
	parser = Parser()
	web = url.urlopen('http://ruoka.0x00.fi')
	c = web.read()
	parser.feed(c.replace('<b>', '').replace('</b>', ''))
	print parser.data
if __name__ == "__main__":
	print "parsing...\n\n"
	run()