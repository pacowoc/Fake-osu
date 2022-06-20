from pygame.locals import *
import Utilities
import pygame

class Circle():
    def __init__(self,posx,posy,radius,time,delta,tex_Surf):
        self.Posx = posx
        self.Posy = posy
        self.Radius = radius
        self.Time = time
        self.Delta = delta
        self.tex_Surfc = tex_Surf.copy()
    def render_hc(self,target,curr_time):
        self.Fade_end = self.Delta*2/3
        alpha = min(255,255*(curr_time-self.Time+self.Delta)//self.Fade_end)
        if alpha>0:
            self.tex_Surfc.set_alpha((alpha))
            target.append((self.tex_Surfc,Utilities.center(self.Posx,self.Posy,2*self.Radius,2*self.Radius)))

    def render_hc_hd(self,target,curr_time):
        self.Fade_start = self.Delta*1/3
        alpha = min(255,255*(self.Time-curr_time+self.Delta)//self.Delta-self.Fade_start)
        if alpha>0:
            self.tex_Surfc.set_alpha((alpha))
            target.append((self.tex_Surfc,Utilities.center(self.Posx,self.Posy,2*self.Radius,2*self.Radius)))


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
        
