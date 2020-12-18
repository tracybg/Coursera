"""
Analyzing a simple dice game

YOUR SOLUTION DOES NOT WORK FOR DICE > 3
"""


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

# example for digits


def max_repeats(seq):
    """
    Compute the maxium number of times that an outcome is repeated
    in a sequence
    """
    
    distinct_num = set(seq)
    return len(seq) - len(distinct_num) + 1


def compute_expected_value():
    """
    Function to compute expected value of simple dice game
    """
    outcomes = set([1, 2, 3, 4, 5, 6])
    sequences = gen_all_sequences(outcomes, 3)
    doubles = 0 
    triples = 0
    total_outcomes = len(sequences)
    for seq in sequences:
        if max_repeats(seq) == 2:
            doubles += 1
        elif max_repeats(seq) == 3:
            triples += 1
            
    return (doubles * 10 + triples * 200) / float(total_outcomes)       
    


def run_test():
    """
    Testing code, note that the initial cost of playing the game
    has been subtracted
    """
    outcomes = set([1, 2, 3, 4, 5, 6])
    print "All possible sequences of three dice are"
    print gen_all_sequences(outcomes, 3)
    print
    print "Test for max repeats"
    print "Max repeat for (3, 1, 2) is", max_repeats((3, 1, 2))
    print "Max repeat for (3, 3, 2) is", max_repeats((3, 3, 2))
    print "Max repeat for (3, 3, 3) is", max_repeats((3, 3, 3))
    print
    print "Ignoring the initial $10, the expected value was $", compute_expected_value()
    
run_test()


