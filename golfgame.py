import math
import matplotlib.pyplot as plt

# Example file showing a basic pygame "game loop"
import pygame

g = 9.81 # graviation 


#print("ball_xMeter_on_ground: ", ball_xMeter_on_ground)
# print(ball_hit_ground_t)
 
# pygame setup
hole_x = 550
hole_y = 20
 
hole_radius = 0.15
circleRadius = 1

screen_width = 1280
screen_height = 720
    
def main():
    
    shooting_grade = int(input("Skriv in graden som du ska skjuta: ")) # 60

    v0_speed = int(input("Skriv in hastighetn du vill skjuta med: ")) # 22 m/s 
    angle_deg = math.radians(shooting_grade)

    x_pos_angle = round(math.cos(angle_deg), 3)
    y_pos_angle = round(math.sin(angle_deg), 3)

    print("speed: ", v0_speed, "m/s \n")

    vox = v0_speed * x_pos_angle
    voy = v0_speed * y_pos_angle


    print("vox: ", vox, "m/s i X-axel")
    print("voy: ", voy ,"m/s i Y-axel\n")

 
    
    x_positions = []
    y_positions = []        
    seconds = 0
    
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    
    YELLOW = (0, 255, 0)
 

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))   
    clock = pygame.time.Clock()
    
    
    
    
    new_ball_posX = 0
    new_ball_posY = 0

    
    running = True

    scale = 10

    while running:
        
        dt = clock.tick(60) / 1000  # dt i sekunder (tid mellan frames)
        seconds += dt  # uppdatera tiden med verklig tid som gått

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill(WHITE)  # Fyll bakgrunden       

        
        # drawing cirle
        pygame.draw.circle(screen, YELLOW, (hole_x, mathConvertToGame(hole_y)), circleRadius * scale) # (20, 0) as in math
        
       
        
        new_ball_posX = new_posX(vox, dt)
        new_ball_posY = new_posY(voy, dt)
        
        x_pixel = int(new_ball_posX * scale)
        y_pixel = int(mathConvertToGame(new_ball_posY * scale))  # invertera y-led
        
        
        distFromhole = calc_pos_from_hole_px(vox, voy, seconds, scale)

        if distFromhole <= (circleRadius * scale):
            print("Målet är träffats!")
            break
    
        if new_ball_posY <= (circleRadius * 2):
            new_ball_posY = circleRadius

        
        
   
        
        # if new_ball_posY < 0:      # träffat marken            
        #     print("new_ball_posX: ", new_ball_posX)
        #     print("Träffat marken")
        #     break

        
        print("new_ball_posX: ", new_ball_posX)
        print("new_ball_posY: ", new_ball_posY)
        
        
        pygame.draw.circle(screen, RED, (x_pixel, y_pixel), circleRadius * scale)


        x_positions.append(new_ball_posX)
        y_positions.append(new_ball_posY)
        
     
        
        pygame.display.update()
        

    
    

    

   
        
    
    # 🔽 När loopen är klar – rita hela banan
    plt.plot(x_positions, y_positions)
    plt.xlabel("Meter i X-led")
    plt.ylabel("Meter i Y-led")
    plt.title("Golfslagets bana")
    plt.grid()
    plt.show()

    
    
    
    # med vinkeln 60 så med hastigheten 22 m / s
    # då efter 2 sekunder kommer pos_X vara 22 och pos_Y vara 18.484
    
    # dt = calc_pos_from_hole(seconds)
    

    # #print("dt: ", dt)
    
    # if(calc_pos_from_hole(dt) <= hole_radius) :
    #     print("Hole in one!")



def new_posY(voy ,t) :
    new_pos_Y = round((voy * t) - 1 / 2 * (g * (t**2)), 3) #y(t) = y₀ + v₀y * t - (1/2)gt²
    #print('new_pos_Y: ', new_pos_Y)                                      
                                                                                
    return new_pos_Y
  
def new_posX(vox,t) :
    new_pos_X = vox * t   #x(t) = x₀ + v₀x * t
    #print('new_pos_X: ', new_pos_X)
    return new_pos_X


def calc_pos_from_hole(vox, voy, t) :    
    dx = (new_posX(vox, t) - hole_x) ** 2
    dy = (new_posY(voy, t) - hole_y) ** 2

    dt = math.sqrt(dx + dy)
    
    return dt


def calc_pos_from_hole_px(vox, voy, t, scale):
    # Bollens pixelposition
    ball_x_px = new_posX(vox, t) * scale
    ball_y_px = mathConvertToGame(new_posY(voy, t) * scale)
    
    # Hålets pixelposition
    hole_x_px = hole_x
    hole_y_px = mathConvertToGame(hole_y)
    
    # Avstånd i pixlar
    dx = ball_x_px - hole_x_px
    dy = ball_y_px - hole_y_px
    return math.sqrt(dx**2 + dy**2)

  
def secounds_ball_toGround(voy) :
   return voy / (0.5 * g) # stop here
  
def new_x_pos_after_curve(vox): 
    return vox * secounds_ball_toGround()

def mathConvertToGame(y):
    return (screen_height - y) - circleRadius

if __name__ == "__main__":
    main()
  