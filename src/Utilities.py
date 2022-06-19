import pygame
from pygame.locals import *

BLACK = (0,0,0)
TRANSPARENT = (0,0,0,0)
TRANSLUCENT = (0,0,0,128)

def center(posX,posY,sizeX,sizeY):
    if sizeX>0 and sizeY>0:
        posnX=posX-1/2*sizeX
        posnY=posY-1/2*sizeY
    else:
        posnX=posX  
        posnY=posY
    return (posnX,posnY)
    
def render(target,curr_Objects):
    target.fill(BLACK)
    for obj in curr_Objects:
      target.blit(obj[0],obj[1])
    pygame.display.update()

def division(a,b):
    return a/b if b else 0