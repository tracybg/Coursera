"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = -1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    Play a game with given board and player by making rnadom moves.
    Function returns when the game is over. Board state is modified. 
    """
    
    while board.get_empty_squares() != []:
        next_square = random.choice(board.get_empty_squares())
        board.move(next_square[0], next_square[1], player)
        player = provided.switch_player(player)

#    while len(board.get_empty_squares()) > 3:
#        next_square = random.choice(board.get_empty_squares())
#        board.move(next_square[0], next_square[1], player)
#        player = provided.switch_player(player)        
    
# Constants
EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}

board = provided.TTTBoard(3)
score_list = [[0] * board.get_dim() for dummy_zero in range(board.get_dim())]
print "Score list is " + str(score_list)


    
def mc_update_scores(scores, board, player):
    """
    Score the completed game board and update the scores grid. 
    """
    lines = []
    lines.extend(board._board)        
    game_result = board.check_win()
    
    if game_result == DRAW:
        pass
    
    else:
        for dummy_row in range(board.get_dim()):
            for dummy_col in range(board.get_dim()):
                if game_result == player:
                    if lines[dummy_row][dummy_col] == player:
                        scores[dummy_row][dummy_col] += SCORE_CURRENT  
                        
                    else:
                        scores[dummy_row][dummy_col] += SCORE_OTHER
                        
                else:
                    if lines[dummy_row][dummy_col] == player:
                        scores[dummy_row][dummy_col] -= SCORE_CURRENT
                        
                    else:
                        scores[dummy_row][dummy_col] -= SCORE_OTHER
                
    return scores

board = provided.TTTBoard(3)
mc_trial(board, provided.PLAYERX)
print board 
print mc_update_scores(score_list, board, PLAYERX)   

board = provided.TTTBoard(3)
mc_trial(board, provided.PLAYERX)
print board 
print mc_update_scores(score_list, board, PLAYERX) 

board = provided.TTTBoard(3)
mc_trial(board, provided.PLAYERX)
print board 
print mc_update_scores(score_list, board, PLAYERX) 

board = provided.TTTBoard(3)
mc_trial(board, provided.PLAYERX)
print board 
print mc_update_scores(score_list, board, PLAYERX) 
 
def test_board(board, player):

    while len(board.get_empty_squares()) > 3:
        next_square = random.choice(board.get_empty_squares())
        board.move(next_square[0], next_square[1], player)
        player = provided.switch_player(player) 
        
board = provided.TTTBoard(3)
test_board(board, provided.PLAYERX)
print board 
print mc_update_scores(score_list, board, PLAYERX)         
    
def get_best_move(board, scores): 
    """
    Takes current board and the grid of scores. Finds empty squares 
    on current board with the maximum score and randomly returns
    one of them as a (row, column) tuple.
    """
#    max_list = []
#    for dummy_list in scores:
#        max_list.append(max(dummy_list))
#            
#    max_value = max(max_list)
#    print "Max value is " + str(max_value)
#    
    empty_squares = board.get_empty_squares()
    print "Empty squares " + str(empty_squares)
    
    max_value = 0
    max_value_squares = []
    
    for dummy_square in empty_squares:
        if scores[dummy_square[0]][dummy_square[1]] > max_value:
            max_value = scores[dummy_square[0]][dummy_square[1]]
            print "New max value is " + str(max_value)
            
    for dummy_square in empty_squares:
        if scores[dummy_square[0]][dummy_square[1]] == max_value:
            max_value_squares.append(dummy_square)
            
    print max_value_squares
    if len(max_value_squares) > 0:
        return random.choice(max_value_squares)
        
print get_best_move(board, score_list)

def mc_move(board,player,trials):
    """
    Take current board, which player the machin player is, and runs
    input number of trials. Runs Monte Carlo simulations using the 
    above functions and returns the best move for machine player
    in the form of a (row, column) tuple.
    """
#    for dummy_trial in range(trials):
#		mc_trial(board, player)

        

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
