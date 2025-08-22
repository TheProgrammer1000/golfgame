from pygame.math import Vector2   # säkrare import

class GameObject:
    def __init__(self, pos, color, radius):
        self.pos = Vector2(pos)
        self.color = color
        self.radius = radius
        
    def setColor(self, color):
        self.color = color
        
    