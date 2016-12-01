#!/usr/local/bin/python3
import json
import time
import urllib.request


logstr = '{time}:{printerdata}  Result: {result}'


def publish(allinfo, url):
    try:
        r = urllib.request.urlopen(
            url,
            data=json.dumps(allinfo).encode('utf8'))
        print(logstr.format(
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            printerdata=allinfo, result=r.msg))
    except Exception as e:
        print(logstr.format(
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            printerdata=allinfo, result=e))


if __name__ == '__main__':
    print('Needs main script to run.')
