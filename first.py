import pygame
from random import randint


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 40
        self.data = []
        for i in range(width):
            d = []
            for j in range(height):
                d.append([i, j, -1])
            self.data.append(d)

    def get_click(self, mouse_pos):
        self.get_cell(mouse_pos)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x - 10 >= 0 and y - 10 >= 0:
            cell_x = (int((x - 10) / 40))
            cell_y = (int((y - 10) / 40))
            if cell_x < self.width and cell_y < self.height:
                coords = [cell_x, cell_y]
                self.on_click(coords)
            else:
                return 'None'
        else:
            return 'None'

    def on_click(self, cell_coords):
        self.coordinates = cell_coords

    def render(self, scrn):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(scrn, (255, 255, 255), (self.left + (j * self.cell_size),
                                                         self.top + (i * self.cell_size), self.cell_size,
                                                         self.cell_size), 1)


class Minesweeper(Board):
    def __init__(self, w, h, mines):
        self.wdth = int(w)
        self.hght = int(h)
        self.mines = int(mines)
        super().__init__(self.wdth, self.hght)
        mns = []
        for i in range(self.mines):
            ran = [randint(0, self.wdth - 1), randint(0, self.hght - 1)]
            while ran in mns:
                ran = [randint(0, self.wdth - 1), randint(0, self.hght - 1)]
            mns.append(ran)
        for elem in mns:
            pygame.draw.rect(screen, 'red', (elem[0] * self.cell_size + self.left, elem[1] * self.cell_size + self.top,
                                             self.cell_size, self.cell_size))
            for i in range(self.wdth):
                for j in range(self.hght):
                    if [int(self.data[i][j][0]), int(self.data[i][j][1])] == elem:
                        self.data[i][j][2] = 10

    def open_cell(self):
        self.get_click(p)
        x, y = int(self.coordinates[0]), int(self.coordinates[1])
        if self.data[x][y][2] != 10:
            cnt = 0
            numb = self.wdth - x
            if numb == self.wdth:
                minus = 0
                n = 2
            else:
                if numb >= 2:
                    n = 3
                else:
                    n = 2
                minus = 1
            numb_y = self.hght - y
            if self.hght > numb_y >= 2:

                for i in range(n):
                    if self.data[x - minus + i][y - 1][2] == 10:
                        cnt += 1
                for i in range(n):
                    if self.data[x - minus + i][y + 1][2] == 10:
                        cnt += 1
            elif numb_y >= self.hght:
                for i in range(n):
                    if self.data[x - minus + i][y + 1][2] == 10:
                        cnt += 1
            else:
                for i in range(n):
                    if self.data[x - minus + i][y - 1][2] == 10:
                        cnt += 1

            for i in range(n):
                if self.data[x - minus + i][y][2] == 10:
                    cnt += 1
            font = pygame.font.Font(None, 40)
            text = font.render(str(cnt), True, (100, 255, 100))
            screen.blit(text, (int(self.coordinates[0]) * self.cell_size + self.left,
                               int(self.coordinates[1]) * self.cell_size + self.top))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Дедушка сапёра')
    screen.fill('black')
    running = True
    count = 0
    fps = 60
    m = Minesweeper(12, 17, 15)
    pygame.display.flip()
    c = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = event.pos
                m.open_cell()
            m.render(screen)
        c.tick(fps)
        pygame.display.flip()
    pygame.quit()
