import random


#
#      Set up suits, ranks and values
#

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':10}

playing = True

#
#      Set up card, hand and deck classes
#

class Card:
    
    def __init__(self, rank, suit):
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()
    
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
    def __len__(self):
        return values[self.rank]
    
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))
    
    def __str__(self):
        deck_str = ''
        for i in self.deck:
            deck_str += '\n'+ i.__str__()
        return 'The deck is: \n'  + deck_str
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        dealt = self.deck.pop()
        return dealt
    
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            
#
#     Set up chips class
#

class Chips:
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#
#     Some functions to run the game
#

def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input('How much would you like to bet?: '))
        except ValueError:
            print('Sorry, please provide an integer!')
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips to bet that much! You have {}'.format(chips.total))
            else:
                break
                
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    playing = True
    
    while True:
        cmd = input('Would you like to hit(h) or stand (s)? ')

        if cmd.lower()[0] == 'h':
            hit(deck,hand)
        elif cmd.lower()[0] == 's':
            print("Player stands, dealer's turn")
            playing = False
        else:
            print('Sorry, please enter H or S only')
            continue
        break
        
def show_some(player,dealer):
    
    print("Dealer's hand:")
    print("********")
    print(dealer.cards[1], "\n")
    print("\n")
    print("Player's hand:")
    print(" ", *player.cards, sep = "\n")
    
def show_all(player,dealer):
    
    print("Dealer's hand:")
    print(dealer.cards, sep = "\n")
    print(f"Dealer's value = {dealer.value}")
    print("Player's hand:")
    print(" ", *player.cards, sep = "\n")
    print(f"Player's value = {player.value}")
    
def player_busts(player,dealer,chips):
    print('Player bust!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player wins!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('Dealer bust!')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('Dealer wins!')
    chips.lose_bet()
    
def push():
    print("Tie, it's a push!")

#
#	Run the game
#

while True:
    print('BLACKJACK')

    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    dealer = Hand()
    player = Hand()
    
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())
    
    player.add_card(deck.deal())
    player.add_card(deck.deal())
        
    # Set up the Player's chips
    chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player,dealer)
    
    playing = True
    
    while playing:  # recall this variable from our hit_or_stand function
        
        hit_or_stand(deck, player)
        
        
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player,dealer,chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        while dealer.value <= player.value:
            hit(deck, dealer)
        # Show all cards
        show_all(player,dealer)
        # Run different winning scenarios
        if dealer.value > 21:
            dealer_busts(player,dealer,chips)
        elif dealer.value > player.value:
        	dealer_wins(player,dealer,chips)
        elif dealer.value < player.value:
        	player_wins(player,dealer,chips)
        else:
        	push()
    
    # Inform Player of their chips total 
    print(f'\nYour chips total is: {chips.total}')
    
    # Ask to play again
    replay = input('Would you like to play again? ')
    if replay[0].lower() == 'y':
        playing = True
        continue
    else:
    	print('Thank you for playing')
    	break
