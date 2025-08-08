import math
import matplotlib.pyplot as plt
import pygame

# Constants
g = 9.81  # gravity (m/s^2)
hole_x = 55.0  # hole position in meters (x)
hole_y = 2.0   # hole position in meters (y)
hole_radius = 0.15  # hole radius in meters
circleRadius = 1  # ball radius in meters

screen_width = 1280
screen_height = 720

def main():
    shooting_grade = int(input("Skriv in graden som du ska skjuta: "))  # e.g., 60
    v0_speed = int(input("Skriv in hastigheten du vill skjuta med: "))  # e.g., 22 m/s
    angle_rad = math.radians(shooting_grade)

    # Calculate initial velocity components
    vox = v0_speed * math.cos(angle_rad)
    voy = v0_speed * math.sin(angle_rad)

    print(f"speed: {v0_speed} m/s")
    print(f"vox: {vox:.3f} m/s i X-axel")
    print(f"voy: {voy:.3f} m/s i Y-axel\n")

    # Physics parameters
    restitution = 0.8  # bounce energy retention (80%)
    friction_x = 0.95  # horizontal friction during bounce

    # Initial state
    current_x = 0.0
    current_y = 0.0
    current_vx = vox
    current_vy = voy

    # Tracking positions for plotting
    x_positions = []
    y_positions = []

    # PyGame setup
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (0, 255, 0)
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Golf Ball Simulation")
    clock = pygame.time.Clock()

    scale = 10  # pixels per meter
    running = True
    hit_target = False

    while running:
        dt = clock.tick(60) / 1000  # delta time in seconds

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(WHITE)

        # Draw hole (converted to pixels)
        hole_x_pixel = hole_x * scale
        hole_y_pixel = mathConvertToGame(hole_y * scale)
        pygame.draw.circle(screen, YELLOW, (int(hole_x_pixel), int(hole_y_pixel)), int(circleRadius * scale))

        # Update physics
        current_vy -= g * dt  # apply gravity
        current_x += current_vx * dt
        current_y += current_vy * dt

        # Bounce when hitting the ground
        if current_y <= 0:
            current_vy = -current_vy * restitution  # reverse and dampen vertical velocity
            current_vx *= friction_x  # apply horizontal friction
            current_y = circleRadius * 2  # reset to ground level

            # Stop if bounce is negligible
            if abs(current_vy) < 0.2:
                current_vy = 0

        # Apply rolling friction when on ground and not bouncing
        if current_y == 0 and current_vy == 0:
            current_vx *= 0.99  # rolling friction
            if abs(current_vx) < 0.01:
                current_vx = 0

        # Track positions for plotting
        x_positions.append(current_x)
        y_positions.append(current_y)

        # Draw ball (converted to pixels)
        ball_x_pixel = int(current_x * scale)
        ball_y_pixel = int(mathConvertToGame(current_y * scale))
        pygame.draw.circle(screen, RED, (ball_x_pixel, ball_y_pixel), int(circleRadius * scale))

        # Check if ball hit the target
        dist = calc_pos_from_hole_px(current_x, current_y, scale)
        if dist <= circleRadius * scale:
            hit_target = True
            print("Målet är träffats!")
            running = False

        # Stop if ball is effectively stopped
        if current_y == 0 and abs(current_vy) == 0 and abs(current_vx) < 0.01:
            print("Bollen har stannat.")
            running = False

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