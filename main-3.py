import copy


# вспомогательная функция разбиения строки на символы
def split(s):
    if s:
        return [char for char in s]
    return None


def min_list_dict_value(list_):
    if list_:
        min_steps = list_[0][2]['steps']
        if len(list_) > 1:
            for item in list_[1:]:
                if item[2]['steps'] < min_steps:
                    min_steps = item[2]['steps']
        return min_steps
    return None


def min_list_dict_value_coords(list_):
    if list_:
        min_coords = list_[0][0], list_[0][1]
        min_steps = list_[0][2]['steps']
        if len(list_) > 1:
            for item in list_[1:]:
                if item[2]['steps'] < min_steps:
                    min_steps = item[0][0], item[0][1]
                    min_coords = item[2]['steps']
        return min_coords
    return None


# волновой алгоритм поиска
def voln(x, y, cur, n, m, lab):
    lab[y][x] = str(cur)
    if x + 1 < m:
        if lab[y][x + 1] == ' ' or (lab[y][x + 1] != '*' and int(lab[y][x + 1]) > cur):
            voln(x + 1, y, cur + 1, n, m, lab)
    if y + 1 < n:
        if lab[y + 1][x] == ' ' or (lab[y + 1][x] != '*' and int(lab[y + 1][x]) > cur):
            voln(x, y + 1, cur + 1, n, m, lab)
    if y - 1 >= 0:
        if lab[y - 1][x] == ' ' or (lab[y - 1][x] != '*' and int(lab[y - 1][x]) > cur):
            voln(x, y - 1, cur + 1, n, m, lab)
    if x - 1 >= 0:
        if lab[y][x - 1] == ' ' or (lab[y][x - 1] != '*' and int(lab[y][x - 1]) > cur):
            voln(x - 1, y, cur + 1, n, m, lab)
    return lab


class LabirintTurtle:
    """Класс Черепашки"""

    def __init__(self):
        self.turtle_map = []
        self.dijkstra_map = []
        self.exits = []
        self.x_start = 0
        self.y_start = 0

    # Проверка правильности координат черепашки
    def turtle_is_valid(self, x, y):
        if self.turtle_map:
            if self.turtle_map[y][x] == ' ':
                return True
        return False

    # Обработчик показа черепашки на карте
    def turtle_map_with_turtle(self):
        x = int(self.x_start)
        y = int(self.y_start)
        copy_turtle_map = copy.deepcopy(self.turtle_map)
        # Проверка на валидность координат черепахи
        if self.turtle_is_valid(x, y):
            copy_turtle_map[y][x] = 'А'
            return copy_turtle_map
        else:
            return None

    # вспомогательная функция для волнового алгоритма
    def find_exit(self):
        if self.turtle_map:
            x = int(self.x_start)  # в строках
            y = int(self.y_start)  # в столбцах
            n = len(self.turtle_map)  # строк - по y
            m = len(self.turtle_map[0])  # столбцов - по x
            copy_turtle_map = copy.deepcopy(self.turtle_map)
            copy_turtle_map = voln(x, y, 0, n, m, copy_turtle_map)
            self.dijkstra_map = copy_turtle_map
            return copy_turtle_map
        return None

    # метод для определения наличия выходов с карты
    def map_has_exit(self):
        if self.turtle_map:
            # проверяем первую строчку массива
            map_with_way = self.find_exit()
            for symbol in range(len(map_with_way[0])):
                curr_cell = map_with_way[0][symbol]
                if curr_cell != ' ' and curr_cell != '*':
                    self.exits.append([symbol, 0, {'steps': int(curr_cell)}])
            # проверяем последнюю строчку массива
            for symbol in range(len(map_with_way[-1])):
                curr_cell = map_with_way[len(map_with_way) - 1][symbol]
                if curr_cell != ' ' and curr_cell != '*':
                    self.exits.append([symbol, len(map_with_way) - 1, {'steps': int(curr_cell)}])
            # проверяем нулевые символы остальных строк
            for symbol in range(len(map_with_way)):
                curr_cell = map_with_way[symbol][0]
                if curr_cell != ' ' and curr_cell != '*':
                    self.exits.append([0, symbol, {'steps': int(curr_cell)}])
            # проверяем последние символы остальных строк
            for symbol in range(len(map_with_way)):
                curr_cell = map_with_way[symbol][len(map_with_way[-1]) - 1]
                if curr_cell != ' ' and curr_cell != '*':
                    self.exits.append([len(map_with_way[-1]) - 1, symbol, {'steps': int(curr_cell)}])

        if self.exits:
            return True
        return False

    def load_map(self, file_path=''):
        """Метод добавления лабиринта из файла"""
        allowed_coords = set('1234567890')
        with open(file_path, 'r') as lmap:
            turtle_map = lmap.readlines()
            if turtle_map and set(list(str(int(turtle_map[-2])))).issubset(allowed_coords) and \
                    set(list(str(int(turtle_map[-1])))).issubset(allowed_coords):
                self.x_start = int(turtle_map[-2])
                self.y_start = int(turtle_map[-1])
                for line in range(len(turtle_map[:-2])):
                    turtle_map[line] = split(turtle_map[line])[:-1]
                self.turtle_map = turtle_map[:-2]
            else:
                print('Неверный формат карты')

    def show_map(self, show_turtle=False):
        """Метод вывода лабиринта в консоль"""
        if self.turtle_map:
            if not show_turtle:
                for line in self.turtle_map:
                    print(''.join(line))
            else:
                map_temp = self.turtle_map_with_turtle()
                if map_temp:
                    for line in map_temp:
                        print(''.join(line))
        else:
            print('Нет загруженной карты')

    def show_wave_map(self):
        for line in self.dijkstra_map:
            print(''.join(line))

    def check_map(self):
        """Метод проверки валидности карты"""
        allowed_chars = set('* ')
        allowed_coords = set('1234567890')
        # Проверка на * и пробелы в карте
        for line in self.turtle_map:
            if not set(''.join(line)).issubset(allowed_chars):
                print('Неверные символы на карте')
                return False
        # Проверка на валидность положения черепашки на карте
        if not self.turtle_is_valid(self.x_start, self.y_start):
            print('Неверные координаты черепашки')
            return False
        # Проверка на отсутствие областей без выхода
        for line in self.find_exit():
            if ' ' in line:
                print('На карте есть области, откуда нет выхода')
                return False
        # Проверка на наличие выхода из лабиринта
        if not self.map_has_exit():
            print('Нет выхода из лабиринта')
            return False
        # Проверка на отсутствие координат черепахи
        if not ({str(self.x_start)}.issubset(allowed_coords)
                and {str(self.y_start)}.issubset(allowed_coords)):
            print('Не указаны координаты черепашки')
            return False
        return True

    def exit_count_step(self):
        """Выводит количество шагов для выхода черепашки из лабиринта"""
        if self.exits:
            print(min_list_dict_value(self.exits))
        else:
            self.map_has_exit()
            print(min_list_dict_value(self.exits))

    def near_coords(self, current_coords):
        """Возвращает лист соседних координат ячейки"""
        if self.dijkstra_map:
            try:
                right = self.dijkstra_map[current_coords[1]][current_coords[0] + 1]
            except:
                right = ''
            try:
                down = self.dijkstra_map[current_coords[1] + 1][current_coords[0]]
            except:
                down = ''
            try:
                left = self.dijkstra_map[current_coords[1]][current_coords[0] - 1]
            except:
                left = ''
            try:
                up = self.dijkstra_map[current_coords[1] - 1][current_coords[0]]
            except:
                up = ''
            return [
                [right, (current_coords[0] + 1, current_coords[1])] if right else None,
                [down, (current_coords[0], current_coords[1] + 1)] if down else None,
                [left, (current_coords[0] - 1, current_coords[1])] if left else None,
                [up, (current_coords[0], current_coords[1] - 1)] if up else None
            ]
        return None

    def draw_steps(self, current_coords):
        """Рисует точки до выхода"""
        if self.turtle_map and self.map_has_exit():
            x_turtle = self.x_start
            y_turtle = self.y_start
            turtle_map = copy.deepcopy(self.turtle_map)

            while current_coords != (x_turtle, y_turtle):
                turtle_map[current_coords[1]][current_coords[0]] = '.'
                current_coord_value = self.dijkstra_map[current_coords[1]][current_coords[0]]
                for coordinate in self.near_coords(current_coords):
                    if coordinate and coordinate[0] != '*':
                        if int(coordinate[0]) < int(current_coord_value):
                            current_coords = coordinate[1] # Новая текущая координата

            turtle_map[current_coords[1]][current_coords[0]] = 'A'
            return turtle_map
        return None

    def exit_show_step(self):
        """Выводит путь для выхода черепашки из лабиринта"""
        if self.exits:
            current_coords = min_list_dict_value_coords(self.exits)
            map_with_path = self.draw_steps(current_coords)
            for line in map_with_path:
                print(''.join(line))
        else:
            print('Выхода нет (с)')


turtle = LabirintTurtle()
turtle.load_map('hard_test.txt')
turtle.show_map(True)
print(turtle.map_has_exit())
print(turtle.exits)
print(turtle.check_map())
turtle.exit_count_step()
turtle.exit_show_step()
