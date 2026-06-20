import random

class Player:
    def __init__(self, deck):
        self.deck = deck
        self.hand = []
        self.active = None
        self.bench = []
        self.prizes = []
        self.time = 0.0

        # One use per turn actions
        self.energy_attached = False
        self.supporter_played = False
        self.retreated = False

    def shuffle_deck(self):
        '''
        '''
        count = random.randint(1, 5)
        for _ in range(count):
            random.shuffle(self.deck)

    def draw(self, amount = 1):
        '''
        '''
        for _ in range(amount):
            if self.deck:
                card = self.deck.pop(0)
                self.hand.append(card)
            else:
                break

    def set_prizes(self):
        '''
        '''
        for _ in range(6):
            card = self.deck.pop(0)
            self.prizes.append(card)

    def take_prize_cards(self, amount = 1):
        '''
        '''
        for _ in range(amount):
            if self.prizes:
                card = self.pop(0)
                self.hand.append(card)
