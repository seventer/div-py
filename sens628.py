#!/usr/bin/python3

import serial, time
import urllib.request

base_url = "http://192.168.14.24:8080/json.htm?type=command&param=udevice&idx=40&nvalue=0&svalue="

ser = serial.Serial()
ser.port = "/dev/ttyS0"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 2

while 1:
    try:
        ser.open()
    except Exception as e:
        print ("error open serial port: " + e)
        exit()

    if ser.isOpen():
        #print (ser.port + " opened.")
        try:
            ser.flushInput()
            ser.flushOutput()
            ser.write(("#00\n\r").encode())
            time.sleep(0.5)
            response = ser.readline().decode()
            domo_url = base_url + response[1:]
            domo_ret = urllib.request.urlopen(domo_url)
            html = domo_ret.read()
            print(html)
            ser.close()
        except Exception as e1:
            print ("error communicating...: " , e1)

    else:
        print ("cannot open serial port ")

    time.sleep(60)
