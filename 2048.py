"""
Clone of 2048 game.
"""
#http://www.codeskulptor.org/#user45_mnZE8eEtkbKBDgL.py

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
    new_line = list(line) 
    
    for idx in range((len(new_line) - 1)):         
        next_idx = idx + 1  
        
        while new_line[next_idx] == 0 and next_idx < (len(new_line) - 1):
            next_idx += 1 
            
        if new_line[idx] == new_line[next_idx]:
            new_line[idx] = new_line[idx] + new_line[next_idx]
            new_line[next_idx] = 0	 
            
    for digit in list(new_line):
        if digit == 0:
            new_line.remove(digit) 
            new_line.append(0)
    
    return new_line


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_width = grid_width
        self._grid_height = grid_height

        self.reset()
        
        self._initial_indices = self.calc_init_indices(grid_height, grid_width)
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._board = [[ 0 for dummy_col in range(self._grid_width)]
                                   for dummy_row in range(self._grid_height)]
        
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._board)

    def get_board(self):
        """ 
        Returns the board in list form for.
        """
        return self._board          
    
    def calc_init_indices(self,grid_height, grid_width):   
        """
        Calculates the indices for initial grids of each movement direction,
        based on grid size.
        """                        
        initial_indices = {UP: [(0, i) for i in range(grid_width)],
                           DOWN: [(grid_height - 1, i) for i in range(grid_width)],
                           LEFT: [(i, 0) for i in range(grid_height)],
                           RIGHT: [(i, grid_width - 1) for i in range(grid_height)]}

        return initial_indices
                
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # Store initial board config to compare with merged results later 
        initial_board = [list(l) for l in self.get_board()]
        
        # Pick the grid lists to work on given direction
        target_initial_indices = self._initial_indices.get(direction)
        
        if direction == UP or direction == DOWN:
            number_of_lists = self.get_grid_width()
            length_each_list = self.get_grid_height()
            
        else:
            number_of_lists = self.get_grid_height()  
            length_each_list = self.get_grid_width()   
        
        #Calculate the indices of cells to operate on based on direction
        for lst in range(number_of_lists):
            line_of_indices_to_process = []
            line_of_indices_to_process.append(target_initial_indices[lst])
            new_item_0 = target_initial_indices[lst][0]
            new_item_1 = target_initial_indices[lst][1]   
        
            for dummy_element in range(length_each_list - 1):            
                new_item_0 += OFFSETS[direction][0]
                new_item_1 += OFFSETS[direction][1]
                line_of_indices_to_process.append([new_item_0, new_item_1])

        # Merge the resulting list of grids            
            to_merge = []
        
            for line in line_of_indices_to_process:   
                to_merge.append(self._board[line[0]][line[1]])

        # Set board values after merge
            for num in range(len(line_of_indices_to_process)): 
                self.set_tile(line_of_indices_to_process[num][0], line_of_indices_to_process[num][1], merge(to_merge)[num])  
                
        # If board has changed, insert new tile
        if initial_board != self.get_board():
            self.new_tile()

            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """                
        new_tile_value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        
        indices_of_0_value = []
        for row in range(self.get_grid_height()):
            for col in range (self.get_grid_width()):
                if self.get_board()[row][col] == 0:
                    indices_of_0_value.append([row, col])        
        
        #pick randomly the location in the list to assign the new value
        random_tile = random.randint(0,len(indices_of_0_value)-1)
        self.set_tile(indices_of_0_value[random_tile][0], indices_of_0_value[random_tile][1], new_tile_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board[row][col]

TwentyFortyEight = TwentyFortyEight(4, 5)
poc_2048_gui.run_gui(TwentyFortyEight)
