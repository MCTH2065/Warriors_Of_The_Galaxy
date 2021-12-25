import pygame
import time
import json


class Spaceship:
    def __init__(self, x, y, size, name, vel, bulletvel, speedrate):
        self.x = x
        self.y = y
        self.size = size
        self.name = name
        self.side = False
        self.bullets = []
        self.vel = vel
        self.bulletvel = bulletvel
        self.speedrate = speedrate
        self.show()

    def go_up(self):
        if self.y >= self.vel:
            self.y -= self.vel
        else:
            self.y = 0

    def go_down(self):
        if self.y <= 900 - self.vel - self.size:
            self.y += self.vel
        else:
            self.y = 900 - self.size

    def go_left(self):
        if self.x >= self.vel:
            self.x -= self.vel
        else:
            self.x = 0

    def go_right(self):
        if self.x <= 1200 - self.vel - self.size:
            self.x += self.vel
        else:
            self.x = 1200 - self.size

    def fire(self):
        self.bullets.append(Blaster(self.x if not self.side else self.x + self.size - 4, self.y, self.bulletvel))
        self.side = not self.side

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


def launchgame():
    try:
        global screen, fps
        pygame.init()
        size = width, height = 1200, 900
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Warriors Of The Galaxy')
        screen.fill('black')
        with open('data.json', 'r+') as file:
            data = json.load(file)
            s = Spaceship(50, 50, 40, 'gogogo', data['upgrades']['speed'], data['upgrades']['bullet speed'], data['upgrades']['fire rate'])
        running = True
        fps = 60
        t = time.time()
        pygame.display.flip()
        c = pygame.time.Clock()
        moves = {
            'down': False,
            'up': False,
            'left': False,
            'right': False,
            'shoot': False
        }
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        moves['up'] = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        moves['down'] = True
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moves['left'] = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moves['right'] = True
                    elif event.key == pygame.K_f:
                        moves['shoot'] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        moves['up'] = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        moves['down'] = False
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        moves['left'] = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        moves['right'] = False
                    elif event.key == pygame.K_f:
                        moves['shoot'] = False
            if time.time() - t >= s.speedrate and moves['shoot']:
                t = time.time()
                s.fire()
            if moves['up']:
                s.go_up()
            if moves['down']:
                s.go_down()
            if moves['left']:
                s.go_left()
            if moves['right']:
                s.go_right()
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
    except Exception as e:
        print(e)