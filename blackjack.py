# Mini-project #6 - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
	
import random

simplegui.Frame._hide_status = True
simplegui.Frame._keep_timers = False

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
message = ""
first_deal = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: %s %s  " % suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return self.hand

    def add_card(self, card):
        return self.hand.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        self.hand_pt = 0
        for card in range(len(self.hand)):
            if self.hand[card].get_rank() in VALUES:
                self.hand_pt = self.hand_pt + VALUES[self.hand[card].get_rank()]
                
        for i in range(len(self.hand)):
            if not 'A' in self.hand[i].get_rank():
                self.hand_pt = self.hand_pt
            elif self.hand_pt + 10 <= 21:
                self.hand_pt = self.hand_pt + 10
            else:
                self.hand_pt = self.hand_pt
        return self.hand_pt
    
    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False
    
    def draw(self, canvas, p):
        self.i = 0
        for card in self.hand:
            card.draw(canvas, [self.i * 90 + 50, p * 200])
            self.i += 1
        
# define deck class
class Deck:
    def __init__(self):
        self.deck = [Card(s, r) for s in SUITS for r in RANKS]
        
    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        return self.deck
    
#define event handlers for buttons
def deal():
    global first_deal, message, outcome, in_play, player, dealer, deck, score, message
    in_play = True
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    for i in range(2): 
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    outcome = ""
    message = ""
    if in_play == True and first_deal == False: 
        score -= 1
        in_play = False
    in_play = True
    first_deal = False

def hit():
    global player, deck, outcome, in_play, message, score
    if in_play:
        if player.busted() == True:
            outcome = "You are Busted!!!"
            message = "Dealer wins!!!"
            score -= 1
            in_play = False
        else:
            player.hand.append(deck.deal_card())
    
def stand():
    global player, dealer, deck, outcome, message, score, in_play
    if in_play:
         while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
         if player.busted == True:
                    outcome = "You are busted!!!"
                    message = "Dealer wins!!!"
                    score -= 1
         elif dealer.busted == True:
                    outcome = "Dealer is busted!!!"
                    message = "Player wins!!!" 
                    score += 1
         elif dealer.get_value() >= player.get_value():
                    outcome = "You are busted!!!"
                    message = "Dealer wins!!!"
                    score -= 1
         else:
                outcome = "Dealer is busted!!!"
                message = "Player wins!!!" 
                score += 1        
         in_play = False
                    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    dealer.draw(canvas, 1)
    player.draw(canvas, 2)
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    canvas.draw_text(outcome, (0, 520), 20, "Black")
    canvas.draw_text(message, (0, 550), 20, "Black")
    canvas.draw_text(str(score), (500, 100), 20, "Black")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()
