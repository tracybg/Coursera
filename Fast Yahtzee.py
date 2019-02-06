http://www.codeskulptor.org/#user45_dN3Bd9z04t6gQkd.py

"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
from collections import Counter as counter
codeskulptor.set_timeout(5)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    score_list = []
    num_count = counter(hand)
    for dummy_num in num_count:
        score_list.append(dummy_num * num_count[dummy_num])
                              
    return max(score_list)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    expt_value = float(0)
    
    outcomes = [digit for digit in range(1, num_die_sides + 1)]
    
    free_dice_sample_space = gen_all_sequences(outcomes, num_free_dice)
    
    for dummy_sample in free_dice_sample_space:
        temp_hand = dummy_sample + held_dice
        expt_value += score(temp_hand) / float((num_die_sides ** num_free_dice))
    
    return expt_value

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = set([()])
        
    for die in hand:
        for hold in set(all_holds):
            new_hold = list(hold)
            new_hold.append(die)
            all_holds.add(tuple(new_hold))      
                      
    return all_holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    all_holds = gen_all_holds(hand)
    
    expt_value = 0
    result_hold = ()
    
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)
        temp_expt_value = expected_value(hold, num_die_sides, num_free_dice)
        if temp_expt_value > expt_value:
            expt_value = temp_expt_value
            result_hold = hold
    
    return (expt_value, result_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
