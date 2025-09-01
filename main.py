import math
import pygame
from classes.Player import Player
from classes.GameObject import GameObject
from classes.Bullet import Bullet
from classes.Enemy import Enemy

# --- Konstanter ---
circleRadius = 1  # bollradie i meter
screen_width = 1280
screen_height = 720
scale = 100  # pixlar per meter (ökad för att synas tydligare)
score = 0

player = None

obstacle = None
bullet = None

obstableHealth = 100
damageBullet = 20

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
    global score
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    
    mouse_math = None

    bullet = Bullet(pygame.Vector2(1, 2), GREEN, 0.08, pygame.Vector2(1,0).normalize(), 2, 2) # 8 pixlar
    player = Player(pygame.Vector2(1, 2), 5, pygame.Vector2(1,0).normalize(), (0, 255, 0), 0.2, bullet) # 20 pixlar
    enemy1 = Enemy(pygame.Vector2(4, 3), RED, 0.2, 100) # 0.2 m = 20 px
    enemy2 = Enemy(pygame.Vector2(6, 2), RED, 0.2, 100) # 0.2 m = 20 px
    
         
    bullet_start = pygame.Vector2(0, 0) 
    
    
    enemies = [] 
    
    enemies.append(enemy1)
    enemies.append(enemy2)

    isBulletActive = False

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Vector Demo")
    font = pygame.font.Font('freesansbold.ttf', 32)
    #create a text surface object,
    # on which text is drawn on it.


    
    
    clock = pygame.time.Clock()

    running = True        
    
    while running:
        dt = clock.tick(60) / 1000.0  # tid per frame i SEKUNDER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_SPACE: 
                    
                    for enemy in enemies.copy():
                                
                        distance = distanceVec(enemy.pos, bullet.pos).magnitude()

                        #print("distance: ", distance)
                        # print("obstacle.radius: ", obstacle.radius_m)
                        
                        if distance < enemy.radius_m + bullet.radius_m:


                            enemy.health -= player.bullet.damage
                            
                            if enemy.health <= 0:
                                enemies.remove(enemy)
                                score += 1

                                        
                    
                    if mouse_math != None:
                        direction_vec = mouse_math.__sub__(player.pos).normalize()
                        bullet.pos = direction_vec + player.pos  
                    else:
                        bullet.pos = player.pos + bullet.direction
                        
                    #bullet.pos = player.pos.copy()
                    bullet_start = bullet.pos.copy()   # 🔑 startpunkten sätts här
                    isBulletActive = True
                        
                    
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_px = pygame.mouse.get_pos()   
                mouse_math = screenToMath(*mouse_px)
                
                direction_vec = mouse_math.__sub__(player.pos).normalize()
                bullet.setBulletPos(direction_vec + player.pos)
                
                bullet.setBulletDirection(direction_vec)       
    
        
        # 🔑 flytta hit så att rörelser sker varje frame
        keys = pygame.key.get_pressed()
        player.update(keys, dt)
        
        for enemy in enemies:        
            distanceBetweenPlayer = distanceVec(enemy.pos, player.pos).magnitude()
            # print("distanceBetweenPlayer: ", distanceBetweenPlayer)
        
            if distanceBetweenPlayer <= 1:
                player.setColor(RED)
                break
            else:
                player.setColor(GREEN)

        # Rita
        screen.fill(WHITE)
        
        scoretext = font.render("Score: "+str(score), 1, (0,255,0))
        screen.blit(scoretext, (5, 10))

        player.draw(screen)
       
        # Shot
        if isBulletActive == True:
            bullet.pos += bullet.direction * bullet.bulletSpeed * dt 
            
        
            bullet_start = player.pos.copy()
        
            
            traveled = (bullet.pos - bullet_start).length()
            
            if traveled >= bullet.bulletRange:
                isBulletActive = False
            else:            
                bullet_screen = mathToScreen(bullet.pos.x, bullet.pos.y)
                pygame.draw.circle(screen, GREEN, bullet_screen, max(1, int(bullet.radius_m * scale)))
                 
        # Obstacle
        for enemy in enemies:   
            enemy.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
