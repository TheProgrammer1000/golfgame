from pygame.math import Vector2   # säkrare import
from classes.GameObject import GameObject

class Bullet(GameObject):
    def __init__(self, pos, color, radius, direction):
        super().__init__(pos, color, radius)
        self.direction = Vector2(direction)
        
    def setBulletPos(self, pos):
        self.pos = pos        
    