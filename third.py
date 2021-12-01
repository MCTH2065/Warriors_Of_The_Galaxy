import pygame
from random import randint

if __name__ == '__main__':
    pygame.init()
    size = width, height = randint(500, 1000), randint(500, 1000)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Жёлтый круг')
    screen.fill('blue')
    running = True
    x_pos = 0
    fps = 60
    v = 10
    r = 1
    pos_x = 0
    pos_y = 0
    c = pygame.time.Clock()
    isclicked = 0
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and isclicked < 1:
                pos_x, pos_y = event.pos
                pygame.draw.circle(screen, 'yellow', event.pos, r)
                isclicked += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and isclicked == 1:
                screen.fill('blue')
                r = 1
                pos_x, pos_y = event.pos
                pygame.draw.circle(screen, 'yellow', event.pos, r)
                isclicked = 1
        if isclicked != 0:
            r += v / fps
            pygame.draw.circle(screen, 'yellow', (pos_x, pos_y), r)
            pygame.display.flip()
            c.tick(fps)

    pygame.quit()
