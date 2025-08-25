from pygame.math import Vector2   # säkrare import
from classes.GameObject import GameObject

class Bullet(GameObject):
    def __init__(self, pos, color, radius_m, direction):
        super().__init__(pos, color, radius_m)
        self.direction = Vector2(direction)
        self.isBulletShot = False
        
    def setBulletPos(self, pos):
        self.pos = pos
        
    def update(self, obstacle, dt):
        distance = obstacle.pos - self.pos
        
        getBulletLength = distance.magnitude()

        print("distance: ", distance)
        # print("obstacle.radius: ", obstacle.radius_m)
        
        if distance < obstacle.radius_m + self.radius_m:
            print("Collision")
                            
        # direction_vec = mouse_math.__sub__(self.pos).normalize()
        self.pos = self.direction + self.pos  
      
    
    