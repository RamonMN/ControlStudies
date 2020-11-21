import pygame
import math

width, height = 800, 600
SIZE = (width, height)
pygame.init()
pygame.display.set_caption('Pendulum Simulation')
fps = 30
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Constants
mass = 100       
length = 200
gravity = 9.8
delta = 0.03                                        # Friction coefficient
ball_radius = math.sqrt(mass/(math.pi*0.065))       # Ball radius with respect to its mass and density

# Angle variables: alpha = omega_d = theta_dd
theta = math.pi/2
omega = 0
alpha = 0

starting_point = (int(width/2), int(height/4))  # Pendulum base

x_offset = starting_point[0]
y_offset = starting_point[1]


run = True
while run:
    clock.tick(fps)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    alpha = -(gravity/length)*math.sin(theta) - delta*omega     # System differential equation

    x = float(length*math.sin(theta) + x_offset)                # Updating mass x
    y = float(length*math.cos(theta) + y_offset)                # Updating mass y

    omega += alpha      # Integrating alpha over time
    theta += omega      # Integrating omega over time

    pygame.draw.line(screen, white, starting_point, (x, y), 5)                   # Drawing the pendulum line
    pygame.draw.circle(screen, (40, 255, 30), (int(x), int(y)), ball_radius)     # Drawing the pendulum mass

    pygame.display.update()

pygame.quit()
