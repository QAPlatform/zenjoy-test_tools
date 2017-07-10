# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import xlrd
import xlrd
import xlwt
from datetime import date, datetime
from collections import Counter
import os
import json
import google_get_credentials

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def scence1(spreadsheetId,rangeName):
	food_result = []
	try:
		service = google_get_credentials.get_service()
		result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
		food_name_map4 = result.get('values', [])

		for x in xrange(0,len(food_name_map4[0])):
			num=0
			for values in  food_name_map4:
				#print values[x]
				if values[x]:
					num=num+1
			food_result.append(num)
	except Exception, e:
		raise e

	return (food_result)

def check_sum(spreadsheetId,rangeName):

	r_sum=[]

	service = google_get_credentials.get_service()
	result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
	food_name_map4 = result.get('values', [])

 	for values in  food_name_map4:
 		r_result=[]
 		for n in xrange(0,len(values),4):
 			x=values[n]
 			if x!='0':
 				num=1
			else:
				num=0
			r_result.append(num)
		r_sum.append(sum(r_result))

	return(r_sum)


def main():
	dict_name={
		"map4":{
			"spreadsheetId_scence":"1mNCquKhkZtt99CfstAx0PWq27zsASlMWNLHfa0eWeP4",
			"rangeName_scence":"Timeline!D2:BK34",
			"spreadsheetId":"1R9LD5Rk4oszr8oQUIufWeLAv5-yN4Q_MyUJGseOISxI",
			"rangeName":"第一稿-关卡设计!BO5:GM64"
		},
		"map3":{
			"spreadsheetId_scence":"1TZGIhA9HTblxyBEzXXcjyGITVnLaMtVoZtpfKmQdkoI",
			"rangeName_scence":"Timeline!D2:BK32",
			"spreadsheetId":"1R9LD5Rk4oszr8oQUIufWeLAv5-yN4Q_MyUJGseOISxI",
			"rangeName":"第一稿-关卡设计!CE5:HC64"
		},
		"map2":{
			"spreadsheetId_scence":"14p8pEnUoSeoMBMIcNWBlaYSzkU1G4yljDnd60qWVBB0",
			"rangeName_scence":"Timeline!D2:BK29",
			"spreadsheetId":"1-_w5j53P4tSO-CFBBMl9RHY2QwiHGoN-Dp_COTee0ds",
			"rangeName":"第一稿-关卡设计!CN5:GR64"
		},
		"map1":{
			"spreadsheetId_scence":"1xzmnONiAhbZT7UrNTL8EHuuLw_HhfN9hqeopLTsG3TU",
			"rangeName_scence":"Timeline!D2:BK29",
			"spreadsheetId":"12yLC7fCT9y96wlY570xTrLzQvMfw7ETkJDr2pWEjywU",
			"rangeName":"第一稿-关卡设计!BQ5:FU64"
		}
	}

	# spreadsheetId_scence = "1TZGIhA9HTblxyBEzXXcjyGITVnLaMtVoZtpfKmQdkoI"  
	# rangeName_scence = "Timeline!D2:BK32"
	# spreadsheetId = "1R9LD5Rk4oszr8oQUIufWeLAv5-yN4Q_MyUJGseOISxI"
	# rangeName = "第一稿-关卡设计!CE5:HC64"   #map3 

	# spreadsheetId_scence = "1TZGIhA9HTblxyBEzXXcjyGITVnLaMtVoZtpfKmQdkoI"  
	# rangeName_scence = "Timeline!D2:BK32"
	# spreadsheetId = "1R9LD5Rk4oszr8oQUIufWeLAv5-yN4Q_MyUJGseOISxI"
	# rangeName = "第一稿-关卡设计!CE5:HC64"   #map3 

	# spreadsheetId_scence = "1TZGIhA9HTblxyBEzXXcjyGITVnLaMtVoZtpfKmQdkoI"  
	# rangeName_scence = "Timeline!D2:BK32"
	# spreadsheetId = "1R9LD5Rk4oszr8oQUIufWeLAv5-yN4Q_MyUJGseOISxI"
	# rangeName = "第一稿-关卡设计!CE5:HC64"   #map3 
	for i in dict_name:
		print i+" check结果："
		r_sum=check_sum(dict_name[i]["spreadsheetId"],dict_name[i]["rangeName"])
		result=scence1(dict_name[i]["spreadsheetId_scence"],dict_name[i]["rangeName_scence"])
		# print r_sum
		# print result
		if len(r_sum)==len(result):
			for j in range(0,len(r_sum)):
				if r_sum[j]==result[j]:
					pass
				else:
					print ("  第 %d 关配置数量不一致:"%(j+1))
					print ("  	关卡设计表数量为%d"%r_sum[j])
					print("  	场景表timeline中数量为%d"%result[j])
		else:
			print "对比结果：两个表中配置数量不等"

main()
	