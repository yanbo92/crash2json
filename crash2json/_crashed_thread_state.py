# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

from collections import OrderedDict
import json
import os


class CrashThreadState:
    def __init__(self, crash_file):
        """"初始化方法"""
        self.crash_file = crash_file
        self.crash_dict = OrderedDict()
        self.crash_dict = self.get_crash_thread_state()

    def get_crash_thread_state(self):
        # 子方法 获取对应的block
        def get_block():
            block_str = ""
            flag = False

            with open(self.crash_file) as f:
                lines = f.readlines()

            for line in lines:
                if flag and "Binary Images:" in line:
                    # 停止存储堆栈
                    flag = False
                    break

                if "crashed with " in line:
                    flag = True
                    continue

                if flag:
                    block_str = block_str + line

            return block_str.replace("\n\n", "")

        # 初始化
        cst_dict = {"fault": "", "addrs": {}}

        block = get_block().split("\n")
        for line in block:
            if "fault" in line:
                strs = line.split("  ")
                cst_dict["fault"] = strs[-1]

        addr_list = []
        for line in block:
            strs = line.split("  ")
            for s in strs:
                if s:
                    if "cpsr" in s:
                        addr_list.append(s.split("cpsr")[0])
                        addr_list.append("cpsr: " + s.split("cpsr:")[1])

                    else:
                        addr_list.append(s)
        addr_list.pop()

        for addr in addr_list:
            cst_dict["addrs"][addr.split(":")[0].replace(" ", "")] = addr.split(":")[1].replace(" ", "")
        return cst_dict

    def toJson(self, filename=""):
        if filename:
            path = os.path.abspath(os.path.dirname(self.crash_file)).replace(self.crash_file, "")
            json_name = path + '/' + filename
        else:
            json_name = self.crash_file.replace(".crash", "").replace(".Crash", "").replace(".CRASH", "")
            json_name = json_name + "-crashed_thread_state"
        json_str = json.dumps(self.crash_dict)
        with open('{}.json'.format(json_name), 'w') as json_file:
            json_file.write(json_str)

