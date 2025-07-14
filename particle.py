import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 4)
        self.color = random.choice([(255, 255, 255), (255, 0, 0), (255, 200, 0)])
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-5, 5)
        self.life = 30 

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1

    def draw(self, win):
        if self.life > 0:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
