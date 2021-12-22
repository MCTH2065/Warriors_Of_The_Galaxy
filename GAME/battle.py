import pygame
import time


class Spaceship:
    def __init__(self, x, y, size, name):
        self.x = x
        self.y = y
        self.size = size
        self.name = name
        #self.side = 'left'
        self.bullets = []
        self.show()

    def go_up(self):
        self.y -= 10

    def go_down(self):
        self.y += 10

    def go_left(self):
        self.x -= 10

    def go_right(self):
        self.x += 10

    def fire(self):
        self.bullets.append(Blaster(self.x + self.size // 2, self.y, 400))

    def show(self):
        pygame.draw.rect(screen, 'white', (self.x, self.y, self.size, self.size))


class Blaster:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel / fps
        self.life = True

    def show(self):
        pygame.draw.rect(screen, 'white', (self.x, self.y, 4, 20))
        self.y -= self.vel
        if self.y < -20:
            self.life = False


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('game')
    screen.fill('black')
    s = Spaceship(50, 50, 40, 'gogogo')
    running = True
    count = 0
    fps = 60
    t = time.time()
    pygame.display.flip()
    c = pygame.time.Clock()
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    s.go_up()
                elif event.key == pygame.K_DOWN:
                    s.go_down()
                elif event.key == pygame.K_LEFT:
                    s.go_left()
                elif event.key == pygame.K_RIGHT:
                    s.go_right()
                elif event.key == pygame.K_g:
                    if time.time() - t >= 0.5:
                        t = time.time()
                        s.fire()
        screen.fill('black')
        s.show()
        for elem in s.bullets:
            if elem.life is False:
                s.bullets.remove(elem)
            else:
                elem.show()
        c.tick(fps)
        pygame.display.flip()
    pygame.quit()
