from __future__ import print_function

import serial_led
import random
import pygame as pg
import argparse
import draw

ports = serial_led.SerialLedController.port_list()

parser = argparse.ArgumentParser(
    description='Scan for explosives and guns! The station will be safe with your awesome scanning gear, officer.')
parser.add_argument('-p','--serial_port', required=False, help='serial port for LED controller')
parser.add_argument('-s','--speed', type=int, default=9600, required=False,
                    help='serial port speed')
parser.add_argument('-F','--fullscreen', action='store_true', default=False, required=False,
                    help='Run in fullscreen')
parser.add_argument('-f','--fps', type=int, default=30, required=False,help='Aim for FPS')
parser.add_argument('-a', '--alarm', default='alarm.wav', required=False, help='Alarm sound file')

args = parser.parse_args()

if args.serial_port is None:
    led  = serial_led.DummyLedController()
else:
    ports = serial_led.SerialLedController.port_list()
    if args.serial_port not in ports:
        print("{} is not a valid serial port. Valid serial ports are: {}".format(
            str(args.serial_port),
            ", ".join(ports)
        ))
        exit(1)
    led = serial_led.SerialLedController(args.serial_port, args.speed)


def scan_segments(mode=None):
    result = []
    n_segments = 10
    if mode == "CLEAR":
        return [True] * n_segments
    elif mode == "RED":
        return [False] * n_segments
    elif mode == "LAST":
        return [True] * (n_segments-1) + [False]
    elif mode == "BOTTOM":
        return [False] * 4 + [True] * (n_segments-4)
    elif mode == "TOP":
        return [True] * (n_segments-4) + [False] * 4
    elif mode == "MIDDLE":
        return [True] * 3 + [False] * 4 + [True] * 3
    elif mode == "FUNERAL":
        return [True, True, False, False, True, False, False, False, False, False]
    percent = 40
    if mode == "HIGH":
        percent = 80
    if mode == "LOW":
        percent = 20
    for i in range(n_segments):
        if random.randint(0,100) >= percent:
            result.append(True)
        else:
            result.append(False)
    return result


def color_for_segment(segment):
    return (255,0,0) if not segment else (0,255,0)


def frame_color_for_segment(segment):
    return (255,200,200) if not segment else (200,200,255)


def colors_for_segments(segments):
    return [color_for_segment(x) for x in segments]


def random_mode():
    return "0b" + "".join([str(random.randint(0,1)) for x in range(8)])

try:
    pg.init()
    pg.display.set_caption("Scanner")
    pg.mouse.set_visible(False)

    pg.mixer.music.load(args.alarm)

    if args.fullscreen:
        pg.display.set_mode((0, 0), pg.FULLSCREEN)
    else:
        pg.display.set_mode((800, 600))

    clock = pg.time.Clock()
    fps = 30.0

    screen = pg.display.get_surface()

    s = 1
    segments = scan_segments("CLEAR")
    running = False

    treshold = 3
    speed = 0.03

    speed_mappings = {
        ord('q'): 0.01,
        ord('w'): 0.02,
        ord('e'): 0.03,
        ord('r'): 0.04,
        ord('t'): 0.05,
    }

    mode_mappings = {
        ord('o'): 'NORMAL',
        ord('p'): 'HIGH',
        ord('i'): 'LOW',
        ord('u'): 'TOP',
        ord('j'): 'MIDDLE',
        ord('m'): 'BOTTOM',
        ord('['): 'FUNERAL',
    }

    mode_bits = {
        'NORMAL':'0b00111010',
        'HIGH':'0b11011111',
        'LOW':'0b00001000',
        'TOP':'0b10000000',
        'MIDDLE':'0b00110000',
        'BOTTOM':'0b00000001',
        'FUNERAL': '0b01010110',
    }

    mode = 'NORMAL'

    rm1 = random_mode()
    rm2 = random_mode()
    rm3 = random_mode()

    ticks = 0

    while True:
        set_leds = False

        if running:
            s += speed
            if s >= 1:
                s = 1
                running = False
                set_leds = True
            ticks += 1
            rm3 = random_mode()
            if ticks % 10 == 0:
                rm2 = random_mode()
            if ticks == 100:
                rm1 = random_mode()
                ticks = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                led.stop_all()
                exit()
            if (event.type == pg.KEYDOWN):
                if event.key == 291:
                    led.stop_all()
                    exit()
                if event.key == 32:
                    if not running:
                        running = True
                        s = 0
                        segments = scan_segments(mode)
                if event.key >= ord('0') and event.key <= ord('9'):
                    treshold = event.key - ord('0')
                    if not running:
                        set_leds = True
                if event.key in speed_mappings:
                    speed = speed_mappings[event.key]
                if event.key in mode_mappings:
                    mode = mode_mappings[event.key]


        active_segment = int(s*10)

        reds = len([x for x in segments[:active_segment] if not x])

        screen.fill((0, 0, 0))
        if running:
            draw.frame(screen, frame_color_for_segment(segments[active_segment]))
        else:
            if reds >= treshold:
                draw.frame(screen, (255, 0, 0))
            else:
                draw.frame(screen, (0,255,0))

        if running:
            if segments[active_segment]:
                led.set_mode(0b011)
            else:
                led.set_mode(0b101)
            draw.ray(screen, (255, 255, 255), s)

        draw.progress(screen, (255, 255, 255), colors_for_segments(segments), s)

        draw.reds(screen, reds, treshold)
        draw.tresh(screen, treshold)

        draw.mode(screen, ["0b00001011","0b01000110", mode_bits[mode], rm1, rm2, rm3 ])

        if set_leds:
            if reds >= treshold:
                led.set_mode(0b100)
                pg.mixer.music.play()
            else:
                led.set_mode(0b010)

        pg.display.flip()
        clock.tick(args.fps)

finally:
    led.stop_all()
