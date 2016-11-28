#!/usr/local/bin/python3
import errno
import os
import subprocess
import json
import urllib.request
import snmpy

printer = {}
url = ''


def main():
    with open('printer.json') as file:
        tmp = json.load(file)
        tmp_printer = tmp['printers']
        url = tmp["url"]
        for item in tmp_printer:
            printer[item] = {'printer': snmpy.Snmpy(tmp_printer[item]['ip'],
                                                    'public',
                                                    ''),
                             'snmp': tmp_printer[item]['snmp']}

    allinfo = {}

    for item in printer:
        allinfo[item] = int(
            printer[item]['printer'].get(printer[item]['snmp']))

    print(allinfo, url)

    # r = urllib.request.urlopen(
    #     'URL',
    #     data=json.dumps(allinfo).encode('utf8'))
    # print(r.msg)


if __name__ == '__main__':
    main()
