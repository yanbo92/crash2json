![publish to pypi](https://github.com/yanbo92/crash2json/actions/workflows/publish-to-test-pypi.yml/badge.svg)

# crash2json
将Apple Crash Report崩溃文件(.crash后缀)解析成json文件的python模块。

A python module to parse .crash file into .json file.

## 安装 Install
```
pip install crash2json
```

## 使用 Usage
```
crash2json yourcrashreport.crash
```

## 其他参数 Other Parameters
```
positional arguments:
  crash_file

optional arguments:
  -h, --help            show this help message and exit
  --binary_image_list_only
                        parse binary_image_list to json only
  --crashed_thread_state_only
                        parse crashed_thread_state to json only
  --diagnostic_messages_only
                        parse diagnostic_messages to json only
  --exception_backtrace_only
                        parse exception_backtrace to json only
  --exception_information_only
                        parse exception_information to json only
  --header_only         parse header to json only
  --other_threads_backtrace_only
                        parse other_threads_backtrace to json only
  --thread0_backtrace_only
                        parse thread0_backtrace to json only
  -s, --simple          output a simple json with only header, exceptionInfo, diagnositcMsg, Thread0Backtrace
  -o OUTPUT_NAME, --output_name OUTPUT_NAME
                        the .json file you want to save result to, no need .json suffix

```
