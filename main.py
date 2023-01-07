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
man2 = 12
knight = 13
big_knight = 14

dict_entity = {1: 'tree', 2: 'stone', 3: 'gold', 4: 'fish', 5: 'castle', 6: 'farm', 7: 'big_farm', 8: 'tower',
               9: 'big_tower', 10: 'town', 11: 'villager', 12: 'man2', 13: 'knight', 14: 'big_knight'}


def render(step_xx, step_y):
    screen.fill((0, 0, 128))
    step_x = step_xx
    # step_x = -15
    for y in range(y_size):
        for x in range(x_size):
            a = m.map[y][x].type
            f = False
            if a == ground:
                cell = load_image('colors\ground2.png', colorkey=(255, 255, 255))
                b = m.map[y][x].goverment
                if b is not None:
                    cell = load_image(f'colors\{dict_colors[b]}.png', colorkey=(255, 255, 255))
                c = m.map[y][x].entity
                if c is not None:
                    f = True
                    cell2 = load_image(f'entities\{dict_entity[c]}.png', colorkey=(255, 255, 255))
            elif a == water:
                cell = load_image('colors\water.png', colorkey=(255, 255, 255))
            # y & 1 == 0 - быстрая проверка на чётность
            screen.blit(cell, (step_x, x * 36 + (18 if y & 1 else 0) - step_y))  # -24
            if f:
                screen.blit(cell2, (step_x, x * 36 + (18 if y & 1 else 0) - step_y))
        step_x += 31
    for i in m.borders:
        pygame.draw.line(screen, (255, 255, 255), (i[0][0] + step_xx, i[0][1] - step_y),
                         (i[1][0] + step_xx, i[1][1] - step_y), width=2)
    if m.selected:
        # создадим группу, содержащую все спрайты
        all_sprites = pygame.sprite.Group()

        sprite_coin = pygame.sprite.Sprite()
        sprite_coin.image = load_image('hud_elems\coin.png', colorkey=(255, 255, 255))
        sprite_coin.rect = sprite_coin.image.get_rect()
        sprite_coin.rect.x = 15
        sprite_coin.rect.y = 15
        all_sprites.add(sprite_coin)
        # screen.blit(load_image('hud_elems\coin.png', colorkey=(255, 255, 255)), (15, 15))
        font = pygame.font.Font(None, 60)
        mon = m.goverments_money[0][0]  # Пока что выводятся деньги нулевой провинции нулевого гос-ва
        text = font.render(str(mon), True, (255, 255, 255))
        screen.blit(text, (110, 45))

        earning = m.goverments_earnings[0][0]  # Пока что выводятся доходы нулевой провинции нулевого гос-ва
        text = font.render(f'+{earning}' if earning > 0 else str(earning), True, (255, 255, 255))
        screen.blit(text, (width // 2, 45))


        screen.blit(load_image('hud_elems\end_turn.png', colorkey=(136, 0, 21)), (width - 250, height - 100))
        screen.blit(load_image('hud_elems\man0.png', colorkey=(255, 255, 255)), (width - 500, height - 100))
        screen.blit(load_image('hud_elems\house.png', colorkey=(255, 255, 255)), (width - 750, height - 100))
        screen.blit(load_image('hud_elems\\undo.png', colorkey=(255, 255, 255)), (width - 1000, height - 100))
        all_sprites.draw(screen)


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

    """Переменные для render"""
    step_x = 0
    step_y = 30

    # step_x = -15
    # step_y = -24

    m = Map(x_size, y_size)

    pygame.init()
    pygame.display.set_caption('Countries of century knights')
    size = width, height = 1000, 750
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width, height))

    fps = 60
    clock = pygame.time.Clock()

    screen.fill((0, 0, 128))
    # screen.fill((0, 0, 0))
    running = True
    rmb_pressed = False
    render(step_x, step_y)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif rmb_pressed and event.type == pygame.MOUSEBUTTONUP:
                rmb_pressed = False
            elif rmb_pressed and event.type == pygame.MOUSEMOTION:
                temp_x, temp_y = event.pos
                step_x = max(-width // 5 * 4, min(temp_x - start_x, width // 5 * 4))
                step_y = max(-height // 2, min(start_y - temp_y, height // 2))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    m.click_processing(m.get_coords(event.pos, step_x, step_y))
                elif event.button == 3:
                    start_x, start_y = event.pos[0] - step_x, event.pos[1] + step_y
                    rmb_pressed = True
            render(step_x, step_y)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
