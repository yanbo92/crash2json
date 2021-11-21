# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

from _header import Header
from _exception_information import ExceptionInformation
from _diagnostic_message import DiagnosticMessage
from _exception_backtrace import ExceptionBacktrace
from _thread_0_backtrace import BacktraceForThread0
from _other_threads_backtrace import BacktraceForAllThreads
from _crashed_thread_state import CrashThreadState
from _binary_image import BinaryImage
from collections import OrderedDict
import os
import json


class Crash2Json:
    def __init__(self, crash_file):
        """"初始化方法"""
        self.crash_file = crash_file
        self.header = Header(crash_file)
        self.exception_information = ExceptionInformation(crash_file)
        self.diagnostic_message = DiagnosticMessage(crash_file)
        self.exception_backtrace = ExceptionBacktrace(crash_file)
        self.thread_0_backtrace = BacktraceForThread0(crash_file)
        self.other_threads_backtrace = BacktraceForAllThreads(crash_file)
        self.crashed_thread_state = CrashThreadState(crash_file)
        self.binary_image = BinaryImage(crash_file)

        self.crash_dict = OrderedDict()
        self.crash_dict = {
            "header": self.header.crash_dict,
            "exceptionInformation": self.exception_information.crash_dict,
            "diagnosticMessages": self.diagnostic_message.crash_dict,
            "exceptionBacktrace": self.exception_backtrace.crash_dict,
            "bacetraceFoThread0": self.thread_0_backtrace.crash_dict,
            "backtraceForOtherThreads": self.other_threads_backtrace.crash_dict,
            "crashThreadState": self.crashed_thread_state.crash_dict,
            "binaryImagesList": self.binary_image.crash_dict
        }

    def toJson(self, filename=""):
        if filename:
            path = os.path.abspath(os.path.dirname(self.crash_file)).replace(self.crash_file, "")
            json_name = path + '/' + filename
        else:
            json_name = self.crash_file.replace(".crash", "").replace(".Crash", "").replace(".CRASH", "")
        json_str = json.dumps(self.crash_dict)
        with open('{}.json'.format(json_name), 'w') as json_file:
            json_file.write(json_str)



