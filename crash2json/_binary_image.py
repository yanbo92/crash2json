# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

from collections import OrderedDict
import json
import os


class BinaryImage:
    def __init__(self, crash_file):
        """"初始化方法"""
        self.crash_file = crash_file
        self.crash_dict = OrderedDict()
        self.crash_dict = self.get_binary_images()

    def get_binary_images(self):
        # 子方法 获取对应的block
        def get_block():
            block_str = ""
            flag = False

            with open(self.crash_file) as f:
                lines = f.readlines()

            for line in lines:
                if flag and "EOF" in line:
                    # 停止存储堆栈
                    break

                if "Binary Images:" in line:
                    flag = True
                    continue

                if flag:
                    block_str = block_str + line

            return block_str.replace("\n\n", "")


        # 子方法 获取每一行中的地址、二进制文件、uuid以及路径
        def get_images_info(line):
            # 初始化
            binary_info_dict = {"addr_start": "", "addr_end": "", "binary_name": "", "architecture": "", "uuid": "",
                           "path": ""}

            strs = line.split(" ")
            binary_info_dict["addr_start"] = strs[0]
            binary_info_dict["addr_end"] = strs[2]

            for s in strs:
                if "<" in s and ">" in s:
                    binary_info_dict["uuid"] = s

            uuid_index = strs.index(binary_info_dict["uuid"])
            binary_info_dict["architecture"] = strs[uuid_index-2]

            binary_name_str = ""
            for i in range(3, uuid_index - 2):
                binary_name_str = binary_name_str + strs[i] + " "
            binary_info_dict["binary_name"] = binary_name_str

            path_str = ""
            for i in range(uuid_index + 1, strs.__len__()):
                path_str = path_str + strs[i] + " "
            binary_info_dict["path"] = path_str
            
            return binary_info_dict



        # 初始化
        binary_images_dict = {"binaryImages": []}
        block = get_block().split("\n")
        for line in block:
            binary_images_dict["binaryImages"].append(get_images_info(line))

        return binary_images_dict

    def toJson(self, filename=""):
        if filename:
            path = os.path.abspath(os.path.dirname(self.crash_file)).replace(self.crash_file, "")
            json_name = path + '/' + filename
        else:
            json_name = self.crash_file.replace(".crash", "").replace(".Crash", "").replace(".CRASH", "")
            json_name = json_name + "-binary_images_list"
        json_str = json.dumps(self.crash_dict)
        with open('{}.json'.format(json_name), 'w') as json_file:
            json_file.write(json_str)

