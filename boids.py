import pygame
import math
import random


boids = []

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.random() * 2 - 1
        self.vy = random.random() * 2 - 1
    
margin = 160
turnfactor = 0.8
visual_range = 50

protect_range = 20

centering_factor = 0.0002
matching_factor = 0.005

avoid_factor = 0.1

min_speed = 2
max_speed = 5

def distance(a, b):
    alpha = 0.9604
    beta = 0.3978
    
    a = abs(a)
    b = abs(b)
    
    return alpha * max(a, b) + beta * min(a, b)


def rotate(origin, point, velocity):
    
    angle = math.atan2(velocity[1], velocity[0])
    
    ox, oy = origin
    px, py = point
    
    dx = px - ox
    dy = py - oy
    
    sin = math.sin(angle)
    cos = math.cos(angle)

    qx = ox + cos * dx - sin * dy
    qy = oy + sin * dx + cos * dy
    return qx, qy
    
def update(boid):
    
    if boid.y < margin:
        boid.vy += turnfactor
    elif boid.y > 640 - margin:
        boid.vy -= turnfactor
    elif boid.x < margin:
        boid.vx += turnfactor
    elif boid.x > 640 - margin:
        boid.vx -= turnfactor
    
    for other in boids:
        if other == boid:
            continue
        dx = other.x - boid.x
        dy = other.y - boid.y
        dist = distance(dx, dy)
        
        neighbors = 0
        
        ax, ay, avx, avy = 0, 0, 0, 0
        close_x, close_y = 0, 0
        if dist < visual_range:
            ax += other.x
            ay += other.y
            avx += other.vx
            avy += other.vy
                        
            neighbors += 1
            
        if dist < protect_range:
            close_x = boid.x - other.x
            close_y = boid.y - other.y

        
        if neighbors > 0:
            ax /= neighbors
            ay /= neighbors
            avx /= neighbors
            avy /= neighbors
            
            boid.vx = (boid.vx + 
                (ax - boid.x)*centering_factor + 
                (avx - boid.vx)*matching_factor)

            boid.vy = (boid.vy + 
                (ay - boid.y)*centering_factor + 
                (avy - boid.vy)*matching_factor)
            
        boid.vx += close_x * avoid_factor
        boid.vy += close_y * avoid_factor    
    
            
    speed = distance(boid.vx, boid.vy)
    if speed > max_speed:
        boid.vx = max_speed * boid.vx / speed
        boid.vy = max_speed * boid.vy / speed
    elif speed < min_speed:
        boid.vx = min_speed * boid.vx / speed
        boid.vy = min_speed * boid.vy / speed
            
    boid.x += boid.vx
    boid.y += boid.vy

        
screen_x = 640
screen_y = 640  

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True

for i in range(200):
    boids.append(Boid(random.randint(0, screen_x), random.randint(0, screen_y)))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # print(x, y)
            boids.append(Boid(x, y))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    for boid in boids:
        points = [(boid.x + 6.66, boid.y), (boid.x - 3.33, boid.y - 5), (boid.x - 3.33, boid.y + 5)]
        points = [rotate((boid.x, boid.y), point, (boid.vx, boid.vy)) for point in points]
        pygame.draw.polygon(screen, "white", points)

        update(boid)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
