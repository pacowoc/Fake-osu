import pygame
import MapPlayer

MAP_NAME = "beta"
MAP_DIFF = "Object type test"
SKIN_NAME = "test"

pygame.init()
screen=pygame.display.set_mode(size=(1080,720))#,flags=pygame.SCALED|pygame.FULLSCREEN)
pygame.display.set_caption("Fake osu!")
MapPlayer.Play(screen,MAP_NAME,MAP_DIFF,SKIN_NAME,[0,1,1]) 

