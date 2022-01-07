import json
import random
import time

import pygame


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, name, vel, bulletvel, firerate, damage, hp, img):
        super().__init__(all_sprites)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.xsize = self.image.get_width()
        self.ysize = self.image.get_height()
        self.name = name
        self.side = False
        self.bullets = []
        self.vel = vel // 2
        self.hp = hp
        self.damage = damage
        self.bulletvel = bulletvel
        self.firerate = firerate
        self.show()

    def go_up(self):
        global height
        if self.y >= height // 2:
            self.y -= self.vel

    def go_down(self):
        if self.y <= 900 - self.vel - self.ysize:
            self.y += self.vel

    def go_left(self):
        if self.x >= self.vel:
            self.x -= self.vel

    def go_right(self):
        if self.x <= 1200 - self.vel - self.xsize:
            self.x += self.vel

    def fire(self):
        self.bullets.append(Blaster(self.x if not self.side else self.x + self.xsize - 4, self.y, self.bulletvel,
                                    'white', -20, "spaceships/testbul1.png"))
        self.side = not self.side

    def show(self):
        self.rect.x = self.x
        self.rect.y = self.y


class EnemySpaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, velx, vely, damage, hp, rew, image):
        super().__init__(all_sprites)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.xsize = self.image.get_width()
        self.ysize = self.image.get_height()
        self.side = False
        self.bullets = []
        self.e_t = time.time()
        self.r_t = 0.35
        self.velx = velx
        self.vely = vely
        self.hp = hp
        self.damage = damage
        self.reward = rew
        self.show()

    def fire(self):
        if self.hp > 0:
            self.bullets.append(EnemyBlaster(self.x if not self.side else self.x + self.xsize - 4, self.y + self.ysize,
                                             400, height + 20, self, "spaceships/testbul2.png"))
        self.side = not self.side

    def collide(self):
        global width, boss, tempbullets
        for elem in enemies:
            if elem != self and pygame.sprite.collide_mask(self, elem):
                if elem == boss:
                    pass
                else:
                    self.velx = -self.velx
                    self.x += 2 * self.velx
                    if self.x <= 0:
                        self.x = 5
                    elif self.x >= width - self.xsize:
                        self.x = width - self.xsize

    def show(self):
        self.collide()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x += self.velx
        self.y += self.vely
        if self.x + self.velx <= 0 or self.x + self.velx + self.xsize >= width:
            self.velx = -self.velx
        if self.y + self.vely <= 0 or self.y + self.vely + self.ysize >= height // 2:
            self.vely = -self.vely


class Boss(pygame.sprite.Sprite):
    def __init__(self, damage, hp, rew, img, boss_type):
        super().__init__(all_sprites)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = 1
        self.places = [(200, 20), (550, 20), (900, 20)]
        self.x, self.y = self.places[self.pos][0], self.places[self.pos][1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.xsize = self.image.get_width()
        self.ysize = self.image.get_height()
        self.side = False
        self.bullets = []
        self.e_t = time.time()
        self.r_t = 0.6
        self.vuln_time = time.time()
        self.hp = hp
        self.maxhp = hp
        self.brkarm = False
        self.isvuln = False
        self.damage = damage
        self.reward = rew
        self.boss_type = boss_type

    def teleport(self):
        global enemies, n, all_sprites
        if len(enemies) == 1 and self.brkarm is False:
            self.brkarm = True
            self.isvuln = True
            self.vuln_time = time.time()
        if time.time() - self.vuln_time >= 5 and self.brkarm is True:
            self.isvuln = False
            self.brkarm = False
            spawn(n)
            if self.pos == 1:
                self.pos = 2
            elif self.pos == 2:
                self.pos = 0
            else:
                self.pos = 1
            self.x, self.y = self.places[self.pos][0], self.places[self.pos][1]
            self.rect.x = self.x
            self.rect.y = self.y
            all_sprites.remove(self)
            all_sprites.add(self)

        elif self.isvuln is True:
            pass

    def fire(self):
        if self.hp > 0:
            self.bullets.append(EnemyBlaster(self.x + self.xsize // 4 if not self.side
                                             else self.x + 3 * (self.xsize // 4), self.y + self.ysize,
                                             400, height + 20, self, "spaceships/testbul3.png"))
        self.side = not self.side

    def show(self):
        global screen
        self.teleport()
        pygame.draw.rect(screen, 'gray', (300, 10, 600, 5))
        pygame.draw.rect(screen, 'red', (300, 10, (self.hp / self.maxhp) * 600, 5))
        self.rect.x = self.x
        self.rect.y = self.y


class Blaster(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, col, bord, img):
        super().__init__(all_sprites)
        self.image = pygame.image.load(img)
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
        global enemies, tempbullets, money, boss
        self.rect.x = self.x
        self.rect.y = self.y
        self.y -= self.vel
        if self.y < self.bord:
            self.life = False
        for elem in enemies:
            if pygame.sprite.collide_mask(self, elem):
                s.bullets.remove(self)
                all_sprites.remove(self)
                if elem != boss:
                    elem.hp -= s.damage
                else:
                    if elem.isvuln is True:
                        elem.hp -= s.damage
                if elem.hp <= 0:
                    all_sprites.remove(elem)
                    enemies.remove(elem)
                    money += elem.reward
                    for bullet in elem.bullets:
                        bullet.temporary = True
                    tempbullets += elem.bullets


class EnemyBlaster(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, bord, spaceship, img):
        super().__init__(all_sprites)
        self.temporary = False
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.bord = bord
        self.vel = vel / fps
        self.life = True
        self.spaceship = spaceship

    def show(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.y += self.vel
        if self.y > self.bord:
            self.life = False
        if pygame.sprite.collide_mask(self, s):
            if not self.temporary:
                self.spaceship.bullets.remove(self)
            else:
                tempbullets.remove(self)
            all_sprites.remove(self)
            s.hp -= self.spaceship.damage


def spawn(n):
    global enemies, boss, all_sprites
    spots = []
    for _ in range(n):
        pos = [random.randint(10, 1160), random.randint(10, 410)]
        while pos in spots:
            pos = [random.randint(10, 1160), random.randint(10, 410)]
        spots.append(pos)
    for i in range(len(spots)):
        speedx, speedy = random.randint(-3, 3), random.randint(-3, 3)
        while speedx == 0 or speedy == 0:
            speedx, speedy = random.randint(-3, 3), random.randint(-3, 3)
        enemies.append(EnemySpaceship(spots[i][0], spots[i][1], speedx, speedy,
                                      1, 1, 50, "spaceships/test2.png"))

def launchgame():
    global all_sprites, fps, s, height, width, enemies, tempbullets, money, n, boss, screen, all_sprites
    money = 0
    enemies = list()
    tempbullets = []
    all_sprites = pygame.sprite.Group()
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Warriors Of The Galaxy')
    screen.fill('black')
    with open('data.json', 'r+') as file:
        data = json.load(file)
        s = Spaceship(600, 700, 'gogogo', data['upgrades']['speed'], data['upgrades']['bullet speed'],
                      data['upgrades']['fire rate'], data['upgrades']['damage'], data['upgrades']['hp'],
                      'spaceships/test1.png')
    level = data['level']
    if level == 'easy':
        n = 2
    elif level == 'medium':
        n = 4
    else:
        n = 6
    waves = 4
    current_wave = 1
    running = True
    fps = 120
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
    ammo = '40'
    max_ammo = '/40'
    col = (255, 255, 255)
    r = 3
    closed = 0
    boss = 0
    wave_cleared = False
    reset_time = time.time()
    stop = False
    while running:
        pygame.display.flip()
        if len(enemies) == 0:
            if waves == current_wave:
                stop = True
            else:
                if wave_cleared is False:
                    wave_cleared = True
                    reset_time = time.time()
                if wave_cleared and time.time() - reset_time >= 2:
                    if current_wave == 1:
                        spawn(n // 2)
                        current_wave += 1
                    elif current_wave == 2:
                        spawn(n)
                        current_wave += 1
                    else:
                        spawn(n + 1)
                        boss = Boss(500, 10000, 500, "spaceships/test3.png", 'first')
                        enemies.append(boss)
                        current_wave += 1
                    wave_cleared = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or stop:
                if closed == 0:
                    with open('data.json', 'r+') as file:
                        data['money'] = data['money'] + money
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()
                    running = False
                    closed += 1
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
        screen.fill('black')
        if time.time() - t >= s.firerate:
            if s.firerate == r:
                ammo = max_ammo[1:]
                col = (255, 255, 255)
                s.firerate = data['upgrades']['fire rate']
        if time.time() - t >= s.firerate and moves['shoot']:
            t = time.time()
            s.fire()
            ammo = str(int(ammo) - 1)
            if int(ammo) >= int(max_ammo[1:]) // 4:
                col = (255, 255, 255)
                s.firerate = data['upgrades']['fire rate']
            else:
                s.firerate = data['upgrades']['fire rate']
                col = (255, 0, 0)
            if int(ammo) == 0:
                s.firerate = r
        if moves['up']:
            s.go_up()
        if moves['down']:
            s.go_down()
        if moves['left']:
            s.go_left()
        if moves['right']:
            s.go_right()
        for e in enemies:
            if time.time() - e.e_t >= e.r_t:
                e.e_t = time.time()
                e.fire()
            e.show()
            for elem in e.bullets:
                if elem.life is False:
                    e.bullets.remove(elem)
                    all_sprites.remove(elem)
                else:
                    elem.show()
        s.show()
        all_sprites.draw(screen)
        for bullet in tempbullets:
            bullet.show()
        for elem in s.bullets:
            if elem.life is False:
                s.bullets.remove(elem)
                all_sprites.remove(elem)
            else:
                elem.show()
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        txt = font.render(ammo + max_ammo, False, col)
        screen.blit(txt, (50, 800))
        font1 = pygame.font.SysFont('Arial', 33)
        txt = font1.render(str(money), False, 'yellow')
        screen.blit(txt, (1125, 10))
        c.tick(fps)
        pygame.display.flip()
    pygame.quit()