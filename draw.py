from __future__ import print_function
import pygame as pg
import random
import os


font = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'digital-7_(mono).ttf')

digits_font = None
tresh_font = None
mode_font = None


def frame(screen, color):
    w,h = screen.get_size()

    median_width = w//2
    frame_width = w//6

    frame_bottom = h//6*5
    frame_top = h//6

    frame_thickness = 1 if w//24 <= 0 else w//24

    pg.draw.polygon(
        screen,
        color,
        [
            (median_width - frame_width, frame_bottom),
            (median_width - frame_width, frame_top),
            (median_width + frame_width, frame_top),
            (median_width + frame_width, frame_bottom),
            (median_width + frame_width - frame_thickness, frame_bottom),
            (median_width + frame_width - frame_thickness, frame_top + frame_thickness),
            (median_width - frame_width + frame_thickness, frame_top + frame_thickness),
            (median_width - frame_width + frame_thickness, frame_bottom),
        ]
    )


def ray(screen, color, height):
    w,h = screen.get_size()

    segments = 12

    median_width = w//2
    ray_width = w//4
    segment_width = w//2//segments

    frame_top = h//6

    ray_height = (h//6*4)

    ray_thickness = 1 if w//128 <= 0 else w//128

    points = []

    points.append((median_width - ray_width, frame_top + int(ray_height*height)))

    for i in range(1,segments):
        points.append((median_width - ray_width + segment_width*i,
                       frame_top + int(
                           ray_height*(height+float(random.randint(-10,10))/700*(segments//2-abs(segments//2-i)))
                       )))

    points.append((median_width + ray_width, frame_top + int(ray_height*height)))

    pg.draw.lines(screen, color, False, points, ray_thickness)


def progress(screen, color, fillcolors, progress):
    w,h = screen.get_size()

    median_width = w//8
    bar_width = w//12

    bar_bottom = h//8*7
    bar_top = h//8

    bar_segments = 10

    bar_segment_height = h//8*6//bar_segments
    bar_segment_spacing = h//8*6//bar_segments*9/10

    for s in range(bar_segments):
        points = [
                (median_width - bar_width, bar_bottom - s * bar_segment_height ),
                (median_width - bar_width, bar_bottom - s * bar_segment_height - bar_segment_spacing),
                (median_width + bar_width, bar_bottom - s * bar_segment_height - bar_segment_spacing),
                (median_width + bar_width, bar_bottom - s * bar_segment_height),
            ]
        if s+1 <= (progress+0.05) * 10:
            #filled
            pg.draw.polygon(screen, fillcolors[s], points)
        pg.draw.lines(screen, color, True, points, 1)


def reds(screen, reds, treshold):
    global digits_font
    w, h = screen.get_size()
    if digits_font is None:
        digits_font = pg.font.Font(font, 72)
    label = digits_font.render("{}".format(reds), True, (0,255,0) if reds < treshold else (255,0,0))
    m = digits_font.render("0", True, (0, 0, 0))
    tw, th = m.get_size()
    screen.blit(label, (w*5//6-tw//2, h//6-th//2))


def tresh(screen, treshold):
    global tresh_font
    w, h = screen.get_size()
    if tresh_font is None:
        tresh_font = pg.font.Font(font, 72)
    label = tresh_font.render("{}".format(treshold), True, (200,200,200))
    m = tresh_font.render("0", True, (0, 0, 0))
    tw, th = m.get_size()
    screen.blit(label, (w*5//6-tw//2, h//12*4-th//2))


def mode(screen, string):
    global mode_font
    w, h = screen.get_size()
    if mode_font is None:
        mode_font = pg.font.Font(font, 14)
    m = mode_font.render("0", True, (0, 0, 0))
    tw, th = m.get_size()
    for i in range(len(string)):
        label = mode_font.render("{}".format(string[i]), True, (255,255,255))
        tw, _ = label.get_size()
        screen.blit(label, (w*5//6-tw//2, h//6*3+th//2*3*i-th//2))