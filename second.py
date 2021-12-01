import pygame

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    fps = 60  # количество кадров в секунду
    clock = pygame.time.Clock()
    running = True
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # обработка остальных событий
        # ...
        # формирование кадра
        # ...
        pygame.display.flip()  # смена кадра
        # изменение игрового мира
        # ...
        # временная задержка
        clock.tick(fps)
    pygame.quit()