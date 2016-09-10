import pygame
import sys
import time
from pygame.locals import *

from fgg import data
from fgg import instrument as ins
from fgg import sonance as son
from fgg import game
from fgg.general import *

def main():
    pygame.time.set_timer(DISPLAY_REFRESH, int(1000/FPS))
    pygame.init()

    inst = ins.Instrument("guitar1", ["0e", "0a", "1d", "1g", "1b", "2e"], "e")
    fadeouts = {}
    oct_offset = 0

    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Super Wicked Sick Nasty Radical Guitar Game")

    fnt = pygame.font.SysFont("monospace", 16)

    muted_strum = pygame.mixer.Sound(data.filepath("sound/muted_strum.ogg"))

    while True: # official theme song: Also sprach Zarathustra, Op. 30
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    sys.exit("\nThanks for playing!")
                if ev.key == pygame.K_SPACE:
                    muted_strum.play()
                    muted_strum.fadeout(300)
                if ev.key == pygame.K_LSHIFT:
                    oct_offset = 3
                    fadeouts.clear()
                if ev.key in kb_map[0]:
                    playSound(inst.mapping[0 + oct_offset][kb_map[0].index(ev.key)])
                    fadeouts[ev.key] = (0 + oct_offset, kb_map[0].index(ev.key))
                if ev.key in kb_map[1]:
                    playSound(inst.mapping[1 + oct_offset][kb_map[1].index(ev.key)])
                    fadeouts[ev.key] = (1 + oct_offset, kb_map[1].index(ev.key))
                if ev.key in kb_map[2]:
                    playSound(inst.mapping[2 + oct_offset][kb_map[2].index(ev.key)])
                    fadeouts[ev.key] = (2 + oct_offset, kb_map[2].index(ev.key))
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_LSHIFT:
                    oct_offset = 0
                if ev.key in fadeouts.keys():
                    inst.mapping[fadeouts[ev.key][0]][fadeouts[ev.key][1]].fadeout(500)
            elif ev.type == SOUND_PLAYED:
                son.prev_tick = son.tick
                son.tick = son.snd_clock.tick()
                game.measure_time += son.tick
                if son.prev_tick != -1:
                    crh = son.calcRhythm(son.prev_tick, son.tick)
                    #print("Max Rhythm: ", crh)
                    if crh > son.max_rhythm:
                        son.max_rhythm = crh
                    if crh < son.min_rhythm and crh != 0:
                        son.min_rhythm = crh
                    son.last_rhythm = crh
                    son.avg_rhythm = (son.avg_rhythm * son.ctr) + crh
                    game.rhythms.append(crh)
                if son.prev_snd is not None:
                    crn = son.calcRoughness(son.snd, son.prev_snd)
                    #print("Roughness: ", crn)
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
            elif ev.type == DISPLAY_REFRESH:
                rn = fnt.render("Roughness:", 1, (0, 0, 0))
                rn_min = fnt.render("Min: " + str(son.min_roughn), 1, (0, 0, 0))
                rn_max = fnt.render("Max: " + str(son.max_roughn), 1, (0, 0, 0))
                rn_last = fnt.render("Last: " + str(son.last_roughn), 1, (0, 0, 0))
                rn_avg = fnt.render("Average: " + str(son.avg_roughn), 1, (0, 0, 0))
                rh = fnt.render("Rhythm:", 1, (0, 0, 0))
                rh_min = fnt.render("Min: " + str(son.min_rhythm), 1, (0, 0, 0))
                rh_max = fnt.render("Max: " + str(son.max_rhythm), 1, (0, 0, 0))
                rh_last = fnt.render("Last: " + str(son.last_rhythm), 1, (0, 0, 0))
                rh_avg = fnt.render("Average: " + str(son.avg_rhythm), 1, (0, 0, 0))
                screen.fill((255, 255, 255))
                screen.blit(img, img_rect)
                screen.blit(rn, (600, 475))
                screen.blit(rn_min, (600, 500))
                screen.blit(rn_max, (600, 525))
                screen.blit(rn_last, (600, 550))
                screen.blit(rn_avg, (600, 575))
                screen.blit(rh, (600, 600))
                screen.blit(rh_min, (600, 625))
                screen.blit(rh_max, (600, 650))
                screen.blit(rh_last, (600, 675))
                screen.blit(rh_avg, (600, 700))
                pygame.display.flip()

        pygame.time.wait(0)

