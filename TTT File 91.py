# http://www.codeskulptor.org/#user45_4qtphAs8QQR5DmX.py
"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 5000         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
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

    
def mc_update_scores(scores, board, player):
    """
    Score the completed game board and update the scores grid. 
    """       
    game_result = board.check_win()
    
    if game_result == provided.DRAW:
        pass
    
    elif game_result == player:
        player = player
        
    else:
        player = provided.switch_player(player)
            
        
    for dummy_row in range(board.get_dim()):
        for dummy_col in range(board.get_dim()):
            
            square_to_score = board.square(dummy_row, dummy_col)
            
            if square_to_score == player:
                scores[dummy_row][dummy_col] += SCORE_CURRENT
                
            elif square_to_score == provided.switch_player(player):
                scores[dummy_row][dummy_col] -= SCORE_OTHER
                                        
def get_best_move(board, scores): 
    """
    Takes current board and the grid of scores. Finds empty squares 
    on current board with the maximum score and randomly returns
    one of them as a (row, column) tuple.
    """
    empty_squares = board.get_empty_squares()
    max_value_squares = []
    empty_square_scores = []
            
    for dummy_square in empty_squares:
        empty_square_scores.append(scores[dummy_square[0]][dummy_square[1]])
    
    for dummy_square in empty_squares:
        if scores[dummy_square[0]][dummy_square[1]] == max(empty_square_scores):
            max_value_squares.append(dummy_square)
            
    if len(max_value_squares) > 0:
        return random.choice(max_value_squares)


def mc_move(board,player,trials):
    """
    Take current board, which player the machin player is, and runs
    input number of trials. Runs Monte Carlo simulations using the 
    above functions and returns the best move for machine player
    in the form of a (row, column) tuple.
    """
    score_list = [[0] * board.get_dim() for dummy_zero in range(board.get_dim())]    
    
    for dummy_trial in range(trials):
        simulation_board = board.clone()
        mc_trial(simulation_board, player)
        mc_update_scores(score_list, simulation_board, player)
    
    return get_best_move(board, score_list)
        

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
