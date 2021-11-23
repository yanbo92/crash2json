# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

import json
import re
import os
from collections import OrderedDict

class BacktraceForAllThreads:
    def __init__(self, crash_file):
        """"初始化方法"""
        self.crash_file = crash_file
        self.crash_dict = OrderedDict()
        self.crash_dict = self.get_all_threads_info()

    def get_stack_frame_info(self, line):
        """
        转化成dict：
        {"index": "1", "binary": "TouchCanvas", "address": "0x0000000102afb3d0",
        "functionName": "CanvasView.updateEstimatedPropertiesForTouches(_:)", "byteOffset": "62416",
         "position": "(CanvasView.swift:231)"}

        :param line: 线程中的一行
        :return: 结果 execute_dict
        """
        # 初始化
        execute_dict = {"index": "", "binary": "", "address": "", "functionName": "", "byteOffset": "", "position": ""}
        strs = re.findall(r"\S+", line)

        # 堆栈序号
        execute_dict["index"] = strs[0]

        # 代码位置，有的话一定在最后，可能没有，所以判断一下内容格式
        if ":" in strs[-1] and ")" in strs[-1]:
            execute_dict["position"] = strs[-1]

        # 地址，特征明显
        for s in strs:
            if "0x" in s:
                execute_dict["address"] = s

        # 二进制文件，为了处理空格会导致字符串不完整，采用求差值拼接形式
        binary = ""
        index = strs.index(execute_dict["index"])
        address = strs.index(execute_dict["address"])
        for i in range(index + 1, address):
            binary = binary + strs[i]
        execute_dict["binary"] = binary

        # 函数名
        execute_dict["functionName"] = strs[address + 1]

        # 从函数的入口点到函数中的当前指令的字节偏移。 byteOffset
        if "+" in strs:
            plus = strs.index("+")
            execute_dict["byteOffset"] = strs[plus + 1]

        return execute_dict

    def get_threads_list(self):
        """
        从.crash文件中获取所有线程信息：
        返回线程列表，每一个元素是一个大字符串：
        Thread 9 name:  com.apple.NSURLConnectionLoader
        Thread 9:
        0   libsystem_kernel.dylib        	0x00000001be9d04fc mach_msg_trap + 8
        1   libsystem_kernel.dylib        	0x00000001be9cf884 mach_msg + 76
        2   CoreFoundation                	0x0000000190783e58 __CFRunLoopServiceMachPort + 372
        3   CoreFoundation                	0x000000019077dcf8 __CFRunLoopRun + 1212
        4   CoreFoundation                	0x000000019077d308 CFRunLoopRunSpecific + 600
        5   CFNetwork                     	0x000000019105bb38 0x190e10000 + 2407224
        6   Foundation                    	0x0000000191bde30c __NSThread__start__ + 864
        7   libsystem_pthread.dylib       	0x00000001dc478bfc _pthread_start + 320
        8   libsystem_pthread.dylib       	0x00000001dc481758 thread_start + 8
           :return:  所有线程的列表 threads list
        """

        crash_thread_str = ""
        crash_thread_flag = False
        with open(self.crash_file) as f:
            lines = f.readlines()

        for line in lines:
            if crash_thread_flag and "crashed with " in line:
                # 停止存储堆栈
                crash_thread_flag = False

            if "Thread 0 " in line and "Thread 0 crashed" not in line:
                crash_thread_flag = True


            if crash_thread_flag:
                crash_thread_str = crash_thread_str + line

        threads_list = crash_thread_str.split("\n\n")

        # 干掉最后一个空的
        threads_list.pop()

        # 干掉第一个回车
        threads_list[0] = threads_list[0][1:]

        return threads_list

    def get_thread_info(self, thread):

        # 初始化
        exception_dict = {"name": "", "stackFrames": []}

        # 线程内容分行
        thread_lines = thread.split("\n")

        for line in thread_lines:
            if "name:" in line:
                strs = line.split("name:")
                exception_dict["name"] = strs[1]
            else:
                if "0x" in line:
                    exception_dict["stackFrames"].append(self.get_stack_frame_info(line))

        return exception_dict

    def get_all_threads_info(self):
        """
        从.crash文件中获取崩溃线程信息：
        :return: 结果 dict
        """
        threads_list = self.get_threads_list()
        threads_info_dict = {"threads": []}
        for f in threads_list:
            threads_info_dict["threads"].append(self.get_thread_info(f))

        threads_info_dict["threads"].remove(threads_info_dict["threads"][0])
        return threads_info_dict

    def toJson(self, filename=""):
        if filename:
            path = os.path.abspath(os.path.dirname(self.crash_file)).replace(self.crash_file, "")
            json_name = path + "/" + filename
        else:
            json_name = self.crash_file.replace(".crash", "").replace(".Crash", "").replace(".CRASH", "")
            json_name = json_name + "-back_trace_for_other_threads"
        json_str = json.dumps(self.crash_dict)
        with open("{}.json".format(json_name), "w") as json_file:
            json_file.write(json_str)

