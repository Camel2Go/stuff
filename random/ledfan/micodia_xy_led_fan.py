#!/usr/bin/env python3
# https://github.com/fergofrog/microwave_usb_fan

from usbfan import Colour, Column, Device, Message, Program, TextMessage, \
    MessageStyle, OpenTransition, CloseTransition

# We can cycle the rainbow here and fill all 144 columns
rainbow_colours = [Colour.red, Colour.yellow, Colour.green,
                   Colour.cyan, Colour.blue, Colour.magenta]
rainbow = [Column([True, True, True, True, True, True, True, True, True, True, True],
                  rainbow_colours[i % len(rainbow_colours)])
           for i in range(Message.MAX_COLUMNS)]
p = Program([Message(rainbow, MessageStyle.Remain, OpenTransition.All, CloseTransition.All) for _ in range(1, 28)])

# Open the device and program
d = Device()
d.program(p)