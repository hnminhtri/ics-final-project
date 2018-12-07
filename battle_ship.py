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
    
    def shooting(self):
        print("It is now your turn!")
        row, column = input('Please enter where you want to shoot (e.g. A 1): ').split()
        while row not in "ABCDEFGHIJ" and int(column) > 10:
            row, column = input('Please enter where you want to shoot (e.g. A 1): ').split()
        return row, int(column)

class BattleShip():
    
    def __init__(self):
        grid1, grid2 = Grid(), Grid()
        player1, player2 = Player('Tri'), Player('Kennedy')
        self.grids = [grid1, grid2]
        self.players = [player1, player2]
        self.whose_turn = 1
        
    def shooting(self):
        if self.whose_turn == 1:
            xy = self.players[0].shooting()
            self.grids[0].shooting(xy)
            self.whose_turn = 2
        else:
            xy = self.players[1].shooting()
            self.grids[1].shooting(xy)
            self.whose_turn = 1

    def rival_grid(self):
        if self.whose_turn == 1:
            return self.grids[1].grid_wo_ships()
        else:
            return self.grids[0].grid_wo_ships()
    
    def own_grid(self):
        if self.whose_turn == 1:
            return self.grids[0].grid_w_ships()
        else:
            return self.grids[1].grid_w_ships()
    
    
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
                if random.randint(0,1) == 0:
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
                print(random_xy)

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
                
                free_cells = [(x, y) for y in range(10) for x in range(10)] #create 10x10 grid
                global_grid = [[" " for y in range(10)] for x in range(10)] #create empty space for each cell
                global_mod_grid = [[Ship((x,y), 0, 1) for y in range(10)] for x in range(10)] #placing ship of length 0 to all cells
                for i in range(1,5):
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
    xy_lst = [(1,0), (-1,0), (0,1), (0,-1)]
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
        xy_lst = [(1,1), (1,-1), (-1,1), (-1,1)]
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
            current[kind] = current[kind]/kind
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
    grid_str = ""+ num_index + line
    letters = "ABCDEFGHIJ"
    for x in range(len(grid_info)):
        grid_str += "    "+letters[x]+"  "
        for y in range(len(grid_info[x])):
            grid_str += "  "+ grid_info[x][y] +"  |"
        grid_str += "\n"
        grid_str += line
    return grid_str
        
game = BattleShip()

while True:
    print("This is your field: ")
    print(game.own_grid())
    print("\n This is your rival's field: ")
    print(game.rival_grid())
    game.shooting()


    