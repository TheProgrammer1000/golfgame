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
    
    def shoot(self):
        self.bullet.pos = self.pos.copy()            # skott börjar vid spelarens nuvarande position
        self.bullet.spawn_pos = self.pos.copy()      # spara spawn-position för range-beräkning
        # sätt korrekt riktning (normera om nollvektor undviks)
        if self.direction.length_squared() != 0:
            self.bullet.direction = self.direction.normalize()
        else:
            self.bullet.direction = Vector2(1, 0)    # fallback-riktning
        self.bullet.isBulletShot = True
        print("Skjuter från", self.bullet.spawn_pos)
        
    def shootRange(self):
        traveled = (self.bullet.pos - self.bullet.spawn_pos).length()
        
        print("self.bullet.pos: ", self.bullet.pos)
        
        if traveled >= self.bullet.bulletRange:
            print("HÄÄÄÄR")
            self.bullet.isBulletShot = False

     
    def update(self, keys, dt):
        if keys[pygame.K_w]:
            self.pos.y += self.movement_speed * dt
        if keys[pygame.K_s]:
            self.pos.y -= self.movement_speed * dt
        if keys[pygame.K_d]:
            self.pos.x += self.movement_speed * dt
        if keys[pygame.K_a]:
            self.pos.x -= self.movement_speed * dt
            
        if self.bullet.isBulletShot == True:
            self.shootRange()
        
        
            
            
                
            
        
    