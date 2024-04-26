from typing import List, Optional, Union, Tuple

class Cell:
    def __init__(self, type: int, entity, pos_parent: tuple):
        self.type = type  # Тип местности на клетке
        self.government: Optional[int] = None  # К какому цвету пренадлежит
        self.capital: Optional[Tuple[int, int]] = None  # Столица
        self.province: Optional[int] = None  # Номер провинции
        self.entity: Optional[int] = entity  # Сущность на клетке
        self.parent = pos_parent  # По идее клетка со столицей, но там багает чёто я хз крч
        self.checked: int = 0  # Это вообще не парься, там сложные слова как DFS
        self.government_size: Optional[int] = None  # Размеры государства
        self.can_move: Optional[int] = None  # Может ли ходить сущность на клетке в этом ходу
        self.defend_level: int = 0  # Уровень защищённости клетки