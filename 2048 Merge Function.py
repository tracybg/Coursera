"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    
    new_line = list(line) 
    
    for dummy_idx in range((len(new_line) - 1)):         
        next_idx = dummy_idx + 1  
        
        while new_line[next_idx] == 0 and next_idx < (len(new_line) - 1):
            next_idx += 1 
            
        if new_line[dummy_idx] == new_line[next_idx]:
            new_line[dummy_idx] = new_line[dummy_idx] + new_line[next_idx]
            new_line[next_idx] = 0	 
            
    for dummy_digit in list(new_line):
        if dummy_digit == 0:
            new_line.remove(dummy_digit) 
            new_line.append(0)
    
    return new_line

    
    
test1 = [2, 0, 2, 4]
print "Original line is " + str(test1)
print "Merge 1 returns " + str(merge(test1))

print
print

test2 = [0, 0, 2, 2]
print "Original line is " + str(test2)
print "Merge 1 returns " + str(merge(test2))

print
print

test3 = [2, 2, 2, 2, 2]
print "Original line is " + str(test3)
print "Merge 1 returns " + str(merge(test3))

print
print

test4 = [8, 16, 16, 8]
print "Original line is " + str(test4)
print "Merge 1 returns " + str(merge(test4))
