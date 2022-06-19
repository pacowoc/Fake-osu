import pygame
from pygame.locals import *
import src.Text as Text

def Render(target,skin):
    MapSelect = pygame.image.load("skins\\"+skin+"\\mapselect.png").convert_alpha()
      