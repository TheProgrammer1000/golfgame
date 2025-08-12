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


    ground_px_from_bottom = 100  # Hur långt från botten i pixlar marken ligger

    x1 = 200
    x2 = screen_width
    
    # Sätt linjen till ground_y_px (t.ex. 700) i pixlar
    # (flyttad högre upp för att ytan ska vara längre upp på skärmen)
    y1 = (screen_height - ground_px_from_bottom)
    y2 = (screen_height)  # lite lutning
    
    ground_y_px = screen_height - 0 * scale  # 0 meter i PyGame-pixel

    # Exempel: startpunkt (bollens position på skärmen)
    start_pos = (ball_x_pixel, ball_y_pixel)
    # Vid musrörelse eller musklick och drag:
    mouse_pos = pygame.mouse.get_pos()

    # Räkna ut vektor från start till mus
    vec_x = mouse_pos[0] - start_pos[0]
    vec_y = mouse_pos[1] - start_pos[1]

    
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
            
            
            if result and result[0]:  # om det finns träffar (förhindrar ValueError)
                collisions, hx, hy, k = result
                    
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
        
        # Konvertera linjens startpunkt från pixlar till meter
        line_x1_m = x1 / scale
        # PyGame har y=0 högst upp, vi vill ha matematiskt koordinatsystem där y=0 längst ner,
        # därför inverterar vi y-koordinaten: (screen_height - y1)
        line_y1_m = (screen_height - y1) / scale

        # Konvertera linjens slutpunkt från pixlar till meter, på samma sätt
        line_x2_m = x2 / scale
        line_y2_m = (screen_height - y2) / scale

       

        # Om linjen inte är vertikal (dvs. x1 och x2 är inte lika)
        
        
        # Så enkelt sagt vi beräknar när bollen höjd Y når marken med den lutningen dessa Y och sedan om bollen är under
        # denna mark ytan så sätter vi den till positionen ovanförmarkytan + circleRadius och hastigheten på y blir omvänt och x hastigheten påverkas bara av bounce_loses_energy
        
        if line_x2_m == line_x1_m:
            # Vertikal vägg
            vertical_x = line_x1_m
            ball_edge_x = current_ball_x + circleRadius if current_hastighet_X > 0 else current_ball_x - circleRadius

            # Kolla om bollen tränger in i väggen
            if (current_hastighet_X > 0 and ball_edge_x > vertical_x) or (current_hastighet_X < 0 and ball_edge_x < vertical_x):
                if min(line_y1_m, line_y2_m) <= current_ball_y <= max(line_y1_m, line_y2_m):
                    # Sätt bollen precis vid väggen
                    if current_hastighet_X > 0:
                        current_ball_x = vertical_x - circleRadius
                    else:
                        current_ball_x = vertical_x + circleRadius

                    # Studs: vänd x-hastigheten och minska med energiförlust
                    current_hastighet_X = -current_hastighet_X * bounce_loses_energy
                    current_hastighet_Y = current_hastighet_Y * bounce_loses_energy

        else:
            # Lutande eller horisontell yta
            k_line = (line_y2_m - line_y1_m) / (line_x2_m - line_x1_m)
            m_line = line_y1_m - k_line * line_x1_m

            ground_y_at_ball_x = k_line * current_ball_x + m_line
            ball_bottom_y = current_ball_y - circleRadius

            if ball_bottom_y < ground_y_at_ball_x and current_hastighet_Y < 0:
                # Sätt bollen på marken
                current_ball_y = ground_y_at_ball_x + circleRadius

                # Studs: vänd y-hastigheten och minska med energiförlust
                current_hastighet_Y = -current_hastighet_Y * bounce_loses_energy
                current_hastighet_X = current_hastighet_X * bounce_loses_energy
                
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
    #print(f"Hastigheter: hx={hx:.2f}, hy={hy:.2f}, lutning k={k:.3f}")

    if k is None:  # Vertikal linje
        new_hx = -hx  # reflektera hastighet i x-led
        new_hy = hy   # behåll hastighet i y-led
        return new_hx, new_hy

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
    obstacle_x1 = obstacle_x1_px / scale - circleRadius
    obstacle_y1 = (screen_height - obstacle_y1_px) / scale + circleRadius
    obstacle_y2 = (screen_height - obstacle_y2_px) / scale + circleRadius
    obstacle_x2 = obstacle_x2_px / scale - circleRadius

    # Kolla om linjen är vertikal
    if obstacle_y1 == obstacle_y2 and obstacle_x1 != obstacle_x2:
        # Horisontell linje
        k = 0
        m = obstacle_y1  # y = m

        a = -0.5 * g
        b = ball_hy_mps
        c = current_ball_y_m - m

        disc = b**2 - 4 * a * c
        if disc < 0:
            return [], None, None, None

        sqrt_disc = math.sqrt(disc)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)

        collision_times = []
        for t in (t1, t2):
            if t > 0:
                cx = current_ball_x_m + ball_hx_mps * t
                cy = current_ball_y_m + ball_hy_mps * t - 0.5 * g * t**2

                # Kolla att collision sker inom linjesegmentet på x-axeln
                if min(obstacle_x1, obstacle_x2) <= cx <= max(obstacle_x1, obstacle_x2):
                    collision_times.append((t, cx, cy))

        if collision_times:
            return collision_times, ball_hx_mps, ball_hy_mps, k
        else:
            return [], None, None, None
    elif obstacle_x1 == obstacle_x2:
        # Vertikal linje
        k = None  # eller annan markör för vertikal linje

        # Beräkna tid då x(t) = obstacle_x1
        if ball_hx_mps != 0:
            t = (obstacle_x1 - current_ball_x_m) / ball_hx_mps
            if t > 0:
                y_at_t = current_ball_y_m + ball_hy_mps * t - 0.5 * g * t**2
                if min(obstacle_y1, obstacle_y2) <= y_at_t <= max(obstacle_y1, obstacle_y2):
                    return [(t, obstacle_x1, y_at_t)], ball_hx_mps, ball_hy_mps, k
        return [], None, None, None

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
