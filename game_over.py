import pygame
import math
import random

def tobloxfonttype(text: str):
    res = ''.join([letter.upper() if idx % 2 == 0 else letter.lower() for idx, letter in enumerate(text)])
    return res


class Particle:
    """class of the floating circles on the screen"""
    def __init__(self, x, y, speedx, speedy, size, color):
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.size = size
        self.color = color

    def show(self):
        """function that draws the circle on the screen"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        """that's how circles moves"""
        self.x += self.speedx
        self.y += self.speedy
        if self.x >= 1200 or self.x <= 0:
            self.speedx = -self.speedx
        if self.y >= 900 or self.y <= 0:
            self.speedy = - self.speedy


def connect(p1: Particle, p2: Particle):
    """connects two particles with a line"""
    dist = math.sqrt(abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2)
    ran = 100
    if dist < ran:
        pygame.draw.line(screen, (255 * (1 - dist / ran), 255 * (1 - dist / ran), 255 * (1 - dist / ran)), (p1.x, p1.y), (p2.x, p2.y), width=3)

def gameover(scr, islose):
    """function that triggers when player kills all of enemies or dies(in game)"""
    global screen
    screen = scr
    #just cool game over window title))
    pygame.display.set_caption("Btw as you lose you don\'t deserve that cool game over window" if islose else 'Game Over')
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    particles = list()
    #particles initialisation
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
        #dummy events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                """
                to make this screen better and interesting we decided to add particle appearance on click
                but for optimisation we needs to remove some particles from stack so it doesn't overflow 
                and for that we just removes first particle from the array
                it doesn't have really bad visual effect so we decided to leave it like that
                """
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
        #here we connects all of the particles
        #difficulty is O(n ** 2) so we only need to initialize not more than 100 of them or there will be lags
        for i, particle in enumerate(particles):
            particle.show()
            particle.move()
            for j in range(i, len(particles)):
                connect(particle, particles[j])

        #here is some beauty font rendering
        font = pygame.font.Font('./fonts/Blox2.ttf', 200)
        game_over = font.render(tobloxfonttype('Game Over'), False, 'red' if islose else 'green')
        font = pygame.font.Font('./fonts/Blox2.ttf', 50)
        iswin = font.render(tobloxfonttype(f'You {"Lost" if islose else "Win" }'), False, 'red' if islose else 'green')
        screen.blit(game_over, (150, 300))
        screen.blit(iswin, (500, 550))
        clock.tick(100)
        pygame.display.flip()
    pygame.quit()
