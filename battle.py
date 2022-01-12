import math
import os
import random
import pygame
import time
import json
import ast

from game_over import *


class Spaceship(pygame.sprite.Sprite):
    """main spaceship class"""
    image = pygame.image.load("spaceships/spaceship.png")

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

    #here is some movement moments, functions doesn't need explanation
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
        """functions that triggers every time spaceship shoots"""
        self.bullets.append(
            Blaster(self.x if not self.side else self.x + self.size - 4, self.y + self.size // 2, self.bulletvel,
                    'white', -20))
        self.side = not self.side

    def show(self):
        """this how we render spaceship"""
        self.rect.x = self.x
        self.rect.y = self.y


class EnemySpaceship(pygame.sprite.Sprite):
    """class of the enemy spaceship"""
    image = pygame.transform.scale(pygame.image.load("spaceships/enemy.png"), (75, 75))

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
        """functions triggers every time enemy need to shoot"""
        if self.hp > 0:
            self.bullets.append(
                EnemyBlaster(self.x if not self.side else self.x + self.size - 4, self.y + self.size // 2,
                             400, 'red', self, 'spaceships/testbul2.png'))
        self.side = not self.side

    def collide(self):
        """function triggers every time when enemies collides, reverses enemy speed direction"""
        global width
        for elem in enemies:
            if elem != self and pygame.sprite.collide_mask(self, elem):
                if elem == boss:
                    pass
                else:
                    self.velx = -self.velx
                    self.x += 3 * self.velx
                    if self.x <= 0:
                        self.x = 15
                    elif self.x >= width - self.size:
                        self.x = width - self.size

    def show(self):
        """"""
        self.collide()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x += self.velx
        self.y += self.vely
        if self.x + self.velx <= 0 or self.x + self.velx + self.size >= width:
            self.velx = -self.velx
        if self.y + self.vely <= 0 or self.y + self.vely + self.size >= height // 2:
            self.vely = -self.vely


class Boss(pygame.sprite.Sprite):
    """boss object"""
    def __init__(self, damage, hp, rew, img, boss_type, enemies_number):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(img), (350, 150))
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = 1
        self.places = [(100, 20), (420, 20), (750, 20)]
        self.x, self.y = self.places[self.pos][0], self.places[self.pos][1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.xsize = self.image.get_width()
        self.ysize = self.image.get_height()
        self.side = False
        self.bullets = []
        self.e_t = time.time()
        self.firerate = 0.6
        self.vuln_time = time.time()
        self.hp = hp
        self.maxhp = hp
        self.brkarm = False
        self.isvuln = False
        self.damage = damage
        self.reward = rew
        self.boss_type = boss_type
        self.enemies_number = enemies_number

    def teleport(self):
        """this function triggers if boss loses health, teleports boss to another place and creates some enemies"""
        global enemies, n, all_sprites, enemy_type
        if len(enemies) == 1 and self.brkarm is False:
            self.brkarm = True
            self.isvuln = True
            self.vuln_time = time.time()
        if time.time() - self.vuln_time >= 5 and self.brkarm is True:
            self.isvuln = False
            self.brkarm = False
            spawn(self.enemies_number, enemy_type)
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
        """function that create enemy bullet and makes shooting beautiful"""
        if self.hp > 0:
            self.bullets.append(EnemyBlaster(self.x + self.xsize // 4 + 15 if not self.side
                                             else self.x + 3 * (self.xsize // 4) - 20, self.y + self.ysize // 1.5 + 10,
                                             400, height + 20, self, 'spaceships/bossbul.png'))
        self.side = not self.side

    def show(self):
        """this function render boss's health on the screen"""
        self.teleport()
        pygame.draw.rect(screen, 'grey', (300, 10, 600, 5))
        pygame.draw.rect(screen, 'red', (300, 10, (self.hp / self.maxhp) * 600, 5))
        self.rect.x = self.x
        self.rect.y = self.y


class Blaster(pygame.sprite.Sprite):
    """main spaceship bullet object"""
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
        """function that shows bullet on the screen and moves it"""
        global enemies, tempbullets, money
        self.rect.x = self.x
        self.rect.y = self.y
        self.y -= self.vel
        if self.y < self.bord:
            self.life = False
        for elem in enemies:
            try:
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
            except:
                pass


class EnemyBlaster(pygame.sprite.Sprite):
    """here is the class of bullet that enemies shoots"""
    def __init__(self, x, y, vel, col, spaceship, image):
        super().__init__(all_sprites)
        self.temporary = False
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.col = col
        self.vel = vel / fps
        self.life = True
        self.spaceship = spaceship

    def show(self):
        """this functions shows bullet in the screen and moves it"""
        self.rect.x = self.x
        self.rect.y = self.y
        self.y += self.vel
        if self.y > 920:
            self.life = False
        if pygame.sprite.collide_mask(self, s):
            if not self.temporary:
                self.spaceship.bullets.remove(self)
            else:
                tempbullets.remove(self)
            all_sprites.remove(self)
            s.hp -= self.spaceship.damage

#here's the first background loading variant using sprites. Might be removed
# class BackGround(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load(f"backgrounds/{random.choice(os.listdir('backgrounds'))}")
#         self.rect = self.image.get_rect()
#         self.rect.y = 0
#         self.rect.x = 0
#         all_sprites.add(self)


def spawn(n, enemy_type):
    """this function creates enemies"""
    global enemies, boss, all_sprites
    spots = []
    for _ in range(n):
        #random position generation
        pos = [random.randint(10, 1100), random.randint(10, 380)]
        while pos in spots:
            pos = [random.randint(10, 1100), random.randint(10, 380)]
        spots.append(pos)
    for i in range(len(spots)):
        #enemies themselves
        speedx, speedy = random.randint(-enemy_type["speed"], enemy_type["speed"]), random.randint(-enemy_type["speed"],
                                                                                                   enemy_type["speed"])
        enemies.append(EnemySpaceship(spots[i][0], spots[i][1], 75, speedx, speedy,
                                      n // 2 * enemy_type['damage'] + 1,
                                      n // 2 * enemy_type['hp'] + 1,
                                      n * enemy_type['coin multiplier'],
                                      enemy_type['fire rate']))


def launchgame():
    """main game function, used to manage events and extract data for enemies creation"""
    global screen, all_sprites, fps, s, height, width, enemies, tempbullets, money, planet_name, boss, enemy_type
    bg = pygame.image.load(f"backgrounds/{random.choice(os.listdir('backgrounds'))}")
    boss = 0
    money = 0
    tempbullets = []
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Warriors Of The Galaxy')
    all_sprites = pygame.sprite.Group()
    enemies = list()
    # here we extract progress and spaceships stats
    with open('data.json', 'r+') as file:
        data = json.load(file)
        s = Spaceship(600, 700, 80, 'gogogo', data['upgrades']['speed'], data['upgrades']['bullet speed'],
                      data['upgrades']['fire rate'], data['upgrades']['damage'], data['upgrades']['hp'])
        ammo = str(data['upgrades']['ammo'])
        max_ammo = str(data['upgrades']['ammo'])
        waves = data['progress'] // 2 + 1
        n = data['progress']
        maxhp = data['upgrades']['hp']
    with open('enemies.txt', 'r+') as e: #json not used cause we need max score for data
        ene = ast.literal_eval(e.read())
        enemy_type = ene[data["level"]]
    # some basic parameters needed to manage spaceship and so on
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
    wave_cleared = False
    col = (255, 255, 255)
    r = 3
    reset_time = time.time()
    lose = True
    #first wave of enemies spawn
    spawn(n // 2 + 1, enemy_type)
    current_wave = 1
    isreloading = False
    try:
        while running:
            if s.hp <= 0 or len(enemies) == 0:
                #this triggers when player clears the wave
                if waves == current_wave or s.hp <= 0:
                    #game end
                    with open('data.json', 'r+') as file:
                        data = json.load(file)
                        data['money'] = data['money'] + money
                        if s.hp > 0:
                            lose = False
                            data['progress'] = data['progress'] + 1
                            if data['progress'] > data['maxprogress']:
                                data['maxprogress'] = data['progress']
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()
                    gameover(screen, lose)
                else:
                    #new wave creation
                    if wave_cleared is False:
                        wave_cleared = True
                        reset_time = time.time()
                    if wave_cleared and time.time() - reset_time >= 5:
                        current_wave += 1
                        if current_wave == 2:
                            spawn(n, enemy_type)
                        else:
                            if current_wave == waves:
                                #here we creates boss each 5 levels
                                spawn(n, enemy_type)
                                if n % 5 == 0:
                                    boss = Boss(n, n * 3, 500, "spaceships/boss.png", 'first', n)
                                    enemies.append(boss)
                            else:
                                spawn(n + 1, enemy_type)
                        wave_cleared = False
            for event in pygame.event.get():
                #some dummy events functions for spaceship
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
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
                    elif event.key == pygame.K_r:
                        if ammo != max_ammo:
                            s.firerate = r
                            isreloading = True
            if time.time() - t >= s.firerate:
                #here is how main spaceship looses an ammo
                if s.firerate == r:
                    isreloading = False
                    ammo = max_ammo
                    col = (255, 255, 255)
                    s.firerate = data['upgrades']['fire rate']
            if time.time() - t >= s.firerate and moves['shoot']:
                #here is how spaceship shoots
                t = time.time()
                s.fire()
                ammo = str(int(ammo) - 1)
                if int(ammo) >= int(max_ammo) // 4:
                    col = (255, 255, 255)
                    s.firerate = data['upgrades']['fire rate']
                else:
                    s.firerate = data['upgrades']['fire rate']
                    col = (255, 0, 0)
                if int(ammo) == 0:
                    s.firerate = r
                    isreloading = True
            if moves['up']:
                s.go_up()
            if moves['down']:
                s.go_down()
            if moves['left']:
                s.go_left()
            if moves['right']:
                s.go_right()
            pygame.display.flip()
            screen.blit(bg, (0, 0)) #filling screen with random background from backgrounds folder
            for e in enemies: #that's how enemies shoots
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
            #here we displays data in the screen
            pygame.font.init()
            font = pygame.font.Font('fonts/Blox2.ttf', 50)
            txt = font.render(tobloxfonttype(ammo + ' of ' + max_ammo), False, col if not isreloading else 'red')
            screen.blit(txt, (50, 800))
            txt = font.render(tobloxfonttype(str(s.hp)), False, (255 - round(255 * s.hp / maxhp), round(255 * s.hp / maxhp), 0))
            screen.blit(txt, (750, 800))
            if isreloading:
                txt = font.render(tobloxfonttype('Reloading'), False, 'red')
                screen.blit(txt, (10, 10))
            if s.hp <= 0 or len(enemies) == 0:
                txt = font.render(tobloxfonttype(f'Wave Cleared'), False, (0, 255, 0))
                screen.blit(txt, (10, 100))
                txt = font.render(tobloxfonttype(f'New Wave In {round(5 - time.time() + reset_time)} Seconds'),
                                  False, (0, 255, 0))
                screen.blit(txt, (10, 160))
            font1 = pygame.font.Font('fonts/Blox2.ttf', 33)
            txt = font1.render(tobloxfonttype(str(money)), False, 'yellow')
            screen.blit(txt, (1125, 10))
            c.tick(fps)
            pygame.display.flip()
    except Exception as e:
        pass