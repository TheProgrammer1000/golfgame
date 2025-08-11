import math
import matplotlib.pyplot as plt
import pygame

# Constants
g = 9.81  # gravity (m/s^2)
hole_x = 55.0  # hole position in meters (x)
hole_y = 2.0   # hole position in meters (y)
hole_radius = 0.15  # hole radius in meters
circleRadius = 1  # radie i meter

screen_width = 1920
screen_height = 1280
scale_line = 10

def main():
    shooting_grade = 60
    inital_hastighet = int(input("Skriv in farten: "))#30
    angle_rad = math.radians(shooting_grade)

    bounce_loses_energy = 0.90

    print(f"speed: {inital_hastighet} m/s")

    current_ball_x = 0.0
    current_ball_y = 0.0

    x_positions = []
    y_positions = []

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Golf Ball Simulation")
    clock = pygame.time.Clock()

    scale = 10  # pixels per meter

    current_hastighet_X = inital_hastighet * math.cos(angle_rad)
    current_hastighet_Y = inital_hastighet * math.sin(angle_rad)

    x1 = 20
    x2 = screen_width
    
    ground_y_px = screen_height - 0 * scale  # 0 meter i PyGame-pixel

    # Sätt linjen till ground_y_px (t.ex. 700) i pixlar
    # (flyttad högre upp för att ytan ska vara längre upp på skärmen)
    y1 = (ground_y_px - 20)
    y2 = (ground_y_px - 120)  # lite lutning
    
    line_start = (x1, y1)
    line_end = (x2, y2)

    simulation_time = 0.0

    running = True

    while running:
        dt = clock.tick(60) / 1000  # Sekunder

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Vi gör en while-loop för att hantera att dt kan behöva delas upp om kollision sker
        time_left = dt

        while time_left > 0.e3:
            # Kolla kollisionstid med linjen för nuvarande bana och hastighet
            result = calcBallCollision(
                x1, y1, x2, y2,
                current_ball_x, current_ball_y,
                current_hastighet_X, current_hastighet_Y,
                scale
            )
            
            print('result: ', result)
            
            print('result[0]: ', result[0])
            print('result[2]: ', result[2])
            
            if result and result[0]:  # om det finns träffar (förhindrar ValueError)
                collisions, hx, hy, k = result
                
                     
                print('hx', hx)
                print('hy', hy)
                print('k', k)

                # Hitta närmsta framtida kollisionstid
                t_hit, cx, cy = min(collisions, key=lambda c: c[0])

                # Om kollision sker inom time_left
                if 0 < t_hit <= time_left:
                    # 1) Flytta fram till kollisionen exakt
                    current_ball_x = cx  # sätt till kollisionspunkt
                    current_ball_y = cy
                    
                    # Uppdatera hastighet vid kollisionspunkt
                    current_hastighet_X, current_hastighet_Y = calcBallOut(current_hastighet_X, current_hastighet_Y, k)

                    current_hastighet_X = current_hastighet_X * bounce_loses_energy
                    current_hastighet_Y = current_hastighet_Y * bounce_loses_energy

                    simulation_time += t_hit
                    time_left -= t_hit

                    # Vi slutar röra bollen här i detta steg (ingen extra rörelse efter kollisionen)
                    time_left = 0

                else:
                    # Ingen kollision inom detta tidssteg - uppdatera hela dt normalt
                    current_ball_x += current_hastighet_X * time_left
                    current_hastighet_Y -= g * time_left
                    current_ball_y += current_hastighet_Y * time_left

                    simulation_time += time_left
                    time_left = 0
            else:
                # Ingen kollision alls - uppdatera hela dt normalt
                current_ball_x += current_hastighet_X * time_left
                current_hastighet_Y -= g * time_left
                current_ball_y += current_hastighet_Y * time_left

                simulation_time += time_left
                time_left = 0

        # Spara för plotten
        x_positions.append(current_ball_x)
        y_positions.append(current_ball_y)

        # Rita grafiskt
        screen.fill(WHITE)
        pygame.draw.line(screen, RED, line_start, line_end, scale_line)

        ball_x_pixel = int(current_ball_x * scale)
        ball_y_pixel = int(mathConvertToGame(current_ball_y * scale))

        pygame.draw.circle(screen, RED, (ball_x_pixel, ball_y_pixel), int(circleRadius * scale))

        pygame.display.flip()

    # Visa plott efter PyGame stängs
    plt.plot(x_positions, y_positions)
    plt.xlabel("Meter i X-led")
    plt.ylabel("Meter i Y-led")
    plt.title("Golfslagets bana")
    plt.grid()
    plt.show()

    pygame.quit()

def calcBallOut(hx, hy, k):
    print(f"Hastigheter: hx={hx:.2f}, hy={hy:.2f}, lutning k={k:.3f}")

    if hx == 0:
        degreeBallin = math.atan2(hy, 0)
    else:
        degreeBallin = math.atan2(hy, hx)
    
    inBallin_deg = math.degrees(degreeBallin)
    print("degreeBallin (grader):", inBallin_deg)

    inObstable = math.atan(k)
    inObstable_deg = math.degrees(inObstable)
    
    print("inObstable_deg (grader):", inObstable_deg)

    outDegreeBall_deg = 2 * inObstable_deg - inBallin_deg
    hypotenusan = math.sqrt(hx**2 + hy**2)
    
    outDegreeBall_rad = math.radians(outDegreeBall_deg)
    new_current_hastighet_X = hypotenusan * math.cos(outDegreeBall_rad)
    new_current_hastighet_Y = hypotenusan * math.sin(outDegreeBall_rad)
    
    return new_current_hastighet_X, new_current_hastighet_Y

        

def calcBallCollision(obstacle_x1_px, obstacle_y1_px,
                      obstacle_x2_px, obstacle_y2_px,
                      current_ball_x_m, current_ball_y_m,
                      ball_hx_mps, ball_hy_mps,
                      scale):

    """
    obstacle_x1_px, obstacle_y1_px, obstacle_x2_px, obstacle_y2_px:
        Väggens koordinater i pixlar (PyGame-format)
    current_ball_x_m, current_ball_y_m:
        Bollens position i meter (matematiska koordinater)
    ball_hx_mps, ball_hy_mps:
        Bollens hastighet i m/s (X och Y)
    scale:
        Antal pixlar per meter
    g:
        Gravitation i m/s²
    """

    # 1️⃣ Konvertera från PyGame-pixlar till matematiska meter-koordinater
    # PyGame har (0,0) i övre vänstra hörnet → vi måste vända Y-axeln
    obstacle_x1 = obstacle_x1_px / scale
    obstacle_y1 = (screen_height - obstacle_y1_px) / scale + circleRadius
    obstacle_y2 = (screen_height - obstacle_y2_px) / scale + circleRadius
    obstacle_x2 = obstacle_x2_px / scale

    isOnlyHorizontal = False

    k = 0


    # Kolla om linjen är vertikal
    if obstacle_y1 == obstacle_y2 and obstacle_x1 != obstacle_x2:
        # Specialhantering för vertikal linje
        # T.ex. sätt k = None eller en flagga
        isOnlyHorizontal = True
        k = 0
    else:
        k = (obstacle_y2 - obstacle_y1) / (obstacle_x2 - obstacle_x1)

    # 2️⃣ Beräkna linjens ekvation: y = kx + m
    m = obstacle_y1 - k * obstacle_x1                              # skärning med y-axeln


    # 3️⃣ Bollens bana i meter: 
    # x(t) = x0 + vx * t
    # y(t) = y0 + vy * t - 0.5 * g * t²
    # För kollision måste bollens bana och linjens ekvation vara lika:
    # y0 + vy*t - 0.5*g*t² = k*(x0 + vx*t) + m

    # 4️⃣ Flytta över allt till ena sidan så vi får en andragradsekvation i t:
    # (-0.5*g)*t² + (vy - k*vx)*t + (y0 - k*x0 - m) = 0
    
    # Formeln: a*t2 + b*t + c = 0 
    if isOnlyHorizontal != True:
        a = -0.5 * g
        b = ball_hy_mps - k * ball_hx_mps
        c = current_ball_y_m - k * current_ball_x_m - m
        

        # 5️⃣ Diskriminanten D = b² - 4ac
        disc = b**2 - 4*a*c
        if disc < 0:
            return []  # ingen skärning alls

        sqrt_disc = math.sqrt(disc)
        
        # lösning för andragradsekvationen:
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)

        collision_times = []
        for t in (t1, t2): 
            # vi ville bara kolla om tiden är större än 0
            if t > 0:  # bara framtida träffar
                # Beräkna skärningspunktens koordinater
                
                # Samma som räkna x-positionen x(t) = hx * t
                cx = current_ball_x_m + ball_hx_mps * t
                
                # Samma som räkna y-positionen y(t) = hy * t - 4.905 * t^2
                cy = current_ball_y_m + ball_hy_mps * t - 0.5 * g * t**2

                # Kontrollera att punkten ligger inom väggsegmentet
                if (min(obstacle_x1, obstacle_x2) <= cx <= max(obstacle_x1, obstacle_x2) and
                    min(obstacle_y1, obstacle_y2) <= cy <= max(obstacle_y1, obstacle_y2)):
                    collision_times.append((t, cx, cy))

        if collision_times:
            return collision_times, ball_hx_mps, ball_hy_mps, k
        else:
            return [], None, None, None
        
        

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
