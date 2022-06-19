import pygame
import bezier
import numpy
from pygame.locals import *
import Utilities

class Slider():
    def __init__(self,posx,posy,radius,time,span,delta):
        self.Posx = posx
        self.Posy = posy
        self.Radius = radius
        self.Time = time
        self.Span = span
        nodes = numpy.asfortranarray([posx,posy])
        self.main_curve = bezier.Curve(nodes, degree=len(posx)-1)
        self.HPosx = posx[0]
        self.HPosy = posy[0]
        self.EPosx = posx[-1]
        self.EPosy = posy[-1]
        self.Delta = delta
        self.HeadHit = False
    def render_head_hc(self,target,tex_Surf):
        target.append((tex_Surf,Utilities.center(self.HPosx,self.HPosy,2*self.Radius,2*self.Radius)))
    def render_head_ac(self,target,tex_Surf,curr_time):
    
        approach_circle_size = 2*self.Radius*(4-3*(curr_time-self.Time+self.Delta)/self.Delta)
        if approach_circle_size>2*self.Radius:
            Approach_circle = pygame.Surface((approach_circle_size,approach_circle_size)).convert_alpha()
            pygame.transform.scale(tex_Surf,(approach_circle_size,approach_circle_size),dest_surface=Approach_circle)
            target.append((Approach_circle,Utilities.center(self.HPosx,self.HPosy,approach_circle_size,approach_circle_size)))

    def render_follow_circle(self,target,tex_Surfhc,tex_Surfac,curr_time):
        target.append((tex_Surfac,Utilities.center(self.get_ball_x(curr_time),self.get_ball_y(curr_time),5*self.Radius,5*self.Radius)))
        target.append((tex_Surfhc,Utilities.center(self.get_ball_x(curr_time),self.get_ball_y(curr_time),2*self.Radius,2*self.Radius)))
    
    def render_body(self,target,tex_Surf):
        for i in range(50):
            evaluated = self.main_curve.evaluate(i/50).tolist()
            target.append((tex_Surf,Utilities.center(evaluated[0][0],evaluated[1][0],2*self.Radius,2*self.Radius)))
    def render_end(self,target,tex_Surf):
            target.append((tex_Surf,Utilities.center(self.EPosx,self.EPosy,2*self.Radius,2*self.Radius)))
    def head_hit_eval(self,curr_time,w50):
        Error = abs(curr_time-self.Time)
        if Error<=w50:
            return 300
        else:
            return 0

    def get_ball_x(self,curr_time):
        return self.main_curve.evaluate((curr_time-self.Time)/self.Span).tolist()[0][0]

    def get_ball_y(self,curr_time):
        return self.main_curve.evaluate((curr_time-self.Time)/self.Span).tolist()[1][0]