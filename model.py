from image import ImageBoard
import math, random


class SchellingModel():

    def __init__(self, n, count_iteration):
        self._ln = n
        self._size = n ** 2
        self._board = [[0] * n for _ in range(n)]
        self._count_iteration = count_iteration
        self._image_count = 0
        self._generate_board()


    def __iter__(self):
        return self


    def __next__(self):
        if self._count_iteration > 0:
            ImageBoard(self._board, self._image_count)
            self._image_count += 1
            unhappy_blue, unhappy_red, blank_list = self._get_lists()

            if len(unhappy_blue) > 0 and len(unhappy_red) > 0:
                take_color = random.randint(0, 1)
            elif len(unhappy_blue) == 0 and len(unhappy_red) > 0:
                take_color = 1
            elif len(unhappy_blue) > 0 and len(unhappy_red) == 0:
                    take_color = 0
            else:
                self._count_iteration = 0
                take_color = 100
            
            match take_color:
                case 0:
                    self._change_block(unhappy_blue, blank_list)
                case 1:
                    self._change_block(unhappy_red, blank_list)
            
            self._count_iteration -= 1
        else:
            raise StopIteration


    def _generate_board(self):
        percent_blue = 45
        percent_red = 45

        amount_blue = math.floor(self._size * (percent_blue / 100))
        amount_red = math.floor(self._size * (percent_red / 100))

        self._add_color('Blue', amount_blue)
        self._add_color('Red', amount_red)


    def _add_color(self, color, amount):
        while amount != 0:
            i = random.randint(0, self._ln - 1)
            j = random.randint(0, self._ln - 1)

            if self._board[i][j] == 0:
                match color:
                    case 'Blue':
                        self._board[i][j] = 1
                    case 'Red':
                        self._board[i][j] = 2
                amount -= 1


    def _change_block(self, unhappy, blank_list):
        coord = random.randint(0, len(unhappy) - 1)
        x = unhappy[coord][0]
        y = unhappy[coord][1]
        self._board[x][y] = 0          

        coord_blank = random.randint(0, len(blank_list) - 1)
        x = blank_list[coord_blank][0]
        y = blank_list[coord_blank][1]
        self._board[x][y] = 2


    def _get_lists(self):
        unhappy_blue, unhappy_red, blank_list = [], [], []

        for i in range(self._ln):
            for j in range(self._ln):
                if self._board[i][j] == 0:
                    blank_list.append([i, j])
                elif not self._check_happiness(i, j):
                    if self._board[i][j] == 1:
                        unhappy_blue.append([i, j])
                    if self._board[i][j] == 2:
                        unhappy_red.append([i, j])
        
        return unhappy_blue, unhappy_red, blank_list


    def _check_happiness(self, x, y):
        check_squares = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        color = self._board[x][y]
        
        same_color_neighbours = 0
        for check in check_squares:
            new_x, new_y = x + check[0], y + check[1]
            if 0 <= new_x < self._ln and 0 <= new_y < self._ln:
                if self._board[new_x][new_y] == color:
                    same_color_neighbours += 1

        return same_color_neighbours >= 2
