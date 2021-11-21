# -*- coding: utf-8 -*-
# @Time    : 20211119 23:09
# @Author  : yanbo92

import argparse
import sys
import os

sys.path.append(os.path.dirname(__file__))
from crash2json._crash2json import Crash2Json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("crash_file")

    parser.add_argument("--binary_image_list_only", help="parse binary_image_list to json only", action="store_true")
    parser.add_argument("--crashed_thread_state_only", help="parse crashed_thread_state to json only",
                        action="store_true")
    parser.add_argument("--diagnostic_messages_only", help="parse diagnostic_messages to json only",
                        action="store_true")
    parser.add_argument("--exception_backtrace_only", help="parse exception_backtrace to json only",
                        action="store_true")
    parser.add_argument("--exception_information_only", help="parse exception_information to json only",
                        action="store_true")
    parser.add_argument("--header_only", help="parse header to json only", action="store_true")
    parser.add_argument("--other_threads_backtrace_only", help="parse other_threads_backtrace to json only",
                        action="store_true")
    parser.add_argument("--thread0_backtrace_only", help="parse thread0_backtrace to json only", action="store_true")

    parser.add_argument("-s", "--simple", help="output a simple json with only header, exceptionInfo, diagnositcMsg,"
                                               " Thread0Backtrace", action="store_true")
    parser.add_argument("-o", "--output_name", type=str, help="the .json file you want to save result to, "
                                                              "no need .json suffix", default="")
    args = parser.parse_args()

    # print("Parameters list:")
    # for arg in vars(args):
    #     print(arg, getattr(args, arg))

    crash_file = args.crash_file
    output_name = args.output_name

    if args.binary_image_list_only:
        Crash2Json(crash_file).binary_image.toJson(output_name)
        exit(0)

    if args.crashed_thread_state_only:
        Crash2Json(crash_file).crashed_thread_state.toJson(output_name)
        exit(0)

    if args.diagnostic_messages_only:
        Crash2Json(crash_file).diagnostic_message.toJson(output_name)
        exit(0)

    if args.exception_backtrace_only:
        Crash2Json(crash_file).exception_backtrace.toJson(output_name)
        exit(0)

    if args.exception_information_only:
        Crash2Json(crash_file).exception_information.toJson(output_name)
        exit(0)

    if args.header_only:
        Crash2Json(crash_file).header.toJson(output_name)
        exit(0)

    if args.other_threads_backtrace_only:
        Crash2Json(crash_file).other_threads_backtrace.toJson(output_name)
        exit(0)

    if args.thread0_backtrace_only:
        Crash2Json(crash_file).thread_0_backtrace.toJson(output_name)
        exit(0)

    if args.simple:
        Crash2Json(crash_file).toSimpleJson(output_name)
        exit(0)
    Crash2Json(crash_file).toJson(output_name)


if __name__ == '__main__':
    main()
