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

def gameover(scr, islose):
    global screen
    screen = scr
    pygame.display.set_caption('Game Over')
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    particles = list()
    for i in range(100):
        particles.append(Particle(random.randint(0, 1200), random.randint(0, 900),
                                  random.randint(-100, 100) / 50, random.randint(-100, 100) / 50,
                                  5,
                                  # (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                  'red' if islose else 'green'))
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
                                  'red' if islose else 'green'
                                          ))
        s += 1
        screen.fill((0, 0, 0))
        for i in particles:
            i.show()
            i.move()
            for j in particles:
                connect(i, j)
        font = pygame.font.Font('./fonts/Blox2.ttf', 200)
        game_over = font.render('Game Over', False, 'red' if islose else 'green')
        font = pygame.font.Font('./fonts/Blox2.ttf', 50)
        iswin = font.render(f'You {"Lost" if islose else "Win" }', False, 'red' if islose else 'green')
        screen.blit(game_over, (150, 300))
        screen.blit(iswin, (500, 550))
        clock.tick(100)
        pygame.display.flip()
    pygame.quit()
