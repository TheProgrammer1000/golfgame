from pygame.math import Vector2   # säkrare import

from classes.GameObject import GameObject

class Player(GameObject):
    def __init__(self, pos, vel, direction, color, radius_m):
        super().__init__(pos, color, radius_m)
        self.vel = Vector2(vel)
        self.direction = Vector2(direction)
        
    def setDirection(self, theta):
        self.direction = theta 
        
    