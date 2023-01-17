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
tower = 7
big_tower = 8
big_farm = 9
town = 10

villager = 11
man1 = 12
knight = 13
big_knight = 14

dict_entity = {1: 'tree', 2: 'stone', 3: 'gold', 4: 'fish', 5: 'castle', 6: 'farm', 7: 'tower', 8: 'big_tower',
               9: 'big_farm', 10: 'town', 11: 'villager', 12: 'man1', 13: 'knight', 14: 'big_knight'}


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
                b = m.map[y][x].government
                if b is not None:
                    cell = load_image(f'colors\{dict_colors[b]}.png', colorkey=(255, 255, 255))
                c = m.map[y][x].entity
                if c is not None:
                    f = True
                    cell2 = load_image(f'entities\{dict_entity[c]}.png', colorkey=(0, 0, 0))
            elif a == water:
                cell = load_image('colors\water.png', colorkey=(255, 255, 255))
            # y & 1 == 0 - быстрая проверка на чётность
            screen.blit(cell, (step_x, x * 36 + (18 if y & 1 else 0) - step_y))  # -24
            if f:
                screen.blit(cell2, (step_x, x * 36 + (18 if y & 1 else 0) - step_y))
        step_x += 31
    if m.buy_character is None and m.buy_building is None and type(m.selected) == bool:
        for i in m.borders:
            pygame.draw.line(screen, (255, 255, 255), (i[0][0] + step_xx, i[0][1] - step_y),
                             (i[1][0] + step_xx, i[1][1] - step_y), width=2)
    else:
        for i in m.borders:
            pygame.draw.line(screen, (91, 217, 227), (i[0][0] + step_xx, i[0][1] - step_y),
                             (i[1][0] + step_xx, i[1][1] - step_y), width=2)

    if m.selected:
        screen.blit(load_image('hud_elems\coin.png', colorkey=(255, 255, 255)), (15, 15))
        font = pygame.font.Font(None, 60)
        mon = m.governments_money[move][0]  # Пока что выводятся деньги нулевой провинции нулевого гос-ва
        text = font.render(str(mon), True, (255, 255, 255))
        screen.blit(text, (110, 45))

        earning = m.governments_earnings[move][0]  # Пока что выводятся доходы нулевой провинции нулевого гос-ва
        text = font.render(f'+{earning}' if earning > 0 else str(earning), True, (255, 255, 255))
        screen.blit(text, (width // 2, 45))

        screen.blit(load_image('hud_elems\end_turn.png', colorkey=(0, 0, 0)), (width - 250, height - 100))
        im = load_image('hud_elems\man0.png', colorkey=(255, 255, 255))
        im = pygame.transform.scale(im, (100, 120))
        screen.blit(im, (width - 500, height - 130))
        screen.blit(load_image('hud_elems\house.png', colorkey=(255, 255, 255)), (width - 750, height - 100))
        screen.blit(load_image('hud_elems\\undo.png', colorkey=(255, 255, 255)), (width - 1000, height - 100))

        if m.buy_character is not None:
            buy = load_image(f'hud_elems\man{m.buy_character}.png', colorkey=(255, 255, 255))
            screen.blit(buy, (width * 0.38, height - 200))
            text = font.render(f'${m.buy_character * 10 + 10}', True, (255, 255, 255))
            screen.blit(text, (width * 0.4, height - 60))
        elif m.buy_building is not None:
            buy = load_image(f'hud_elems\{dict_entity[m.buy_building + 6]}.png', colorkey=(255, 255, 255))
            screen.blit(buy, (width * 0.38, height - 200))
            text = font.render(f'${m.buy_building * 5 + 15}', True, (255, 255, 255))
            screen.blit(text, (width * 0.4, height - 60))


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

    governments_num = 2
    m = Map(x_size, y_size, governments_num)
    move = 0

    pygame.init()
    pygame.display.set_caption('Countries of century knights')
    size = width, height = 1000, 750
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width, height))

    end_turn_pos = ((width - 250, height - 100), (width - 160, height - 10))
    charact_shop = ((width - 500, height - 130), (width - 400, height - 10))
    build_shop = ((width - 750, height - 100), (width - 654, height - 4))
    undo_pos = ((width - 1000, height - 100), (width - 904, height - 4))

    fps = 60
    clock = pygame.time.Clock()

    screen.fill((0, 0, 128))
    # screen.fill((0, 0, 0))
    running = True
    rmb_pressed = False
    m.buy_character = None
    # None - если нет покупок, 0-3 - если покупаются персонажи
    buy_building = None
    # None - если нет покупок, 0-2 - если покупаются сооружения
    render(step_x, step_y)

    m.governments_money[0][0] += m.governments_earnings[0][0]
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
                for i in range(m.y):
                    for j in range(m.x):
                        m.map[i][j].checked = 0
                if event.button == 1:
                    x, y = event.pos
                    if m.selected:
                        if end_turn_pos[0][0] < x < end_turn_pos[1][0] and end_turn_pos[0][1] < y < end_turn_pos[1][1]:
                            move = (move + 1) % governments_num
                            m.move = (m.move + 1) % governments_num
                            m.borders = []
                            m.selected = False
                            m.where_click = ()
                            for i in range(len(m.governments_money[move])):
                                m.governments_money[move][i] += m.governments_earnings[move][i]
                            for i in range(x_size):
                                for j in range(y_size):
                                    pass
                            for i in range(y_size):
                                for j in range(x_size):
                                    if m.map[i][j].government == m.move + 1 and m.map[i][j].entity is not None:
                                        if 10 < m.map[i][j].entity < 15:
                                            m.map[i][j].can_move = 1
                        elif charact_shop[0][0] < x < charact_shop[1][0] and charact_shop[0][1] < y < charact_shop[1][
                            1]:
                            """Покупка персонажа"""
                            m.selected = True
                            if m.buy_character is None:
                                m.buy_character = 0
                            else:
                                m.buy_character = (m.buy_character + 1) % 4
                            for i in range(m.y):
                                for j in range(m.x):
                                    m.map[i][j].checked = 0
                            m.borders = m.stroke_borders(m.where_click[0], m.where_click[1])
                        elif build_shop[0][0] < x < build_shop[1][0] and build_shop[0][1] < y < build_shop[1][1]:
                            """Покупка сооружений"""
                            m.selected = True
                            if m.buy_building is None:
                                m.buy_building = 0
                            else:
                                m.buy_building = (m.buy_building + 1) % 3
                            m.borders = m.government_borders(m.where_click[0], m.where_click[1])
                        elif undo_pos[0][0] < x < undo_pos[1][0] and undo_pos[0][1] < y < undo_pos[1][1]:
                            """Возврат хода назад"""
                            pass
                        else:
                            m.click_processing(m.get_coords((x, y), step_x, step_y))
                            m.buy_character = None
                            m.buy_building = None
                    else:
                        m.buy_character = None
                        m.buy_building = None
                        m.click_processing(m.get_coords((x, y), step_x, step_y))
                elif event.button == 3:
                    start_x, start_y = event.pos[0] - step_x, event.pos[1] + step_y
                    rmb_pressed = True
            render(step_x, step_y)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
