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
        image = load_image('hud_elems\man0.png', colorkey=(255, 255, 255))
        # image = pygame.transform.scale(image, (100, 120))
        screen.blit(image, (width - 500, height - 140))
        screen.blit(load_image('hud_elems\house.png', colorkey=(255, 255, 255)), (width - 750, height - 140))
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
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Fight(pygame.sprite.Sprite):
    image = load_image("fight.png", (255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Fight.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 3 - 50
        self.rect.y = height * 0.2 - 30

    def update(self, *args):
        global start_window, m
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            governments_num = 4
            m = Map(x_size, y_size, governments_num)
            m.buy_character = None
            # None - если нет покупок, 0-3 - если покупаются персонажи
            buy_building = None
            # None - если нет покупок, 0-2 - если покупаются сооружения
            m.governments_money[0][0] += m.governments_earnings[0][0]
            start_window = False


class Stats(pygame.sprite.Sprite):
    image = load_image("stats.png", (255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Stats.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 3 - 50
        self.rect.y = height * 0.75 - 30

    def update(self, *args):
        global start_window, m, is_stat
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            is_stat = True


class Training(pygame.sprite.Sprite):
    image = load_image("training.png", (255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Training.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 3 - 50
        self.rect.y = height * 0.44

    def update(self, *args):
        global start_window, m, step_x, step_y, training
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            governments_num = 2
            m = Map(x_size, y_size, governments_num, training=True)
            m.buy_character = None
            # None - если нет покупок, 0-3 - если покупаются персонажи
            buy_building = None
            # None - если нет покупок, 0-2 - если покупаются сооружения
            m.governments_money[0][0] += m.governments_earnings[0][0]
            start_window = False
            training = True
            step_x = 250
            step_y = -200


class Tip(pygame.sprite.Sprite):
    image = load_image("tip.png", (255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Tip.image
        self.rect = self.image.get_rect()
        self.rect.x = width * 0.15
        self.rect.y = 0
        self.stage = 0
        self.texts = ["Нажми на государство", "Выбери юнита", "Нажми на поле", "Нажми на кнопку", "Ещё раз",
                      "Построй башню", "Нажми на кнопку", "Ещё раз", "Поставь копейщика", '', '']

    def update(self, stage=False):
        global tip_text, is_tip, im_flag
        font = pygame.font.Font(None, 60)
        if self.stage == 0:
            im_flag = (470, 330)
        elif self.stage == 1:
            im_flag = (570, 355)
        elif self.stage == 2:
            im_flag = ()
            is_tip = 2
            exp.update()
        elif self.stage == 3:
            im_flag = (350, height - 100)
        elif self.stage == 4:
            im_flag = (500, 350)
        elif self.stage == 5:
            is_tip = 2
        elif self.stage == 6:
            im_flag = (630, height - 100)
        elif self.stage == 7:
            im_flag = (530, 370)
        elif self.stage == 8:
            is_tip = 2
        if stage:
            self.stage += 1
        tip_text = font.render(self.texts[self.stage], True, (0, 0, 0))
        # print(self.stage, "- tip")


class Explanation(pygame.sprite.Sprite):
    image = load_image("explonation.png", (255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Explanation.image
        self.rect = self.image.get_rect()
        self.rect.x = width * 0.15
        self.rect.y = height * 0.7
        self.stage = 0
        self.texts1 = ["Атакуй своими юнитами,", "Чем больше земель,",
                       "Строй башни, чтобы защитить", "Юниты тоже защищают",
                       "Юниты тратят деньги.", "Если деньги кончатся,",
                       "Деревья уменьшают доход,", "Для победы нужно не оставить", "Обучение окончено.",
                       "Соединяй юнитов, чтобы получить более сильных"]
        self.texts2 = ["чтобы захватить земли", "тем больше прибыль", "соседние клетки", "соседние клетки",
                       "Сильные едят больше", "то юниты умрут", "поэтому их надо рубить", "ни одной клетки противника",
                       "ЛКМ чтобы выйти"]

    def update(self, *args, stage=False):
        global exp_text1, exp_text2, is_tip
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if self.stage == 0:
                is_tip = 1
                tip.update()
            elif self.stage == 3:
                is_tip = 1
                tip.update()
            elif self.stage == 6:
                is_tip = 1
                tip.update()
            font = pygame.font.Font(None, 60)
            exp_text1 = font.render(self.texts1[self.stage], True, (0, 0, 0))
            exp_text2 = font.render(self.texts2[self.stage], True, (0, 0, 0))
            if stage:
                self.stage += 1
        # print(self.stage, "- exp")


def start_menu():
    global is_stat, running
    if not is_stat:
        screen.fill((230, 238, 156))
        font = pygame.font.SysFont('arial', 95)
        title = font.render('Countries of century knights', True, (255, 255, 255))
        screen.blit(load_image("2.jpg"), (0, 0))
        # screen.blit(load_image('play_button.png', colorkey=(0, 0, 0)), (360, 250))
        # screen.blit(load_image('shut_down.png', colorkey=(255, 255, 255)), (830, 600))
        screen.blit(title, (1000 / 2 - title.get_width() / 2, 100 / 2 - title.get_height() / 2))
        start_sprites.draw(screen)
        pygame.display.update()
    else:
        while is_stat:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    is_stat = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    is_stat = False
                screen.blit(load_image("2.jpg"), (0, 0))
                with open('data/stats.txt') as file:
                    values = file.read().split("\n")
                h = values[0]
                m = values[1]
                font = pygame.font.SysFont('arial', 50)
                text = font.render(f'Время: {h} ч {m} мин', True, (255, 255, 255))
                screen.blit(text, (50, 100))
                pygame.display.flip()





if __name__ == '__main__':
    x_size, y_size = 20, 30

    """Переменные для render"""
    step_x = 0
    step_y = 30

    pygame.init()
    pygame.display.set_caption('Countries of century knights')
    size = width, height = 1000, 750
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_icon(load_image('icon.png'))

    start_sprites = pygame.sprite.Group()
    fight = Fight(start_sprites)
    training = Training(start_sprites)
    stat = Stats(start_sprites)

    game_sprite1 = pygame.sprite.Group()
    game_sprite2 = pygame.sprite.Group()
    tip = Tip(game_sprite1)
    exp = Explanation(game_sprite2)
    im = load_image("cursor.png", (255, 255, 255))
    im_flag = ()

    start_window = True
    training = False
    font = pygame.font.Font(None, 60)
    tip_text = font.render("Выбери юнита", True, (0, 0, 0))
    exp_text1 = font.render("Атакуй своими юнитами,", True, (0, 0, 0))
    exp_text2 = font.render("чтобы захватить земли", True, (0, 0, 0))
    is_tip = 2
    is_stat = False

    end_turn_pos = ((width - 250, height - 100), (width - 160, height - 10))
    charact_shop = ((width - 500, height - 130), (width - 400, height - 10))
    build_shop = ((width - 750, height - 100), (width - 654, height - 4))
    undo_pos = ((width - 1000, height - 100), (width - 904, height - 4))

    fps = 60
    clock = pygame.time.Clock()

    running = True
    rmb_pressed = False
    move = 0

    out = 0

    screen.fill((0, 0, 128))
    # screen.fill((0, 0, 0))
    timer = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if start_window:
                start_sprites.update(event)
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
                    if not training:
                        if m.selected:
                            if end_turn_pos[0][0] < x < end_turn_pos[1][0] and end_turn_pos[0][1] < y < end_turn_pos[1][
                                1]:
                                move = (move + 1) % m.governments_num
                                m.move = (m.move + 1) % m.governments_num
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
                            elif charact_shop[0][0] < x < charact_shop[1][0] and charact_shop[0][1] < y < \
                                    charact_shop[1][
                                        1]:
                                """Покупка персонажа"""
                                m.selected = True
                                if m.buy_character is None:
                                    m.buy_character = 0
                                else:
                                    m.buy_character = (m.buy_character + 1) % 4
                                m.checked_to_zero()
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
                    else:
                        if exp.stage == 0:  # tip - 0, exp - 0
                            exp.update(event, stage=True)
                        elif tip.stage == 0:  # tip - 0, exp - 1
                            i, j = m.get_coords((x, y), step_x, step_y)
                            if i == 6 and j == 4:
                                m.click_processing((i, j))
                                tip.update(stage=True)
                        elif tip.stage == 1:  # tip - 1, exp - 1
                            i, j = m.get_coords((x, y), step_x, step_y)
                            if i == 6 and j == 4:
                                m.click_processing((i, j))
                                tip.update(stage=True)
                        elif tip.stage == 2:  # tip - 2, exp - 1
                            i, j = m.get_coords((x, y), step_x, step_y)
                            if i == 9 and j == 4:
                                m.click_processing((i, j))
                                tip.update(stage=True)
                        if exp.stage == 1:  # tip - 2, exp - 1
                            exp.update(event, stage=True)
                        elif exp.stage == 2:  # tip - 2, exp - 2
                            exp.update(event, stage=True)
                        elif exp.stage == 3:  # tip - 2, exp - 3
                            exp.update(event, stage=True)
                        elif tip.stage == 3:
                            if build_shop[0][0] < x < build_shop[1][0] and build_shop[0][1] < y < build_shop[1][1]:
                                """Покупка сооружений"""
                                m.selected = True
                                m.buy_building = 0
                                m.borders = m.government_borders(m.where_click[0], m.where_click[1])
                                tip.update(stage=True)
                        elif tip.stage == 4:
                            if build_shop[0][0] < x < build_shop[1][0] and build_shop[0][1] < y < build_shop[1][1]:
                                """Покупка сооружений"""
                                m.selected = True
                                m.buy_building = 1
                                m.borders = m.government_borders(m.where_click[0], m.where_click[1])
                                tip.update(stage=True)
                        elif tip.stage == 5:
                            i, j = m.get_coords((x, y), step_x, step_y)
                            if i == 7 and j == 4:
                                m.click_processing((i, j))
                                m.checked_to_zero()
                                m.borders = m.government_borders(m.where_click[0], m.where_click[1])
                                m.buy_building = None
                                tip.update(stage=True)
                        elif exp.stage == 4:
                            exp.update(event, stage=True)
                        elif exp.stage == 5:
                            exp.update(event, stage=True)
                        elif exp.stage == 6:
                            exp.update(event, stage=True)
                        elif tip.stage == 6:
                            if charact_shop[0][0] < x < charact_shop[1][0] and charact_shop[0][1] < y < \
                                    charact_shop[1][
                                        1]:
                                """Покупка персонажа"""
                                m.selected = True
                                m.buy_character = 0
                                m.checked_to_zero()
                                m.borders = m.stroke_borders(m.where_click[0], m.where_click[1])
                                tip.update(stage=True)
                        elif tip.stage == 7:
                            if charact_shop[0][0] < x < charact_shop[1][0] and charact_shop[0][1] < y < \
                                    charact_shop[1][
                                        1]:
                                """Покупка персонажа"""
                                m.selected = True
                                m.buy_character = 1
                                m.checked_to_zero()
                                m.borders = m.stroke_borders(m.where_click[0], m.where_click[1])
                                tip.update(stage=True)
                        elif tip.stage == 8:
                            i, j = m.get_coords((x, y), step_x, step_y)
                            if i == 8 and j == 5:
                                m.click_processing((i, j))
                                m.checked_to_zero()
                                m.borders = m.government_borders(m.where_click[0], m.where_click[1])
                                m.buy_character = None
                                tip.update(stage=True)
                        elif exp.stage == 7:
                            exp.update(event, stage=True)
                        elif exp.stage == 8:
                            exp.update(event, stage=True)
                        elif exp.stage == 9:
                            start_window = True
                            training = False
                            step_y = 30
                            step_x = 0
                elif event.button == 3:
                    start_x, start_y = event.pos[0] - step_x, event.pos[1] + step_y
                    rmb_pressed = True
            if start_window:
                start_menu()
            else:
                render(step_x, step_y)
                if training:
                    if is_tip == 1:
                        game_sprite1.draw(screen)
                        screen.blit(tip_text, (width * 0.3, 20))
                        if im_flag:
                            screen.blit(im, im_flag)
                    elif is_tip == 2:
                        game_sprite2.draw(screen)
                        screen.blit(exp_text1, (width * 0.2, height * 0.7 + 5))
                        screen.blit(exp_text2, (width * 0.2, height * 0.7 + 55))
        out += clock.get_time()
        clock.tick(fps)
        pygame.display.flip()
    with open('data/stats.txt', 'r') as file:
        values = file.read().split("\n")
        values[2] = f'{int(values[2]) + (out // 1000)}'
        values[1] = f'{int(values[1]) + int(values[2]) // 60}'
        values[2] = f'{int(values[2]) % 60}'
        values[0] = f'{int(values[1]) // 60 + int(values[0])}'
        values[1] = f'{int(values[1]) % 60}'
    with open('data/stats.txt', 'w') as file:
        file.write("\n".join(values))
    pygame.quit()
