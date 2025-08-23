import math
import pygame
from classes.Player import Player
from classes.GameObject import GameObject

# --- Konstanter ---
circleRadius = 1  # bollradie i meter
screen_width = 1280
screen_height = 720
scale = 100  # pixlar per meter (ökad för att synas tydligare)

player = None

obstacle = None



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
    
    
    theta = 20
    
    # Player & obstacle position i meter    
    player = Player(pygame.Vector2(1, 2), pygame.Vector2(1, 1), pygame.Vector2(1,0).normalize(), (0, 255, 0), 8)
    obstacle = GameObject(pygame.Vector2(4, 3), RED, 8)


    # print("player.pos", player.pos)
    # print("player.vel", player.vel)
    # print("player.direction", player.direction)

    bullet_array = []
    bullet_speed = 2
    bullet_pos = pygame.Vector2(player.pos)
    isBulletActive = False
    
    bullet_velocity = player.direction
    
    
    
    print("bullet_velocity: ", bullet_velocity)
     


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
                    bullet_pos = player.pos.__add__(bullet_velocity)
                    isBulletActive = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_px = pygame.mouse.get_pos()   
                mouse_math = screenToMath(*mouse_px)               
                
                    
    
        distanceBetweenPlayer = distanceVec(obstacle.pos, player.pos).magnitude()
        
    
        if distanceBetweenPlayer <= 1:
            # print("INOM RADIEN!")
            player.setColor(RED)
        else:
            player.setColor(GREEN)

        # Rita
        screen.fill(WHITE)

        # Player
        player_screen = mathToScreen(player.pos.x, player.pos.y)
        pygame.draw.circle(screen, player.color, player_screen, player.radius)
       
    
        
        # Shot
        if isBulletActive == True:
            bullet_screen = mathToScreen(bullet_pos.x, bullet_pos.y)
            pygame.draw.circle(screen, GREEN, bullet_screen, 15)

            isBulletActive = False
                 

        # Obstacle
        obs_screen = mathToScreen(obstacle.pos.x, obstacle.pos.y)
        pygame.draw.circle(screen, RED, obs_screen, obstacle.radius)


        
        # Rita riktning som linje (valfritt)
        # pygame.draw.line(screen, (0,0,255), player_screen, obs_screen, 2)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
