import math
import matplotlib.pyplot as plt
import pygame

# Constants
g = 9.81  # gravity (m/s^2)
hole_x = 55.0  # hole position in meters (x)
hole_y = 2.0   # hole position in meters (y)
hole_radius = 0.15  # hole radius in meters
circleRadius = 1  # radie i meter

screen_width = 1280
screen_height = 720

def main():
    shooting_grade = 60
    inital_hastighet = 25
    angle_rad = math.radians(shooting_grade)
    
    bounce_loses_energy = 0.7



    print(f"speed: {inital_hastighet} m/s")


    # Initial state
    current_ball_x = 0.0
    current_ball_y = 0.0

    # Tracking positions for plotting
    x_positions = []
    y_positions = []

    # PyGame setup
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Golf Ball Simulation")
    clock = pygame.time.Clock()

    scale = 10  # pixels per meter
    running = True


    current_hastighet_X = inital_hastighet * math.cos(angle_rad) # 13m/s
    current_hastighet_Y = inital_hastighet * math.sin(angle_rad) # 7.5m/s
    
    


    while running:
        dt = clock.tick(60) / 1000  # delta time in seconds

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(WHITE)
        
        wall_x = 300
        # Väg
        pygame.draw.line(screen, RED, (wall_x, 400), (wall_x, 600), 3)

        
      
        # räknar ut nya positioner och hastigheten på Y
        current_ball_x += current_hastighet_X * dt # first frame 0.208, secound frame = 0.208 + 13 * 0.016
        current_hastighet_Y -= g * dt # Här vill vi beräkna den nya hastigheten med gravitationen        
        current_ball_y += current_hastighet_Y * dt
        
        
        
        if current_ball_y < 0:
            current_ball_y = 0
            current_hastighet_Y = -current_hastighet_Y * bounce_loses_energy

        # # Track positions for plotting
        x_positions.append(current_ball_x)
        y_positions.append(current_ball_y)

        # # Draw ball (converted to pixels)
        ball_x_pixel = int(current_ball_x * scale)
        ball_y_pixel = int(mathConvertToGame(current_ball_y * scale))
        pygame.draw.circle(screen, RED, (ball_x_pixel, ball_y_pixel), int(circleRadius * scale))


        # Träffat vägen, kollar att bollen_y också är i den höjden från 400 till 600 där väggen är. Och kollar om bollen_x_pos - wall_x <= circleRadius * scale då vet vi att den nuddat!
        if abs(ball_x_pixel - wall_x) <= circleRadius * scale and 400 <= ball_y_pixel <= 600:
            print("Träffat en väg!")
            
            
            time_when_ball_touch_wall = (wall_x / scale) / current_hastighet_X
            
            print("time_when_ball_touch_wall: ", time_when_ball_touch_wall)
            
            YposWhenHit = current_hastighet_Y * time_when_ball_touch_wall - (0.5 * g) * (time_when_ball_touch_wall**2)
            
            Y_hastighet_when_hit = current_hastighet_Y + (-g * time_when_ball_touch_wall) 
            
            #newAngle = math.atan(Y_hastighet_when_hit / (current_hastighet_X))
            #print("newAngle i grader:", math.degrees(newAngle))
            
            newAngle2 = math.atan2(Y_hastighet_when_hit, current_hastighet_X)
            
            
            angle_deg = math.degrees(newAngle2)
            
            if angle_deg < 0:
                angle_deg += 360

            ball_new_angle_after_hit_wall = angle_deg
            
            new_angle_rad = math.radians(ball_new_angle_after_hit_wall)
            
            
            total_hastighet = math.sqrt(Y_hastighet_when_hit**2 + current_hastighet_X**2)
            total_hastighet *= bounce_loses_energy
            
            
            current_hastighet_X = -total_hastighet * math.cos(new_angle_rad)
            current_hastighet_Y = total_hastighet * math.sin(new_angle_rad) # 7.5m/s
        
            


        # Check if ball hit the target
     
        pygame.display.flip()

    # Plot trajectory after simulation ends
    plt.plot(x_positions, y_positions)
    plt.xlabel("Meter i X-led")
    plt.ylabel("Meter i Y-led")
    plt.title("Golfslagets bana")
    plt.grid()
    plt.show()

    pygame.quit()

def calc_pos_from_hole_px(ball_x, ball_y, scale):
    """Calculate distance between ball and hole in pixels."""
    ball_x_px = ball_x * scale
    ball_y_px = mathConvertToGame(ball_y * scale)
    
    
    hole_x_px = hole_x * scale
    hole_y_px = mathConvertToGame(hole_y * scale)
    dx = ball_x_px - hole_x_px
    dy = ball_y_px - hole_y_px
    return math.sqrt(dx**2 + dy**2)

def mathConvertToGame(y):
    """Convert mathematical y-coordinate to PyGame's coordinate system."""
    return screen_height - y

if __name__ == "__main__":
    main()