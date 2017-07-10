#-*- encoding:utf-8 -*-
from __future__ import print_function
import sys
sys.path.append("../")
from datetime import date, datetime
import json
import google_get_credentials
import os

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

reload(sys)
sys.setdefaultencoding("utf-8")

# https://docs.google.com/spreadsheets/d/16zNo9Sp9c8kYu4UQLtxKhdxJqIwFMYI27n7Z4sesxew/edit#gid=1182478001


def get_food_name_map():
    spreadsheetId = "16zNo9Sp9c8kYu4UQLtxKhdxJqIwFMYI27n7Z4sesxew"  # google后缀设计4
    rangeName = "食物!B3:B47"
    food_result = []
    try:
        service = google_get_credentials.get_service()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        food_name_map4 = result.get('values', [])
        for values in food_name_map4:
            food_result.append(values[0])
        print (food_result)
        return food_result

    except Exception, e:
        raise e


if __name__ == '__main__':
    get_food_name_map()
