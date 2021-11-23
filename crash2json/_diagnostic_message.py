# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

from collections import OrderedDict
import json
import os


class DiagnosticMessage:
    def __init__(self, crash_file):
        """"初始化方法"""
        self.crash_file = crash_file
        self.crash_dict = OrderedDict()
        self.crash_dict = self.get_diagnostic_msg()

    def get_diagnostic_msg(self):
        """
        从.crash文件中获取诊断信息：
            {
            "Termination Reason:": " Namespace SPRINGBOARD, Code 0x8badf00d",
            "Termination Description:": " SPRINGBOARD, <RBSTerminateContext| domain:10 code:0x8BADF00D explanation:scene-update watchdog transgression: application<com.insta360.oner>:39563 exhausted real (wall clock) time allowance of 10.00 seconds | ProcessVisibility: Foreground | ProcessState: Running | WatchdogEvent: scene-update | WatchdogVisibility: Foreground | WatchdogCPUStatistics: ( | "Elapsed total CPU time (seconds): 32.550 (user 32.550, system 0.000), 54% CPU", | "Elapsed application CPU time (seconds): 15.526, 26% CPU" | ) reportType:CrashLog maxTerminationResistance:Interactive>",
             "Triggered by Thread:": "  0"}


        :param filename: 崩溃文件名
        :return: 结果 exception字典
        """

        # 初始化
        diagnostic_msg_dict = {"Termination Reason": {"NameSpace": "", "Code": ""},  "Termination Description": {},
                               "Termination Signal": "", "Terminating Process": "", "Triggered by Thread": ""}

        # 字符串处理子方法
        def get_diagnostic_value(string, exception_type):
            if exception_type in string:
                temp = string.replace(exception_type, "")
                temp = temp.replace("\n", "")
                return temp

        def get_termination_description(lines):
            # 初始化
            termination_description_dict = {"process": "",
                                            "RBSTerminateContext": {
                                                "domain": "",
                                                "ProcessVisibility": "",
                                                "ProcessState": "",
                                                "WatchdogEvent": "",
                                                "WatchdogVisibility": "",
                                                "WatchdogCPUStatistics": {
                                                    "Elapsed total CPU time (seconds)": "",
                                                    "Elapsed application CPU time (seconds)": ""
                                                },
                                                "reportType": ""
                                            }}

            termination_description_split1 = lines.split("|")
            for strs in termination_description_split1:
                if "Termination Description:" in strs:
                    termination_description_dict["process"] = strs.split(":")[1].split(",")[0]
                if "domain:" in strs:
                    termination_description_dict["RBSTerminateContext"]["domain"] = strs.split(":")[-1]
                if "ProcessVisibility:" in strs:
                    termination_description_dict["RBSTerminateContext"]["ProcessVisibility"] = strs.split(":")[-1]
                if "ProcessState:" in strs:
                    termination_description_dict["RBSTerminateContext"]["ProcessState"] = strs.split(":")[-1]
                if "WatchdogEvent:" in strs:
                    termination_description_dict["RBSTerminateContext"]["WatchdogEvent"] = strs.split(":")[-1]
                if "WatchdogVisibility:" in strs:
                    termination_description_dict["RBSTerminateContext"]["WatchdogVisibility"] = strs.split(":")[-1]
                if "reportType:" in strs:
                    strs_list = strs.split(":")
                    termination_description_dict["RBSTerminateContext"]["reportType"] = strs_list[1] + strs[2].replace(
                        ">", "")
                if "Elapsed total CPU time (seconds):" in strs:
                    termination_description_dict["RBSTerminateContext"]["WatchdogCPUStatistics"][
                        "Elapsed total CPU time (seconds)"] = strs.split(":")[1]
                if "Elapsed application CPU time (seconds):" in strs:
                    termination_description_dict["RBSTerminateContext"]["WatchdogCPUStatistics"][
                        "Elapsed application CPU time (seconds)"] = strs.split(":")[1]

            return termination_description_dict

        with open(self.crash_file) as f:
            lines = f.readlines()

        for line in lines:

            if not diagnostic_msg_dict["Termination Reason"]["NameSpace"]:
                terminate_reason = get_diagnostic_value(line, "Termination Reason:")
                if terminate_reason:
                    terminate_reason = str(terminate_reason)
                    name_space = terminate_reason.split(",")[0].split(" ")[2]
                    diagnostic_msg_dict["Termination Reason"]["NameSpace"] = name_space

            if not diagnostic_msg_dict["Termination Reason"]["Code"]:
                terminate_reason = get_diagnostic_value(line, "Termination Reason:")
                if terminate_reason:
                    terminate_reason = str(terminate_reason)
                    code = terminate_reason.split(",")[1].split(" ")[2]
                    diagnostic_msg_dict["Termination Reason"]["Code"] = code

            if not diagnostic_msg_dict["Termination Description"]:
                if "Termination Description:" in line:
                    diagnostic_msg_dict["Termination Description"] = get_termination_description(line)

            if not diagnostic_msg_dict["Termination Signal"]:
                diagnostic_msg_dict["Termination Signal"] = get_diagnostic_value(line, "Termination Signal:")

            if not diagnostic_msg_dict["Terminating Process"]:
                diagnostic_msg_dict["Terminating Process"] = get_diagnostic_value(line, "Terminating Process:")

            if not diagnostic_msg_dict["Triggered by Thread"]:
                diagnostic_msg_dict["Triggered by Thread"] = get_diagnostic_value(line, "Triggered by Thread:")

        return diagnostic_msg_dict

    def toJson(self, filename=""):
        if filename:
            path = os.path.abspath(os.path.dirname(self.crash_file)).replace(self.crash_file, "")
            json_name = path + "/" + filename
        else:
            json_name = self.crash_file.replace(".crash", "").replace(".Crash", "").replace(".CRASH", "")
            json_name = json_name + "-diagnostic_messages"
        json_str = json.dumps(self.crash_dict)
        with open("{}.json".format(json_name), "w") as json_file:
            json_file.write(json_str)


