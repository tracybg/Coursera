http://www.codeskulptor.org/#user47_tBDKh0fTPG_4.py

"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

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
    distinct_values = set(sorted(hand))
    max_score = 0
    
    for dummy_value in distinct_values:
        repeats = hand.count(dummy_value)
        temp_score = dummy_value * repeats
        if max_score <= temp_score:
            max_score = temp_score
        
    return max_score    

def max_repeats(seq):
    """
    Compute the maxium number of times that an outcome is repeated
    in a sequence
    """
    item_count = [seq.count(item) for item in seq]
    return max(item_count)    


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    possible_throws = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    total_outcomes = len(possible_throws)
    
    score_value = 0
    for throw in possible_throws:
        hand = held_dice + throw
        temp_score = score(hand)
        score_value += temp_score / float(total_outcomes)
    
    return score_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    all_holds = set([()])
    
    for dummy_die in hand:
        for dummy_hold in set(all_holds):
            new_hold = list(dummy_hold)
            new_hold.append(dummy_die)
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
    best_hold = set([()])
    best_ev = 0
    
    for dummy_hold in all_holds:
        temp_ev = expected_value(dummy_hold, num_die_sides, len(hand) - len(dummy_hold))
        if temp_ev > best_ev:
            best_ev = temp_ev
            best_hold = dummy_hold
    
    return (best_ev, best_hold)


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
                                       
    
    
    



