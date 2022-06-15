import pygame
from pygame.locals import *

BLACK = (0,0,0)
TRANSPARENT = (0,0,0,0)
TRANSLUCENT = (0,0,0,128)

def center(posX,posY,sizeX,sizeY):
    posnX=posX-1/2*sizeX
    posnY=posY-1/2*sizeY

    return (posnX,posnY)

def render_text(Content,font,size,color):
    Font = pygame.font.Font(font,size)
    Text = Font.render(Content,False,color,None)

    return (Text,Font.size(Content)[0],Font.size(Content)[1])
def render(target,curr_Objects):
    target.fill(BLACK)
    for obj in curr_Objects:
      target.blit(obj[0],obj[1])
    pygame.display.update()