http://www.codeskulptor.org/#user48_xqKQeyOg7Ua1cEz.py

"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    
    ans = []
    previous = ''
    
    for item in list1:
        if item != previous:
            previous = item
            ans.append(item)
    
    return ans

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    
    ans = []
    
    for item in list1:
        if item in list2:
            ans.append(item)
    
    return ans

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    temp1 = list(list1)
    temp2 = list(list2)
    ans = []
    
    while temp1 and temp2:
        if temp1[0] < temp2[0]:
            ans.append(temp1.pop(0))
        
        else:
            ans.append(temp2.pop(0)) 
            
    return ans + temp1 + temp2
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    
    if len(list1) < 2:
        return list1 
    
    mid = int(math.floor(len(list1) / 2))
    
    temp1 = list1[:mid]
    temp2 = list1[mid:]
    
    return merge(merge_sort(temp1), merge_sort(temp2))
                                      
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    
    if len(word) == 0:
        return [""]
    
    else:
        first_letter = word[0]
        rest_of_strings = gen_all_strings(word[1:])

        all_strings = []
    
        for string in rest_of_strings:
            for idx in range(len(string) + 1):
                all_strings.append(string[:idx] + first_letter + string[idx:])
    
        return all_strings + rest_of_strings
           
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    
