import pygame
import sys
from fgg import data

# time constraint inspired solutions to multiple problems
NOTES = {} # dictionary of sounds and their notes e.g. Sound object at 0xabcdef12345 : "1c#"
OCTAVE = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"] # Cx to Bx is indeed not actually an OCTAVE
FREQS = [[65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.0, 116.54, 123.47],
        [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.0, 196.0, 207.65, 220.0, 233.08, 246.94],
        [261.6, 277.2, 293.7, 311.1, 329.6, 349.2, 370.0, 392.0, 415.3, 440.0, 466.2, 493.9],
        [523.3, 554.4, 587.3, 622.3, 659.3, 698.5, 740.0, 784.0, 830.6, 880.0, 932.3, 987.8],
        [1047, 1109, 1175, 1245, 1319, 1397, 1480, 1568, 1661, 1760, 1865, 1976]] # freq table for roughness, begins from C2

class Instrument:
    # end note is the last note the instrument is capable of NOT the last note in an OCTAVE
    def __init__(self, name, octs, end_note="b"):
        print("Instrument mapping:")
        self.name = name
        self.mapping = []
        #ctr = 0
        for x in range(0, len(octs)):
            self.mapping.append([])
            ind = OCTAVE.index(octs[x][1])
            off = int(octs[x][0]) - x
            for n in range(0, 12): # 12 being the number of keyboard keys per row used
                self.mapping[x].append(pygame.mixer.Sound(data.filepath("sound/" + name + "/" + str(x + off) + OCTAVE[ind] + ".ogg")))
                NOTES[self.mapping[x][n]] = str(x+off) + OCTAVE[ind]
                print(str(x+off) + OCTAVE[ind], end=" ")
                if (n == 0):
                    self.mapping[x][n].play()
                    self.mapping[x][n].fadeout(500)
                if (ind == len(OCTAVE) - 1):
                    off += 1
                    ind = 0
                else:
                    ind += 1
                #ctr += 1
                #sys.stdout.write("\rLoaded {}/{} notes".format(ctr, len(OCTAVE) * len(octs)))
            print()
        sys.stdout.flush()
        print("Done!")
