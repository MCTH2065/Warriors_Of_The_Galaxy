import pygame
import time
import json


class Spaceship(pygame.sprite.Sprite):
    image = pygame.image.load("spaceships/test1.png")

    def __init__(self, x, y, size, name, vel, bulletvel, firerate):
        super().__init__(all_sprites)
        self.image = Spaceship.image
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.size = size
        self.name = name
        self.side = False
        self.bullets = []
        self.vel = vel
        self.bulletvel = bulletvel
        self.firerate = firerate
        self.show()

    def go_up(self):
        if self.y >= self.vel:
            self.y -= self.vel

    def go_down(self):
        if self.y <= 900 - self.vel - self.size:
            self.y += self.vel

    def go_left(self):
        if self.x >= self.vel:
            self.x -= self.vel

    def go_right(self):
        if self.x <= 1200 - self.vel - self.size:
            self.x += self.vel

    def fire(self):
        self.bullets.append(Blaster(self.x if not self.side else self.x + self.size - 4, self.y, self.bulletvel,
                                    'white', -20))
        self.side = not self.side

    def show(self):
        self.rect.x = self.x
        self.rect.y = self.y


class EnemySpaceship(pygame.sprite.Sprite):
    image = pygame.image.load("spaceships/test2.png")

    def __init__(self, x, y, size, vel):
        super().__init__(all_sprites)
        self.image = EnemySpaceship.image
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.dir = 'r'
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.size = size
        self.side = False
        self.bullets = []
        self.vel = vel
        self.show()

    def go_up(self):
        if self.y >= self.vel:
            self.y -= self.vel

    def go_down(self):
        if self.y <= 900 - self.vel - self.size:
            self.y += self.vel

    def go_left(self):
        if self.x >= self.vel:
            self.x -= self.vel
        else:
            self.dir = 'r'

    def go_right(self):
        if self.x <= 1200 - self.vel - self.size:
            self.x += self.vel
        else:
            self.dir = 'l'

    def fire(self):
        self.bullets.append(EnemyBlaster(self.x if not self.side else self.x + self.size - 4, self.y + self.size, 400,
                                         'red', height + 20))
        self.side = not self.side

    def show(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Blaster(pygame.sprite.Sprite):
    image = pygame.image.load("spaceships/testbul1.png")

    def __init__(self, x, y, vel, col, bord):
        super().__init__(all_sprites)
        self.image = Blaster.image
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.bord = bord
        self.col = col
        self.vel = vel / fps
        self.life = True

    def show(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.y -= self.vel
        if self.y < self.bord:
            self.life = False
        if pygame.sprite.collide_mask(self, e):
            s.bullets.remove(self)
            all_sprites.remove(self)
            print('enemy hit')


class EnemyBlaster(pygame.sprite.Sprite):
    image = pygame.image.load("spaceships/testbul2.png")

    def __init__(self, x, y, vel, col, bord):
        super().__init__(all_sprites)
        self.image = EnemyBlaster.image
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.bord = bord
        self.col = col
        self.vel = vel / fps
        self.life = True

    def show(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.y += self.vel
        if self.y > self.bord:
            self.life = False
        if pygame.sprite.collide_mask(self, s):
            e.bullets.remove(self)
            all_sprites.remove(self)
            print('ally hit')


def launchgame():
    global all_sprites, e, fps, s, height
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Warriors Of The Galaxy')
    screen.fill('black')
    all_sprites = pygame.sprite.Group()
    with open('data.json', 'r+') as file:
        data = json.load(file)
        s = Spaceship(50, 50, 40, 'gogogo', data['upgrades']['speed'], data['upgrades']['bullet speed'],
                      data['upgrades']['fire rate'])
    e = EnemySpaceship(100, 20, 30, 5)
    running = True
    fps = 60
    t = time.time()
    e_t = time.time()
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
        if time.time() - t >= s.firerate and moves['shoot']:
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
        if e.dir == 'r':
            e.go_right()
        else:
            e.go_left()
        if time.time() - e_t >= 0.25:
            e_t = time.time()
            e.fire()
        screen.fill('black')
        s.show()
        e.show()
        all_sprites.draw(screen)
        for elem in s.bullets:
            if elem.life is False:
                s.bullets.remove(elem)
                all_sprites.remove(elem)
            else:
                elem.show()
        for elem in e.bullets:
            if elem.life is False:
                e.bullets.remove(elem)
                all_sprites.remove(elem)
            else:
                elem.show()
        c.tick(fps)
        pygame.display.flip()
    pygame.quit()
