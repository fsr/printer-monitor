#!/usr/local/bin/python3
import os
import json
import time
import logging
import urllib.request


basepath = os.path.dirname(os.path.abspath(__file__))
logstr = '{time}:{printerdata}  Result: {result}'
logging.basicConfig(filename=os.path.join(
    basepath, '../printerreport.log'), level=logging.INFO)


def publish(data):
    allinfo, url = data
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
