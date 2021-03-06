import pygame
from fgg import sonance as son
from fgg.general import *

draw_imgs = {} # objects to draw, their coords
draw_txts = {} # texts to draw and coordinate tuples

ui_x = 10 
ui_y = 10 

def drawImg():
    global draw_imgs
    for img in draw_imgs:
        screen.blit(img, draw_imgs[img])
    draw_imgs.clear()

def drawTxt(fnt):
    global draw_txts
    draw_txts = {
        fnt.render("Roughness:", 1, (0, 0, 0)):(ui_x, ui_y),
        fnt.render("Last: " + str(son.last_roughn), 1, (0, 0, 0)):(ui_x, ui_y+25),
        fnt.render("Average: " + str(son.avg_roughn), 1, (0, 0, 0)):(ui_x, ui_y+50),
        fnt.render("Rhythm:", 1, (0, 0, 0)):(ui_x, ui_y+100),
        fnt.render("Last: " + str(son.last_rhythm), 1, (0, 0, 0)):(ui_x, ui_y+125),
        fnt.render("Average: " + str(son.avg_rhythm), 1, (0, 0, 0)):(ui_x, ui_y+150),
    }
    for txt in draw_txts:
        screen.blit(txt, draw_txts[txt])

