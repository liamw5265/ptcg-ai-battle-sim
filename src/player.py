import random
from card import Card, Attack, Ability, PokemonCard, TrainerCard, EnergyCard
from globals import EFFECTS_DICT, ACTION_DICT

class Player:
    def __init__(self, deck: list[Card]):
        self.deck: list[Card] = deck
        self.hand: list[Card] = []
        self.active: PokemonCard | None = None
        self.bench: list[PokemonCard] = []
        self.prizes: list[Card] = []
        self.discard_pile: list[Card] = []
        self.time: float = 0.0

        # One use per turn actions
        self.energy_attached: bool = False
        self.supporter_played: bool = False
        self.retreated: bool = False

    # Set up phase
    def shuffle_deck(self):
        '''
        '''
        for _ in range(random.randint(1, 5)):
            random.shuffle(self.deck)

        return True
    
    def draw_hand(self):
        '''
        '''
        for _ in range(7):
            card = self.deck.pop(0)
            self.hand.append(card)

        return True
    
    def hand_has_basic(self):
        '''
        '''
        mulligan = 0

        while True:
            if not self.draw_hand():
                for card in self.bench:
                    self.deck.append(card)

                self.hand.clear()
                self.shuffle_deck()
                mulligan += 1
            else:
                break

        return True, mulligan
    
    def play_basic_to_active(self, pokemon: PokemonCard):
        '''
        '''
        if self.active is not None:
            return False
        
        if pokemon.stage != 0:
            return False
        
        self.active = pokemon
        self.hand.remove(pokemon)

        return True
    
    def play_basic_to_bench(self, pokemon: PokemonCard, max_bench: int = 5):
        '''
        '''
        if len(self.bench) >= max_bench:
            return False
        
        if pokemon.stage != 0:
            return False
        
        self.bench.append(pokemon)
        self.hand.remove(pokemon)

        return True
    
    def set_prizes(self):
        '''
        '''
        if self.prizes:
            return False
        
        for _ in range(6):
            card = self.deck.pop(0)
            self.prizes.append(card)

        return True
    

    # Action Phase
    def draw(self, amount: int = 1):
        '''
        '''
        if not self.deck:
            return False
        
        for _ in range(amount):
            card = self.deck.pop(0)
            self.hand.append(card)

    








