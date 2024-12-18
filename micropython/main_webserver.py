from machine import Pin, Timer, I2C
import utime
import time
from ssd1306 import SSD1306_I2C
from rotary_irq_rp2 import RotaryIRQ
from hx711 import *
import network
import socket

# Pins and Components Initialization
dir_pin = Pin(18, Pin.OUT)
step_pin = Pin(19, Pin.OUT)
en_pin = Pin(20, Pin.OUT)
hx = hx711(Pin(12), Pin(13))
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
button = Pin(6, Pin.IN, Pin.PULL_UP)
count2mg = 18
little_val = 40000
lots_val = 80000
all_val = 240000

display = SSD1306_I2C(128, 64, i2c)

hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_10)

en_pin.value(1)
dir_pin.value(1)

print("Started")

# Rotate Function (Motor Control)
def rotate(steps):
    en_pin.low()
    for i in range(steps):
        step_pin.high()
        utime.sleep_us(70)
        step_pin.low()
        utime.sleep_us(70)
    en_pin.high()

# Display Milligrams
def display_mg(mg):
    mg = str(mg)
    display.fill(0)
    display.text("", 0, 0)
    display.text("", 0, 17)
    display.text("   Dispensed", 0, 27)
    display.text("   " + mg + " mg", 0, 37)
    display.text("", 0, 47)
    display.text("", 0, 57)
    display.show()
    utime.sleep(4)

# Update Display Function
def update_display(ip):
    display.fill(0)
    display.text("PepperMill 1.2", 0, 0)
    display.text("IP Address:", 0, 20)
    display.text(ip, 0, 40)
    display.show()

# Read Weight
def read_weight(readings):
    total = 0
    for i in range(readings):
        total += hx.get_value()
        utime.sleep_us(5000)
    return total / readings

# Dispense Pepper
def pepper_dispense(val_new):
    
    if val_new == 0:
        rotate(little_val)
    elif val_new == 1:
        rotate(lots_val)
    elif val_new == 2:
        rotate(all_val)

    

# Wi-Fi Setup
def setup_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print("Connected to Wi-Fi")
    print(f"IP address: {wlan.ifconfig()[0]}")
    return wlan.ifconfig()[0]

# Generate HTML
def generate_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pepper Dispenser</title>
    </head>
    <body>
        <h1>PepperMill 1.0</h1>
        <p>Select how much pepper you want:</p>
        <form action="/dispense" method="get">
            <button name="amount" value="0">A little bit</button><br><br>
            <button name="amount" value="1">Lots please</button><br><br>
            <button name="amount" value="2">All of it</button>
        </form>
    </body>
    </html>
    """

# Start Web Server
def start_webserver():
    ip = setup_wifi("SSID", "password")  # Replace with your Wi-Fi credentials
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print(f"Listening on {ip}:80")
    ip_disp = str(ip)
    update_display(ip_disp)
    
    while True:
        cl, addr = s.accept()
        print(f"Connection from {addr}")
        request = cl.recv(1024).decode()
        print("Request:")
        print(request)
        
        if "/dispense?amount=" in request:
            try:
                amount = int(request.split("amount=")[1].split(" ")[0])
                if 0 <= amount <= 2:
                    pepper_dispense(amount)
                    response = "Dispensing... Please wait!"
                else:
                    response = "Invalid selection!"
            except Exception as e:
                response = f"Error: {e}"
        else:
            response = generate_html()
        
        cl.send("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()

# Main Function
if __name__ == '__main__':
    start_webserver()

