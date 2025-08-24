from pygame.math import Vector2   # säkrare import
import pygame

class GameObject:
    scale = 100

    def __init__(self, pos, color, radius_m):
        self.pos = Vector2(pos)
        self.color = color
        self.radius_m = radius_m
        
    def setColor(self, color):
        self.color = color
        
    def update(self, dt):
        pass
    
    def draw(self, screen):
        """Rita objektet på skärmen
           Vi gångar med scale för att få från meter vi räknar med till pixlar
           screen_y är skärmen är Y på toppen till vänster
           Så då tar vi - Y hela skärmen så vi ändrar rikningen så det blir rätt mattematiskt
        """
        screen_height = screen.get_height()
        
        screen_x = int(self.pos.x * self.scale) 
        screen_y = int(screen_height - self.pos.y * self.scale)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), int(self.radius_m * self.scale))

        
    