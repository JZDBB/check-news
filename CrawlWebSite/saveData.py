#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import json
import os
import hashlib
import base64

def get_md5_value(strdata):
	my_md5 = hashlib.md5()
	my_md5.update(strdata)
	my_md5_Digest = my_md5.hexdigest()
	return my_md5_Digest
def saveData(fileName,data):
	message=data
	for key in message.keys():
		if message[key]==None:
			continue
		message[key]=message[key]
	try:
		fileName = get_md5_value(fileName)
		filePath =os.path.join(os.getcwd(),"resultData")
		filePath =os.path.join(filePath,fileName)
		with open(filePath, 'w') as file_obj:
			json.dump(message,file_obj)
			file_obj.close()	
	except:
		pass


def loadData(fileName):
	fileName = get_md5_value(fileName)
	filePath =os.path.join(os.getcwd(),"resultData")
	filePath =os.path.join(filePath,fileName)
	decodeData={}
	with open(filePath) as file_obj:
		data = json.load(file_obj)
		for k in data.keys():
			if data[k]==None:
				decodeData[k]=data[k]
			else:
				decodeData[k]=base64.b64decode(data[k])
		file_obj.close()
		return decodeData

