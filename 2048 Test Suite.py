"""
Template testing suite for Solitaire Mancala
"""

import poc_simpletest

def count_non_zero_tiles(game_to_test, board):
    non_zero_tiles = 0
    for height_index in range(game_to_test.get_grid_height()):
        for width_index in range(game_to_test.get_grid_width()):
            if board[height_index][width_index] != 0:
                non_zero_tiles += 1    
    return non_zero_tiles


INIT_DICT = {'UP': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)], 
        'DOWN': [(9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)], 
        'LEFT': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)], 
        'RIGHT': [(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)]}

OFFSETS = {'UP': (1, 0),
           'DOWN': (-1, 0),
           'LEFT': (0, 1),
           'RIGHT': (0, -1)}


board = [[ 2 for dummy_col in range(6)]
             for dummy_row in range(6)]        

print board

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project

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
        
        
def move(direction, grid_size):
    
    to_process = INIT_DICT[direction][:grid_size]
    print "Initial index to process is: " + str(to_process)
    print 
    
    for i in range(len(to_process)):
        new_list = []
        new_list.append(to_process[i])
        new_item_0 = to_process[i][0]
        print "New item 0 is: " + str(new_item_0)
        new_item_1 = to_process[i][1]
        print "New item 1 is: " + str(new_item_1)
        
        
        for n in range(grid_size - 1):

            
            new_item_0 += OFFSETS[direction][0]
            new_item_1 += OFFSETS[direction][1]
            new_item = (new_item_0, new_item_1)
            new_list.append(new_item)
            
        print "New list is: " + str(new_list)
        print 
        to_merge = []
        for e in new_list:
            print e
            
            to_merge.append(board[e[0]][e[1]])
        
        print to_merge
        print merge(to_merge)
        print 
        
                                                                
move('UP', 5)    


def run_suite(game_class):
    """
    Some informal testing code
    """
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()    
    
    # create a game
    game = game_class
    
    # add tests using suite.run_test(....) here
    suite.run_test(str(game.get_grid_height()), str(5), "Test #0a: init and reset, width")
    suite.run_test(str(game.get_grid_width()), str(7), "Test #0b: init and reset, height")
    
    # count number of tiles that are not 0	
    suite.run_test(str(count_non_zero_tiles(game, game.get_board())), str(2), "Test 1: reset functions")
    
    # test the set_tile and get_tile functions
    game.set_tile(2, 1, 5) 
    game.set_tile(3, 0, 7)
        
    suite.run_test(str(game.get_tile(2, 1)), str(5), "Test 2a: set_tile and get_tile")
    suite.run_test(str(game.get_tile(3, 0)), str(7), "Test 2b: set_tile and get_tile") 
    
    game_init_indices = game.calc_init_indices(7, 6)
    suite.run_test(str(game_init_indices[1][1]), str((0, 1)), "Test 3a: Calculate initial indices, up")
    suite.run_test(str(game_init_indices[3][5]), str((5, 0)), "Test 3b: Calculate initial indices, left")
    
#    # test the initial configuration of the board using the str method
#    suite.run_test(str(game), str([0]), "Test #0: init")
#
#    # check the str and get_num_seeds methods
#    config1 = [0, 0, 1, 1, 3, 5, 0]    
#    game.set_board(config1)   
#    suite.run_test(str(game), str([0, 5, 3, 1, 1, 0, 0]), "Test #1a: str")
#    suite.run_test(game.get_num_seeds(1), config1[1], "Test #1b: get_num_seeds")
#    suite.run_test(game.get_num_seeds(3), config1[3], "Test #1c: get_num_seeds")
#    suite.run_test(game.get_num_seeds(5), config1[5], "Test #1d: get_num_seeds")    
    
    # report number of tests and failures
    suite.report_results()
