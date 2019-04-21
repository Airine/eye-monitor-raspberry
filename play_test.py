import pygame
pygame.mixer.init()
pygame.mixer.music.load("raw_data/sig1822k_210duo_pi.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
