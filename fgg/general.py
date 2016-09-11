import pygame
from pygame.locals import *
from fgg import data
from fgg import sonance as son
from fgg import game

KB_MAP = [[pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS],
        [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET],
        [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_RETURN]]
img = pygame.image.load(data.filepath("img/dope_guitar.png"))
img_rect = img.get_rect()
FPS = 30

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Super Wicked Sick Nasty Radical Guitar Game")

DISPLAY_REFRESH = USEREVENT
GAME_REFRESH =  USEREVENT + 1
UPDATE_GAME = USEREVENT + 2
SOUND_PLAYED = USEREVENT + 3
GAME_OVER = USEREVENT + 4
 
def playSound(snd):
    snd.play()
    if game.game_started:
        son.prev_snd = son.snd
        son.snd = snd
        pygame.event.post(pygame.event.Event(SOUND_PLAYED))
    if game.player_frame == 0:
        game.player_frame = 1
