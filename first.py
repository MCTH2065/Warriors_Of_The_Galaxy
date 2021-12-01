import pygame
from random import randint

if __name__ == '__main__':
    pygame.init()
    size = width, height = randint(500, 1000), randint(500, 1000)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Жёлтый круг')
    screen.fill('black')
    running = True
    x_pos = 0
    fps = 60
    v = 10
    r = 10
    balls = []
    c = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos_x, pos_y = event.pos
                pygame.draw.circle(screen, 'white', event.pos, r)
                balls.append([pos_x, pos_y, 'topleft'])
        count = 0
        screen.fill('black')
        for elem in balls:
            x = elem[0]
            y = elem[1]
            tpe = elem[2]
            if tpe == 'topleft':
                x -= v / fps
                y -= v / fps
            pygame.draw.circle(screen, 'white', (x, y), r)
            balls[count] = [x, y, 'topleft']
            count += 1

        pygame.display.flip()

    pygame.quit()
