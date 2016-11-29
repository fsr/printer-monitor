#!/usr/local/bin/python3
import math
import Adafruit_GPIO as GPIO
import Adafruit_CharLCD as LCD


basepath = None
get_printerdata = None
lcdstatus = 1
printers = []
current_printer = 0
reset_counter = {}

# PIN CONFIG
bus = 1
address = 0x20

lcd_rs = 0
lcd_en = 1
lcd_d4 = 2
lcd_d5 = 3
lcd_d6 = 4
lcd_d7 = 5
lcd_backlight = 6
lcd_columns = 20
lcd_rows = 4

pin_changeprinter = 8
pin_reset = 9
pin_refresh = 10
pin_lcd = 14

mcp = GPIO.MCP230xx.MCP23017(address, busnum=bus)
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight, gpio=mcp,
                           initial_backlight=0)

# Button setup
mcp.setup(pin_changeprinter, GPIO.IN)
mcp.setup(pin_reset, GPIO.IN)
mcp.setup(pin_refresh, GPIO.IN)
mcp.setup(pin_lcd, GPIO.IN)
mcp.pullup(pin_changeprinter, 1)
mcp.pullup(pin_reset, 1)
mcp.pullup(pin_refresh, 1)
mcp.pullup(pin_lcd, 1)


def initalize_run(func, path):
    get_printerdata = func
    basepath = path
    tmp = get_printerdata()[0]
    for entry in tmp:
        reset_counter[entry] = tmp[entry]
        printers.append(entry)
    print(printercount, '\n', reset_counter, '\n', printers)


def switchlcd():
    global lcdstatus
    lcdstatus = (lcdstatus + 1) % 2
    lcd.enable_display(lcdstatus)
    lcd.set_backlight(lcdstatus)


def switchprinter():
    global current_printer
    current_printer = (current_printer + 1) % len(printers)
    refresh()


def refresh():
    _printer = printers[current_printer]
    current_counter = get_printerdata()[0]
    differece = current_counter[_printer]-reset_counter[_printer]
    lcd.clear()
    lcd.message("{printer}: {total}\n".format(_printer,
                                              current_counter[_printer]))
    lcd.message("{pages} - {price}".format(differece, calcprice(differece)))


def calcprice(pages):
    return math.ceil(pagecounter*2/5)*5


def reset():
    _printer = printers[current_printer]
    reset_counter[_printer] = get_printerdata()[0][_printer]
    refresh()


# TODO: Add trigger

# timing = 0
# while(True):
# 	timing+=1
# 	if(mcp.input(10)==0):
# 		refresh()
# 	if(mcp.input(9)==0):
# 		resetcounter()
# 	if(mcp.input(14)==0):
# 		switchlcd()
# 	if(mcp.input(8)==0):
# 		switchprinter()
# 	if(timing>300):
# 		timing=0
# 		refresh()
# 	time.sleep(0.2)
