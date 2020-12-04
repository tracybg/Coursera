"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    merged_list = []
    for dummy_index in range(len(line)): 
        if line[dummy_index] != 0:
            merged_list.append(line[dummy_index])
    
    for dummy_index in range(len(merged_list) - 1):
        if merged_list[dummy_index] == merged_list[dummy_index + 1]:
            merged_list[dummy_index] = merged_list[dummy_index] * 2
            merged_list[dummy_index + 1] = 0
    
    for dummy_index in range(len(merged_list)): 
        if merged_list[dummy_index] == 0:
            merged_list.pop(dummy_index)
            merged_list.append(0)
            
    filler = len(line) - len(merged_list)
    
    merged_list.extend([0] * filler)
            
    return merged_list 

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    
    def __init__(self, grid_height, grid_width):
        # initialize board
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        
        up_list = []
        down_list = []
        
        for dummy_num in range(grid_width):
            up_list.append((0, dummy_num))
            down_list.append((grid_height - 1, dummy_num))
        
        self._up_initial_tiles = up_list
        self._down_initial_tiles = down_list
        
        left_list = []
        right_list = []
        
        for dummy_num in range(grid_height):
            left_list.append((dummy_num, 0))
            right_list.append((dummy_num, grid_width - 1))
            
        self._left_initial_tiles = left_list
        self._right_initial_tiles = right_list            

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[ 0 for dummy_col in range(self._grid_width)]
                                   for dummy_row in range(self._grid_height)]
        
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        # Store initial board config to compare with merged results later 
        initial_grid = [list(l) for l in self._grid]
        
        # Figure out which initial indies to work on based on direction
        initial_tiles_dict = {UP: self._up_initial_tiles,
                              DOWN: self._down_initial_tiles,
                              LEFT: self._left_initial_tiles,
                              RIGHT: self._right_initial_tiles}        
        
        initial_tiles = initial_tiles_dict.get(direction)

        # Number of lines to work on based on direction
        num_steps = self.get_grid_height()
        if direction == LEFT or direction == RIGHT:
            num_steps = self.get_grid_width()
  
        # Merge lines, then set the board based on merged lines
        for dummy_index in range(len(initial_tiles)):
            indices_to_merge = self.traverse_grid(initial_tiles[dummy_index], OFFSETS.get(direction), num_steps)
            print "Indices to merge" + str(indices_to_merge)
            
            line_to_merge = []
            for dummy_index in range(len(indices_to_merge)):
                line_to_merge.append(self.get_tile(indices_to_merge[dummy_index][0], indices_to_merge[dummy_index][1]))
            
            merged_line = merge(line_to_merge)
            print "Line to merge" + str(line_to_merge)
            print "Merged line" + str(merged_line)
            
            for dummy_index in range(len(indices_to_merge)):
                self.set_tile(indices_to_merge[dummy_index][0], indices_to_merge[dummy_index][1], merged_line[dummy_index])

            
        # If board has changed, insert new tile     
        if initial_grid != self._grid:
            self.new_tile()
        
    def traverse_grid(self, start_cell, direction, num_steps):
        """
        Helper method to prepare list of indices to operate on based on 
        initial tiles and direction.
        """
        
        traversed_index = []
        
        for dummy_step in range(num_steps):
            row = start_cell[0] + dummy_step * direction[0]
            col = start_cell[1] + dummy_step * direction[1]
            traversed_index.append([row, col])

        return traversed_index
        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # Pick new tile value
        inventory = [2] * 9 + [4]
        new_tile_value = random.choice(inventory)
        
        #Find cells with 0 value
        indices_of_0_value = []
        for dummy_row in range(self.get_grid_height()):
            for dummy_col in range (self.get_grid_width()):
                if self.get_tile(dummy_row, dummy_col) == 0:
                    indices_of_0_value.append([dummy_row, dummy_col]) 
                    
        
        #Pick random location and set cell value to new tile value
        random_tile = random.choice(indices_of_0_value)
        self.set_tile(random_tile[0], random_tile[1], new_tile_value)                       
                                 
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(5, 4))
#game = TwentyFortyEight(3, 4)
#print game
#print game.move(UP)
#
#print game.move(LEFT)


#Phase 2 test prior to working new_tile method                                 
#import user47_3hszfGJOPs_6 as test_2048_phase_2
#test_2048_phase_2.run_suite(TwentyFortyEight)

#Phase 3 test for initial tiles calulation
#import user47_3hszfGJOPs_11 as test_2048_phase_3
#test_2048_phase_3.run_suite(TwentyFortyEight)
