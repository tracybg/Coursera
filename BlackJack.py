# Mini-project #6 - Blackjack

#Direct access using this link - http://www.codeskulptor.org/#user45_MbDnAMQ3viDtL9x.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)

card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
            self.suit = suit
            self.rank = rank

    def __str__(self):
        return self.suit + self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
#define hand class            
class Hand:
    def __init__(self):
        self.hand_of_cards = []

    def __str__(self):
        cards = ""
        for card in self.hand_of_cards:
            cards += str(card) + " "
        return "Your hand consists of " + cards       
    
    def add_card(self, card):
        self.hand_of_cards.append(card)

    def get_value(self):
        hand_value = 0
        ace_count = 0
        
        for card in self.hand_of_cards:
            hand_value += VALUES[card.rank]
            if card.rank == 'A':
                ace_count += 1
                                
        if hand_value + 10 <= 21 and ace_count >0:
                hand_value += 10
            
        return hand_value
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand_of_cards)):            
            self.hand_of_cards[i].draw(canvas, (pos[0] + (CARD_SIZE[0] + 10) * i, pos[1]))
        
# define deck class 
class Deck:
    def __init__(self):
        self.current_deck = [Card(s, r) for s in SUITS for r in RANKS]        

    def shuffle(self):
        random.shuffle(self.current_deck)

    def deal_card(self):
        self.card_dealt = self.current_deck.pop()
        return self.card_dealt
    
    def __str__(self):
        deck_string = ''
        for card in self.current_deck:
            deck_string += str(card) + " "
        return "The deck containts " + deck_string   

player_hand = Hand()
dealer_hand = Hand()
deck = Deck()

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, score
    
    if in_play == True:
        score -= 1
    
    deck.current_deck = [Card(s, r) for s in SUITS for r in RANKS]  
    deck.shuffle()
    
    dealer_hand.hand_of_cards = []
    player_hand.hand_of_cards = []
    
    outcome = 'Hit or stand? Or admit defeat by dealing now...'
        
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    in_play = True
   
def hit():
    
    global in_play, score, outcome
    
    if in_play == True:
        player_hand.add_card(deck.deal_card())
    
        if player_hand.get_value() > 21:
            in_play = False
            score -= 1
            outcome = "Player has busted! New deal?"
          
def stand():
# if hand is in play, repeatedly hit dealer until his hand has value 17 or more   
# then determin game outcome    

    global in_play, score, outcome

    if in_play:
        in_play = False
                
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())            
            
        if dealer_hand.get_value() >= player_hand.get_value() and dealer_hand.get_value()  <= 21:
            outcome = "The dealer has beat you! New deal?"
            score -= 1
    
        else:
            outcome = "You have beat the dealer! New deal?"
            score += 1  

# draw necessary graphics on the canvas   
def draw(canvas):
    #Headings and basic game info
    canvas.draw_text('Blackjack', [200, 80], 42, 'Black')
    canvas.draw_text(outcome, [100, 130], 25, 'Black')
    canvas.draw_text('Score: ' + str(score), [500, 80], 22, 'Black')
    canvas.draw_text('Player hand valued at ' + str(player_hand.get_value()), [80, 380], 22, 'Black')  
    
    #Drawing card hands
    dealer_hand.draw(canvas, [150, 200])    
    player_hand.draw(canvas, [150, 400])
    
    #Hide dealer's hole card and hand value when in play
    if in_play == True:
        canvas.draw_image(card_back, (CARD_CENTER[0], CARD_CENTER[1]), CARD_SIZE, [150 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)
        canvas.draw_text('Dealer hand', [80, 180], 22, 'Black')	
        
    else:
        canvas.draw_text('Dealer hand valued at ' + str(dealer_hand.get_value()), [80, 180], 22, 'Black')        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
