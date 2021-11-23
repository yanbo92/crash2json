# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

import os
import json
from collections import OrderedDict

class Header:
    def __init__(self, crash_file):
        """"初始化方法"""
        self.crash_file = crash_file
        self.crash_dict = OrderedDict
        self.crash_dict = self.get_header()

    def get_header(self):
        """
        从.crash文件中获取Header信息：
        :return: 结果 header字典
        """

        # 获取 environments 子方法
        def get_environments():
            """
                从.crash文件中获取前几行的环境信息：
                {"app_name": "Insta360 ONE R", "timestamp": "2021-11-17 00:07:08.00 +0800", "app_version": "1.8.0",
                "slice_uuid": "417c4896-4e9d-3900-ab19-2381998c46a2", "adam_id": 0, "build_version": "869", "platform": 2,
                 "bundleID": "com.insta360.oner", "share_with_app_devs": 0, "is_first_party": 0, "bug_type": "109",
                 "os_version": "iPhone OS 14.7.1 (18G82)", "incident_id": "78F1FF4F-E74A-4294-B2E8-564824ED593B",
                  "name": "Insta360 ONE R"}

               :param filename: 崩溃文件名
               :return: 结果 environment字典
            """
            with open(self.crash_file) as f:
                lines = f.readlines()

            environment_string = ""
            for line in lines:
                if "}" in line:
                    environment_string = environment_string + line
                    break
                else:
                    environment_string = environment_string + line

            environments_dict = json.loads(environment_string)
            return environments_dict

        def get_header_value(line):
            return line.split(":")[1].replace("\n", "").replace("     ", "").replace("    ", "").replace("   ", "")

        # 初始化
        header_dict = {"environments": get_environments(), "Incident Identifier": "", "CrashReporter Key": "",
                       "Hardware Model": "", "Process": "", "Path": "", "Identifier": "", "Version": "",
                       "Code Type": "", "Role": "", "Parent Process": "", "Coalition": "", "Date/Time": "",
                       "Launch Time": "", "OS Version": "", "Release Type": "", "Baseband Version": "",
                       "Report Version": ""}

        with open(self.crash_file) as f:
            lines = f.readlines()

        for line in lines:
            if "Exception Type" in line:
                break
            for name in header_dict.keys():
                if not name == "environments":
                    if name in line:
                        header_dict[name] = get_header_value(line)

        return header_dict

    def toJson(self, filename=""):
        if filename:
            path = os.path.abspath(os.path.dirname(self.crash_file)).replace(self.crash_file, "")
            json_name = path + "/" + filename
        else:
            json_name = self.crash_file.replace(".crash", "").replace(".Crash", "").replace(".CRASH", "")
            json_name = json_name + "-header"
        json_str = json.dumps(self.crash_dict)
        with open("{}.json".format(json_name), "w") as json_file:
            json_file.write(json_str)

