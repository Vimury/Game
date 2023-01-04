from Classes import Map, Cell
import pygame
import os
import sys

'''Прописал id типа местности'''
water = 0
ground = 1

'''Прописал id государств'''
colors = [(red := 1), (pink := 2), (green := 3), (light_green := 4), (blue := 5), (light_blue := 6), (orange := 7),
          (yellow := 8), (purple := 9)]
dict_colors = {1: 'red', 2: 'pink', 3: 'green', 4: 'light_green', 5: 'blue', 6: 'light_blue', 7: 'orange', 8: 'yellow',
               9: 'purple'}

'''Прописал id сущностей'''
tree = 1
stone = 2
gold = 3
# Не придумал сущность
fish = 4

castle = 5
farm = 6
big_farm = 7
tower = 8
big_tower = 9
town = 10

villager = 11
# Не придумал название
knight = 13
big_knight = 14

dict_entity = {1: 'tree', 2: 'stone', 3: 'gold', 4: 'fish', 5: 'castle', 6: 'farm', 7: 'big_farm', 8: 'tower',
               9: 'big_tower', 10: 'town', 11: 'villager', 12: 'None', 13: 'knight', 14: 'big_knight'}


def render():  # Загрузка стартовой земли
    # step_x = -15
    step_x = 0
    for y in range(y_size):
        for x in range(x_size):
            a = m.map[y][x].type
            f = False
            if a == ground:
                cell = load_image('ground2.png', colorkey=(255, 255, 255))
                b = m.map[y][x].goverment
                if b is not None:
                    cell = load_image(f'{dict_colors[b]}.png', colorkey=(255, 255, 255))
                c = m.map[y][x].entity
                if c is not None:
                    f = True
                    cell2 = load_image(f'{dict_entity[c]}.png', colorkey=(255, 255, 255))
            elif a == water:
                cell = load_image('water2.png', colorkey=(255, 255, 255))
            # y & 1 == 0 - быстрая проверка на чётность
            screen.blit(cell, (step_x, x * 36 + (18 if y & 1 else 0)))  # -24
            if f:
                screen.blit(cell2, (step_x, x * 36 + (18 if y & 1 else 0)))
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
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width, height))

    fps = 30
    clock = pygame.time.Clock()

    screen.fill((0, 0, 128))
    # screen.fill((0, 0, 0))
    running = True
    render()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m.click_processing(m.get_coords(event.pos))

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
