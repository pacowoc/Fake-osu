import pygame
from pygame.locals import *
import Utilities

class Text():
    def __init__(self,font,size,color):
        self.Font = pygame.font.Font(font,size) 
        self.Color = color
    def render_center(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,Utilities.center(posx,posy,self.get_size_x(content),self.get_size_y(content))))
    
    def render_tlcorner(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,(posx,posy))) 
    
    def render_trcorner(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,(posx-self.get_size_x(content),posy))) 

    def render_blcorner(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,(posx,posy-self.get_size_y(content)))) 

    def render_brcorner(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,(posx-self.get_size_x(content),posy-self.get_size_y(content)))) 
    
    def get_size_x(self,content):
        return self.Font.size(str(content))[0]
    
    def get_size_y(self,content):
        return self.Font.size(str(content))[1]