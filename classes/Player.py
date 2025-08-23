from pygame.math import Vector2   # säkrare import

class Player:
    def __init__(self, pos, vel, direction, color, radius):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.direction = Vector2(direction)
        self.color = color
        self.radius = radius
        
    def setColor(self, color):
        self.color = color
        
    def setDirection(self, theta):
        self.direction = theta 
        
    