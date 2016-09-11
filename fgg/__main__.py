import pygame
import sys
import time
from pygame.locals import *

from fgg import data
from fgg import instrument as ins
from fgg import sonance as son
from fgg import game
from fgg.general import *
from fgg import draw


def main():
    pygame.time.set_timer(DISPLAY_REFRESH, int(1000/FPS))
    pygame.time.set_timer(GAME_REFRESH, 1000)
    pygame.init()

    inst = ins.Instrument("guitar1", ["0e", "0a", "1d", "1g", "1b", "2e"], "e")
    fadeouts = {}
    oct_offset = 0

    dec = pygame.image.load(data.filepath("img/dec.png")).convert_alpha() # cute decoration

    fnt = pygame.font.SysFont("monospace", 16)

    muted_strum = pygame.mixer.Sound(data.filepath("sound/muted_strum.ogg"))

    title_page = pygame.image.load(data.filepath("img/title_page.png"))
    screen.blit(title_page, (0, 0))
    pygame.display.flip()
    pygame.time.wait(500)

    game.crowd = game.crowd.convert_alpha()
    for i in range(0, len(game.player)):
        game.player[i].convert()

    game.init() 

    while True:  # official theme song: Also sprach Zarathustra, Op. 30
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if game.game_started == False and game.game_over == False:
                    game.game_started = True
                if ev.key == pygame.K_ESCAPE:
                    sys.exit("\nThanks for playing!")
                if ev.key == pygame.K_SPACE:
                    muted_strum.play()
                    muted_strum.fadeout(300)
                if ev.key == pygame.K_LSHIFT:
                    oct_offset = 3
                    fadeouts.clear()
                if ev.key in KB_MAP[0]:
                    playSound(inst.mapping[0 + oct_offset][KB_MAP[0].index(ev.key)])
                    fadeouts[ev.key] = (0 + oct_offset, KB_MAP[0].index(ev.key))
                if ev.key in KB_MAP[1]:
                    playSound(inst.mapping[1 + oct_offset][KB_MAP[1].index(ev.key)])
                    fadeouts[ev.key] = (1 + oct_offset, KB_MAP[1].index(ev.key))
                if ev.key in KB_MAP[2]:
                    playSound(inst.mapping[2 + oct_offset][KB_MAP[2].index(ev.key)])
                    fadeouts[ev.key] = (2 + oct_offset, KB_MAP[2].index(ev.key))
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_LSHIFT:
                    oct_offset = 0
                if ev.key in fadeouts.keys():
                    inst.mapping[fadeouts[ev.key][0]][fadeouts[ev.key][1]].fadeout(500)
            elif ev.type == SOUND_PLAYED:
                son.prev_tick = son.tick
                son.tick = son.snd_clock.tick()
                if son.prev_tick != -1:
                    crh = son.calcRhythm(son.prev_tick, son.tick)
                    if crh > son.max_rhythm:
                        son.max_rhythm = crh
                    if crh < son.min_rhythm and crh != 0:
                        son.min_rhythm = crh
                    if crh == 0:
                        crh = 1
                    son.last_rhythm = crh
                    son.avg_rhythm = (son.avg_rhythm * son.ctr) + crh
                if son.prev_snd is not None:
                    crn = son.calcRoughness(son.snd, son.prev_snd)
                    if crn > son.max_roughn:
                        son.max_roughn = crn
                    if crn < son.min_roughn and crn != 0:
                        son.min_roughn = crn
                    if game.roughnesses.get(crn) is not None:
                        game.roughnesses[crn] += 1
                        crn /= (game.roughnesses[crn] * 1.5)
                    else:
                        game.roughnesses[crn] = 1
                    son.last_roughn = crn
                    son.avg_roughn = (son.avg_roughn * son.ctr) + crn
                    son.ctr += 1
                    son.avg_rhythm = son.avg_rhythm / son.ctr
                    son.avg_roughn = son.avg_roughn / son.ctr
                    game.updateCombos(son.last_roughn, son.last_rhythm, son.tick)
                    if son.ctr >= son.MAX_CTR:
                        son.ctr_tick = son.ctr_clock.tick()
                        gson = son.getSonance()
                        if son.ctr_tick < 1500:
                            gson = abs(gson) * -1
                            print("Punished!")
                        game.updateCrowd(gson * (1 + (game.offbeat_chain / 10) * (1 + (game.offkey_chain) / 5) * (1 + (game.long_time_chain / 2)))) # where the magic happens
                        son.ctr = 0
                        son.last_avg_rhythm = son.avg_rhythm
                        son.last_avg_roughn = son.avg_roughn
                        game.roughnesses.clear()
            elif ev.type == GAME_OVER:
                game.game_started = False
                game.game_over = True
                game.gameOver()
            elif ev.type == GAME_REFRESH:
                game.updateCrowd(game.crowd_x_inc)
            elif ev.type == DISPLAY_REFRESH:
                game.updateCrowd()
                game.updatePlayer()
                if pygame.mixer.get_busy():
                    draw.draw_imgs[dec] = (game.player_xy[0] + 40, game.player_xy[1] - 40)
                screen.fill((255, 255, 255))
                """rn = fnt.render("Roughness:", 1, (0, 0, 0))
                screen.blit(img, img_rect)
                screen.blit(rn, (500, 275))
                screen.blit(rn_min, (500, 300))
                screen.blit(rn_max, (500, 325))
                screen.blit(rn_last, (500, 350))
                screen.blit(rn_avg, (500, 375))
                screen.blit(rh, (500, 425))
                screen.blit(rh_min, (500, 450))
                screen.blit(rh_max, (500, 475))
                screen.blit(rh_last, (500, 525))
                screen.blit(rh_avg, (500, 550))
                pygame.display.flip()"""
                draw.drawTxt(fnt)
                draw.drawImg()

                pygame.display.flip()

        pygame.time.wait(0)

