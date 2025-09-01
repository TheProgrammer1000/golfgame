from pygame.math import Vector2   # säkrare import
from classes.GameObject import GameObject

class Bullet(GameObject):
    def __init__(self, pos, color, radius_m, direction, bulletSpeed, bulletRange):
        super().__init__(pos, color, radius_m)
        self.direction = Vector2(direction)
        self.bulletSpeed = bulletSpeed
        self.bulletRange = bulletRange
        self.isBulletShot = False
        self.damage = 20
        
    def setBulletPos(self, pos):
        self.pos = pos
    
    def setBulletDirection(self, direction):
        self.direction = direction
        
    def update(self, obstacle, dt):
        pass    
    