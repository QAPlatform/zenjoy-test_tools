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

# map1 80行
# map4 90行
dict_name = {
    "map4": {
        "spreadsheetId_scence": "1HO9ZA93QW-jZBlhLSgF_IKwqBbIpBa1TJURQ1vaULBU",
        "rangeName_scence": "Timeline!D2:BK33",
        "rangeName_scence2": "Timeline!D1:BK34",
        "spreadsheetId": "1v-eAQHSLTcj2u_msdtkedBB4wrj0uIVVi1e-tKZMeFI",
        "rangeName": "第一稿-关卡设计!BO5:GM64",
        "foodName": "食物!B3:B50"
    },
    "map3": {
        "spreadsheetId_scence": "11SzQ6trYp1DK86z-ktRT0ANr76fmdPiyng5Ts_ICcHU",
        "rangeName_scence": "Timeline!D2:BK33",
        "rangeName_scence2": "Timeline!D1:BK34",
        "spreadsheetId": "1DfqZ5v20o7jgKKP9HQR2k6OnqP10i5B93MpoqD3T10s",
        "rangeName": "第一稿-关卡设计!CE5:HC64",
        "foodName": "食物!B3:B47"
    },
    "map2": {
        "spreadsheetId_scence": "1n8FjPc78y6TjNmexwVZFBtMqHcGCwTwv99Khw6TLthE",
        "rangeName_scence": "Timeline!D2:BK33",
        "rangeName_scence2": "Timeline!D1:BK34",
        "spreadsheetId": "1lPXokBK3zI8fz_swSBAOa0QRyEX32ypX3PDe7IAyn4g",
        "rangeName": "第一稿-关卡设计!CN5:GR64",
        "foodName": "食物!B3:B47"
    },
    "map1": {
        "spreadsheetId_scence": "1jcZfcQn823qbn3XlcuZJJOa0fkZFOXwssYzAJc_M4F8",
        "rangeName_scence": "Timeline!D2:BK33",
        "rangeName_scence2": "Timeline!D1:BK34",
        "spreadsheetId": "1tOnLTdR_m94ioN0xjQsmtVKvAxOpULMKytUucbj4-D0",
        "rangeName": "第一稿-关卡设计!BQ5:FU64",
        "foodName": "食物!B3:B47"
    }
}


# dict_value = {"id": "1", "level": "1", "cash": "1", "diamond": "1", "exp": "1"}


def check_upgrade():
    dict_value = {}
    for i in range(1, 90):
        dict_value[i] = {}

    # spreadsheet_id = "1jcZfcQn823qbn3XlcuZJJOa0fkZFOXwssYzAJc_M4F8"  # map1
    spreadsheet_id = "1n8FjPc78y6TjNmexwVZFBtMqHcGCwTwv99Khw6TLthE"  # map2
    # spreadsheet_id = "11SzQ6trYp1DK86z-ktRT0ANr76fmdPiyng5Ts_ICcHU"  # map3
    # spreadsheet_id = "1HO9ZA93QW-jZBlhLSgF_IKwqBbIpBa1TJURQ1vaULBU"  # map4
    range_names = []
    range_names.append("upgrade!B4:B93")  # map1 94
    range_names.append("upgrade!c4:c93")  # map4 92
    range_names.append("upgrade!i4:I93")  # map2 93
    range_names.append("upgrade!j4:j93")  # map3 90
    range_names.append("upgrade!m4:m93")
    service = google_get_credentials.get_service()
    re = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_names).execute()
    result = re.get('valueRanges', [])

    for i in range(1, 90):
        row_value = []
        for line in result:
            value = line.get('values', [])
            # print value
            row_value.append(value[i])
        dict_value[i]["id"] = row_value[0]
        dict_value[i]["level"] = row_value[1]
        dict_value[i]["cash"] = row_value[2]
        dict_value[i]["diamond"] = row_value[3]
        dict_value[i]["exp"] = row_value[4]

    return dict_value


def read_test_file():
    test_info = []
    f = open("D:/map2")
    for line in f.readlines():
        if 'UpgradeMan.js' and "testinfo:" in line:
            line = line.split("testinfo: ")
            # print line
            line = line[1]
            # line = line[1].replace("}", "")
            line_json = json.loads(line)
            # print line_json
            test_info.append(line_json)
    f.close
    # print test_info
    return test_info


def main():
    upgrade_file = read_test_file()
    upgrade_google = check_upgrade()
    # print upgrade_file
    for test_value in upgrade_file:
        for i in upgrade_google:
            # print upgrade_google[i]["id"][0]
            # print test_value
            # print upgrade_google[i]
            if test_value.get("id") == int(upgrade_google[i]["id"][0]) and test_value.get("level") == int(upgrade_google[i]["level"][0]):
                if(test_value.get("exp") == int(upgrade_google[i]["exp"][0]) and test_value.get("diamond") == int(upgrade_google[i]["diamond"][0]) and test_value.get("cash") == int(upgrade_google[i]["cash"][0])):
                    print str(upgrade_google[i]["id"]) + "ok"
                else:
                    # print "数值表中id:" + str(upgrade_google[i]["id"][0]) + ",level:" + str(test_value.get("level")) + "的经验为" + str(upgrade_google[i]["exp"][0])
                    print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表经验" + str(upgrade_google[i]["exp"][0]) + ":游戏中" + str(test_value.get("exp"))
                    print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表钻石" + str(upgrade_google[i]["diamond"][0]) + ":游戏中" + str(test_value.get("diamond"))
                    print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表金币" + str(upgrade_google[i]["cash"][0]) + ":游戏中" + str(test_value.get("cash"))

if __name__ == '__main__':
    main()
