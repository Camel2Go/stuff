#!/usr/bin/env python3

import board
import neopixel
import time
import random

def run():
    print("Default speed: 0.1")
    print("Default runtime: 10")
    print("Default fadeval: 0.73")
    print("")
    speed = 0.1
    runtime = 10
    fadeval = 0.73
    menu()
    user = ""

    while user != "q":
        user = input(">> ").lower()
        try:
            user = int(user)
            if user == 1: setRGB()
            elif user == 2: circle(speed, runtime, fadeval)
            elif user == 3: randomRGB(speed, runtime, fadeval)
            elif user == 4: rainbow(speed, runtime)
            elif user == 5: flashing(speed, runtime)
            clear()
        except ValueError:
            if user == "c": clear()
            elif user == "s": speed = getValue("speed (sec): ")
            elif user == "t": runtime = getValue("runtime (sec): ")
            elif user == "m": menu()
            elif user == "f": fadeval = getFadeval("fadeval (decimal): ")
        except KeyboardInterrupt:
            print(" -> stopped...")
            clear()

def menu():
    print("[m] Print menu")
    print("========== Modes ==========")
    print("[1] Set RGB of pixel")
    print("[2] Circle")
    print("[3] Random")
    print("[4] Rainbow")
    print("[5] Flashing")
    print("======== Settings =========")
    print("[s] Set speed")
    print("[t] Set runtime")
    print("[f] Set fadeval")
    print("[c] Clear pixels")
    print("[q] Quit")

def getRGB():

    rgb = input("R,G,B: ").split(",")

    try:
        rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        for val in rgb:
            if val not in range(256):
                print(rgb,"not valid")
        return rgb

    except ValueError:
        print("Not a valid Number!")

def getValue(msg):
    try:
        val = float(input(msg))
        if val <= 0:
            print("Must be greater than zero!")
            return getValue(msg)
        return val
    except ValueError:
        print("Not a valid Number!")
        return getValue(msg)

def getFadeval(msg):
    try:
        val = float(input(msg))
        if val <= 0:
            print("Must be greater than zero!")
            return getFadeval(msg)
        elif val >= 1:
            print("Must be lower than one!")
            return getFadeval(msg)
        return val
    except ValueError:
        print("Not a valid Number!")
        return getFadeval(msg)

def fade(value):
    for index in range(8):
        rgb = pixels[index]
        for i in range(3):
            rgb[i] *= value
            if rgb[i]<5: rgb[i]=0
        pixels[index] = rgb


def setRGB():
    pixel = int(input("Pixel (1-8): "))-1
    rgb = getRGB()
    if pixel in range(7):
        pixels[pixel] = rgb

def circle(speed, runtime, fadeval):
    rgb = (random.randint(0,70), random.randint(0,70), random.randint(0,70))
    starttime = time.time()
    pixel = 0

    while starttime+runtime > time.time():
        fade(fadeval)
        pixels[pixel % 8] = rgb
        time.sleep(speed)
        pixel += 1

def randomRGB(speed, runtime, fadeval):
    starttime = time.time()
    while starttime+runtime > time.time():
        fade(fadeval)
        pixels[random.randint(0,7)] = (random.randint(0,70), random.randint(0,70), random.randint(0,70))
        time.sleep(speed)

def rainbow(speed, runtime):
    colors = [(127,0,127),(127,0,64),(127,55,0),(127,110,0),(100,127,0),(0,106,14),(1,47,113),(50,0,75)]
    position = 0
    starttime = time.time()
    while starttime+runtime > time.time():
        for i in range(8):
            pixels[i] = colors[(position + i) % 8]
        position += 1
        time.sleep(speed)

def flashing(speed, runtime):
    starttime = time.time()
    while starttime+runtime > time.time():
        rgb = (random.randint(0,70), random.randint(0,70), random.randint(0,70))
        for i in range(8):
            pixels[i] = rgb
        time.sleep(speed)
        clear()
        time.sleep(speed)

def clear():
    for index in range(len(pixels)):
        pixels[index] = (0, 0, 0)


if __name__ == '__main__':

    # connect IN to GPIO18 (Pin12)
    pixels = neopixel.NeoPixel(board.D18, 8)

    try:
        run()
        print("\nStopping...")
        clear()

    except KeyboardInterrupt:
        print("\nStopping...")
        clear()
