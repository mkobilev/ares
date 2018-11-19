#!/usr/bin/python

import socket
import sys

HOST = "localhost"
PORT = 31337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('hello')

data = s.recv(32)

print data
s.close()
print "Received: '%s'"%data