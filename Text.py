import pygame
from pygame.locals import *
import Utilities

class Text():
    def __init__(self,font,size,color):
        self.Font = pygame.font.Font(font,size) 
        self.Color = color
    def render_center(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,Utilities.center(posx,posy,self.Font.size(str(content))[0],self.Font.size(str(content))[1])))
    
    def render_corner(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,(posx,posy))) 
    
    def render_centercorner(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,Utilities.center(posx,posy,self.Font.size(str(content))[0],0))) 

    def render_cornercenter(self,target,content,posx,posy):
        Text_ = self.Font.render(content,False,self.Color,None)
        target.append((Text_,Utilities.center(posx,posy,0,self.Font.size(str(content))[1]))) 
    
    def get_size_x(self,content):
        return self.Font.size(str(content))[0]
    
    def get_size_y(self,content):
        return self.Font.size(str(content))[1]