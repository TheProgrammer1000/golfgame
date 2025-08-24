from pygame.math import Vector2   # säkrare import

class GameObject:
    def __init__(self, pos, color, radius, scale):
        self.pos = Vector2(pos)
        self.color = color
        self.radius = radius
        self.scale = scale
        
    def setColor(self, color):
        self.color = color
        
    