from MainField import Map
from math import sqrt
from typing import List, Optional, Union, Tuple
import numpy as np
from variables import *
from Cell_class import *

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
                self.governments_money[pink - 1].append(1)
                self.dfs_2(x, y)
        self.checked_to_zero()
