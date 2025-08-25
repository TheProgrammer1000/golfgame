import math
import pygame
from classes.Player import Player
from classes.GameObject import GameObject
from classes.Bullet import Bullet

# --- Konstanter ---
circleRadius = 1  # bollradie i meter
screen_width = 1280
screen_height = 720
scale = 100  # pixlar per meter (ökad för att synas tydligare)

player = None

obstacle = None
bullet = None


def screenToMath(x, y):
    """Omvandla skärm-pixlar till matematiska koordinater (meter)."""
    math_x = x / scale
    math_y = (screen_height - y) / scale
    return pygame.Vector2(math_x, math_y)


# --- Hjälpfunktioner ---
def mathToScreen(x, y):
    """
    Omvandla matematiska koordinater (m) till Pygame-skärmkoordinater (px).
    Origo = nedre vänstra hörnet.
    """
    screen_x = int(x * scale)
    screen_y = int(screen_height - y * scale)
    

    return (screen_x, screen_y)


def distanceVec(v1, v2):
    return v1 - v2

def addVec(player, vec):
    return player + vec


# --- Huvudprogram ---
def main():
    
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    
    
    mouse_math = None

    bullet = Bullet(pygame.Vector2(1, 2), GREEN, 0.08, pygame.Vector2(1,0).normalize()) # 8 pixlar
    player = Player(pygame.Vector2(1, 2), pygame.Vector2(7, 7), pygame.Vector2(1,0).normalize(), (0, 255, 0), 0.2, bullet) # 20 pixlar
    obstacle = GameObject(pygame.Vector2(4, 3), RED, 0.2) # 0.2 m = 20 px

    isBulletActive = False

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Vector Demo")
    clock = pygame.time.Clock()

    running = True        
    
    while running:
        dt = clock.tick(60) / 1000.0  # tid per frame i SEKUNDER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    player.pos.x += player.vel.x * dt
                if event.key == pygame.K_a:
                    player.pos.x -= player.vel.x * dt
                if event.key == pygame.K_w:
                    player.pos.y += player.vel.y * dt
                if event.key == pygame.K_s:
                    player.pos.y -= player.vel.y * dt
                if event.key == pygame.K_SPACE:                                      
                    distance = distanceVec(obstacle.pos, bullet.pos).magnitude()

                    print("distance: ", distance)
                    # print("obstacle.radius: ", obstacle.radius_m)
                    
                    if distance < obstacle.radius_m + bullet.radius_m:
                        print("Collision")
                                        
                    if mouse_math != None:
                        direction_vec = mouse_math.__sub__(player.pos).normalize()
                        bullet.pos = direction_vec + player.pos  
                    else:
                        bullet.pos = player.pos + bullet.direction
                        
                    isBulletActive = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_px = pygame.mouse.get_pos()   
                mouse_math = screenToMath(*mouse_px)
                
                direction_vec = mouse_math.__sub__(player.pos)
                bullet.setBulletPos(direction_vec + player.pos)                    
    
        distanceBetweenPlayer = distanceVec(obstacle.pos, player.pos).magnitude()
        # print("distanceBetweenPlayer: ", distanceBetweenPlayer)
    
        if distanceBetweenPlayer <= 1:
            player.setColor(RED)
        else:
            player.setColor(GREEN)

        # Rita
        screen.fill(WHITE)

        player.draw(screen)
       
       
       
        # Shot
        if isBulletActive == True:
            bullet_screen = mathToScreen(bullet.pos.x, bullet.pos.y)
            pygame.draw.circle(screen, GREEN, bullet_screen, max(1, int(bullet.radius_m * scale)))

            isBulletActive = False
                 
        # Obstacle
        obstacle.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
