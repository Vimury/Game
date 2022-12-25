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

from random import randint, choices


class Map:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map = self.pre_generate()
        self.after_generate()

        for i in range(x):
            for j in range(y):
                print(self.map[j][i].type, end=' ')
            print()
        print()
        # for i in range(x):
        #     for j in range(y):
        #         print(self.map[j][i].entity, end=' ')
        #     print()

    # Функция генерации
    def pre_generate(self):
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
        for i in range(3):
            res.append([Cell(water, None) for j in range(self.x)])
        for i in range(3, self.y - 3):
            row = []
            for j in range(self.x):
                if j < 3 or j > self.x - 3:
                    row.append(Cell(water, None))
                else:
                    row.append(
                        Cell(choices([ground, water], weights=[8, 9 - sp1[2 * i // self.y][2 * j // self.x] -
                                                               sp2[5 * i // self.y][j * 5 // self.x] -
                                                               sp3[i * 10 // self.y][j * 10 // self.x] - sp4[i][j]])[0],
                             choices([tree, stone, gold, None], weights=[6, 3, 1, 12])[0]))
            res.append(row)
        for i in range(3):
            res.append([Cell(water, None) for j in range(self.x)])
        return res

    def after_generate(self):
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    if not self.check_neighbours(ground, i, j):
                        self.map[i][j].type = water

    def check_neighbours(self, type, i, j):
        neighbours = 0
        if i & 1:
            if self.map[i + 1][j].type == type:
                neighbours += 1
            if self.map[i - 1][j].type == type:
                neighbours += 1
            if self.map[i - 1][j + 1].type == type:
                neighbours += 1
            if self.map[i + 1][j + 1].type == type:
                neighbours += 1
            if self.map[i][j + 1].type == type:
                neighbours += 1
            if self.map[i][j - 1].type == type:
                neighbours += 1
        else:
            if self.map[i + 1][j].type == type:
                neighbours += 1
            if self.map[i - 1][j].type == type:
                neighbours += 1
            if self.map[i + 1][j - 1].type == type:
                neighbours += 1
            if self.map[i - 1][j - 1].type == type:
                neighbours += 1
            if self.map[i][j + 1].type == type:
                neighbours += 1
            if self.map[i][j - 1].type == type:
                neighbours += 1
        return neighbours


class Cell:
    def __init__(self, type, entity):
        self.type = type
        self.entity = entity
        self.goverment = None
