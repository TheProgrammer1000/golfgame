from pygame.math import Vector2   # säkrare import
import pygame

from classes.GameObject import GameObject

class Enemy(GameObject):
    scale = 100

    def __init__(self, pos, color, radius_m, health):
        super().__init__(pos, color, radius_m)
        self.health = health
        
        
    def setColor(self, color):
        self.color = color
        
    def update(self, dt):
        pass

        
    