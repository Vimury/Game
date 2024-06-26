from math import sqrt
from typing import List, Optional, Union, Tuple
import numpy as np

'''Прописал id типа местности'''
water = 0
ground = 1

'''Прописал id государств'''
sp = [(red := 1), (pink := 2), (green := 3), (light_green := 4), (blue := 5), (light_blue := 6), (orange := 7),
      (yellow := 8), (purple := 9)]

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

grave = 15

dict_units_earnings = {villager: 2, man1: 5, knight: 10, big_knight: 15}

from random import randint, choices


class Map:
    def __init__(self, x, y, governments_num):
        self.x: int = x
        self.y: int = y
        # Размер поля в шестиугольниках
        self.selected: Union[bool, tuple] = False
        # selected - 3 вариации
        # False - если ничего не выбрано, True - если выбрано государство, Tuple - если выбран персонаж
        self.governments_num: int = governments_num  # Количество государств
        self.governments_money: List[List[int]] = []
        # governments_money[i][j] - количество денег j-той провинции i-того государства
        self.governments_earnings: List[List[int]] = []
        # governments_money[i][j] - заработок j-той провинции i-того государства
        self.borders = []
        # Хранение кортежей, между точками которых нужно провести границы
        self.move: int = 0
        # Чей ход
        self.where_click: tuple = ()
        # Куда был сделан последний клик на государство
        self.bfs_queue = []
        # Надо для обхода в ширину
        self.buy_unit: Optional[int] = None
        self.buy_building: Optional[int] = None
        self.centres = np.array([np.array([[0, 0] for j in range(self.x)]) for i in range(self.y)])
        # centres[i][j] - расположение центра [i][j] шестиугольника(в пикселях)
        self.update = True
        self.logs = []
        self.bots = []
        self.num_move = 1
        for i in range(2, governments_num):
            self.bots.append(i)
        step_x = 0
        for i in range(self.y):
            for j in range(self.x):
                self.centres[i][j] = [step_x + 22, (j * 36 + (18 if i & 1 else 0)) + 24]
            step_x += 31
        self.gr = 0
        # Количество земли на карте
        # self.map: List[List[Cell]] = self.pre_generate()
        self.pre_generate()
        self.after_generate()
        # max_gr = (self.x - 1) * (self.y - 1) * 3 // 4
        # min_gr = (self.x - 1) * (self.y - 1) // 4
        max_gr = (self.x - 4) * (self.y - 4) * 3 // 4  # Максимальное количество клеток земли на карте
        min_gr = (self.x - 4) * (self.y - 4) // 4  # Минимальное количество клеток земли на карте
        while self.gr > max_gr or self.gr < min_gr:
            self.gr = 0
            self.pre_generate()
            self.after_generate()
        self.generate_governments()

        # for i in range(self.y):
        #     for j in range(self.x):
        #         self.map[i][j].type = water
        # self.map[2][2].type = ground
        # self.map[2][3].type = ground
        # self.map[2][2].government = red
        # self.map[2][3].government = red
        # self.map[2][2].capital = (2, 2)
        # self.map[2][3].capital = (2, 2)
        # self.map[2][2].entity = castle
        # self.map[3][3].type = ground

        # for i in range(x):
        #     for j in range(y):
        #         print(self.map[j][i].type, end=' ')
        #     print()
        # print()

        # for i in range(x):
        #     for j in range(y):
        #         print(self.map[j][i].entity, end=' ')
        #     print()
        # sp = []
        # for i in range(x):
        #     for j in range(y):
        #         if self.map[j][i].type == ground:
        #             if self.map[j][i].parent not in sp:
        #                 sp.append(self.map[j][i].parent)
        #             print(self.map[j][i].parent, end=' ')
        #         else:
        #             print((0, 0), end=' ')
        #     print()

        # for i in range(y):
        #     for j in range(x):
        #         self.map[i][j].type = water
        #         self.map[i][j].entity = None
        # for i in [(13, 6), (12, 6), (11, 7), (11, 8), (11, 6), (11, 9), (11, 10), (12, 11), (13, 10),
        #           (15, 9), (15, 10), (16, 11), (16, 9), (17, 9), (17, 10),
        #           (19, 9), (19, 10), (20, 11), (21, 10), (21, 9),
        #           (23, 9), (23, 10), (24, 9), (25, 10), (25, 9),
        #           (27, 10), (28, 11), (29, 10), (27, 9), (27, 8), (27, 7), (27, 6), (26, 7), (28, 8),
        #           (31, 10), (31, 9), (31, 8), (32, 8), (33, 8),
        #           (35, 6), (35, 8), (35, 9), (35, 10),
        #           (37, 8), (38, 9), (39, 8), (39, 7), (38, 7), (37, 7), (37, 9), (37, 10), (38, 11), (39, 10),
        #           (41, 10), (42, 11), (43, 10), (43, 9), (42, 9), (41, 8), (42, 7), (43, 7), (41, 7)]:
        #     self.map[i[0]][i[1] - 5].type = ground
        # И чтоб красивее было смонтировать немного(e, s)

    # Функция генерации
    def pre_generate(self):
        sp1 = np.array([[randint(0, 2)] * 2 for i in range(2)])
        sp2 = np.array([[randint(0, 2)] * 5 for i in range(5)])
        sp3 = np.array([[randint(0, 2)] * 10 for i in range(10)])
        sp4 = np.array([[randint(0, 2)] * self.x for i in range(self.y)])
        self.map = np.array([[Cell(water, None, (-1, -1))] * self.x for i in range(self.y)])
        for i in range(2, self.y - 2):
            for j in range(self.x):
                if j < 2 or j > self.x - 2:
                    continue
                else:
                    if sp1[2 * i // self.y][2 * j // self.x] == 0:
                        self.map[i][j] = Cell(
                            choices([ground, water], weights=[5, 8 - sp2[5 * i // self.y][j * 5 // self.x] -
                                                              sp3[i * 10 // self.y][j * 10 // self.x] -
                                                              sp4[i][j]])[0], None, (i, j))
                    else:
                        self.map[i][j] = Cell(
                            choices([ground, water], weights=[8, 8 - sp1[2 * i // self.y][2 * j // self.x] -
                                                              sp2[5 * i // self.y][j * 5 // self.x] -
                                                              sp3[i * 10 // self.y][j * 10 // self.x] - sp4[i][
                                                                  j]])[0],
                            None, (i, j))
                    if self.map[i][j].type == ground:
                        self.map[i][j].entity = choices([tree, stone, gold, None], weights=[6, 0, 0, 12])[0]

    def unite_islands(self, first: tuple, i: int, j: int) -> None:
        temp = self.check_neighbours(water, i, j)
        for k in temp[1]:
            if 1 < k[0] < self.y - 1:
                if 1 < k[1] < self.x - 1:
                    if randint(0, 2) > 0:
                        self.map[k[0]][k[1]] = Cell(ground, None, self.map[i][j].parent)

        temp = self.check_neighbours(ground, i, j)
        for k in temp[1]:
            if not self.map[k[0]][k[1]].checked:
                self.map[k[0]][k[1]].checked = 1
                if self.map[k[0]][k[1]].parent == first:
                    self.unite(i, j, k[0], k[1])
                    break
                else:
                    self.unite_islands(first, k[0], k[1])

    def after_generate(self) -> None:
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    temp = self.check_neighbours(ground, i, j)
                    if not temp[0]:
                        self.map[i][j].type = water
                        self.map[i][j].entity = None
                        self.map[i][j].parent = (-1, -1)
                    else:
                        for k in temp[1]:
                            self.unite(i, j, k[0], k[1])
                else:
                    self.map[i][j].parent = (-1, -1)
        sp = []
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    if self.map[i][j].parent not in sp:
                        sp.append(self.map[i][j].parent)
        for o in range(1, len(sp)):
            i = sp[o][0]
            j = sp[o][1]
            self.unite_islands(sp[0], i, j)
            self.checked_to_zero()

        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    self.gr += 1

    def generate_governments(self):
        self.capitals = []
        for k in range(self.governments_num):
            i, j = randint(2, self.y - 2), randint(2, self.x - 2)
            while True:
                if self.map[i][j].type == ground:
                    for t in self.capitals:
                        if abs(t[0] - i) < 3 or abs(t[1] - j) < 3:
                            i, j = randint(2, self.y - 2), randint(2, self.x - 2)
                            break
                    else:
                        break
                else:
                    i, j = randint(2, self.y - 2), randint(2, self.x - 2)
            self.capitals.append((i, j))
        c = 1
        for k in self.capitals:
            a, sp = self.check_neighbours(ground, k[0], k[1])
            self.map[k[0]][k[1]].government = c
            self.map[k[0]][k[1]].province = 0
            self.map[k[0]][k[1]].capital = (k[0], k[1])
            self.map[k[0]][k[1]].government_size = 1
            self.map[k[0]][k[1]].entity = castle
            self.governments_money.append([1000])
            self.governments_earnings.append([1])
            for t in sp:
                self.map[t[0]][t[1]].government = c
                self.map[t[0]][t[1]].capital = (t[0], t[1])
                self.map[t[0]][t[1]].government_size = 1
                self.governments_earnings[-1].append(1)
                self.map[t[0]][t[1]].province = 1
                self.governments_money[-1].append(0)
                if self.map[t[0]][t[1]].entity == tree:
                    self.governments_earnings[-1][-1] -= 1

                self.unite_governments(k[0], k[1], t[0], t[1])

            c += 1

    # Проверка соседей с определённым типом
    def check_neighbours(self, type: int, i: int, j: int) -> (int, list):
        neighbours = 0
        pos = []
        a = i & 1
        # Сосед справа сверху
        # Спасибо Кузнецову Тимуру за консультацию
        if i + 1 < self.y and j - 1 + a >= 0 and self.map[i + 1][j - 1 + a].type == type:
            neighbours += 1
            pos.append((i + 1, j - 1 + a))
        # Сосед справа снизу
        if i + 1 < self.y and j + a < self.x and self.map[i + 1][j + a].type == type:
            neighbours += 1
            pos.append((i + 1, j + a))
        # Сосед слева сверху
        if i - 1 >= 0 and j - 1 >= 0 and self.map[i - 1][j - 1 + a].type == type:
            neighbours += 1
            pos.append((i - 1, j - 1 + a))
        # Сосед слева снизу
        if i - 1 >= 0 and j + a < self.x and self.map[i - 1][j + a].type == type:
            neighbours += 1
            pos.append((i - 1, j + a))
        # Сосед снизу
        if j + 1 < self.x and self.map[i][j + 1].type == type:
            neighbours += 1
            pos.append((i, j + 1))
        # Сосед сверху
        if j - 1 >= 0 and self.map[i][j - 1].type == type:
            neighbours += 1
            pos.append((i, j - 1))
        return (neighbours, pos)

    # Получение координат шестиугольника из координат клика
    def get_coords(self, pos: tuple, step_x, step_y) -> tuple:
        x, y = pos
        x -= step_x
        y += step_y
        dist = 64
        q, r = -5, -5
        for i in range(self.y):
            for j in range(self.x):
                a = sqrt((self.centres[i][j][0] - x) ** 2 + (self.centres[i][j][1] - y) ** 2)
                if a < dist:
                    dist = a
                    q, r = i, j
        print(q, r)
        # print(self.map[q][r].defend_level, "- defend")
        # print(self.map[q][r].capital, "- capital")
        # print(self.governments_earnings, "- g_e")
        print(self.map[q][r].province, "- province")
        # print(self.governments_money[self.map[q][r].government - 1][self.map[q][r].province], "q-m")
        return (q, r)

    # Обработка клика
    def click_processing(self, coords: tuple):  # на вход клетка НЕ в пикселях
        self.borders = []
        x, y = coords
        self.checked_to_zero()
        if self.map[x][y].type == ground:
            if type(self.selected) == tuple and self.selected != (x, y):
                self.can_move_bfs(self.selected[0], self.selected[1])
                if 0 < self.map[x][y].checked < 5:
                    self.do_move(self.selected[0], self.selected[1], x, y)
            else:
                if self.map[x][y].government is not None and self.map[x][y].government == self.move + 1:
                    if self.map[x][y].entity is not None and 10 < self.map[x][y].entity < 15:
                        if self.buy_unit is None:
                            """Выбираю персонажа или провинцию"""
                            if self.map[x][y].can_move:
                                if not self.selected:
                                    self.selected = True
                                    self.borders = self.government_borders(x, y)
                                else:
                                    self.selected = (x, y)
                                    self.borders = self.stroke_borders(x, y)
                                self.where_click = (x, y)

                            else:
                                self.selected = True
                                self.borders = self.government_borders(x, y)
                        else:
                            self.governments_earnings[self.move][self.map[x][y].province] += dict_units_earnings[
                                self.map[x][y].entity]
                            if self.map[x][y].entity + self.buy_unit + 1 < 15 and self.governments_money[self.move][
                                0] - (self.buy_unit * 10) + 10 >= 0:
                                self.map[x][y].entity += self.buy_unit + 1
                                self.defend_level_up(x, y)
                                self.governments_money[self.move][0] -= (self.buy_unit * 10) + 10

                            self.governments_earnings[self.move][self.map[x][y].province] -= \
                                dict_units_earnings[self.map[x][y].entity]
                            self.borders = self.government_borders(x, y)

                    elif self.buy_unit is not None and self.governments_money[self.move][0] >= (
                            self.buy_unit * 10) + 10:
                        f = True
                        if self.map[x][y].government == self.move + 1:
                            """Проверка на здание"""
                            if self.map[x][y].entity is not None and 4 < self.map[x][y].entity < 11:
                                f = False
                        if f:
                            if self.map[x][y].capital == self.map[self.where_click[0]][self.where_click[1]].capital:
                                '''Покупка юнита'''
                                """В своё гос-во"""
                                if self.map[x][y].entity == tree:
                                    self.governments_earnings[self.move][
                                        self.map[self.where_click[0]][self.where_click[1]].province] += 1
                                    self.governments_money[self.move][
                                        self.map[self.where_click[0]][self.where_click[1]].province] += 3
                                    self.map[x][y].can_move = 0
                                elif self.map[x][y].entity == grave:
                                    self.governments_earnings[self.move][
                                        self.map[self.where_click[0]][self.where_click[1]].province] += 1
                                    self.map[x][y].can_move = 0
                                else:
                                    self.map[x][y].can_move = 1
                                self.map[x][y].entity = self.buy_unit + 11
                                self.defend_level_up(x, y)
                                self.governments_earnings[self.move][
                                    self.map[self.where_click[0]][self.where_click[1]].province] -= \
                                    dict_units_earnings[self.map[x][y].entity]
                                self.governments_money[self.move][self.map[self.where_click[0]][self.where_click[1]].province] -= (
                                                                                                                self.buy_unit * 10) + 10
                                self.borders = self.government_borders(x, y)
                            else:
                                """В другое гос-во или в клетку без него"""
                                t = self.check_neighbours(ground, x, y)[1]
                                for i in t:
                                    if self.map[i[0]][i[1]].capital == \
                                            self.map[self.where_click[0]][self.where_click[1]].capital:
                                        self.map[x][y].government = self.move + 1
                                        self.map[x][y].capital = (x, y)
                                        self.map[x][y].government_size = 1
                                        self.map[x][y].province = len(self.governments_earnings[self.move])
                                        self.governments_earnings[self.move].append(
                                            -1 * dict_units_earnings[self.buy_unit + 11])
                                        self.map[x][y].entity = self.buy_unit + 11
                                        self.unite_governments(x, y, i[0], i[1])
                                        self.defend_level_up(x, y)
                                        self.governments_money[self.move][0] -= (self.buy_unit * 10) + 10
                                        self.borders = self.government_borders(x, y)
                                        print("БИЛ ЗДЕСЬ")
                                        for t in self.check_neighbours(ground, x, y)[1]:
                                            if self.map[x][y].government == self.map[t[0]][t[1]].government and self.map[x][
                                                y].province != self.map[t[0]][t[1]].province:
                                                self.unite_governments(x, y, t[0], t[1])
                                        break

                                else:
                                    if self.selected:
                                        self.update = True
                                    self.selected = False
                        else:
                            self.selected = True
                            self.borders = self.government_borders(x, y)
                            self.where_click = (x, y)
                    elif self.buy_building is not None:
                        if self.governments_money[self.move][
                            self.map[self.where_click[0]][self.where_click[1]].province] \
                                >= self.buy_building * 5 + 15:
                            if self.map[x][y].entity is None or self.map[x][y].entity == tree:
                                self.map[x][y].entity = self.buy_building + 6
                                if self.buy_building + 6 == farm:
                                    self.governments_earnings[self.move][
                                        self.map[self.where_click[0]][self.where_click[1]].province] += 4
                                self.governments_money[self.move][self.map[self.where_click[0]][
                                    self.where_click[1]].province] -= self.buy_building * 5 + 15
                        self.borders = self.government_borders(x, y)
                    else:
                        if self.map[x][y].government == (self.move + 1):
                            self.where_click = (x, y)
                            self.borders = self.government_borders(x, y)
                            self.selected = True
                elif self.map[x][y].government is not None:
                    """Атака на другое гос-во"""
                    if self.buy_unit is not None and self.governments_money[self.move][0] >= (
                            self.buy_unit * 10) + 10:
                        t = self.check_neighbours(ground, x, y)[1]
                        for i in t:
                            if self.map[i[0]][i[1]].capital == \
                                    self.map[self.where_click[0]][self.where_click[1]].capital:
                                self.checked_to_zero()
                                if self.dfs((x, y)):
                                    self.checked_to_zero()
                                    self.map[x][y].checked = 1
                                    f = False
                                    for j in self.check_neighbours(ground, x, y)[1]:
                                        if self.map[j[0]][j[1]].government == self.map[x][y].government and not \
                                                self.map[j[0]][j[1]].checked:
                                            if f:
                                                self.map[j[0]][j[1]].capital = j
                                                self.map[j[0]][j[1]].government_size = 1
                                                self.map[j[0]][j[1]].entity = castle
                                                self.governments_money[self.map[j[0]][j[1]].government - 1].append(
                                                    self.governments_money[self.map[j[0]][j[1]].government - 1][
                                                        self.map[j[0]][j[1]].province] // 3)  # Пересчитать деньги
                                                self.map[j[0]][j[1]].province = len(
                                                    self.governments_earnings[self.map[j[0]][j[1]].government - 1])
                                                self.governments_earnings[self.map[j[0]][j[1]].government - 1].append(1)
                                                self.dfs_2(j[0], j[1])
                                            else:
                                                f = True
                                                self.map[j[0]][j[1]].capital = j
                                                self.map[j[0]][j[1]].government_size = 1
                                                self.map[j[0]][j[1]].entity = castle
                                                self.governments_money[self.map[j[0]][j[1]].government - 1][
                                                    self.map[j[0]][j[1]].province] //= 3  # Пересчитать деньги
                                                self.governments_earnings[self.map[j[0]][j[1]].government - 1][
                                                    self.map[j[0]][j[1]].province] = 1
                                                self.dfs_2(j[0], j[1])

                                a = self.get_capital(i[0], i[1])
                                self.map[x][y].government = self.move + 1
                                self.map[x][y].capital = (x, y)
                                self.map[x][y].government_size = 1
                                self.map[x][y].province = len(self.governments_earnings[self.move])
                                self.map[x][y].entity = self.buy_unit + 11
                                self.governments_earnings[self.move].append(
                                    1 - dict_units_earnings[self.buy_unit + 11])
                                self.governments_money[self.move].append(0)
                                self.unite_governments(x, y, a[0], a[1])
                                self.defend_level_up(x, y)
                                self.governments_money[self.move][0] -= (self.buy_unit * 10) + 10
                                self.checked_to_zero()
                                self.borders = self.government_borders(x, y)
                                for t in self.check_neighbours(ground, x, y)[1]:
                                    if self.map[x][y].government == self.map[t[0]][t[1]].government and self.map[x][
                                        y].province != self.map[t[0]][t[1]].province:
                                        self.unite_governments(x, y, t[0], t[1])
                                break
                        else:
                            if self.selected:
                                self.update = True
                            self.selected = False
                    else:
                        if self.selected:
                            self.update = True
                        self.selected = False
                else:
                    if self.buy_unit is not None and self.governments_money[self.move][0] >= (
                            self.buy_unit * 10) + 10:
                        t = self.check_neighbours(ground, x, y)[1]
                        for i in t:
                            if self.map[i[0]][i[1]].capital == \
                                    self.map[self.where_click[0]][self.where_click[1]].capital:
                                a = self.get_capital(i[0], i[1])
                                self.map[x][y].government = self.move + 1
                                self.map[x][y].capital = (x, y)
                                self.map[x][y].government_size = 1
                                self.map[x][y].province = len(self.governments_earnings[self.move])
                                self.map[x][y].entity = self.buy_unit + 11
                                self.governments_earnings[self.move].append(
                                    1 - dict_units_earnings[self.buy_unit + 11])
                                self.governments_money[self.move].append(0)
                                self.unite_governments(x, y, a[0], a[1])
                                self.defend_level_up(x, y)
                                self.governments_money[self.move][0] -= (self.buy_unit * 10) + 10
                                self.borders = self.government_borders(x, y)
                                for t in self.check_neighbours(ground, x, y)[1]:
                                    if self.map[x][y].government == self.map[t[0]][t[1]].government and self.map[x][
                                        y].province != self.map[t[0]][t[1]].province:
                                        self.unite_governments(x, y, t[0], t[1])
                                break
                        else:
                            if self.selected:
                                self.update = True
                            self.selected = False
                    else:
                        if self.selected:
                            self.update = True
                        self.selected = False
        else:
            if self.selected:
                self.update = True
            self.selected = False

    def update_logs(self, what, where, prov=False):
        pass

    def bot_do_turn(self, color):
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].government == color:
                    if self.map[i][j].entity is None:
                        if self.governments_money[color - 1][self.map[i][j].province] >= 15 and randint(0, 1):
                            '''Бот покупает ферму'''
                            self.map[i][j].entity = farm
                            self.governments_money[color - 1][self.map[i][j].province] -= 15
                            self.governments_earnings[color - 1][self.map[i][j].province] += 4
                    if self.governments_money[color - 1][self.map[i][j].province] >= 10:
                        '''Бот покупает юнита'''
                        if self.map[i][j].entity is not None and self.map[i][j].entity == tree:
                            self.governments_earnings[color - 1][self.map[i][j].province] += 1
                            self.governments_money[color - 1][self.map[i][j].province] += 3
                            self.map[i][j].can_move = 0
                            self.map[i][j].entity = villager
                            self.defend_level_up(i, j)
                            self.governments_earnings[color - 1][self.map[i][j].province] -= \
                                dict_units_earnings[villager]
                            self.governments_money[self.move][self.map[i][j].province] -= 10
                        else:
                            self.selected = (i, j)
                            res = self.bot_buy_priority(i, j)
                            res.sort(key=lambda x: x[2], reverse=True)
                            self.checked_to_zero()
                            for t in res:
                                if t[2] > 0 and self.governments_money[color - 1][self.map[i][j].province] > 10 * t[3] and\
                                        self.governments_earnings[color - 1][self.map[i][j].province] > dict_units_earnings[t[3] + 11]:
                                    if self.map[i][j].entity == grave:
                                        self.governments_earnings[self.move][
                                            self.map[self.selected[0]][self.selected[1]].province] += 1
                                    self.map[i][j].can_move = 1
                                    self.map[i][j].entity = t[3] + 11
                                    self.do_move(i, j, t[0], t[1])
                                    self.selected = (i, j)
                                    self.governments_earnings[self.move][
                                        self.map[self.selected[0]][self.selected[1]].province] -= \
                                        dict_units_earnings[t[3] + 11]
                                    self.governments_money[self.move][self.map[self.selected[0]][self.selected[1]].province] -= (
                                                                                                                t[3] * 10) + 10

                    if self.map[i][j].entity is not None and 10 < self.map[i][j].entity < 15 and self.map[i][j].can_move:
                        """Бот двигает юнита"""
                        res = self.bot_move_priority(i, j, i, j)
                        self.checked_to_zero()
                        res.sort(key=lambda x: x[2], reverse=True)
                        self.where_click = (i, j)
                        self.can_move_bfs(i, j)
                        for t in res:
                            if 0 < self.map[t[0]][t[1]].checked < 5 and t[2] >= 0:
                                self.selected = (i, j)
                                self.do_move(i, j, t[0], t[1])
                                break
        self.update = True

    def bot_buy_priority(self, x, y):
        res = []
        if self.map[x][y].government != self.map[self.selected[0]][self.selected[1]].government:
            res.append(self.bot_do_priority(x, y, self.map[x][y].government) + [self.map[x][y].defend_level])
        else:
            res.append(self.bot_do_priority(x, y, self.map[x][y].government) + [0])
        self.map[x][y].checked = 1
        a, t = self.check_neighbours(ground, x, y)
        for i in t:
            if not self.map[i[0]][i[1]].checked:
                for k in self.bot_buy_priority(i[0], i[1]):
                    res.append(k)
        self.update = True
        return res

    def bot_move_priority(self, x, y, x0, y0):
        res = []  # Список клеток и их приоритетности
        if x == x0 and y == y0:
            res.append((x, y, -1))
        else:
            res.append(self.bot_do_priority(x, y, self.map[x0][y0].government))
        if self.map[x][y].capital == self.map[x0][y0].capital:
            if self.map[x][y].checked < 5:
                t = self.check_neighbours(ground, x, y)[1]
                for i in t:
                    if not self.map[i[0]][i[1]].checked:
                        self.map[i[0]][i[1]].checked = self.map[x][y].checked + 1
                        self.bfs_queue.append((i[0], i[1]))
            while self.bfs_queue:
                a, b = self.bfs_queue[0][0], self.bfs_queue[0][1]
                del self.bfs_queue[0]
                for k in self.bot_move_priority(a, b, x0, y0):
                    res.append(k)
        else:
            self.map[x][y].checked = 1
        return res

    def bot_do_priority(self, x, y, government) -> list:
        priority = 0
        if self.map[x][y].government == government:
            if self.map[x][y].entity is not None:
                if self.map[x][y].entity == tree:
                    priority = 2
                elif self.map[x][y].entity == grave:
                    priority = 1
                elif 4 < self.map[x][y].entity < 11:
                    priority = -1
        else:
            if self.map[x][y].government is not None:
                priority = 4
            else:
                priority = 3
        return [x, y, priority]

    def dfs_2(self, x, y, size=1):
        self.map[x][y].checked = 1
        for i in self.check_neighbours(ground, x, y)[1]:
            if self.map[i[0]][i[1]].checked == 0 and self.map[i[0]][i[1]].government == self.map[x][y].government:
                self.map[i[0]][i[1]].government_size = 1
                self.map[i[0]][i[1]].capital = i
                self.map[i[0]][i[1]].province = len(self.governments_earnings[self.map[x][y].government - 1])
                if self.map[i[0]][i[1]].entity is not None:
                    if 10 < self.map[i[0]][i[1]].entity < 15:
                        self.governments_earnings[self.map[x][y].government - 1].append(
                            1 - dict_units_earnings[self.map[i[0]][i[1]].entity])
                    elif self.map[i[0]][i[1]].entity == tree:
                        self.governments_earnings[self.map[x][y].government - 1].append(0)
                    else:
                        self.governments_earnings[self.map[x][y].government - 1].append(1)
                else:
                    self.governments_earnings[self.map[x][y].government - 1].append(1)
                self.governments_money[self.map[x][y].government - 1].append(0)
                self.unite_governments(x, y, i[0], i[1])
                size += 1
                self.dfs_2(i[0], i[1], size)

    # Рисование границ государства из клетки
    def government_borders(self, x: int, y: int) -> list:
        sp = []
        self.map[x][y].checked = 1
        a, t = self.check_neighbours(water, x, y)
        for i in t:
            diff_x = i[0] - x
            diff_y = i[1] - y
            sp.append(self.do_borders(x, y, diff_x, diff_y))
        a, t = self.check_neighbours(ground, x, y)
        for i in t:
            if not self.map[i[0]][i[1]].checked:
                if self.map[i[0]][i[1]].government == self.map[x][y].government:
                    for j in self.government_borders(i[0], i[1]):
                        sp.append(j)
                else:
                    diff_x = i[0] - x
                    diff_y = i[1] - y
                    sp.append(self.do_borders(x, y, diff_x, diff_y))
        self.update = True
        return sp

    # Рисование границ хода из клетки
    def stroke_borders(self, x: int, y: int) -> list:
        if self.map[x][y].checked == 0:
            self.map[x][y].checked = 1
        sp = []
        if type(self.selected) == tuple:
            t = self.check_neighbours(water, x, y)[1]
            for i in t:
                diff_x = i[0] - x
                diff_y = i[1] - y
                sp.append(self.do_borders(x, y, diff_x, diff_y))
            if self.map[x][y].capital == self.map[self.where_click[0]][self.where_click[1]].capital:
                t = self.check_neighbours(ground, x, y)[1]
                if self.map[x][y].checked < 5:
                    for i in t:
                        if not self.map[i[0]][i[1]].checked:
                            f = True
                            if self.map[i[0]][i[1]].government != self.move + 1 and \
                                    self.map[i[0]][i[1]].defend_level >= self.map[self.selected[0]][
                                self.selected[1]].entity - 10:
                                f = False
                            if f:
                                self.map[i[0]][i[1]].checked = self.map[x][y].checked + 1
                                self.bfs_queue.append((i[0], i[1]))
                else:
                    for i in self.check_neighbours(ground, x, y)[1]:
                        if not self.map[i[0]][i[1]].checked:
                            diff_x = i[0] - x
                            diff_y = i[1] - y
                            sp.append(self.do_borders(x, y, diff_x, diff_y))
                while self.bfs_queue:
                    ind = 0
                    for i in range(len(self.bfs_queue)):
                        if self.map[self.bfs_queue[i][0]][self.bfs_queue[i][1]].capital == \
                                self.map[self.where_click[0]][self.where_click[1]].capital:
                            ind = i
                            break
                    a, b = self.bfs_queue[ind][0], self.bfs_queue[ind][1]
                    del self.bfs_queue[ind]
                    for i in self.check_neighbours(ground, x, y)[1]:
                        f = False
                        if self.map[i[0]][i[1]].government != self.move + 1 and \
                                self.map[i[0]][i[1]].defend_level >= self.map[self.selected[0]][
                            self.selected[1]].entity - 10:
                            f = True
                        if f:
                            diff_x = i[0] - x
                            diff_y = i[1] - y
                            sp.append(self.do_borders(x, y, diff_x, diff_y))
                    for j in self.stroke_borders(a, b):
                        sp.append(j)
            else:
                for i in self.check_neighbours(ground, x, y)[1]:
                    if not self.map[i[0]][i[1]].checked:
                        diff_x = i[0] - x
                        diff_y = i[1] - y
                        sp.append(self.do_borders(x, y, diff_x, diff_y))
        else:
            t = self.check_neighbours(water, x, y)[1]
            for i in t:
                diff_x = i[0] - x
                diff_y = i[1] - y
                sp.append(self.do_borders(x, y, diff_x, diff_y))
            if self.map[x][y].capital == self.map[self.where_click[0]][self.where_click[1]].capital:
                t = self.check_neighbours(ground, x, y)[1]
                for i in t:
                    if not self.map[i[0]][i[1]].checked:
                        f = True
                        if self.map[i[0]][i[1]].government != self.map[x][y].government and \
                                self.map[i[0]][i[1]].defend_level >= self.buy_unit + 1:
                            f = False
                        if f:
                            self.bfs_queue.append((i[0], i[1]))
                            self.map[i[0]][i[1]].checked = self.map[x][y].checked + 1
                while self.bfs_queue:
                    ind = 0
                    for i in range(len(self.bfs_queue)):
                        if self.map[self.bfs_queue[i][0]][self.bfs_queue[i][1]].capital == \
                                self.map[self.where_click[0]][self.where_click[1]].capital:
                            ind = i
                            break
                    a, b = self.bfs_queue[ind][0], self.bfs_queue[ind][1]
                    del self.bfs_queue[ind]
                    # if self.map[a][b].checked: не знаю зачем было
                    for i in self.check_neighbours(ground, x, y)[1]:
                        f = False
                        if self.map[i[0]][i[1]].government != self.move + 1 and \
                                self.map[i[0]][i[1]].defend_level >= self.buy_unit + 1:
                            f = True
                        if f:
                            diff_x = i[0] - x
                            diff_y = i[1] - y
                            sp.append(self.do_borders(x, y, diff_x, diff_y))
                    for j in self.stroke_borders(a, b):
                        sp.append(j)
            else:
                for i in self.check_neighbours(ground, x, y)[1]:
                    if not self.map[i[0]][i[1]].checked:
                        diff_x = i[0] - x
                        diff_y = i[1] - y
                        sp.append(self.do_borders(x, y, diff_x, diff_y))
        self.update = True
        return sp

    def do_borders(self, x, y, diff_x, diff_y):
        if diff_x == 1:
            if diff_y - (x & 1) == -1:
                a, b = self.centres[x][y]
                res = [(a + 22, b), (a + 11, b - 18)]
                # print("Справа сверху")
            else:
                a, b = self.centres[x][y]
                res = [(a + 22, b), (a + 11, b + 18)]
                # print("Справа снизу")
        elif diff_x == 0:
            if diff_y == 1:
                a, b = self.centres[x][y]
                res = [(a - 10, b + 18), (a + 10, b + 18)]
                # print("Снизу")
            else:
                a, b = self.centres[x][y]
                res = [(a - 10, b - 18), (a + 10, b - 18)]
                # print("Сверху")
        else:
            if diff_y - (x & 1) == -1:
                a, b = self.centres[x][y]
                res = [(a - 22, b), (a - 11, b - 18)]
                # print("Слева сверху")
            else:
                a, b = self.centres[x][y]
                res = [(a - 21, b), (a - 10, b + 18)]
                # print("Слева снизу")
        return res

    def do_move(self, x1, y1, x2, y2):
        if self.map[x1][y1].government == self.map[x2][y2].government:
            """Если юнит из клетки ходит в своё гос-во"""
            if self.map[x2][y2].entity is not None and 4 < self.map[x2][y2].entity < 11:
                """С зданием"""
                """Ничего не делаем в таком случае"""
                self.selected = True
                self.checked_to_zero()
                self.borders = self.government_borders(x2, y2)
            elif self.map[x2][y2].entity is not None and 10 < self.map[x2][y2].entity < 15:
                """С другим юнитом"""
                """Объединение юнитов"""
                self.governments_earnings[self.move][self.map[x2][y2].province] += dict_units_earnings[
                    self.map[x2][y2].entity]
                if self.map[x2][y2].entity + self.map[x1][y1].entity - 10 < 15:
                    self.map[x2][y2].entity += self.map[x1][y1].entity - 10
                    self.map[x1][y1].entity = None
                    self.defend_level_up(x2, y2)
                    self.defend_level_down(x1, y1)
                self.governments_earnings[self.move][self.map[x2][y2].province] -= \
                    dict_units_earnings[self.map[x2][y2].entity]
                self.selected = True
                self.checked_to_zero()
                self.borders = self.government_borders(x2, y2)
            else:
                """В своё гос - во с незначительной сущностью (из клетки)"""
                self.map[x2][y2].entity = self.map[x1][y1].entity
                self.map[x1][y1].entity = None
                self.defend_level_up(x2, y2)
                self.defend_level_down(x1, y1)
                self.checked_to_zero()
                self.borders = self.government_borders(x2, y2)
                self.selected = True
        else:
            """Если ход в чужое гос-во или в клетку без него(из клетки)"""
            if self.map[x2][y2].defend_level <= \
                    self.map[self.selected[0]][self.selected[1]].entity - 10:
                for i in self.check_neighbours(ground, x2, y2)[1]:
                    self.checked_to_zero()
                    if self.map[x2][y2].government is not None and self.dfs((x2, y2)):
                        """Разбиение на провинции(переделать)"""
                        self.checked_to_zero()
                        self.map[x2][y2].checked = 1
                        for j in self.check_neighbours(ground, x2, y2)[1]:
                            f = False
                            if self.map[j[0]][j[1]].government == self.map[x2][y2].government and not \
                                    self.map[j[0]][j[1]].checked:
                                if f:
                                    self.map[j[0]][j[1]].capital = j
                                    self.map[j[0]][j[1]].government_size = 1
                                    self.map[j[0]][j[1]].entity = castle
                                    self.governments_money[self.map[j[0]][j[1]].government - 1].append(
                                        [self.governments_money[self.move][self.map[x2][y2].province] // 3])  # Пересчитать деньги БЫСТРО
                                    self.map[j[0]][j[1]].province = len(self.governments_earnings[self.map[j[0]][j[1]].government - 1])
                                    self.governments_earnings.append([1])
                                    self.dfs_2(j[0], j[1])
                                else:
                                    f = True
                                    self.map[j[0]][j[1]].capital = j
                                    self.map[j[0]][j[1]].government_size = 1
                                    self.map[j[0]][j[1]].entity = castle
                                    self.governments_money[self.map[j[0]][j[1]].government - 1][
                                        self.map[j[0]][j[1]].province] //= 3  # Пересчитать деньги БЫСТРО
                                    self.governments_earnings.append([1])
                                    self.dfs_2(j[0], j[1])

                    if self.map[i[0]][i[1]].capital == self.map[x1][y1].capital:
                        self.map[x2][y2].government = self.move + 1
                        self.map[x2][y2].capital = (x2, y2)
                        self.map[x2][y2].government_size = 1
                        self.map[x2][y2].province = len(self.governments_earnings[self.move])
                        self.governments_earnings[self.move].append(1)
                        self.map[x2][y2].entity = self.map[x1][y1].entity
                        self.map[x2][y2].can_move = 0
                        self.map[x1][y1].entity = None
                        self.map[x1][y1].can_move = None
                        self.governments_money[self.move].append(0)
                        self.unite_governments(x2, y2, i[0], i[1])
                        self.defend_level_down(x1, y1)
                        self.defend_level_up(x2, y2)
                        self.checked_to_zero()
                        self.borders = self.government_borders(x1, y1)
                        self.selected = True
                        for t in self.check_neighbours(ground, x2, y2)[1]:
                            if self.map[x2][y2].government == self.map[t[0]][t[1]].government and self.map[x2][y2].province != self.map[t[0]][t[1]].province:
                                self.unite_governments(x2, y2, t[0], t[1])
                        break
                else:
                    self.selected = False
            else:
                self.selected = False
        self.update = True

    def can_move_bfs(self, x: int, y: int) -> None:
        """Просто расставляет checked по правилам bfs"""
        if self.map[x][y].capital == self.map[self.where_click[0]][self.where_click[1]].capital:
            if self.map[x][y].checked < 5:
                t = self.check_neighbours(ground, x, y)[1]
                for i in t:
                    if not self.map[i[0]][i[1]].checked:
                        self.map[i[0]][i[1]].checked = self.map[x][y].checked + 1
                        self.bfs_queue.append((i[0], i[1]))
            while self.bfs_queue:
                a, b = self.bfs_queue[0][0], self.bfs_queue[0][1]
                del self.bfs_queue[0]
                self.can_move_bfs(a, b)
        else:
            self.map[x][y].checked = 1

    def get(self, x: int, y: int) -> tuple:
        """Для островов"""
        if self.map[x][y].parent != (x, y):
            self.map[x][y].parent = self.get(self.map[x][y].parent[0], self.map[x][y].parent[1])
            return self.map[x][y].parent
        return (x, y)

    def unite(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Для островов"""
        u = self.get(x1, y1)
        v = self.get(x2, y2)
        if (u != v):
            if (u[0] < v[0] or u[1] < v[1]):
                self.map[v[0]][v[1]].parent = u
            else:
                self.map[u[0]][u[1]].parent = v
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    self.map[i][j].parent = self.get(i, j)

    def unite_governments(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Для государств"""
        u = self.get_capital(x1, y1)
        v = self.get_capital(x2, y2)
        if (u != v):
            if self.map[u[0]][u[1]].province < self.map[v[0]][v[1]].province:
                self.map[u[0]][u[1]].government_size += self.map[v[0]][v[1]].government_size
                self.governments_earnings[self.map[u[0]][u[1]].government - 1][self.map[u[0]][u[1]].province] += \
                    self.governments_earnings[self.map[v[0]][v[1]].government - 1][self.map[v[0]][v[1]].province]
                self.governments_money[self.map[u[0]][u[1]].government - 1][self.map[u[0]][u[1]].province] += \
                    self.governments_money[self.map[v[0]][v[1]].government - 1][self.map[v[0]][v[1]].province]
                del self.governments_money[self.map[v[0]][v[1]].government - 1][self.map[v[0]][v[1]].province]
                del self.governments_earnings[self.map[v[0]][v[1]].government - 1][self.map[v[0]][v[1]].province]
                self.map[v[0]][v[1]].capital = u
                # self.map[v[0]][v[1]].government_size = self.map[u[0]][u[1]].government_size
                self.map[v[0]][v[1]].province = self.map[u[0]][u[1]].province
            else:
                self.map[v[0]][v[1]].government_size += self.map[u[0]][u[1]].government_size
                self.governments_earnings[self.map[v[0]][v[1]].government - 1][self.map[v[0]][v[1]].province] += \
                    self.governments_earnings[self.map[u[0]][u[1]].government - 1][self.map[u[0]][u[1]].province]
                self.governments_money[self.map[v[0]][v[1]].government - 1][self.map[v[0]][v[1]].province] += \
                    self.governments_money[self.map[u[0]][u[1]].government - 1][self.map[u[0]][u[1]].province]
                del self.governments_money[self.map[u[0]][u[1]].government - 1][self.map[u[0]][u[1]].province]
                del self.governments_earnings[self.map[u[0]][u[1]].government - 1][self.map[u[0]][u[1]].province]
                # self.map[u[0]][u[1]].government_size = self.map[v[0]][v[1]].government_size
                self.map[u[0]][u[1]].capital = v
                self.map[u[0]][u[1]].province = self.map[v[0]][v[1]].province
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].government is not None:
                    self.map[i][j].capital = self.get_capital(i, j)
                    if self.map[i][j].entity == castle and self.map[i][j].capital != (i, j):
                        self.map[i][j].entity = None
                    self.map[i][j].province = self.map[self.map[i][j].capital[0]][self.map[i][j].capital[1]].province

    def get_capital(self, x: int, y: int) -> tuple:
        """Для столиц"""
        if self.map[x][y].capital != (x, y):
            self.map[x][y].capital = self.get_capital(self.map[x][y].capital[0], self.map[x][y].capital[1])
            self.map[x][y].government_size = self.map[self.map[x][y].capital[0]][
                self.map[x][y].capital[1]].government_size
            return self.map[x][y].capital
        return (x, y)

    def checked_to_zero(self):
        for i in range(self.y):
            for j in range(self.x):
                self.map[i][j].checked = 0

    def defend_level_down(self, x, y):
        f = 0
        for k in self.check_neighbours(ground, x, y)[1]:
            if self.map[k[0]][k[1]].government == self.map[x][y].government:
                flag = 0
                if self.map[k[0]][k[1]].entity is not None:
                    if 10 < self.map[k[0]][k[1]].entity < 15:
                        f = max(f, min(self.map[k[0]][k[1]].entity - 10, 3))
                        flag = min(self.map[k[0]][k[1]].entity - 10, 3)
                    elif self.map[k[0]][k[1]].entity in [tower, big_tower]:
                        f = max(f, self.map[k[0]][k[1]].entity - 5)
                        flag = self.map[k[0]][k[1]].entity - 5
                for p in self.check_neighbours(ground, k[0], k[1])[1]:
                    if self.map[p[0]][p[1]].government == self.map[x][y].government:
                        if p != self.selected:
                            if self.map[p[0]][p[1]].entity is not None:
                                if 10 < self.map[p[0]][p[1]].entity < 15:
                                    flag = max(flag, min(self.map[p[0]][p[1]].entity - 10, 3))
                                elif self.map[p[0]][p[1]].entity in [tower, big_tower]:
                                    flag = max(flag, self.map[p[0]][p[1]].entity - 5)
                            self.map[k[0]][k[1]].defend_level = flag
        self.map[x][y].defend_level = f

    def defend_level_up(self, x, y):
        self.map[x][y].defend_level = max(self.map[x][y].defend_level, min(self.map[x][y].entity - 10, 3))
        for k in self.check_neighbours(ground, x, y)[1]:
            if self.map[k[0]][k[1]].government == self.map[x][y].government:
                self.map[k[0]][k[1]].defend_level = max(self.map[k[0]][k[1]].defend_level,
                                                        min(self.map[x][y].entity - 10, 3))

    def dfs(self, v: tuple, p=(-1, -1)):
        x, y = v
        self.map[x][y].checked = 1
        children = 0
        for i in self.check_neighbours(ground, x, y)[1]:
            if not self.map[i[0]][i[1]].checked and self.map[i[0]][i[1]].government == self.map[x][y].government:
                self.dfs(i, v)
                children += 1
        if children > 1 and p == (-1, -1):
            return True
        return False


class Training(Map):
    def __init__(self, x, y, governments_num):
        self.x: int = x
        self.y: int = y
        # Размер поля в шестиугольниках
        self.selected: Union[bool, tuple] = False
        # selected - 3 вариации
        # False - если ничего не выбрано, True - если выбрано государство, Tuple - если выбран персонаж
        self.governments_num: int = governments_num  # Количество государств
        self.governments_money: List[List[int]] = []
        # governments_money[i][j] - количество денег j-той провинции i-того государства
        self.governments_earnings: List[List[int]] = []
        # governments_money[i][j] - заработок j-той провинции i-того государства
        self.centres: List[List[Tuple[int, int]]] = []
        # centres[i][j] - расположение центра [i][j] шестиугольника(в пикселях)
        self.borders = []
        # Хранение кортежей, между точками которых нужно провести границы
        self.move: int = 0
        # Чей ход
        self.where_click: tuple = ()
        # Куда был сделан последний клик на государство
        self.bfs_queue = []
        # Надо для обхода в ширину
        self.buy_unit: Optional[int] = None
        self.buy_building: Optional[int] = None
        self.update = True
        self.logs = []
        step_x = 0
        for i in range(self.y):
            row = []
            for j in range(self.x):
                row.append((step_x + 22, (j * 36 + (18 if i & 1 else 0)) + 24))
            step_x += 31
            self.centres.append(row)
        self.pre_generate()

        for i in range(self.y):
            for j in range(self.x):
                self.map[i][j].type = water
                self.map[i][j].entity = None

        # Создаю красных
        self.map[2][2].type = ground
        self.map[2][2].capital = (2, 2)
        self.map[2][2].entity = castle
        self.map[2][2].government = red
        self.map[2][2].government_size = 1
        self.map[2][2].province = 0
        self.governments_money.append([100])
        self.governments_earnings.append([1])
        x, y = 2, 2

        for i in [(2, 3), (2, 4), (3, 2), (3, 3), (4, 3), (5, 3), (5, 4), (6, 4), (5, 2), (6, 3), (4, 2), (3, 1),
                  (7, 4), (7, 3), (7, 2), (8, 3), (8, 4)]:
            self.map[i[0]][i[1]].type = ground
            self.map[i[0]][i[1]].government = red
            self.map[i[0]][i[1]].capital = i
        self.map[6][4].entity = villager
        self.map[6][4].can_move = 1
        self.map[2][3].entity = tree

        for j in self.check_neighbours(ground, x, y)[1]:
            if self.map[j[0]][j[1]].government == self.map[x][y].government and not self.map[j[0]][j[1]].checked:
                self.map[j[0]][j[1]].government_size = 1
                # Пересчитать деньги БЫСТРО
                self.map[j[0]][j[1]].province = len(
                    self.governments_earnings[self.map[j[0]][j[1]].government - 1]) - 1
                self.dfs_2(x, y)
        self.checked_to_zero()

        # Создаю розовых
        self.map[7][8].type = ground
        self.map[7][8].capital = (7, 8)
        self.map[7][8].entity = castle
        self.map[7][8].government = pink
        self.map[7][8].government_size = 1
        self.map[7][8].province = 0
        self.governments_money.append([100])
        self.governments_earnings.append([1])
        for i in [(8, 8), (8, 7), (8, 6), (8, 5), (7, 7), (7, 6), (7, 5), (6, 8), (6, 9), (5, 7), (5, 8),
                  (9, 4), (9, 5), (9, 6), (9, 7)]:
            self.map[i[0]][i[1]].type = ground
            self.map[i[0]][i[1]].government = pink
            self.map[i[0]][i[1]].capital = i

        self.map[8][6].entity = villager
        self.defend_level_up(8, 6)

        x, y = 7, 8
        for j in self.check_neighbours(ground, x, y)[1]:
            if self.map[j[0]][j[1]].government == self.map[x][y].government and not self.map[j[0]][j[1]].checked:
                self.map[j[0]][j[1]].government_size = 1
                # Пересчитать деньги БЫСТРО
                self.map[j[0]][j[1]].province = len(self.governments_earnings[pink - 1]) - 1
                self.governments_earnings[pink - 1].append(1)
                self.governments_money[pink - 1].append(0)
                self.dfs_2(x, y)
        self.checked_to_zero()


# class Government:
#     def __init__(self, color, player):
#         self.color = color
#         self.earnings = []
#         self.money = []
#         self.capitals = []
#         self.cells = []
#         self.sizes = []


class Cell:
    def __init__(self, type: int, entity, pos_parent: tuple):
        self.type = type  # Тип местности на клетке
        self.government: Optional[int] = None  # К какому цвету пренадлежит
        self.capital: Optional[Tuple[int, int]] = None  # Столица
        self.province: Optional[int] = None  # Номер провинции
        self.entity: Optional[int] = entity  # Сущность на клетке
        self.parent = pos_parent  # Снова не парься
        self.checked: int = 0  # Это вообще не парься, там сложные слова как DFS
        self.government_size: Optional[int] = None  # Размеры государства
        self.can_move: Optional[int] = None  # Может ли ходить сущность на клетке в этом ходу
        self.defend_level: int = 0  # Уровень защищённости клетки
