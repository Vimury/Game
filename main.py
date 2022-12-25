from Classes import Map, Cell
import pygame
import os
import sys

'''Прописал id государств'''
red = 1
pink = 2
green = 3
light_green = 4
blue = 5
light_blue = 6
orange = 7
yellow = 8
purple = 9

'''Прописал id сущностей'''
tree = 1
stone = 2
gold = 3
# Не придумал сущность
fish = 4

farm = 5
big_farm = 6
tower = 7
big_tower = 8
town = 9

villager = 10
# Не придумал название
knight = 12
big_knight = 13

'''Прописал id типа местности'''
water = 0
ground = 1


def render():  # Загрузка стартовой земли
    step_x = 0
    for y in range(y_size):
        for x in range(x_size):
            a = m.map[y][x].type
            if a == ground:
                cell = load_image('ground.png', colorkey=(237, 28, 36))
            elif a == water:
                cell = load_image('water.png', colorkey=(237, 28, 36))
            if m.map[y][x].entity == tree:
                cell2 = load_image('tree.png', colorkey=(255, 255, 255))
                screen.blit(cell2, (step_x, x * 36 + (18 if y & 1 else 0)))
            # y & 1 == 0 - быстрая проверка на чётность
            screen.blit(cell, (step_x, x * 36 + (18 if y & 1 else 0)))
        step_x += 31


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    x_size, y_size = 20, 30
    m = Map(x_size, y_size)
    pygame.init()
    pygame.display.set_caption('Countries of century knights')
    size = width, height = 1000, 750
    #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width, height))

    fps = 30
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0))
    running = True
    render()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
