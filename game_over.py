import pygame
import math
import random

class Particle:
    def __init__(self, x, y, speedx, speedy, size, color):
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.size = size
        self.color = color

    def show(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.x >= 1200 or self.x <= 0:
            self.speedx = -self.speedx
        if self.y >= 900 or self.y <= 0:
            self.speedy = - self.speedy


def connect(p1: Particle, p2: Particle):
    dist = math.sqrt(abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2)
    ran = 100
    if dist < ran:
        pygame.draw.line(screen, (255 * (1 - dist / ran), 255 * (1 - dist / ran), 255 * (1 - dist / ran)), (p1.x, p1.y), (p2.x, p2.y), width=3)

def gameover():
    global screen
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    particles = list()
    for i in range(100):
        particles.append(Particle(random.randint(0, 1200), random.randint(0, 900),
                                  random.randint(-100, 100) / 50, random.randint(-100, 100) / 50,
                                  5,
                                  # (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                  (255, 0, 0
                                   )))
    running = True
    clock = pygame.time.Clock()
    s = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                del particles[0]
                particles.append(Particle(*pos,
                                  random.randint(-100, 100) / 50, random.randint(-100, 100) / 50,
                                  5,
                                  # (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                  (255, 0, 0
                                   )))
        s += 1
        screen.fill((0, 0, 0))
        for i in particles:
            i.show()
            i.move()
            for j in particles:
                connect(i, j)
        font = pygame.font.Font('./fonts/Blox2.ttf', 200)
        txt = font.render('Game Over', False, 'red')
        screen.blit(txt, (150, 300))
        clock.tick(100)
        pygame.display.flip()
    pygame.quit()
