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
        
    def update(self, dt):        
        print(self.pos)
        if self.isBulletShot:
            self.pos += self.direction * self.bulletSpeed * dt
            
            
            
            # bullet_screen = mathToScreen(bullet.pos.x, bullet.pos.y)
            # pygame.draw.circle(screen, GREEN, bullet_screen, max(1, int(bullet.radius_m * scale)))
        
            # bullet_start = player.pos.copy()
        
            
            # traveled = (bullet.pos - bullet_start).length()
            
            # if traveled >= bullet.bulletRange:
            #     isBulletActive = False
            # else:            
            #     bullet_screen = mathToScreen(bullet.pos.x, bullet.pos.y)
            #     pygame.draw.circle(screen, GREEN, bullet_screen, max(1, int(bullet.radius_m * scale)))
    
     