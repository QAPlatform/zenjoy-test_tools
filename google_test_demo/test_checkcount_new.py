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
import data
import json
import google_get_credentials
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

dict_name = data.slot2
#dict_name = data.slot4


class check_timeline_count():

    def scence1(self, spreadsheetId, rangeName):
        food_result = []
        try:
            service = google_get_credentials.get_service()
            result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
            food_name_map4 = result.get('values', [])

            for x in xrange(0, len(food_name_map4[0])):
                num = 0
                for values in food_name_map4:
                    # print values[x]
                    if values[x]:
                        num = num + 1
                food_result.append(num)
        except Exception, e:
            raise e

        return (food_result)

    def check_sum(self, spreadsheetId, rangeName):

        r_sum = []

        service = google_get_credentials.get_service()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        food_name_map4 = result.get('values', [])

        for values in food_name_map4:
            r_result = []
            for n in xrange(0, len(values), 4):
                x = values[n]
                if x != '0':
                    num = 1
                else:
                    num = 0
                r_result.append(num)
            r_sum.append(sum(r_result))

        return(r_sum)

    def main(self):
        global dict_name
        print "开始检查timeline数量"
        for i in dict_name:
            print i + " check:"
            r_sum = self.check_sum(dict_name[i]["spreadsheetId"], dict_name[i]["rangeName"])
            result = self.scence1(dict_name[i]["spreadsheetId_scence"], dict_name[i]["rangeName_scence"])
            # print r_sum
            # print result
            if len(r_sum) == len(result):
                for j in range(0, len(r_sum)):
                    if r_sum[j] == result[j]:
                        pass
                    else:
                        print ("  the %d level is :" % (j + 1))
                        print ("  	desgian_count%d" % r_sum[j])
                        print("  	timeline%d" % result[j])
            else:
                print "对比结果：两个表中配置数量不等"


class check_timeline_food():

    def get_food_name_map(self, spreadsheetId, rangeName):
        food_result = []
        try:
            service = google_get_credentials.get_service()
            result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
            food_name_map = result.get('values', [])
            for values in food_name_map:
                food_result.append(values[0])
            # print (food_result)
            return food_result

        except Exception, e:
            raise e

    def get_timeline_name(self, spreadsheetId, rangeName):
        food_result = []
        try:
            service = google_get_credentials.get_service()
            result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
            google_value = result.get('values', [])
            for values in google_value:

                food_result_value = []
                for foodname in values:
                    food_result_value.append(foodname)
                food_result.append(food_result_value)

            # print (food_result[8])
            return food_result
        except Exception, e:
            print (e)

    def main(self):
        global dict_name
        print "开始检查timeline名称"
        for i in dict_name:
            print i + "check结果："
            time_line_value = self.get_timeline_name(dict_name[i]["spreadsheetId_scence"], dict_name[i]["rangeName_scence2"])
            food_name_map = self.get_food_name_map(dict_name[i]["spreadsheetId"], dict_name[i]["foodName"])
            # food_name_range = self.get_food_name_map(dict_name[i]["spreadsheetId_scence"], dict_name[i]["foodrange"])

            level_name = time_line_value[0]

            for index in range(1, len(time_line_value)):  # index为行数
                    # print (index)
                    # print (level_name[index])
                for col_num, time_line_name in enumerate(time_line_value[index]):  # col_num为列数
                    food_name = time_line_name.split(",")
                    if len(food_name) > 1:  # 前两个字符没用，删了增加效率
                        # print len(time_line_name)
                        del food_name[1]
                        del food_name[0]

                    if len(food_name) > 3:  # 检查食物大于3饿行数
                        print ("第" + str(level_name[col_num]) + "关的" + line_name + "食物大于3了")

                    for line_name in food_name:
                        if(line_name != ""):
                            check_count = 0
                            for food in food_name_map:
                                # print food
                                if type(line_name) != type(1):
                                    line_name = line_name.replace("(", "").replace(")", "")
                                    if line_name == food:
                                        check_count += 1
                                    else:
                                        pass

                            if check_count < 1:
                                print ("第" + str(index + 1) + "行第" + str(level_name[col_num]) + "关的" + line_name + "设计表中不存在").decode('utf-8')
                        else:
                            pass

    def check_foodrange(self):
        global dict_name
        dict_food = {}
        print "开始检查食物范围"
        for i in dict_name:
            foodrange_arr = []
            print i + "check结果："
            time_line_value = self.get_timeline_name(dict_name[i]["spreadsheetId_scence"], dict_name[i]["rangeName_scence2"])
            food_name_range = self.get_food_name_map(dict_name[i]["spreadsheetId_scence"], dict_name[i]["foodrange"])
            food = self.get_food_name_map(dict_name[i]["spreadsheetId_scence"], dict_name[i]["food"])
            time_line_value_col = map(list, zip(*time_line_value))

            for i in food_name_range:  # 获取食物范围
                food_range = int(i.split(',')[0])
                foodrange_arr.append(food_range)

            # for index, i in enumerate(food_name):  # 建立名称和解锁等级对应关系索引
            #     dict_food[i] = foodrange_arr[index]
            print "*************"
            print len(foodrange_arr)
            print len(food)
            for food_value in time_line_value_col:  # 按列取整张表
                food_count = []
                check_count = 0
                # for food in food_name:

                for value_f in food_value:  # 循环每列
                    for index, range_food in enumerate(foodrange_arr):
                        # print value_f[0]
                        if(int(food_value[0])) < int(range_food):  # 如果表中的关卡数小于食物的起始等级
                            food_name = value_f.split(",")
                            if len(food_name) > 1:  # 前两个字符没用，删了增加效率
                                del food_name[1]
                                del food_name[0]
                                for line_name in food_name:
                                    if(line_name != ""):
                                        if type(line_name) != type(1):
                                            line_name = line_name.replace("(", "").replace(")", "")  # line_name为每个食物名称
                                            if (line_name == food[index]):
                                                print food[index] + "不应该出现在" + food_value[0]


if __name__ == '__main__':

    check_timeline_food().main()
    check_timeline_food().check_foodrange()
    # check_timeline_food().get_name_range("1zsRwqwAcM22ilYvdyNic-ynlXbD4oZm0RmmPCLO1n-Q")
    check_timeline_count().main()
