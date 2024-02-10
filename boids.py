import pygame
from pygame import Color
from pygame import Rect
import math
import random

boids = []


class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.random() * 2 - 1
        self.vy = random.random() * 2 - 1
    
margin = 40
turnfactor = 0.02
visual_range = 50

protect_range = 20

centering_factor = 0.0005
matching_factor = 0.005

avoid_factor = 0.04

min_speed = 2
max_speed = 6
    
def update(boid):
    
    if boid.y < margin and boid.vy < 0:
        boid.vy += turnfactor * (margin - boid.y)
    elif boid.y > 640 - margin and boid.vy > 0:
        boid.vy -= turnfactor * (margin - boid.y + 640)
    elif boid.x < margin and boid.vx < 0:
        boid.vx += turnfactor * (margin - boid.x)
    elif boid.x > 640 - margin and boid.vx > 0:
        boid.vx -= turnfactor * (margin - boid.x + 640)
    
    for other in boids:
        if other == boid:
            continue
        dx = other.x - boid.x
        dy = other.y - boid.y
        dist = math.sqrt(pow(dx, 2) + pow(dy, 2))
        
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
    
            
    speed = math.sqrt(pow(boid.vx, 2) + pow(boid.vy, 2))
    if speed > max_speed:
        boid.vx = max_speed * boid.vx / speed
        boid.vy = max_speed * boid.vy / speed
    elif speed < min_speed:
        boid.vx = min_speed * boid.vx / speed
        boid.vy = min_speed * boid.vy / speed
            
    boid.x += boid.vx
    boid.y += boid.vy

        
        

# pygame setup
pygame.init()
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()
running = True

for i in range(200):
    boids.append(Boid(random.randint(0, 640), random.randint(0, 640)))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)
            boids.append(Boid(x, y))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    for boid in boids:
        pygame.draw.rect(screen, "white", Rect(boid.x, boid.y, 10, 10))
        update(boid)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
