from pygame.locals import *
import Utilities
import pygame

class Circle():
    def __init__(self,posx,posy,radius,time,delta):
        self.Posx = posx
        self.Posy = posy
        self.Radius = radius
        self.Time = time
        self.Delta = delta
        self.Fade_end = delta*2/3
    def render_hc(self,target,tex_Surf,curr_time):
        alpha = min(255,255*(curr_time-self.Time+self.Delta)//self.Fade_end)
        if alpha>0:
            tex_Surf.set_alpha((alpha))
            target.append((tex_Surf,Utilities.center(self.Posx,self.Posy,2*self.Radius,2*self.Radius)))
            tex_Surf.set_alpha((255))

    def render_ac(self,target,tex_Surf,curr_time):
        approach_circle_size = 2*self.Radius*(4-3*(curr_time-self.Time+self.Delta)/self.Delta)
        if approach_circle_size>2*self.Radius:
            Approach_circle = pygame.Surface((approach_circle_size,approach_circle_size)).convert_alpha()
            pygame.transform.scale(tex_Surf,(approach_circle_size,approach_circle_size),dest_surface=Approach_circle)
            target.append((Approach_circle,Utilities.center(self.Posx,self.Posy,approach_circle_size,approach_circle_size)))
    
    def hit_eval(self,curr_time,w300,w100,w50):
        Error = abs(curr_time-self.Time)
        if Error<=w300:
            return 300
        elif Error<=w100:
            return 100
        elif Error<=w50:
            return 50
        else:
            return 0
        
