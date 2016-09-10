import pygame
from fgg import sonance as son

score = 0
offbeat_chain = 0 # off-beat combo is self-explanatory
offkey_chain = 0 # odd - bad - terrible - horrendous - wtf? combo for hitting off-key notes
long_time_chain = 0 # sniper: 200ms or more between bad notes

offbeat_errs = 0
offkey_errs = 0
long_time_errs = 0

OFFBEAT_THRESHOLD = 0.8
OFFKEY_THRESHOLD = 0.1
LONG_TIME_THRESHOLD = 300 # parameter limits for combos

OFFBEAT_ERR_THRESHOLD = 5
OFFKEY_ERR_THRESHOLD = 5
LONG_TIME_ERR_THRESHOLD = 2 # how many times you can play correctly before losing that combo

measure_time = 0
rhythms = []
roughnesses = {} # different structure for anti-cheesing

ROUGHNESS_MAX_REPEAT = 3

def updateCombos(rn, rh, mt):
    global score
    global offbeat_chain
    global offkey_chain
    global long_time_chain
    global offbeat_errs
    global offkey_errs
    global long_time_errs # last minute best practices
    global roughnesses

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
    if long_time_errs == LONG_TIME_ERR_THRESHOLD:
        score += 1000 * long_time_chain
        long_time_chain = 0

    if mt <= LONG_TIME_THRESHOLD and offkey_chain > 0 and offbeat_chain > 0:
        long_time_chain += 1
        long_time_errs = 0
    elif mt > OFFKEY_THRESHOLD:
        long_time_errs += 1

    if offbeat_chain > 0 and offbeat_errs == 0:
        print("Off-beat COMBO: ", offbeat_chain)
    if offkey_chain > 0 and offkey_errs == 0:
        print("Off-key COMBO: ", offkey_chain)
    if long_time_chain > 0 and long_time_errs == 0:
        print("Sniper COMBO: ", long_time_chain)

