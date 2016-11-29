#!/usr/local/bin/python3
import Adafruit_GPIO as GPIO
import Adafruit_CharLCD as LCD

basepath = None
get_printerdata = None

PIN CONFIG
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
    print(get_printerdata())


# TODO: Rewrite old code from below

# def readcounter():
# 	try:
# 		counts = subprocess.check_output(commands[printer], shell=True).split()
# 	except:
# 		return 0
# 	return int(counts[0])
#
# def resetcounter():
# 	global counter, previous
# 	counter[printer] = 0
# 	previous[printer] = readcounter()
# 	refresh()
#
# def calcprice(pages):
# 	if(pages==0):
# 		return 0
# 	return int((math.ceil((pages*2)/5.0)))*5
#
# def refresh():
# 	global counter
# 	total = readcounter()
# 	counter[printer] = total-previous[printer]
# 	lcd.clear()
# 	lcd.message("{1:s}: {0:d}".format(total, printers[printer]))
# 	lcd.message("\n")
# 	lcd.message("{0:d} S - {1:d} ct".format(counter[printer], calcprice(counter[printer])))
#
# def speak():
# 	speakcmd = 'espeak -vde+f3 "Du hast {} Seiten auf dem {} gedruckt, das kostet {} Cent." 2>/dev/null'.format(counter[printer], printers[printer], calcprice(counter[printer]))
# 	subprocess.call(speakcmd, shell=True)
#
# def switchlcd():
# 	global lcdstatus
# 	if(lcdstatus==1):
# 		lcdstatus=0
# 		lcd.enable_display(lcdstatus)
# 	else:
# 		lcdstatus=1
# 		lcd.enable_display(lcdstatus)
# 	lcd.set_backlight((lcdstatus+1)%2)
# 	refresh()
#
# def switchprinter():
# 	global printer
# 	printer = (printer+1)%len(printers)
# 	refresh()
#
# for p in range(len(printers)):
# 	printer = p
# 	resetcounter()
#
# timing = 0
# while(True):
# 	timing+=1
# 	mcp.setup(10, GPIO.IN)
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
