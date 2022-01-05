import random
import pygame
import time
import json


class Spaceship(pygame.sprite.Sprite):
    image = pygame.image.load("spaceships/test1.png")

    def __init__(self, x, y, size, name, vel, bulletvel, firerate, damage, hp):
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

    def __init__(self, x, y, size, velx, vely, damage, hp, rew, firerate):
        super().__init__(all_sprites)
        self.image = EnemySpaceship.image
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
        self.size = size
        self.side = False
        self.bullets = []
        self.e_t = time.time()
        self.velx = velx
        self.vely = vely
        self.hp = hp
        self.firerate = firerate
        self.damage = damage
        self.reward = rew
        self.show()

    def fire(self):
        if self.hp > 0:
            self.bullets.append(EnemyBlaster(self.x if not self.side else self.x + self.size - 4, self.y + self.size,
                                             400, 'red', height + 20, self))
        self.side = not self.side

    def collide(self):
        global width
        for elem in enemies:
            if elem != self and pygame.sprite.collide_mask(self, elem):
                self.velx = -self.velx
                self.x += 2 * self.velx
                if self.x <= 0:
                    self.x = 5
                elif self.x >= width - self.size:
                    self.x = width - self.size

    def show(self):
        self.collide()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x += self.velx
        self.y += self.vely
        if self.x + self.velx <= 0 or self.x + self.velx + self.size >= width:
            self.velx = -self.velx
        if self.y + self.vely <= 0 or self.y + self.vely + self.size >= height // 2:
            self.vely = -self.vely


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
        global enemies, tempbullets, money
        self.rect.x = self.x
        self.rect.y = self.y
        self.y -= self.vel
        if self.y < self.bord:
            self.life = False
        for elem in enemies:
            if pygame.sprite.collide_mask(self, elem):
                s.bullets.remove(self)
                all_sprites.remove(self)
                elem.hp -= s.damage
                if elem.hp <= 0:
                    all_sprites.remove(elem)
                    enemies.remove(elem)
                    money += elem.reward
                    for bullet in elem.bullets:
                        bullet.temporary = True
                    tempbullets += elem.bullets


class EnemyBlaster(pygame.sprite.Sprite):
    image = pygame.image.load("spaceships/testbul2.png")

    def __init__(self, x, y, vel, col, bord, spaceship):
        super().__init__(all_sprites)
        self.temporary = False
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


def launchgame():
    global all_sprites, fps, s, height, width, enemies, tempbullets, money
    money = 0
    tempbullets = []
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Warriors Of The Galaxy')
    screen.fill('black')
    all_sprites = pygame.sprite.Group()
    enemies = list()
    spots = []
    with open('data.json', 'r+') as file:
        data = json.load(file)
        s = Spaceship(600, 700, 40, 'gogogo', data['upgrades']['speed'], data['upgrades']['bullet speed'],
                      data['upgrades']['fire rate'], data['upgrades']['damage'], data['upgrades']['hp'])
        ammo = str(data['upgrades']['ammo'])
        max_ammo = '/' + str(data['upgrades']['ammo'])
        with open('enemies.json', 'r+') as e:
            ene = json.load(e)
            enemy_type = ene[data["level"]]
    for _ in range(data['progress']):
        pos = [random.randint(10, 1160), random.randint(10, 410)]
        while pos in spots:
            pos = [random.randint(10, 1160), random.randint(10, 410)]
        spots.append(pos)
    for i in range(len(spots)):
        speedx, speedy = random.randint(-enemy_type["speed"], enemy_type["speed"]), random.randint(-enemy_type["speed"], enemy_type["speed"])
        enemies.append(EnemySpaceship(spots[i][0], spots[i][1], 30, speedx, speedy,
                                    data['progress'] // 2 * enemy_type['damage'] + 1,
                                      data['progress'] // 2 * enemy_type['hp'] + 1,
                                      data['progress'] * enemy_type['coin multiplier'],
                                      enemy_type['fire rate']))
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

    col = (255, 255, 255)
    r = 3
    while running:
        pygame.display.flip()
        if len(enemies) == 0 or s.hp <= 0:
            with open('data.json', 'r+') as file:
                data = json.load(file)
                data['money'] = data['money'] + money
                if s.hp > 0:
                    data['progress'] = data['progress'] + 1
                    if data['progress'] > data['maxprogress']:
                        data['maxprogress'] = data['progress']
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
            running = False
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
            if time.time() - e.e_t >= e.firerate:
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
