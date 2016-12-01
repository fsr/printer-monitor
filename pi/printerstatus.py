#!/usr/local/bin/python3
import os
import sys
import json
import printerlcd
import printerreport
from subprocess import check_output
from threading import Timer

basepath = os.path.dirname(os.path.abspath(__file__))
printer = {}
url = ''


def main(publish=False):
    if publish:
        Timer(300, call_report).start()
    setup_data()
    call_lcd()


def call_report():
    printerreport.publish(allinfo=get_printerdata(), url=url)
    Timer(300, call_report).start()


def call_lcd():
    printerlcd.initialize_run(func=get_printerdata, snmp=printer)


def setup_data():
    global printer, url
    with open(os.path.join(basepath, 'printer.json'), 'r') as f:
        tmp = json.load(f)
        tmp_printer = tmp['printers']
        url = tmp["url"]
        for item in tmp_printer:
            printer[item] = 'snmpget -v2c -O vq -c public {ip} {snmp}'.format(ip=tmp_printer[item]['ip'],
                                                                              snmp=tmp_printer[item]['snmp']).split()


def get_printerdata():
    allinfo = {}
    for item in printer:
        allinfo[item] = int(check_output(printer[item]))
    return allinfo


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'publish':
            main(True)
        else:
            print('Unknows argument')
    else:
        main()
