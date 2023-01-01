'''Прописал id типа местности'''
water = 0
ground = 1
'''Прописал id государств'''
red = 2
pink = 3
green = 4
light_green = 5
blue = 6
light_blue = 7
orange = 8
yellow = 9
purple = 10

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
        sp = []
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    self.map[i][j].parent = self.get(i, j)
        for i in range(x):
            for j in range(y):
                if self.map[j][i].type == ground:
                    if self.map[j][i].parent not in sp:
                        sp.append(self.map[j][i].parent)
                    print(self.map[j][i].parent, end=' ')
                else:
                    print((0, 0), end=' ')
            print()
        print()
        print(len(sp))

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
        for i in range(3):
            res.append([Cell(water, None, (-1, -1)) for j in range(self.x)])
        for i in range(3, self.y - 3):
            row = []
            for j in range(self.x):
                if j < 3 or j > self.x - 3:
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
                                                                   sp3[i * 10 // self.y][j * 10 // self.x] - sp4[i][j]])[0],
                                 None, (i, j)))
                    if row[-1].type == ground:
                        row[-1].entity = choices([tree, stone, gold, None], weights=[6, 3, 0, 12])[0]
            res.append(row)
        for i in range(3):
            res.append([Cell(water, None, (-1, -1)) for j in range(self.x)])
        return res

    def unite_islands(self, first, i, j):
        delta_x = abs(first[0] - self.map[i][j].parent[0])
        delta_y = abs(first[1] - self.map[i][j].parent[1])
        temp = self.check_neighbours(water, i, j)
        for k in temp[1]:
            if 2 < k[0] < self.y - 3:
                if 2 < k[1] < self.x - 3:
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

    def after_generate(self):
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
        first = ()
        for i in range(self.y):
            for j in range(self.x):
                if self.map[i][j].type == ground:
                    if first:
                        if self.map[i][j].parent != first:
                            self.unite_islands(first, i, j)
                            for k in range(self.y):
                                for l in range(self.x):
                                    self.map[i][j].checked = 0
                    else:
                        first = self.map[i][j].parent

        # for i in range(self.y):
        #     for j in range(self.x):
        #         if self.map[i][j].type == ground:
        #             self.map[i][j].parent = self.get(i, j)
        #             if not first:
        #                 first = self.map[i][j].parent
        #             elif first != self.map[i][j].parent:
        #                 delta_x = abs(first[0] - self.map[i][j].parent[0])
        #                 delta_y = abs(first[1] - self.map[i][j].parent[1])
        #                 for a in range(delta_x):
        #                     for b in range(delta_y):
        #                         self.map[first[0] + a][first[1] + b] = Cell(ground, gold, (i, j))
        #                 self.unite(first[0], first[1], i, j)
        #                 self.map[i][j].parent = self.get(i, j)
        # for i in range(self.y):
        #     for j in range(self.x):
        #         if self.map[i][j].type == ground:
        #             temp = self.check_neighbours(ground, i, j)
        #             if not temp[0]:
        #                 self.map[i][j].type = water
        #                 self.map[i][j].entity = None
        #                 self.map[i][j].parent = (-1, -1)
        #             else:
        #                 for k in temp[1]:
        #                     self.unite(i, j, k[0], k[1])
        # for i in range(self.y):
        #     for j in range(self.x):
        #         if self.map[i][j].type == ground:
        #             self.map[i][j].parent = self.get(i, j)

    def check_neighbours(self, type: int, i: int, j: int) -> (int, list):
        neighbours = 0
        pos = []
        if i & 1:
            if i + 1 < self.y and self.map[i + 1][j].type == type:
                neighbours += 1
                pos.append((i + 1, j))
            if i - 1 >= 0 and self.map[i - 1][j].type == type:
                neighbours += 1
                pos.append((i - 1, j))
            if i - 1 >= 0 and j + 1 < self.x and self.map[i - 1][j + 1].type == type:
                neighbours += 1
                pos.append((i - 1, j + 1))
            if i + 1 < self.y and j + 1 < self.x and self.map[i + 1][j + 1].type == type:
                neighbours += 1
                pos.append((i + 1, j + 1))
            if j + 1 < self.x and self.map[i][j + 1].type == type:
                neighbours += 1
                pos.append((i, j + 1))
            if j - 1 >= 0 and self.map[i][j - 1].type == type:
                neighbours += 1
                pos.append((i, j - 1))
        else:
            if i + 1 < self.y and self.map[i + 1][j].type == type:
                neighbours += 1
                pos.append((i + 1, j))
            if i - 1 >= 0 and self.map[i - 1][j].type == type:
                neighbours += 1
                pos.append((i - 1, j))
            if i + 1 < self.y and j - 1 >= 0 and self.map[i + 1][j - 1].type == type:
                neighbours += 1
                pos.append((i + 1, j - 1))
            if i - 1 >= 0 and j - 1 >= 0 and self.map[i - 1][j - 1].type == type:
                neighbours += 1
                pos.append((i - 1, j - 1))
            if j + 1 < self.x and self.map[i][j + 1].type == type:
                neighbours += 1
                pos.append((i, j + 1))
            if j - 1 >= 0 and self.map[i][j - 1].type == type:
                neighbours += 1
                pos.append((i, j - 1))
        return (neighbours, pos)

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
        self.goverment = None
        self.entity = entity
        self.parent = pos_parent
        self.checked = 0
        self.rank = 1
