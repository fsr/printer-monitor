#!/usr/local/bin/python3
import errno
import os
import subprocess
import json
import urllib.request
import snmpy
import time
import logging

logstr = '{time}:{printerdata}  Result: {result}'
printer = {}
url = ''
logging.basicConfig(filename=os.path.join(
    basepath, '../printerreport.log'), level=logging.INFO)


def publish(allinfo, basepath):
    try:
        r = urllib.request.urlopen(
            url,
            data=json.dumps(allinfo).encode('utf8'))
        logging.info(logstr.format(
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            printerdata=allinfo, result="OK"))
    except Exception as e:
        logging.error(logstr.format(
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            printerdata=allinfo, result=e))


if __name__ == '__main__':
    print('Needs main script to run.')
