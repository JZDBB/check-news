#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import socket
import json
import base64


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    try:
        #print "Send: {}".format(message)
        sock.sendall(message)
        #response = sock.recv(1024)
        #jresp = json.loads(response)
        #print "Recv: ",jresp

    finally:
        sock.close()

def sendata(HOST,PORT,message):
     #print message
     for key in message.keys():
        if message[key]==None:
            continue
        message[key]=base64.b64encode(message[key])
     #print message
     jmsg1 = json.dumps([message])
     #print type(jmsg1)
     client(HOST,PORT,jmsg1)

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 50001
    msg1 = [{'src':"zj", 'dst':"zjdst"}]
    msg2 = [{'src':"ln", 'dst':"lndst"}]
    msg3 = [{'src':"xj", 'dst':"xjdst"}]
    jmsg1 = json.dumps(msg1)
    jmsg2 = json.dumps(msg2)
    jmsg3 = json.dumps(msg3)

    client(HOST, PORT, jmsg1)
    client(HOST, PORT, jmsg2)
    client(HOST, PORT, jmsg3)

