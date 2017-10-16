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
        "spreadsheetId_scence": "16i_V-NmIhIqxFyD8HgeNucV70DYoE3iqjyD3fpqNXkI",
        "rangeName_scence": "Timeline!D2:BK34",
        "rangeName_scence2": "Timeline!D1:BK34",
        "spreadsheetId": "1mm-sURsigZ3Q_gLgU3RzP14BhljqgyiWED6rPaEM6qI",
        "rangeName": "第一稿-关卡设计!BO5:GM64",
        "foodName": "食物!B3:B60"
    },
    "map3": {
        "spreadsheetId_scence": "1_zKvv9zotGnuJj0KscltwqaM_lUU_987ihbFlN8oevo",
        "rangeName_scence": "Timeline-c!D2:BK32",
        "rangeName_scence2": "Timeline-c!D1:BK34",
        "spreadsheetId": "1pFQNMChfSSqV1vMCEjM8mw7fqViKd03TseTMs4Mnp-I",
        "rangeName": "第一稿-关卡设计!CE5:HC64",
        "foodName": "食物!B3:B47"
    },
    "map2": {
        "spreadsheetId_scence": "16HsFF7iy6w88lUSIUesHes6MYZYEnq4Wy7J-L8z3qTo",
        "rangeName_scence": "Timeline-c!D2:BK29",
        "rangeName_scence2": "Timeline-c!D1:BK34",
        "spreadsheetId": "1SmQNevKYlJzJht8gsnhA29CC74Qav35TDALVf4_zFKI",
        "rangeName": "第一稿-关卡设计!CN5:GR64",
        "foodName": "食物!B3:B47"
    },
    "map1": {
        "spreadsheetId_scence": "1JzGhU8JBgBx47IZ7DXPhb4sUZnly1t-OSqGQCNmna9E",
        "rangeName_scence": "Timeline-c!D2:BK29",
        "rangeName_scence2": "Timeline-c!D1:BK34",
        "spreadsheetId": "1NY4V8naN-LsnkBELWHyPerBOarBg3VSev6ahMBct7iY",
        "rangeName": "第一稿-关卡设计!BQ5:FU64",
        "foodName": "食物!B3:B47"
    }
}


# dict_value = {"id": "1", "level": "1", "cash": "1", "diamond": "1", "exp": "1"}


def check_upgrade():
    dict_value = {}
    for i in range(1, 45):
        dict_value[i] = {}
# 1HO9ZA93QW - jZBlhLSgF_IKwqBbIpBa1TJURQ1vaULBU
# spreadsheet_id = "1JzGhU8JBgBx47IZ7DXPhb4sUZnly1t-OSqGQCNmna9E"  #map1
# spreadsheet_id = "16HsFF7iy6w88lUSIUesHes6MYZYEnq4Wy7J-L8z3qTo"  # map2
# spreadsheet_id = "1_zKvv9zotGnuJj0KscltwqaM_lUU_987ihbFlN8oevo"  # map3
    # spreadsheet_id = "16i_V-NmIhIqxFyD8HgeNucV70DYoE3iqjyD3fpqNXkI"  # map4
    spreadsheet_id = "1jndZFK4gXLrwbl3AnOgjyXqKBJW2NHxk8gG_318y5kQ"  # slot5
    range_names = []
    range_names.append("upgrade!B4:B48")  # map1 83
    range_names.append("upgrade!c4:c48")  # map4 93
    range_names.append("upgrade!i4:I48")  # map2 81
    range_names.append("upgrade!j4:j48")  # map3 90
    # range_names.append("upgrade!m4:m48")  # 经验
    service = google_get_credentials.get_service()
    re = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_names).execute()
    result = re.get('valueRanges', [])

    for i in range(1, 45):
        row_value = []
        for line in result:
            value = line.get('values', [])
            # print value, len(value)
            row_value.append(value[i])
        dict_value[i]["id"] = row_value[0]
        dict_value[i]["level"] = row_value[1]
        dict_value[i]["cash"] = row_value[2]
        dict_value[i]["diamond"] = row_value[3]
        #dict_value[i]["exp"] = row_value[4]

    return dict_value


def read_test_file():
    test_info = []
    f = open("slot5map1.log")
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
                # if(test_value.get("exp") == int(upgrade_google[i]["exp"][0]) and
                # test_value.get("diamond") == int(upgrade_google[i]["diamond"][0]) and
                # test_value.get("cash") == int(upgrade_google[i]["cash"][0])):
                if(test_value.get("diamond") == int(upgrade_google[i]["diamond"][0]) and test_value.get("cash") == int(upgrade_google[i]["cash"][0])):
                    print str(upgrade_google[i]["id"]) + "ok"
                else:
                    # print "数值表中id:" + str(upgrade_google[i]["id"][0]) + ",level:" + str(test_value.get("level")) + "的经验为" + str(upgrade_google[i]["exp"][0])
                   # print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表经验" + str(upgrade_google[i]["exp"][0]) + ":游戏中" + str(test_value.get("exp"))
                    print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表钻石" + str(upgrade_google[i]["diamond"][0]) + ":游戏中" + str(test_value.get("diamond"))
                    print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表金币" + str(upgrade_google[i]["cash"][0]) + ":游戏中" + str(test_value.get("cash"))

if __name__ == '__main__':
    main()
