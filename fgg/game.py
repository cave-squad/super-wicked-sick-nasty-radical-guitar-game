import math
import pygame
from fgg import sonance as son
from fgg import data
from fgg import draw
from fgg.general import *

game_started = False
game_over = True

score = 0
offbeat_chain = 0 # off-beat combo is self-explanatory
offkey_chain = 0 # odd - bad - terrible - horrendous - wtf? combo for hitting off-key notes
long_time_chain = 0 # sniper: 350ms or more between bad notes

offbeat_errs = 0
offkey_errs = 0
long_time_errs = 0

OFFBEAT_THRESHOLD = 0.8
OFFKEY_THRESHOLD = 0.1
LONG_TIME_THRESHOLD = 350 # parameter limits for combos

OFFBEAT_ERR_THRESHOLD = 3
OFFKEY_ERR_THRESHOLD = 5
LONG_TIME_ERR_THRESHOLD = 2 # how many times you can play correctly before losing that combo

roughnesses = {} # different structure for anti-cheesing

ROUGHNESS_MAX_REPEAT = 3

crowd = pygame.image.load(data.filepath("img/crowd.png"))
crowd_xy = (800, 400)
crowd_x_inc = -10 # initially

player = [ pygame.image.load(data.filepath("img/player/player.png")), 
        pygame.image.load(data.filepath("img/player/player_strum0.png")),
        pygame.image.load(data.filepath("img/player/player_strum1.png")),
        pygame.image.load(data.filepath("img/player/player_strum2.png")),
        pygame.image.load(data.filepath("img/player/player_strum3.png")) ]
player_rect = player[0].get_rect()
player_xy = (50, 500)
player_frame = 0

def init():
    global game_started
    game_started = True
    draw.draw_imgs[crowd] = crowd_xy

def updateCrowd(mov_x=0):
    global crowd_xy
    global game_started
    if game_started:
        crowd_xy = (crowd_xy[0] + mov_x, crowd_xy[1])
        if crowd_xy[0] < player_xy[0] - 50:
            pygame.event.post(pygame.event.Event(GAME_OVER))
    draw.draw_imgs[crowd] = crowd_xy

def updatePlayer():
    global player_frame
    if player_frame == 4:
        player_frame = 0
    if player_frame > 0:
        player_frame += 0.5 # to slow anim
    draw.draw_imgs[player[math.ceil(player_frame)]] = player_xy

def gameOver(): 
    global score
    global offbeat_chain
    global offkey_chain
    global long_time_chain
    global offbeat_errs
    global offkey_errs
    global long_time_errs 
    global roughnesses 

    score = 0
    offbeat_chain = 0 
    offkey_chain = 0 
    long_time_chain = 0 
    offbeat_errs = 0
    offkey_errs = 0
    long_time_errs = 0
    roughnesses.clear()

    son.tick = -1
    son.prev_tick = -1
    son.snd = None
    son.prev_snd = None
    son.avg_roughn = 0
    son.last_roughn = 0
    son.last_avg_roughn = -1 
    son.avg_rhythm = 0
    son.last_rhythm = 0
    son.last_avg_rhythm = -1


def updateCombos(rn, rh, mt):
    global score
    global offbeat_chain
    global offkey_chain
    global long_time_chain
    global offbeat_errs
    global offkey_errs
    global long_time_errs 
    global roughnesses # theoretically this is a design best practice SOMEWHERE out there

    if rn >= OFFKEY_THRESHOLD :
        if roughnesses.get(rn) is not None:
            if roughnesses[rn] < ROUGHNESS_MAX_REPEAT:
                offkey_chain += 1
                offkey_errs = 0
        else:
            offkey_chain += 1
            offkey_errs = 0
    elif rn < OFFKEY_THRESHOLD:
        offkey_errs += 1
    if rh <= OFFBEAT_THRESHOLD:
        offbeat_chain += 1
        offbeat_errs = 0
    elif rh > OFFBEAT_THRESHOLD:
        offbeat_errs += 1 

    if offbeat_errs == OFFBEAT_ERR_THRESHOLD:
        score += 100 * offbeat_chain
        offbeat_chain = 0
    if offkey_errs == OFFKEY_ERR_THRESHOLD:
        score += 250 * offkey_chain
        offkey_chain = 0

    if mt >= LONG_TIME_THRESHOLD and offkey_chain > 0 and offbeat_chain > 0:
        long_time_chain += 1
        long_time_errs = 0
    elif mt > OFFKEY_THRESHOLD:
        long_time_errs += 1
    if long_time_errs == LONG_TIME_ERR_THRESHOLD:
        score += 1000 * long_time_chain
        long_time_chain = 0

    if offbeat_chain > 0 and offbeat_errs == 0:
        print("Off-beat COMBO: ", offbeat_chain)
    if offkey_chain > 0 and offkey_errs == 0:
        print("Off-key COMBO: ", offkey_chain)
    if long_time_chain > 0 and long_time_errs == 0:
        print("Sniper COMBO: ", long_time_chain)

