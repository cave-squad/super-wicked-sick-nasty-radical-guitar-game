import pygame
import sys
import numpy
import math
from fgg import data
from fgg import instrument as ins

snd_clock = pygame.time.Clock()
tick = -1
prev_tick = -1
snd = None
prev_snd = None

sonance = 0 # the real(ly faked) deal

roughness_cache = {} # roughness algo might be nasty enough to merit memoization

max_roughn = 0
min_roughn = 1
max_rhythm = 0
min_rhythm = 1

MAX_CTR = 10
ctr = 0 
ctr_clock = pygame.time.Clock()
ctr_tick = -1
prev_ctr_tick = -1

avg_roughn = 0
last_roughn = 0
last_avg_roughn = -1 
avg_rhythm = 0
last_rhythm = 0
last_avg_rhythm = -1

# roughness calculation by ffting sounds so they are sinusoidal and incorrectly using vassilakis roughness model
# for some reason unknown to me worse-sounding music generally makes the average roughness go down despite lower roughness meaning less
def calcRoughness(snd, snd1):
    if roughness_cache.get((snd, snd1)) is not None:
        return roughness_cache[(snd, snd1)] 
    else:
        arr = pygame.sndarray.array(snd)
        arr = numpy.fft.fft(arr)
        arr = arr / numpy.sqrt(len(arr))
        arr1 = pygame.sndarray.array(snd1)
        arr1 = numpy.fft.fft(arr1)
        arr1 = arr1 / numpy.sqrt(len(arr1))
        f_max = ins.FREQS[int(ins.NOTES[snd][0])][ins.OCTAVE.index(ins.NOTES[snd][1:])]
        f_min = ins.FREQS[int(ins.NOTES[snd1][0])][ins.OCTAVE.index(ins.NOTES[snd1][1:])]

        if int(ins.NOTES[snd][0]) < int(ins.NOTES[snd1][0]):
            f_max = ins.FREQS[int(ins.NOTES[snd1][0])][ins.OCTAVE.index(ins.NOTES[snd1][1:])]
            f_min = ins.FREQS[int(ins.NOTES[snd][0])][ins.OCTAVE.index(ins.NOTES[snd][1:])]
        elif int(ins.NOTES[snd][0]) == int(ins.NOTES[snd1][0]):
            if ins.OCTAVE.index(ins.NOTES[snd][1:]) < ins.OCTAVE.index(ins.NOTES[snd1][1:]):
                f_max = ins.FREQS[int(ins.NOTES[snd1][0])][ins.OCTAVE.index(ins.NOTES[snd1][1:])]
                f_min = ins.FREQS[int(ins.NOTES[snd][0])][ins.OCTAVE.index(ins.NOTES[snd][1:])]

        arr_amp = numpy.mean((arr * arr.conj()).real)
        arr1_amp = numpy.mean((arr1 * arr1.conj()).real)
        a_min = min(arr_amp, arr1_amp)
        a_max = max(arr_amp, arr1_amp)
        x = a_min * a_max
        y = 2 * a_min / (a_min + a_max)
        s_fmax_fmin = (0.24 / (0.0207 * f_min + 18.96)) * (f_max - f_min) # separated for (somewhat) easier reading
        z = math.exp(-1 * 3.5 * s_fmax_fmin) - math.exp(-1 * 5.75 * s_fmax_fmin)
        ans = pow(x, 0.1) * 0.5 * (pow(y, 3.11)) * z
        roughness_cache[(snd, snd1)] = ans
        roughness_cache[(snd1, snd)] = ans

        return pow(x, 0.1) * 0.5 * (pow(y, 3.11)) * z

def calcRhythm(t, prev_t): # dead simple rhythm calculation written when tired
    min_t = min(t, prev_t)
    max_t = max(t, prev_t)
    ret = 0 
    if min_t == 0:
        return ret
    elif max_t / min_t < 4:
        ret =  min_t / (max_t / int(max_t / min_t))
    return ret

def getSonance(): # no arguments no problem
    if last_avg_rhythm < avg_rhythm and last_avg_roughn > avg_roughn: # consonant (bad)
        return -1
    elif last_avg_rhythm > avg_rhythm and last_avg_roughn < avg_roughn: # dissonant (good) 
        return 5 
    else:
       return 1

