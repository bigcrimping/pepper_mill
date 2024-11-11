from machine import Pin, Timer, I2C
import utime
import time
from ssd1306 import SSD1306_I2C
from rotary_irq_rp2 import RotaryIRQ
from hx711 import *
 
dir_pin = Pin(18, Pin.OUT)
step_pin = Pin(19, Pin.OUT)
en_pin = Pin(20, Pin.OUT)
hx = hx711(Pin(12), Pin(13))
i2c=I2C(1,sda=Pin(2), scl=Pin(3), freq=400000)
button = Pin(6, Pin.IN, Pin.PULL_UP)

r = RotaryIRQ(pin_num_clk=4, 
              pin_num_dt=5, 
              min_val=0, 
              max_val=2, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)


display = SSD1306_I2C(128, 64, i2c)
display.fill(0)

hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_10)

en_pin.value(1)
dir_pin.value(1)

display.text("PepperMill 1.0",0,0)
display.text("How much pepper?",0,17)
display.text("",0,27)
display.text("A little bit  <-",0,37)
display.text("Lots please",0,47)
display.text("All of it!!",0,57)
display.show()

def rotate(steps):
    en_pin.low()
    for i in range(steps):
        step_pin.high()
        utime.sleep_us(50)
        step_pin.low()
        utime.sleep_us(50)
    en_pin.high()
    
def update_display(val_new):

    if (val_new == 0):
        display.fill(0)
        display.text("PepperMill 1.0",0,0)
        display.text("How much pepper?",0,17)
        display.text("",0,27)
        display.text("A little bit  <-",0,37)
        display.text("Lots please",0,47)
        display.text("All of it!!",0,57)
        display.show()
    elif (val_new == 1):
        display.fill(0)
        display.text("PepperMill 1.0",0,0)
        display.text("How much pepper?",0,17)
        display.text("",0,27)
        display.text("A little bit",0,37)
        display.text("Lots please   <-",0,47)
        display.text("All of it!!",0,57)
        display.show()
    elif (val_new == 2):
        display.fill(0)
        display.text("PepperMill 1.0",0,0)
        display.text("How much pepper?",0,17)
        display.text("",0,27)
        display.text("A little bit",0,37)
        display.text("Lots please",0,47)
        display.text("All of it!!   <-",0,57)
        display.show()
        
def pepper_dispense(val_new):

    if (val_new == 0):
        rotate(10000)
    elif (val_new == 1):
        rotate(20000)
    elif (val_new == 2):
        rotate(60000)


def loop():
    
    val_old = r.value()
    debounce_time=10
    
    while True:
    
        val_new = r.value()
    
        if val_old != val_new:
            val_old = val_new
            update_display(val_new)
            
        if ((button.value() is 0) and (time.ticks_ms()-debounce_time) > 300):
            
            r._disable_clk_irq()
            r._disable_dt_irq()
            debounce_time=time.ticks_ms()
            #print("Button Pressed")
            #pepper_dispense(val_new)
            r._enable_clk_irq()
            r._enable_dt_irq()
    
if __name__ == '__main__':
    loop()