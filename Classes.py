from math import sqrt

import pygame.sprite

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
big_farm = 7
tower = 8
big_tower = 9
town = 10

villager = 11
man2 = 12
knight = 13
big_knight = 14

from random import randint, choices


class Map:
    def __init__(self, x, y, goverments_num):
        self.x = x
        self.y = y
        # Размер поля в шестиугольниках
        self.selected = False
        # selected - 3 вариации
        # False - если ничего не выбрано, True - если выбрано государство, Tuple - если выбран персонаж
        self.goverments_num = goverments_num  # Количество государств
        self.goverments_money = []
        # goverments_money[i][j] - количество денег j-той провинции i-того государства
        self.goverments_earnings = []
        # goverments_money[i][j] - заработок j-той провинции i-того государства
        self.centres = []
        # centres[i][j] - расположение центра [i][j] шестиугольника(в пикселях)
        self.borders = []
        # Хранение кортежей, между точками которых нужно провести границы
        self.move = 0
        # Чей ход
        self.where_click = ()
        # Куда был сделан последний клик на государство
        self.bfs_queue = []
        # Надо для обхода в ширину
        step_x = 0
        for i in range(self.y):
            row = []
            for j in range(self.x):
                row.append((step_x + 22, (j * 36 + (18 if i & 1 else 0)) + 24))
            step_x += 31
            self.centres.append(row)
            print(row)
        self.gr = 0
        # Количество земли на карте
        self.map = self.pre_generate()
        self.after_generate()
        max_gr = (self.x - 4) * (self.y - 4) * 3 // 4  # Максимальное количество клеток земли на карте
        min_gr = (self.x - 4) * (self.y - 4) // 4  # Минимальное количество клеток земли на карте
        while self.gr > max_gr or self.gr < min_gr:
            self.gr = 0
            self.map = self.pre_generate()
            self.after_generate()
        self.generate_goverments()
        # for i in range(self.y):
        #     for j in range(self.x):
        #         self.map[i][j].type = water
        # self.map[2][2].type = ground
        # self.map[2][3].type = ground
        # self.map[2][2].goverment = red
        # self.map[2][3].goverment = red
        # self.map[2][2].capital = (2, 2)
        # self.map[2][3].capital = (2, 2)
        # self.map[2][2].entity = castle
        # self.map[3][3].type = ground

        for i in range(x):
            for j in range(y):
                print(self.map[j][i].type, end=' ')
            print()
        print()
        # for i in range(x):
        #     for j in range(y):
        #         print(self.map[j][i].entity, end=' ')
        #     print()
        sp = []
        # for i in range(x):
        #     for j in range(y):
        #         if self.map[j][i].type == ground:
        #             if self.map[j][i].parent not in sp:
        #                 sp.append(self.map[j][i].parent)
        #             print(self.map[j][i].parent, end=' ')
        #         else:
        #             print((0, 0), end=' ')
        #     print()
        print(self.gr)

    # Функция генерации
    def pre_generate(self) -> list:
        sp1 = []
        for i in range(2):
            sp1.append([randint(0, 2) for j in range(2)])
        print(sp1)
        sp2 = []
        for i in range(5):
            sp2.append([randint(0, 2) for j in range(5)])
        sp3 = []
        for i in range(10):
            sp3.append([randint(0, 2) for j in range(10)])
        sp4 = []
        for i in range(self.y):
            sp4.append([randint(0, 2) for j in range(self.x)])
        res = []
        for i in range(2):
            res.append([Cell(water, None, (-1, -1)) for j in range(self.x)])
        for i in range(2, self.y - 2):
            row = []
            for j in range(self.x):
                if j < 2 or j > self.x - 2:
                    row.append(Cell(water, None, (-1, -1)))
                else:
                    if sp1[2 * i // self.y][2 * j // self.x] == 0:
                        row.append(Cell(choices([ground, water], weights=[5, 8 - sp2[5 * i // self.y][j * 5 // self.x] -
                                                                          sp3[i * 10 // self.y][j * 10 // self.x] -
                                                                          sp4[i][j]])[0], None, (i, j)))
                    else:
                        row.append(
                            Cell(choices([ground, water], weights=[8, 8 - sp1[2 * i // self.y][2 * j // self.x] -
                                                                   sp2[5 * i // self.y][j * 5 // self.x] -
                                                                   sp3[i * 10 // self.y][j * 10 // self.x] - sp4[i][
                                                                       j]])[0],
                                 None, (i, j)))
                    if row[-1].type == ground:
                        row[-1].entity = choices([tree, stone, gold, None], weights=[6, 0, 0, 12])[0]
            res.append(row)
        for i in range(2):
            res.append([Cell(water, None, (-1, -1)) for j in range(self.x)])
        return res

    def unite_islands(self, first: tuple, i: int, j: int) -> None:
        delta_x = abs(first[0] - self.map[i][j].parent[0])
        delta_y = abs(first[1] - self.map[i][j].parent[1])
        temp = self.check_neighbours(water, i, j)
        for k in temp[1]:
            if 1 < k[0] < self.y - 1:
                if 1 < k[1] < self.x - 1:
                    if randint(0, 2) > 0:
                        self.map[k[0]][k[1]] = Cell(ground, None, self.map[i][j].parent)
                    # if delta_y > abs(first[0] - self.map[k[0]][k[1]].parent[0]):
                    #     if delta_x < abs(first[1] - self.map[k[0]][k[1]].parent[1]):
                    #         self.map[k[0]][k[1]] = Cell(ground, None, self.map[i][j].parent)
                    # elif delta_x > abs(first[1] - self.map[k[0]][k[1]].parent[1]):
                    #     if randint(0, 2) > 0:
                    #         self.map[k[0]][k[1]] = Cell(ground, None, self.map[i][j].parent)
                    # else:
                    #     if randint(0, 10) > 9:
                    #         self.map[k[0]][k[1]] = Cell(ground, None, self.map[i][j].parent)

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
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    self.map[i][j].parent = self.get(i, j)
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
            for k in range(self.y):
                for l in range(self.x):
                    self.map[i][j].checked = 0
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    self.gr += 1

    def generate_goverments(self):
        self.capitals = []
        for k in range(self.goverments_num):
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
            self.map[i][j].entity = gold
        c = 1
        for k in self.capitals:
            a, sp = self.check_neighbours(ground, k[0], k[1])
            self.map[k[0]][k[1]].goverment = c
            self.map[k[0]][k[1]].capital = (k[0], k[1])
            self.map[k[0]][k[1]].goverment_size = 1
            self.map[k[0]][k[1]].entity = castle
            self.goverments_money.append([10])
            self.goverments_earnings.append([a + 1])
            for t in sp:
                self.map[t[0]][t[1]].capital = (k[0], k[1])
                self.map[k[0]][k[1]].goverment_size = a
                self.map[t[0]][t[1]].goverment_size = a
                self.map[t[0]][t[1]].goverment = c
                if self.map[t[0]][t[1]].entity == tree:
                    self.goverments_earnings[-1][-1] -= 1
            self.goverments_money[-1][0] -= self.goverments_earnings[-1][0]
            c += 1

    def check_neighbours(self, type: int, i: int, j: int) -> (int, list):
        neighbours = 0
        pos = []
        a = i & 1
        # Сосед справа сверху
        if i + 1 < self.y and j - 1 + (i & 1) >= 0 and self.map[i + 1][j - 1 + (i & 1)].type == type:
            neighbours += 1
            pos.append((i + 1, j - 1 + (i & 1)))
        # Сосед справа снизу
        if i + 1 < self.y and j + (i & 1) < self.x and self.map[i + 1][j + (i & 1)].type == type:
            neighbours += 1
            pos.append((i + 1, j + (i & 1)))
        # Сосед слева сверху
        if i - 1 >= 0 and j - 1 >= 0 and self.map[i - 1][j - 1 + (i & 1)].type == type:
            neighbours += 1
            pos.append((i - 1, j - 1 + (i & 1)))
        # Сосед слева снизу
        if i - 1 >= 0 and j + (i & 1) and self.map[i - 1][j + (i & 1)].type == type:
            neighbours += 1
            pos.append((i - 1, j + (i & 1)))
        # Сосед снизу
        if j + 1 < self.x and self.map[i][j + 1].type == type:
            neighbours += 1
            pos.append((i, j + 1))
        # Сосед сверху
        if j - 1 >= 0 and self.map[i][j - 1].type == type:
            neighbours += 1
            pos.append((i, j - 1))
        return (neighbours, pos)

    def get_coords(self, pos: tuple, step_x, step_y) -> tuple:
        x, y = pos
        x -= step_x
        y += step_y
        """Добавить работу с худом"""
        dist = 64
        q, r = -5, -5
        for i in range(self.y):
            for j in range(self.x):
                a = sqrt((self.centres[i][j][0] - x) ** 2 + (self.centres[i][j][1] - y) ** 2)
                if a < dist:
                    dist = a
                    q, r = i, j
        print(q, r)
        return (q, r)

    def click_processing(self, coords: tuple):  # на вход клетка НЕ в пикселях
        self.borders = []
        x, y = coords
        if self.map[x][y].type == ground:
            if self.selected is tuple:
                pass
                """Проверить возможность перехода"""
            else:
                for i in range(self.y):
                    for j in range(self.x):
                        self.map[i][j].checked = 0
                if self.map[x][y].goverment is not None:
                    if self.map[x][y].entity is not None and 10 < self.map[x][y].entity < 15:
                        self.selected = (x, y)
                        """Вывести худ и обвести границы хода"""
                    else:
                        if self.map[x][y].goverment == (self.move + 1):
                            self.where_click = (x, y)
                            self.borders = self.goverment_borders(x, y)
                            self.selected = True
                else:
                    self.selected = False
        else:
            self.selected = False

    def goverment_borders(self, x: int, y: int) -> list:
        sp = []
        self.map[x][y].checked = 1
        a, t = self.check_neighbours(water, x, y)
        for i in t:
            diff_x = i[0] - x
            diff_y = i[1] - y
            for j in self.do_borders(x, y, diff_x, diff_y):
                sp.append(j)
        a, t = self.check_neighbours(ground, x, y)
        for i in t:
            if not self.map[i[0]][i[1]].checked:
                if self.map[i[0]][i[1]].goverment == self.map[x][y].goverment:
                    for j in self.goverment_borders(i[0], i[1]):
                        sp.append(j)
                else:
                    diff_x = i[0] - x
                    diff_y = i[1] - y
                    for j in self.do_borders(x, y, diff_x, diff_y):
                        sp.append(j)
        return sp

    def move_borders(self, x: int, y: int) -> list:
        sp = []
        if self.selected is tuple:
            pass
        else:
            t = self.check_neighbours(water, x, y)[1]
            for i in t:
                diff_x = i[0] - x
                diff_y = i[1] - y
                for j in self.do_borders(x, y, diff_x, diff_y):
                    sp.append(j)
            if self.map[x][y].capital == self.map[self.where_click[0]][self.where_click[1]].capital:
                self.map[x][y].checked = 1
                t = self.check_neighbours(ground, x, y)[1]
                for i in t:
                    if not self.map[i[0]][i[1]].checked:
                        self.bfs_queue.append((i[0], i[1]))
                        self.map[i[0]][i[1]].checked = 1
                while self.bfs_queue:
                    ind = 0
                    for i in range(len(self.bfs_queue)):
                        if self.map[self.bfs_queue[i][0]][self.bfs_queue[i][1]].capital == \
                                self.map[self.where_click[0]][self.where_click[1]].capital:
                            ind = i
                            break
                    a, b = self.bfs_queue[ind][0], self.bfs_queue[ind][1]
                    del self.bfs_queue[ind]
                    if self.map[a][b].checked == 1:
                        for j in self.move_borders(a, b):
                            sp.append(j)
            else:
                for i in self.check_neighbours(ground, x, y)[1]:
                    if not self.map[i[0]][i[1]].checked:
                        diff_x = i[0] - x
                        diff_y = i[1] - y
                        for k in self.do_borders(x, y, diff_x, diff_y):
                            sp.append(k)
        return sp

    def do_borders(self, x, y, diff_x, diff_y):
        sp = []
        if diff_x == 1:
            if diff_y - (x & 1) == -1:
                a, b = self.centres[x][y]
                sp.append([(a + 22, b), (a + 11, b - 18)])
                # print("Справа сверху")
            else:
                a, b = self.centres[x][y]
                sp.append([(a + 22, b), (a + 11, b + 18)])
                # print("Справа снизу")
        elif diff_x == 0:
            if diff_y == 1:
                a, b = self.centres[x][y]
                sp.append([(a - 11, b + 18), (a + 11, b + 18)])
                # print("Снизу")
            else:
                a, b = self.centres[x][y]
                sp.append([(a - 11, b - 18), (a + 11, b - 18)])
                # print("Сверху")
        else:
            if diff_y - (x & 1) == -1:
                a, b = self.centres[x][y]
                sp.append([(a - 22, b), (a - 11, b - 18)])
                # print("Слева сверху")
            else:
                a, b = self.centres[x][y]
                sp.append([(a - 21, b), (a - 10, b + 18)])
                # print("Слева снизу")
        return sp

    def get(self, x: int, y: int) -> tuple:
        if self.map[x][y].parent != (x, y):
            self.map[x][y].parent = self.get(self.map[x][y].parent[0], self.map[x][y].parent[1])
            return self.map[x][y].parent
        else:
            return (x, y)

    def unite(self, x1: int, y1: int, x2: int, y2: int) -> None:
        u = self.get(x1, y1)
        v = self.get(x2, y2)
        if (u != v):
            if (u[0] < v[0] or u[1] < v[1]):
                self.map[u[0]][u[1]].rank += self.map[v[0]][v[1]].rank
                self.map[v[0]][v[1]].parent = u
            else:
                self.map[v[0]][v[1]].rank += self.map[u[0]][u[1]].rank
                self.map[u[0]][u[1]].parent = v


class Cell:
    def __init__(self, type: int, entity, pos_parent: tuple):
        self.type = type  # Тип местности на клетке
        self.goverment = None  # К какому цвету пренадлежит
        self.capital = None  # Не парься
        self.entity = entity  # Сущность на клетке
        self.parent = pos_parent  # Снова не парься
        self.checked = 0  # Это вообще не парься, там сложные слова как DFS
        self.rank = 1  # Это вообще бесполезно(нет)
        self.goverment_size = None  # Размеры государства
