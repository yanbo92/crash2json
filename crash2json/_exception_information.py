# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

import json
import os
from collections import OrderedDict


class ExceptionInformation:
    def __init__(self, crash_file):
        """"初始化方法"""
        self.crash_file = crash_file
        self.crash_dict = OrderedDict()
        self.crash_dict = self.get_exception()

    def get_exception(self):
        """
        从.crash文件中获取异常信息：
            {

            "Termination Reason:": " Namespace SPRINGBOARD, Code 0x8badf00d",
            "Termination Description:": " SPRINGBOARD, <RBSTerminateContext| domain:10 code:0x8BADF00D explanation:scene-update watchdog transgression: application<com.insta360.oner>:39563 exhausted real (wall clock) time allowance of 10.00 seconds | ProcessVisibility: Foreground | ProcessState: Running | WatchdogEvent: scene-update | WatchdogVisibility: Foreground | WatchdogCPUStatistics: ( | "Elapsed total CPU time (seconds): 32.550 (user 32.550, system 0.000), 54% CPU", | "Elapsed application CPU time (seconds): 15.526, 26% CPU" | ) reportType:CrashLog maxTerminationResistance:Interactive>",
             "Triggered by Thread:": "  0"}


        :param filename: 崩溃文件名
        :return: 结果 exception字典
        """

        # 初始化
        exception_dict = {"Exception Type": "", "Exception Codes": "", "Exception Note": "", "Exception Subtype": "",
                          "VM Region Info": ""}

        # 字符串处理子方法
        def get_exception_value(string, exception_type):
            if exception_type in string:
                temp = string.replace(exception_type, "")
                temp = temp.replace("\n", "")
                return temp

        with open(self.crash_file) as f:
            lines = f.readlines()

        for line in lines:
            if not exception_dict["Exception Type"]:
                exception_dict["Exception Type"] = get_exception_value(line, "Exception Type:")

            if not exception_dict["Exception Codes"]:
                exception_dict["Exception Codes"] = get_exception_value(line, "Exception Codes:")

            if not exception_dict["Exception Note"]:
                exception_dict["Exception Note"] = get_exception_value(line, "Exception Note:")

            if not exception_dict["Exception Subtype"]:
                exception_dict["Exception Subtype"] = get_exception_value(line, "Exception Subtype:")

            if not exception_dict["VM Region Info"]:
                exception_dict["VM Region Info"] = get_exception_value(line, "VM Region Info:")

        return exception_dict

    def toJson(self, filename=""):
        if filename:
            path = os.path.abspath(os.path.dirname(self.crash_file)).replace(self.crash_file, "")
            json_name = path + "/" + filename
        else:
            json_name = self.crash_file.replace(".crash", "").replace(".Crash", "").replace(".CRASH", "")
            json_name = json_name + "-exception_information"
        json_str = json.dumps(self.crash_dict)
        with open("{}.json".format(json_name), "w") as json_file:
            json_file.write(json_str)

