from pygame.locals import *

class Spinner():
    def __init__(self,time,span,req):
        self.Time = time
        self.Span = span
        self.Req = req
        self.Quadrants = [0,0,0,0]
        self.Spins = 0
    def End(self):
        print(str((self.Spins,self.Req)))
        if self.Spins>=self.Req:
            return 300
        elif self.Spins>=self.Req/2:
            return 100
        elif self.Spins>=1:
            return 50
        else:
            return 0