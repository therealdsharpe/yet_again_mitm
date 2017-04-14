#! /usr/bin/env python2
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from mimetypes import guess_type
from SocketServer import ThreadingMixIn
import threading
import fcntl
import os


PORT_NUMBER = 1337
method = "maymay"
class rickRollHandler(BaseHTTPRequestHandler):
	
	#use self.path for deciding content to pump out
	def _set_headers(self,mime_type):
		self.send_response(200)
		self.send_header('Content-type', mime_type)
                self.send_header('Cache-Control','max-age=864000')
		self.end_headers()
		
	def do_HEAD(self):
		mime = guess_type(self.path)
		mime_list = list(mime)
		if mime_list[0] == None:
			print 'No valid mime_type\n changing type'
			self.path = 'index.html'
			mime = guess_type(self.path)
		print "Mime TYPE:"+str(mime)
		self._set_headers(mime)
	
	#Handler for the GET requests
	def do_GET(self):
		print '-'*20
		print 'Requested HOST:%s' % self.headers.getheader('Host')
		print 'Requested PATH:%s' % self.path
		if self.path == '/favicon.ico':
			print 'favicon wanted'
		elif method == "404":
			if self.path != '/404img.png':
				self.path = '/404.html'
		elif method == "maymay":
			print 'MAYMAY AYYYY LMAO x3'
			pointer = self.path.rfind("maymay")
			if pointer != -1:
				print 'pointer to maymay'+ str(pointer)
				print 'maymay string ' + self.path[pointer-1:]
				self.path = self.path[pointer-1:]
                        else:
                            self.path='/index.html'
		if self.path == '/':
			self.path = '/index.html'
		elif "404.png" in self.path:
			self.path = '/404.png'
		self.path = self.path[1:]
		print "PATH:"+self.path
		self.do_HEAD()
		try:
			with open(self.path,'r') as f:
				flag = fcntl.fcntl(f.fileno(), fcntl.F_GETFD)
				fcntl.fcntl(f, fcntl.F_SETFL, flag | os.O_NONBLOCK)
				# Send the html message
				self.wfile.write(f.read())
		except IOError:
			print "Exception caught. 404 %s" % self.path
			with open('404.html','r') as f:
				for l in f:
					self.wfile.write(l)
			return
		return

	def do_POST(self):
		pass

class threadedHTTP(ThreadingMixIn, HTTPServer):
	'''handles shit'''
	pass
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = threadedHTTP(('', PORT_NUMBER), rickRollHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
