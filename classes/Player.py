from pygame.math import Vector2   # säkrare import
import pygame

from classes.GameObject import GameObject
from classes.Bullet import Bullet   




class Player(GameObject):
    def __init__(self, pos, movement_speed, direction, color, radius_m, bullet):
        super().__init__(pos, color, radius_m)
        self.direction = Vector2(direction)
        self.bullet = bullet
        self.movement_speed = movement_speed
    
    def setDirection(self, theta):
        self.direction = theta 
    
    
    # def shootBullet():
        
    def update(self, keys, dt):
        if keys[pygame.K_w]:
            self.pos.y += self.movement_speed * dt
        if keys[pygame.K_s]:
            self.pos.y -= self.movement_speed * dt
        if keys[pygame.K_d]:
            self.pos.x += self.movement_speed * dt
        if keys[pygame.K_a]:
            self.pos.x -= self.movement_speed * dt
            
            
                
            
        
    