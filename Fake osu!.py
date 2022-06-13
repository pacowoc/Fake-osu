import pygame
import MapPlayer
import ResultScreen

MAP_NAME = "Example"
MAP_DIFF = "Normal"
SKIN_NAME = "test"

pygame.init()
screen=pygame.display.set_mode(size=(1080,720),#flags=pygame.SCALED|pygame.FULLSCREEN#
)
pygame.display.set_caption("Fake osu!")
Results = MapPlayer.Play(screen,MAP_NAME,MAP_DIFF,SKIN_NAME,[0]) 
ResultScreen.Render(screen,MAP_NAME,MAP_DIFF,SKIN_NAME,[0],Results["Score"],Results["Acc"],Results["Rating_count"],Results["Max_combo"])
