import pygame
import Menu
SKIN_NAME = "test"
pygame.init()
pygame.key.set_repeat()
pygame.mouse.set_visible(0)
screen=pygame.display.set_mode(size=(1080,720))#,flags=pygame.SCALED|pygame.FULLSCREEN)
pygame.display.set_caption("Fake osu!")
Menu.Render(screen,SKIN_NAME)
