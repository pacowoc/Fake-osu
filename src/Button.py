import pygame

class ClickButton():
    def __init__(self,image:pygame.Surface,image_overlayed:pygame.Surface,posx,posy):
        self.image = image
        self.image_overlayed = image_overlayed
        self.rect = self.image.get_rect()
        self.rect.center = (posx,posy)

    def get_overlay(self,Mposx,Mposy):
        return self.rect.collidepoint(Mposx,Mposy)
    
    def render_center(self,target,do_overlay):
        if do_overlay:
            target.append((self.image_overlayed,self.rect.topleft))
        else: 
            target.append((self.image,self.rect.topleft))

class ToggleButton():
    def __init__(self,images,posx,posy):
        self.states = len(images)
        self.images = images
        self.rect = images[0].get_rect()
        self.rect.center = (posx,posy)
        self.state = 0

    def get_overlay(self,Mposx,Mposy):
        return self.rect.collidepoint(Mposx,Mposy)
    
    def next_state(self):
        self.state+=1

    def previous_state(self):
        self.state-=1
    
    def get_state(self):
        return self.state%self.states

    def render_center(self,target):
        target.append((self.images[self.state%self.states],self.rect.topleft))
