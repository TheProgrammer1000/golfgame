from pygame.math import Vector2   # säkrare import
import pygame
from classes.GameObject import GameObject

class Bullet(GameObject):
    def __init__(self, pos, color, radius_m, direction, bulletSpeed, bulletRange):
        super().__init__(pos, color, radius_m)
        self.direction = Vector2(direction)
        self.bulletSpeed = bulletSpeed
        self.bulletRange = bulletRange
        self.isBulletShot = False
        self.spawn_pos = Vector2(pos)
        self.damage = 20
        
    def setBulletPos(self, pos):
        self.pos = pos
    
    def setBulletDirection(self, direction):
        self.direction = direction
         
    def draw(self, screen):
        if self.isBulletShot == True:            
            screen_height = screen.get_height()
            screen_x = int(self.pos.x * self.scale) 
            screen_y = int(screen_height - self.pos.y * self.scale)
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), int(self.radius_m * self.scale))

        

    def update(self, dt):        
        if self.isBulletShot:
            self.pos += self.direction * self.bulletSpeed * dt
    
     