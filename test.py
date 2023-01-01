"""Файл только для того чтобы не выходя из проекта тестить что-то(потом удалим)"""
"""Юзлесс фигня"""
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