# Simple HTTP Server Example
# Control an LED and read a Button using a web browser

import time
import network
import socket
from machine import Pin
import time
import network
import socket
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import framebuf
from time import sleep
import dht
import threading
from neopixel import Neopixel
import random
import threading

numpix = 20
strip = Neopixel(numpix, 0, 28, "RGB")

red = (255, 0, 0)

red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

delay = 0.5
strip.brightness(32)
blank = (0,0,0)

led = machine.Pin("LED", machine.Pin.OUT)
ledState = 'LED State Unknown'


button = Pin(15, Pin.IN, Pin.PULL_UP)

ssid = 'BTHub6-P5GR'
password = 'Breed77!'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# replace the "html" variable with the following to create a more user-friendly control panel
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonRed { background-color: #D11D53; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style></head>
<body><center><h1>Control Panel</h1></center><br><br>
<form><center>
<center> <button class="buttonGreen" name="led" value="on" type="submit">LED ON</button>
<br><br>
<center> <button class="buttonRed" name="led" value="off" type="submit">LED OFF</button>
</form>
<br><br>
<br><br>
<p>%s<p></body></html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

# Listen for connections, serve client
while True:
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
        
        if led_on == 8:
                print("led on")
                led.value(1)
                led.toggle()
                strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
                strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
                strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
                strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
                strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
                strip.show()
                time.sleep(delay)
                strip.fill((0,0,0))
            
        if led_off == 8:
                print("led off")
                led.value(0)
                strip.show()
                time.sleep(delay)
                strip.fill((0,0,0))
        
        ledState = "LED is OFF" if led.value() == 0 else "LED is ON" # a compact if-else statement
        
        if button.value() == 1: # button not pressed
            print("button NOT pressed")
            buttonState = "Button is NOT pressed"
        else:
            print("button pressed")
            buttonState = "Button is pressed"
        
        # Create and send response
        stateis = ledState + " and " + buttonState
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')