#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 09:58:56 2018

@author: hnminhtri
"""
import random
random.seed(0)


class Player():
    def __init__(self, name):
        self.name = name
        self.shooting_list = []
        
class BattleShip():

    def __init__(self, p1, p2):
        grid1, grid2 = Grid(), Grid()
        player1, player2 = Player(p1), Player(p2)
        self.grids = [grid1, grid2]
        self.players = [player1, player2]
        self.whose_turn = 0  # player1's turn

    def shooting(self, xy):
        try:
            row, column = xy.split()
            column = int(column)
            if row not in "ABCDEFGHIJ" or column > 10 or column < 1:
                return False, 'Error: Coordinate is wrong'
            else:
                your_id = self.whose_turn
                if xy not in self.players[your_id].shooting_list:
                    pre_shooting = self.grids[abs(your_id-1)].player_grid.copy()
                    self.grids[abs(self.whose_turn-1)].shooting((row, column))
                    if pre_shooting[convert_row_letter(row)][column-1] != "*":
                        self.whose_turn = 0 if self.whose_turn else 1
                    self.players[your_id].shooting_list.append(xy)
                    return True, self.get_context_mess_status(your_id)
                else:
                    return False, "This cell is already damanged. Shoot another cell!"
        except:
            return False, 'Opps! Something wrong happened!'

    def rival_grid(self, player):
        rival_id = 0 if player else 1
        return self.grids[rival_id].grid_wo_ships()

    def own_grid(self, player):
        return self.grids[player].grid_w_ships()

    def get_grids_info(self, player):
        own_grid = self.own_grid(player)
        rival_grid = self.rival_grid(player)
        return own_grid, rival_grid

    def check_winning(self, player):
        grid_1 = self.get_grids_info(player)[0]
        grid_2 = self.get_grids_info(abs(player-1))[0]
        if "*" not in grid_1 and "*" in grid_2:
           return 2
        elif "*" not in grid_2 and "*" in grid_1:
            return 1
        else:
            return 0
                          
    def get_current_status_round(self, player):
        
        if player == self.whose_turn:
            round_mess = 'Go! It is your turn!\n'
            round_mess += 'Please enter where you want to shoot (e.g. A 1):'
        else:
            round_mess = "Wait, it's your opponent's turn!"
        return round_mess

    def get_context_mess_status(self, player):
        grids_info = self.get_grids_info(player)
        msg_content = "This is your grid: \n"
        msg_content += grids_info[0]
        msg_content += "\n This is your opponent's grid: \n"
        msg_content += grids_info[1]
        if self.check_winning(player) == 0: 
            msg_content += '\n' + self.get_current_status_round(player)
        return msg_content

class Ship():
    def __init__(self, xy_start, length, horizontal):
        self.xy_start = xy_start
        self.length = length
        self.hrztl = horizontal
        self.hit = [False for i in range(length)]

    def get_shoot(self, xy):
        if self.length != 0:
            self.hit[abs(xy[0] + xy[1] - self.xy_start[0] - self.xy_start[1])] == True
        else:
            self.hit = [True]


class Grid():
    def __init__(self):
        def create_Grid():

            def gen_direction():
                if random.randint(0, 1) == 0:
                    return "h"
                else:
                    return "v"

            def place_ship(size, empty_cells, grid, mod_grid):
                direction = gen_direction()

                if direction == "v":
                    empty_cells = list(filter(lambda item: item[0] <= 10 - size, empty_cells))
                else:
                    empty_cells = list(filter(lambda item: item[1] <= 10 - size, empty_cells))

                if len(empty_cells) == 0:
                    return empty_cells, grid, mod_grid
                random_xy = random.choice(empty_cells)
                if direction == "v":
                    for y in [-1, 0, 1]:
                        for x in range(-1, size + 1):
                            try:
                                empty_cells.remove((random_xy[0] + x, random_xy[1] + y))
                            except:
                                pass
                    for i in range(size):
                        grid[random_xy[0] + i][random_xy[1]] = "*"
                        new_ship = Ship(random_xy, size, 0)
                        mod_grid[random_xy[0] + i][random_xy[1]] = new_ship

                if direction == "h":
                    for x in [-1, 0, 1]:
                        for y in range(-1, size + 1):
                            try:
                                empty_cells.remove((random_xy[0] + x, random_xy[1] + y))
                            except:
                                pass
                    for i in range(size):
                        grid[random_xy[0]][random_xy[1] + i] = "*"
                        new_ship_2 = Ship(random_xy, size, 1)
                        mod_grid[random_xy[0]][random_xy[1] + i] = new_ship_2
                return [empty_cells, grid, mod_grid] 

            while 1:

                free_cells = [(x, y) for y in range(10) for x in range(10)]  # create 10x10 grid
                global_grid = [[" " for y in range(10)] for x in range(10)]  # create empty space for each cell
                global_mod_grid = [[Ship((x, y), 0, 1) for y in range(10)] for x in
                                   range(10)]  # placing ship of length 0 to all cells
                for i in range(1, 5):
                    if i == 1:
                        new_grid_info = place_ship(1, free_cells, global_grid, global_mod_grid)
                        free_cells = new_grid_info[0]
                        grid = new_grid_info[1]
                        mod_grid = new_grid_info[2]
                    for j in range(5 - i):
                        new_grid_info = place_ship(j, free_cells, global_grid, global_mod_grid)
                        free_cells = new_grid_info[0]
                        grid = new_grid_info[1]
                        mod_grid = new_grid_info[2]

                if valid(grid):
                    return grid, mod_grid

        grids = create_Grid()
        self.ships = grids[1]
        self.player_grid = grids[0]
        self.shot_cells = [[' ' for y in range(10)] for x in range(10)]

    def shooting(self, raw_xy):
        xy = (convert_row_letter(raw_xy[0]), raw_xy[1] - 1)
        self.ships[xy[0]][xy[1]].get_shoot(xy)
        self.shot_cells[xy[0]][xy[1]] = "X"

    def grid_wo_ships(self):
        return convert_string(self.shot_cells)

    def grid_w_ships(self):
        player_grid = [["X" if self.shot_cells[x][y] == "X" else self.player_grid[x][y] \
                        for y in range(10)] for x in range(10)]
        return convert_string(player_grid)


def convert_row_letter(letter):
    print(letter, type(letter))
    string = "ABCDEFGHIJ"
    return string.index(letter)


def check_size(grid_info, raw_xy):
    x_0 = convert_row_letter(raw_xy[0])
    y_0 = raw_xy[1] - 1
    xy_lst = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    count = 1
    for x, y in xy_lst:
        x_1 = x
        y_1 = y
        try:
            while grid_info[x_0 + x][y_0 + y] != ' ':
                x += x_1
                y += y_1
                count += 1
        except:
            pass
    return count


def valid(grid_info):
    def check_position(mtrx):
        xy_lst = [(1, 1), (1, -1), (-1, 1), (-1, 1)]
        for x in range(len(mtrx)):
            for y in range(len(mtrx)):
                if mtrx[x][y] != ' ':
                    for x_1, y_1 in xy_lst:
                        try:
                            if mtrx[x + x_1][y + y_1] in ("*", "X"):
                                return False
                        except:
                            pass

    return True

    def check_num_ships(mtrx):
        required = {1: 4, 2: 3, 3: 2, 4: 1}
        current = {1: 0, 2: 0, 3: 0, 4: 0}
        string = "ABCDEFGHIJ"
        for x in range(len(mtrx)):
            for y in range(len(mtrx)):
                if mtrx[x][y] != ' ':
                    ship = check_size(mtrx, (string[x], y + 1))
                    if ship == 1:
                        current[1] += 1
                    elif ship == 2:
                        current[2] += 1
                    elif ship == 3:
                        current[3] += 1
                    elif ship == 4:
                        current[4] += 1
                    else:
                        return False
        for kind in current.keys():
            current[kind] = current[kind] / kind
        if current == required:
            return True
        else:
            return False

    if sum(len(item) for item in grid_info) != 100:
        return False
    if not check_position(grid_info):
        return False
    if not check_num_ships(grid_info):
        return False
    return True


def convert_string(grid_info):
    line = "        ___________________________________________________________\n"
    num_index = "         1     2     3     4     5     6     7     8     9     10     \n"
    grid_str = "" + num_index + line
    letters = "ABCDEFGHIJ"
    for x in range(len(grid_info)):
        grid_str += "    " + letters[x] + "  "
        for y in range(len(grid_info[x])):
            grid_str += "  " + grid_info[x][y] + "  |"
        grid_str += "\n"
        grid_str += line
    return grid_str
