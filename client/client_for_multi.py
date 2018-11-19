# -*- coding: utf-8 -*-
import socket
 
  
host = "localhost"
port = 1337
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
 
s.send("test")
 
     
s.close()