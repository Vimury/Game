from MainField import Map
from Train_map_class import Training
import pygame
import os
import sys
from variables import *


def render(step_xx, step_y):
    if m.update:
        # screen.fill((0, 0, 128))
        screen.blit(water_bg, (-100, -100))
        step_x = step_xx
        # step_x = -15
        for y in range(y_size):
            for x in range(x_size):
                a = m.map[y][x].type
                f = False
                f2 = False
                if a == ground:
                    cell = load_image('colors\ground3.png')
                    b = m.map[y][x].government
                    if b is not None:
                        cell = load_image(f'colors\{dict_colors[b]}.png')
                    c = m.map[y][x].entity
                    if c is not None:
                        f = True
                        if c == castle and m.move + 1 == b:
                            f2 = True
                            cell3 = load_image('entities\exclamation_mark.png')

                        cell2 = load_image(f'entities\{dict_entity[c]}.png')
                elif a == water:
                    cell = load_image('colors\water4.png')
                # y & 1 == 0 - быстрая проверка на чётность
                screen.blit(cell, (step_x, x * 36 + (18 if y & 1 else 0) - step_y))  # -24
                if f:
                    screen.blit(cell2, (step_x, x * 36 + (18 if y & 1 else 0) - step_y))
                if f2:
                    screen.blit(cell3, (step_x, x * 36 + (18 if y & 1 else 0) - step_y))
            step_x += 31
        if m.borders:
            if m.buy_unit is None and m.buy_building is None and type(m.selected) == bool:
                for i in m.borders:
                    pygame.draw.line(screen, (255, 255, 255), (i[0][0] + step_xx, i[0][1] - step_y),
                                     (i[1][0] + step_xx, i[1][1] - step_y), width=3)
            else:
                for i in m.borders:
                    pygame.draw.line(screen, (91, 217, 227), (i[0][0] + step_xx, i[0][1] - step_y),
                                     (i[1][0] + step_xx, i[1][1] - step_y), width=3)
                m.borders = []

        if m.selected:
            screen.blit(load_image('hud_elems\coin.png'), (15, 15))
            font = pygame.font.Font(None, 60)
            mon = m.governments_money[m.move][m.map[m.where_click[0]][m.where_click[1]].province]
            text = font.render(str(mon), True, (255, 255, 255))
            screen.blit(text, (110, 45))

            # print(m.where_click[0], m.where_click[1], m.map[m.where_click[0]][m.where_click[1]].province)
            earning = m.governments_earnings[m.move][m.map[m.where_click[0]][m.where_click[1]].province]
            text = font.render(f'+{earning}' if earning > 0 else str(earning), True, (255, 255, 255))
            screen.blit(text, (width // 2, 45))

            screen.blit(load_image('hud_elems\end_turn.png'), (width - 250, height - 100))
            image = load_image('hud_elems\man0.png')
            # image = pygame.transform.scale(image, (100, 120))
            screen.blit(image, (width - 500, height - 160))
            screen.blit(load_image('hud_elems\house.png'), (width - 750, height - 140))
            screen.blit(load_image('hud_elems\\undo.png'), (width - 1000, height - 100))

            if m.buy_unit is not None:
                buy = load_image(f'hud_elems\man{m.buy_unit}.png')
                screen.blit(buy, (width * 0.35, height - 210))
                text = font.render(f'${m.buy_unit * 10 + 10}', True, (255, 255, 255))
                screen.blit(text, (width * 0.4, height - 60))
            elif m.buy_building is not None:
                buy = load_image(f'hud_elems\{dict_entity[m.buy_building + 6]}.png')
                screen.blit(buy, (width * 0.38, height - 200))
                text = font.render(f'${m.buy_building * 5 + 15}', True, (255, 255, 255))
                screen.blit(text, (width * 0.4, height - 60))
        m.update = False


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
            m.buy_unit = None
            # None - если нет покупок, 0-3 - если покупаются персонажи
            buy_building = None
            # None - если нет покупок, 0-2 - если покупаются сооружения
            start_window = False


class Training_button(pygame.sprite.Sprite):
    image = load_image("training.png", (255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Training_button.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 3 - 50
        self.rect.y = height * 0.44

    def update(self, *args):
        global start_window, m, step_x, step_y, training
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            governments_num = 2
            exp.stage = 0
            tip.stage = 0
            m = Training(x_size, y_size, governments_num)
            # m = Map(x_size, y_size, governments_num, training=True)

            m.buy_unit = None
            # None - если нет покупок, 0-3 - если покупаются персонажи
            buy_building = None
            # None - если нет покупок, 0-2 - если покупаются сооружения
            m.governments_money[0][0] += m.governments_earnings[0][0]
            start_window = False
            training = True
            step_x = 250
            step_y = -200


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
        match self.stage:
            case 0:
                im_flag = (470, 310)
            case 1:
                im_flag = (570, 335)
            case 2:
                is_tip = 2
            case 3:
                im_flag = (350, height - 120)
            case 4:
                im_flag = (500, 330)
            case 5:
                is_tip = 2
            case 6:
                im_flag = (600, height - 120)
            case 7:
                im_flag = (530, 340)
            case 8:
                is_tip = 2
        if stage:
            self.stage += 1
        tip_text = font.render(self.texts[self.stage], True, (0, 0, 0))
        # print(self.stage, "- tip")

        m.update = True


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
                       "Деревья уменьшают доход,", "Для победы нужно не оставить", "Завершить ход можно",
                       "Обучение окончено.", "", "Соединяй юнитов, чтобы получить более сильных"]
        self.texts2 = ["чтобы захватить земли", "тем больше прибыль", "соседние клетки", "соседние клетки",
                       "Сильные едят больше", "то юниты умрут", "поэтому их надо рубить", "ни одной клетки противника",
                       "нажав на кнопку справа внизу", "ЛКМ чтобы выйти", ""]

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
        m.update = True
        # print(self.stage, "- exp")


def start_menu():
    global is_stat, running
    if not is_stat:
        screen.fill((230, 238, 156))
        font = pygame.font.SysFont('arial', 95)
        title = font.render('Countries of century knights', True, (255, 255, 255))
        screen.blit(load_image("2.jpg"), (0, 0))
        # screen.blit(load_image('play_button.png'), (360, 250))
        # screen.blit(load_image('shut_down.png'), (830, 600))
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
                wins = values[3]
                font = pygame.font.SysFont('arial', 50)
                text = font.render(f'Время: {h} ч {m} мин', True, (255, 255, 255))
                screen.blit(text, (50, 100))
                text = font.render(f'Победы: {wins}', True, (255, 255, 255))
                screen.blit(text, (50, 160))
                pygame.display.flip()


def end_menu():
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f'Вы победили, поздравляю', True, (255, 255, 255))
    screen.blit(text, (width // 4, height // 2))
    text = font.render(f'Выйти', True, (255, 255, 255))
    screen.blit(text, (width // 3, height // 2 + 100))


def pause_menu():
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f"Продолжить", True, (255, 255, 255))
    screen.blit(text, (width // 3, height // 2.5))
    text = font.render(f'Выйти в меню', True, (255, 255, 255))
    screen.blit(text, (width // 3, height // 2.5 + 100))


if __name__ == '__main__':
    x_size, y_size = 20, 30

    """Переменные для render"""
    step_x = 30
    step_y = 0

    pygame.init()
    pygame.display.set_caption('Countries of century knights')
    size = width, height = 1000, 750
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_icon(load_image('icon.png'))

    start_sprites = pygame.sprite.Group()
    fight = Fight(start_sprites)
    training = Training_button(start_sprites)
    stat = Stats(start_sprites)

    game_sprite1 = pygame.sprite.Group()
    game_sprite2 = pygame.sprite.Group()
    tip = Tip(game_sprite1)
    exp = Explanation(game_sprite2)
    im = load_image("cursor3.png", (255, 255, 255))
    im = pygame.transform.scale(im, (150, 100))
    im_flag = ()

    start_window = True
    training = False
    font = pygame.font.Font(None, 60)
    tip_text = font.render("Выбери юнита", True, (0, 0, 0))
    exp_text1 = font.render("Атакуй своими юнитами,", True, (0, 0, 0))
    exp_text2 = font.render("чтобы захватить земли", True, (0, 0, 0))
    is_tip = 2
    is_stat = False
    end_game = False
    pause = False

    water_bg = load_image("water_bg.png")

    end_turn_pos = ((width - 250, height - 100), (width - 160, height - 10))
    unit_shop = ((width - 470, height - 130), (width - 360, height - 10))
    build_shop = ((width - 750, height - 120), (width - 630, height - 4))
    undo_pos = ((width - 1000, height - 100), (width - 904, height - 4))

    fps = 100
    clock = pygame.time.Clock()

    running = True
    rmb_pressed = False

    out = 0

    screen.fill((0, 0, 128))
    # screen.fill((0, 0, 0))
    timer = 0
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    ind = 0

    while running:
        for event in pygame.event.get():
            # print(clock.get_fps())
            if event.type == pygame.QUIT:
                running = False
            if start_window:
                start_sprites.update(event)
            elif event.type == pygame.KEYDOWN:
                pause = not pause
                m.update = True
            elif rmb_pressed and event.type == pygame.MOUSEBUTTONUP:
                rmb_pressed = False
            elif rmb_pressed and event.type == pygame.MOUSEMOTION:
                if not pause:
                    temp_x, temp_y = event.pos
                    m.update = True
                    step_x = max(-width // 5, min(temp_x - start_x, width // 5))
                    step_y = max(-height // 5, min(start_y - temp_y, height // 5))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    m.checked_to_zero()
                    if end_game:
                        end_game = False
                        start_window = True
                    x, y = event.pos
                    if pause:
                        if width // 3 < x < width // 1.7 and height // 2.4 < y < height // 2.1:
                            # print("Продолжаем")
                            pause = False
                            m.update = True
                        elif width // 3 < x < width // 1.5 and height // 1.9 < y < height // 1.6:
                            # print("Выход")
                            start_window = True
                            pause = False
                    elif not training:
                        if m.selected:
                            if end_turn_pos[0][0] < x < end_turn_pos[1][0] and end_turn_pos[0][1] < y < end_turn_pos[1][1]:
                                # m.move = (m.move + 1) % m.governments_num
                                countries = []
                                for i in range(y_size):
                                    for j in range(x_size):
                                        if m.map[i][j].government is not None:
                                            if m.map[i][j].government not in countries:
                                                countries.append(m.map[i][j].government)
                                countries = sorted(countries)

                                if len(countries) == 1:
                                    end_game = True
                                else:
                                    ind = (ind + 1) % len(countries)
                                    m.move = countries[ind] - 1
                                    while m.move in m.bots:
                                        m.borders = []
                                        m.selected = False
                                        m.where_click = ()
                                        for i in range(y_size):
                                            for j in range(x_size):
                                                if m.map[i][j].government == m.move + 1 and m.map[i][j].entity is not None:
                                                    if 10 < m.map[i][j].entity < 15:
                                                        if m.governments_money[m.map[i][j].government - 1][
                                                            m.map[i][j].province] < 0:
                                                            m.governments_earnings[m.map[i][j].government - 1][
                                                                m.map[i][j].province] += dict_units_earnings[
                                                                                             m.map[i][j].entity] - 1
                                                            m.map[i][j].entity = grave
                                                            m.defend_level_down(i, j)
                                                        m.map[i][j].can_move = 1
                                                    elif m.map[i][j].entity == grave:
                                                        m.map[i][j].entity = tree
                                        for i in range(len(m.governments_money)):
                                            for j in range(len(m.governments_money[i])):
                                                if m.governments_money[i][j] < 0:
                                                    m.governments_money[i][j] = 0 + m.governments_earnings[i][j]
                                        m.bot_do_turn(m.move + 1)
                                        ind = (ind + 1) % len(countries)
                                        m.move = countries[ind] - 1
                                    if ind == 0:
                                        m.num_move += 1
                                    m.borders = []
                                    m.selected = False
                                    m.where_click = ()
                                    if m.num_move > 1:
                                        for i in range(len(m.governments_money[m.move])):
                                            m.governments_money[m.move][i] += m.governments_earnings[m.move][i]
                                    for i in range(y_size):
                                        for j in range(x_size):
                                            if m.map[i][j].government == m.move + 1 and m.map[i][j].entity is not None:
                                                if 10 < m.map[i][j].entity < 15:
                                                    if m.governments_money[m.map[i][j].government - 1][
                                                        m.map[i][j].province] < 0:
                                                        m.governments_earnings[m.map[i][j].government - 1][
                                                            m.map[i][j].province] += dict_units_earnings[
                                                                                         m.map[i][j].entity] - 1
                                                        m.map[i][j].entity = grave
                                                        m.defend_level_down(i, j)
                                                    m.map[i][j].can_move = 1
                                                elif m.map[i][j].entity == grave:
                                                    m.map[i][j].entity = tree
                                for i in range(len(m.governments_money)):
                                    for j in range(len(m.governments_money[i])):
                                        if m.governments_money[i][j] < 0:
                                            m.governments_money[i][j] = 0 + m.governments_earnings[i][j]
                                m.update = True
                            elif unit_shop[0][0] < x < unit_shop[1][0] and unit_shop[0][1] < y < \
                                    unit_shop[1][1]:
                                """Покупка персонажа"""
                                m.selected = True
                                if m.buy_unit is None:
                                    m.buy_unit = 0
                                else:
                                    m.buy_unit = (m.buy_unit + 1) % 4
                                m.checked_to_zero()
                                m.borders = m.stroke_borders(m.where_click[0], m.where_click[1])
                            elif build_shop[0][0] < x < build_shop[1][0] and build_shop[0][1] < y < build_shop[1][1]:
                                """Покупка сооружений"""
                                m.buy_unit = None
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
                                m.buy_unit = None
                                m.buy_building = None
                        else:
                            m.buy_unit = None
                            m.buy_building = None
                            m.click_processing(m.get_coords((x, y), step_x, step_y))
                    else:
                        if exp.stage == 0:  # tip - 0, exp - 0
                            exp.update(event, stage=True)
                        elif tip.stage == 0:  # tip - 0, exp - 1
                            i, j = m.get_coords((x, y), step_x, step_y)
                            if m.map[i][j].government == red:
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
                            if unit_shop[0][0] < x < unit_shop[1][0] and unit_shop[0][1] < y < \
                                    unit_shop[1][
                                        1]:
                                """Покупка персонажа"""
                                m.selected = True
                                m.buy_unit = 0
                                m.checked_to_zero()
                                m.borders = m.stroke_borders(m.where_click[0], m.where_click[1])
                                tip.update(stage=True)
                        elif tip.stage == 7:
                            if unit_shop[0][0] < x < unit_shop[1][0] and unit_shop[0][1] < y < \
                                    unit_shop[1][
                                        1]:
                                """Покупка персонажа"""
                                m.selected = True
                                m.buy_unit = 1
                                m.checked_to_zero()
                                m.borders = m.stroke_borders(m.where_click[0], m.where_click[1])
                                tip.update(stage=True)
                        elif tip.stage == 8:
                            i, j = m.get_coords((x, y), step_x, step_y)
                            if i == 8 and j == 5:
                                m.click_processing((i, j))
                                m.checked_to_zero()
                                m.borders = m.government_borders(m.where_click[0], m.where_click[1])
                                m.buy_unit = None
                                tip.update(stage=True)
                        elif exp.stage == 7:
                            exp.update(event, stage=True)
                        elif exp.stage == 8:
                            exp.update(event, stage=True)
                        elif exp.stage == 9:
                            exp.update(event, stage=True)
                        elif exp.stage == 10:
                            start_window = True
                            training = False
                            step_y = 30
                            step_x = 0
                            exp.stage = 0
                            tip.stage = 0
                            tip_text = font.render("Выбери юнита", True, (0, 0, 0))
                            exp_text1 = font.render("Атакуй своими юнитами,", True, (0, 0, 0))
                            exp_text2 = font.render("чтобы захватить земли", True, (0, 0, 0))
                            is_tip = 2
                elif event.button == 3:
                    start_x, start_y = event.pos[0] - step_x, event.pos[1] + step_y
                    rmb_pressed = True
            if start_window:
                start_menu()
            elif end_game:
                end_menu()
            elif pause:
                pause_menu()
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
