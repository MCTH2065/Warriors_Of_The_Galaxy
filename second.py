import pygame
from random import randint

if __name__ == '__main__':
    pygame.init()
    size = width, height = randint(500, 1000), randint(500, 1000)
    print(width)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Шарики')
    screen.fill('black')
    running = True
    x_pos = 0
    fps = 20
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
                fut_x = x - (v / fps)
                fut_y = y - (v / fps)
                if fut_x <= 0:
                    tpe = 'topright'
                elif fut_y <= 0:
                    tpe = 'botleft'
                else:
                    x = fut_x
                    y = fut_y

            elif tpe == 'topright':
                fut_x = x + (v / fps)
                fut_y = y - (v / fps)
                if fut_y <= 0:
                    tpe = 'botright'
                elif fut_x >= width:
                    tpe = 'topleft'
                else:
                    x = fut_x
                    y = fut_y
            elif tpe == 'botleft':
                fut_x = x - v / fps
                fut_y = y + v / fps
                if fut_x <= 0:
                    tpe = 'botright'
                elif fut_y >= height:
                    tpe = 'topleft'
                else:
                    x = fut_x
                    y = fut_y
            elif tpe == 'botright':
                fut_x = x + v / fps
                fut_y = y + v / fps
                if fut_x >= width:
                    tpe = 'botleft'
                elif fut_y >= height:
                    tpe = 'topright'
                else:
                    x = fut_x
                    y = fut_y

            pygame.draw.circle(screen, 'white', (x, y), r)
            balls[count] = [x, y, tpe]
            count += 1

        pygame.display.flip()

    pygame.quit()
