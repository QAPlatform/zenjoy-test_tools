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
# dict_name = data.slot4
# dict_name = data.slot5


class check_timeline_count():

    def scence1(self, spreadsheetId, rangeName):
        food_result = []
        try:
            service = google_get_credentials.get_service()
            result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
            food_name_map4 = result.get('values', [])
            # print food_name_map4
            for x in xrange(0, len(food_name_map4[0])):
                num = 0
                # print len(food_name_map4[0])
                for values in food_name_map4:
                    if(len(values) > x):  # 处理越界的问题
                        try:
                            if values[x]:
                                num = num + 1
                        except Exception, e:
                            print e, len(values), x, values[x]
                    else:
                        pass
                food_result.append(num)
                # print len(values), x, num, len(food_result), values[x]
        except Exception, e:
            # raise e
            print e
        # print food_result
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
            if(i == 'map1'):  # map1 是错的，影响结果
                continue
            else:
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
                    print "Result:there are different counts in two sheet,design is %s,timeline is %s " % (len(r_sum), len(result))


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
                                print ("the " + str(index + 1) + " row and the " + str(level_name[col_num]) + " level " + line_name + " is not in design sheet").decode('utf-8')
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
    #           print "*************"
#            print len(foodrange_arr)
#            print len(food)
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
                                                print food[index] + "不应该出现在" + food_value[0], "起始关卡应该在" + str(range_food)


class check_timeline_upgrade():

    def get_tragetads(self, spreadsheetId, rangeName):
        foodid = []
        service = google_get_credentials.get_service()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        google_value = result.get('values', [])
        for x in google_value:
            foodid.append(x[0])  # foodid列数据转化格式
        return foodid

    def main(self):
        # get_foodid={}
        print "开始检查升级traget ads"
        res = []
        newget_foodid = {}
        global dict_name
        for i in dict_name:
            print i + " check:"
            get_foodid = self.get_tragetads(dict_name[i]["spreadsheetId_scence"], dict_name[i]["upgrade_id"])  # upgrade表foodid列数据
            get_tragetads = self.get_tragetads(dict_name[i]["spreadsheetId_scence"], dict_name[i]["upgrade_tragetads"])  # upgrade表upgrade_tragetads列数据

            if len(get_foodid) != len(get_tragetads):
                print ("失败，id与tragetads长度不一致")  # 比较两个列的数据数量是否一致
            else:

                newget_foodid = set(get_foodid)  # 去重的数据
                for a in newget_foodid:
                    # indearr=[]
                    res = []
                    for index, b in enumerate(get_foodid):  # 枚举foodid中的数据
                        if a == b:
                            # indearr.append(index)
                            res.append(get_tragetads[index])  # 去重的数据在foodid中找到对应数据的索引X在traget中的数据res
                            # print "come on"
                    if(len(set(res)) > 1):  # 同一id对应res数据去重后，打印不是相同的数据
                        print("失败，tragetads中不一致的数据:", res)
                    else:
                        pass


class check_guide():

    def get_guidelevel(self, spreadsheetId, rangeName,col_level):
        guidelevel = []
        guidefood = []
        food = []
        dic = {}
        service = google_get_credentials.get_service()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        guide_levelvalue = result.get('values', [])

        for x in guide_levelvalue:
            if len(x) == int(col_level)+1:
                dic[x[int(col_level)]] = x[0]
        # print "食物id：关卡id"
        # print dic
        return dic

    def get_guidefood(self, spreadsheetId, rangeName,col_food):
        dic1 = {}
        service = google_get_credentials.get_service()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        guide_foodvalue = result.get('values', [])

        for y in guide_foodvalue:
            if len(y) == int(col_food)+1:
                dic1[y[0]] = y[int(col_food)]
        # print "食物id：引导id"
        # print dic1
        return dic1

    def main(self):
        print "开始检查新手引导配置"
        global dict_name

        for i in dict_name:
            print i + " check:"
            get_levelguide = self.get_guidelevel(dict_name[i]["spreadsheetId_scence"], dict_name[i]["level_guide"],dict_name[i]["col_level"])
            get_foodguide = self.get_guidefood(dict_name[i]["spreadsheetId_scence"], dict_name[i]["foodg_uide"],dict_name[i]["col_food"])

            if len(get_levelguide) == len(get_foodguide):
                print "两个表中的食物id一致"
                for x in get_levelguide:
                    if get_foodguide.has_key(x):
                        pass
                    else:
                        print get_levelguide[x] + " have not in food sheet"
            else:
                if len(get_levelguide) > len(get_foodguide):
                   for x in get_levelguide:
                        if get_foodguide.has_key(x):
                            pass
                        else:
                            print x + " have not in food sheet"
                else:
                    for x in get_foodguide:
                        if get_levelguide.has_key(x):
                            pass
                        else:
                            print x + " have not in level sheet"


            # if get_levelguide.=get_foodguide[0]:
            #     print "新手引导检查通过"
            # else:
            #     print x[14]


if __name__ == '__main__':

    check_timeline_food().main()
    check_timeline_food().check_foodrange()
    # check_timeline_food().get_name_range("1zsRwqwAcM22ilYvdyNic-ynlXbD4oZm0RmmPCLO1n-Q")
    check_timeline_count().main()
    check_timeline_upgrade().main()
    check_guide().main()
