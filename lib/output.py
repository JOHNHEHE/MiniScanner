# coding=utf-8
# 设置输出的样式

import sys
import time

HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
RED = '\033[31m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def console(plugins, domain, text):
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    timestamp = BLUE + '[' + timestamp + ']' + ENDC
    plugins = RED + plugins + ENDC
    text = GREEN + text + ENDC
    sys.stdout.write(timestamp + ' - ' + plugins + ' - ' + domain + '    ' + text)
