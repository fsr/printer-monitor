#!/usr/local/bin/python3
import os
import sys
import json
import time
import snmpy
import printerlcd
import printerreport
import urllib.request
from threading import Timer

basepath = os.path.dirname(os.path.abspath(__file__))


def main(publish=False):
    if publish:
        Timer(300, call_report).start()
    call_lcd()


def call_report():
    printerreport.publish(get_printerdata())
    Timer(300, call_report).start()


def call_lcd():
    printerlcd.initalize_run(get_printerdata, basepath)


def get_printerdata():
    printer = {}
    url = ''
    with open(os.path.join(basepath, 'printer.json'), 'r') as file:
        tmp = json.load(file)
        tmp_printer = tmp['printers']
        url = tmp["url"]
        for item in tmp_printer:
            printer[item] = {'printer': snmpy.Snmpy(tmp_printer[item]['ip'],
                                                    'public', ''),
                             'snmp': tmp_printer[item]['snmp']}
    allinfo = {}
    for item in printer:
        allinfo[item] = int(printer[item]['printer']
                            .get(printer[item]['snmp']))
    return allinfo, url


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'publish':
            main(True)
        else:
            print('Unknows argument')
    else:
        main()
