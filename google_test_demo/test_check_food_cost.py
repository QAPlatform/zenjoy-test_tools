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
slot2 = {
    "slot2map4": {
        "spreadsheet_id": "16i_V-NmIhIqxFyD8HgeNucV70DYoE3iqjyD3fpqNXkI",
        "for_range": "90",
        "append_range": "93"
    },
    "slot2map3": {
        "spreadsheet_id": "1_zKvv9zotGnuJj0KscltwqaM_lUU_987ihbFlN8oevo",
        "for_range": "87",
        "append_range": "90"
    },
    "slot2map2": {
        "spreadsheet_id": "16HsFF7iy6w88lUSIUesHes6MYZYEnq4Wy7J-L8z3qTo",
        "for_range": "78",
        "append_range": "81"
    },
    "slot2map1": {
        "spreadsheet_id": "1JzGhU8JBgBx47IZ7DXPhb4sUZnly1t-OSqGQCNmna9E",
        "for_range": "80",
        "append_range": "83"
    }
}

slot4 = {
    "slot4map5": {
        "spreadsheet_id": "1WTFPc0QZmYjs-wmOwBrkWL2dnJxlzBq5xi4iXJo3JM8",
        "for_range": "82",
        "append_range": "85"
    }
}

slot5 = {
    "slot5map1": {
        "spreadsheet_id": "1ntiReFa7JM2iytT0ZBDMtV5zhzmar-c4bGx4QH3UQHo",#改这个，对应map的表
        "for_range": "42",#upgrade表行数-3
        "append_range": "45"#upgrade表行数
    }
}
# dict_value = {"id": "1", "level": "1", "cash": "1", "diamond": "1", "exp": "1"}


def check_upgrade():
    global slot5

    dict_value = {}
    spreadsheet_id = slot5["slot5map1"]["spreadsheet_id"]
    for_range = int(slot5["slot5map1"]["for_range"])
    append_range = slot5["slot5map1"]["append_range"]

    for i in range(1, for_range):
        dict_value[i] = {}

    range_names = []
    range_names.append("upgrade!B4:B" + str(append_range))  # map1 83
    range_names.append("upgrade!c4:c" + str(append_range))  # map4 93
    range_names.append("upgrade!i4:I" + str(append_range))  # map2 81
    range_names.append("upgrade!j4:j" + str(append_range))  # map3 90
    range_names.append("upgrade!A4:A" + str(append_range))  #
    # range_names.append("upgrade!m4:m48")  # 经验
    service = google_get_credentials.get_service()
    re = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_names).execute()
    result = re.get('valueRanges', [])

    for i in range(1, for_range):
        row_value = []
        for line in result:
            value = line.get('values', [])
            # print value, len(value)
            row_value.append(value[i])
        dict_value[i]["id"] = row_value[0]
        dict_value[i]["level"] = row_value[1]
        dict_value[i]["cash"] = row_value[2]
        dict_value[i]["diamond"] = row_value[3]
        dict_value[i]["name"] = row_value[4]
        # dict_value[i]["exp"] = row_value[4]

    return dict_value


def read_test_file():
    test_info = []
    f = open("slot5map1.log")#全部升级一遍后取出log放到该文件目录下
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
    # print upgrade_google
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
                    print str(upgrade_google[i]["name"][0]) + "ok"
                else:
                    # print "数值表中id:" + str(upgrade_google[i]["id"][0]) + ",level:" + str(test_value.get("level")) + "的经验为" + str(upgrade_google[i]["exp"][0])
                   # print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表经验" + str(upgrade_google[i]["exp"][0]) + ":游戏中" + str(test_value.get("exp"))
                    print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表钻石" + str(upgrade_google[i]["diamond"][0]) + ":游戏中" + str(test_value.get("diamond"))
                    print "id为" + str(test_value.get("id")) + "等级为" + str(test_value.get("level")) + "的表金币" + str(upgrade_google[i]["cash"][0]) + ":游戏中" + str(test_value.get("cash"))

if __name__ == '__main__':
    main()
