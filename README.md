# PepperMill

A Raspberry Pi pico project built on Micropython to mill, dispense and weigh pepper

![pepper](https://github.com/user-attachments/assets/c2a5d115-3f15-4f5c-9b1b-34eb589b6913)

A short video of in in action

https://github.com/user-attachments/assets/c9c53ded-4c93-4834-9c5d-54ee37c73243


## Project Code

The code is here: [https://github.com/bigcrimping/lightning_popper/tree/main/lightning_code](https://github.com/bigcrimping/pepper_mill/tree/main/micropython)

I have added in libraries from the following:

https://github.com/endail/hx711-pico-c <-- scales interface

https://github.com/miketeachman/micropython-rotary/tree/master <-- rotary controller

https://github.com/stlehmann/micropython-ssd1306/tree/master <-- for the display

## Wiring

The base contains:
1) Raspberry Pi Pico W
2) A HX711 based scales interface
3) USB C decoy (12V) and step down converter (12V to 5V to power the pico)
4) "L298N DC Motor Driver MX1508 Mini Dual Channel 1.5A"
5) SSD1306 I2C display
6) Digital rotary encoder

Wiring is as below:


![Wiring](https://github.com/user-attachments/assets/6ebd9db8-6699-4514-912d-9047a004d1da)

![image](https://github.com/user-attachments/assets/00cb2592-b35a-4b3e-8a65-4214e0ec6f15)


## Mechanical Files

Mechanical files here: https://github.com/bigcrimping/pepper_mill/tree/main/mech (3mf format)

The design comprises of the following parts:

![mech_parts](https://github.com/user-attachments/assets/87ea9545-0024-499d-aadf-d75d9e7d9839)

The grinder is a handheld part available online multiple places.
