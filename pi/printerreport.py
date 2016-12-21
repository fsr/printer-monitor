#!/usr/local/bin/python3
import time
import urllib.request


logstr = '{time}:{printerdata}  Result: {result}'


def publish(allinfo, url):
    allinfo["ts"] = int(time.time())
    try:
        r = urllib.request.urlopen(
            url,
            data=allinfo)
        print(logstr.format(
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            printerdata=allinfo, result=r.msg))
    except Exception as e:
        print(logstr.format(
            time=time.strftime("%Y-%m-%d %H:%M:%S"),
            printerdata=allinfo, result=e))


if __name__ == '__main__':
    print('Needs main script to run.')
