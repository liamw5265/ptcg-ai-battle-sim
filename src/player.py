import random
from card import Card, Attack, Ability, PokemonCard, TrainerCard, EnergyCard
from game import Game
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
    def shuffle_deck(self) -> bool:
        '''
        '''
        for _ in range(random.randint(1, 5)):
            random.shuffle(self.deck)

        return True
    
    def draw_hand(self) -> bool:
        '''
        '''
        for _ in range(7):
            card = self.deck.pop(0)
            self.hand.append(card)

        return True
    
    def hand_has_basic(self) -> list[bool, int]:
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

        return [True, mulligan]
    
    def play_basic_to_active(self, pokemon: PokemonCard) -> bool:
        '''
        '''
        if self.active is not None:
            return False
        
        if pokemon.stage != 0:
            return False
        
        self.active = pokemon
        self.hand.remove(pokemon)

        return True
    
    def play_basic_to_bench(self, pokemon: PokemonCard, max_bench: int = 5) -> bool:
        '''
        '''
        if len(self.bench) >= max_bench:
            return False
        
        if pokemon.stage != 0:
            return False
        
        if pokemon not in self.hand:
            return False
        
        self.bench.append(pokemon)
        self.hand.remove(pokemon)

        return True
    
    def set_prizes(self) -> bool:
        '''
        '''
        if self.prizes:
            return False
        
        for _ in range(6):
            card = self.deck.pop(0)
            self.prizes.append(card)

        return True
    

    # Action Phase
    def draw(self, amount: int = 1) -> bool:
        '''
        '''
        if not self.deck:
            return False
        
        for _ in range(amount):
            card = self.deck.pop(0)
            self.hand.append(card)

    def can_evolve_pokemon(self, pre_evo: PokemonCard, evo_pokemon: PokemonCard) -> bool:
        '''
        '''
        if pre_evo.evolved:
            return False
        
        if evo_pokemon.card_id != pre_evo.card_id - 1 and evo_pokemon.stage != pre_evo.stage - 1:
            return False
        
        if pre_evo not in self.bench or pre_evo != self.active:
            return False
        
        return True

    def evolve_pokemon(self, pre_evo: PokemonCard, evo_pokemon: PokemonCard) -> bool:
        '''
        '''
        if not self.can_evolve_pokemon(pre_evo, evo_pokemon):
            return False
        
        evo_pokemon.damage = pre_evo.damage
        evo_pokemon.status_cond = pre_evo.status_cond
        evo_pokemon.tool = pre_evo.tool

        if pre_evo == self.active:
            temp = self.active
            self.active = evo_pokemon

        if pre_evo in self.bench:
            index = self.bench.index(pre_evo)
            self.bench.insert(index, evo_pokemon)

        return True
    
    def can_attach_energy(self, pokemon: PokemonCard, energy: EnergyCard) -> bool:
        '''
        '''
        if self.energy_attached:
            return False
        
        if pokemon not in self.bench:
            return False
        
        if pokemon != self.active:
            return False
        
        return True
    
    def attach_energy(self, pokemon: PokemonCard, energy: EnergyCard) -> bool:
        '''
        '''
        if not self.can_attach_energy(pokemon, energy):
            return False
        
        pokemon.attached_energy.append(energy)
        self.hand.remove(energy)
        self.energy_attached = True

        return True
    
    def can_retreat_active(self, bench_pokemon: PokemonCard) -> bool:
        '''
        '''
        if self.retreated:
            return False

        if self.active is None:
            return False
        
        if bench_pokemon == self.active:
            return False
        
        if bench_pokemon not in self.bench:
            return False
        
        return False

    def retreat_active(self, bench_pokemon: PokemonCard) -> bool:
        '''
        '''
        if not self.can_retreat_active(bench_pokemon):
            return False
        
        self.bench.append(self.active)
        self.active = bench_pokemon
        self.retreated = True

        return True
    
    def can_play_trainer(self, card: TrainerCard, pokemon: PokemonCard = None) -> bool:
        '''
        '''
        if card.card_type == 'Supporter' and self.supporter_played:
            return False
        
        if pokemon is None and card.use_on_pokemon:
            return False
        
        return True
    
    def play_trainer(self, game: Game, card: TrainerCard, pokemon: PokemonCard = None) -> bool:
        '''
        '''
        if not self.can_play_trainer(card):
            return False
        
        if card.card_type == 'Suppoerter' or card.card_type == 'Item':
            if card.card_type == 'Supporter':
                self.supporter_played = True
            effect_function = EFFECTS_DICT.get(card.effect_id)

            if effect_function is not None:
                effect_function(self, card)

        elif card.card_type == 'Stadium':
            if game.stadium is not None:
                old_stadium = game.stadium['card']
                old_owner = game.stadium['owner']

                old_owner.discard_pile.append(old_stadium)

                game.stadium = {
                    'card': card,
                    'owner': self
                }

                self.hand.remove(card)
                return True

        elif card.card_type == 'Tool':
            pokemon.tool = card
            self.hand.remove(card)
            return True

        self.hand.remove(card)
        self.discard_pile.append(card)

        return True
    
    def can_use_ability(self, pokemon: PokemonCard) -> bool:
        '''
        '''
        if pokemon.ability is None:
            return False
        
        if pokemon.ability.once_per_turn and pokemon.ability.used:
            return False
        
        return True
    
    def use_ability(self, pokemon: PokemonCard) -> bool:
        '''
        '''
        if not self.can_use_ability(pokemon):
            return False
        
        effect_function = EFFECTS_DICT.get(pokemon.ability.effect_id)

        if effect_function is not None:
            effect_function(self, pokemon)

        pokemon.ability.used = True

        return True
    
    def can_use_stadium(self, game: Game) -> bool:
        '''
        '''
        if game.stadium is None:
            return False
        
        if game.stadium.once_per_turn and game.stadium.used:
            return False

        return True
    
    def use_stadium(self, game: Game) -> bool:
        '''
        '''
        if not self.can_use_stadium(game):
            return False
        
        effect_function = EFFECTS_DICT.get(game.stadium.effect_id)

        if effect_function is not None:
            effect_function(self)

        game.stadium.used = True

        return True
    
    def get_legal_actions(self, game: Game) -> list[dict[str, str | Card]]:
        '''
        '''
        legal_actions = []
        pokemon_in_play = self.get_all_pokemon_in_play()

        for card in [self.active] + self.bench + self.hand:
            if isinstance(card, PokemonCard):
                for pokemon in pokemon_in_play:
                    if self.can_retreat_active(pokemon):
                        legal_actions.append({
                            'action': 'retreat_active',
                            'pokemon': pokemon
                        })
                    if self.can_use_ability(pokemon):
                        legal_actions.append({
                            'action': 'use_ability',
                            'pokemon': pokemon
                        })
                    for pokemon2 in pokemon_in_play:
                        if self.can_evolve_pokemon(pokemon, pokemon2):
                            legal_actions.append({
                                'action': 'evolve_pokemon',
                                'pre_evo': pokemon,
                                'evo_pokemon': pokemon2
                            })
            if isinstance(card, TrainerCard):
                if pokemon in pokemon_in_play:
                    if self.can_play_trainer(card, pokemon):
                        legal_actions.append({
                            'action': 'play_trainer',
                            'card': card,
                            'pokemon': pokemon
                        })
                else:
                    if self.can_play_trainer(card):
                        legal_actions.append({
                            'action': 'play_trainer',
                            'card': card,
                            'pokemon': None
                        })

            if isinstance(card, EnergyCard):
                for pokemon in pokemon_in_play:
                    if self.can_attach_energy(pokemon, card):
                        legal_actions.append({
                            'action': 'attach_energy',
                            'pokemon': pokemon,
                            'energy': card
                        })
            if self.can_use_stadium(game):
                legal_actions.append({
                    'action': 'use_stadium',
                    'game': game
                })
    
    # Action phase subsequent actions

    def take_prize(self, amount: int = 1) -> bool:
        '''
        '''
        if not self.prizes:
            return False
        
        for _ in range(amount):
            card = self.prizes.pop(0)
            self.hand.append(card)

        return True
    
    def can_bench_to_active(self, pokemon: PokemonCard) -> bool:
        '''
        '''
        if self.bench is None:
            return False
        
        if pokemon not in self.bench:
            return False
        
        return True
    
    def bench_to_active(self, pokemon: PokemonCard) -> bool:
        '''
        '''
        if not self.can_bench_to_active(pokemon):
            return False
        
        temp = self.active
        self.active = pokemon
        self.bench.remove(pokemon)
        self.bench.append(temp)

        return True
    
    def can_bench_to_active_no_active(self, pokemon: PokemonCard) -> bool:
        '''
        '''
        if self.active is not None:
            return False
        
        if pokemon not in self.bench:
            return False
        
        return True
    
    def bench_to_active_no_active(self, pokemon: PokemonCard) -> bool:
        '''
        '''
        if not self.can_bench_to_active_no_active(pokemon):
            return False
        
        self.active = pokemon
        self.bench.remove(pokemon)

        return True
    
    def check_knockout(self) -> bool:
        '''
        '''
        if self.active is not None:
            return False
        
        if self.active.damage >= self.active.hp:
            return True
        
        return False
    
    # Attack phase

    # Accessor Functions
    def get_active(self) -> list[PokemonCard]:
        '''
        '''
        return [self.active]
    
    def get_bench(self) -> list[PokemonCard]:
        '''
        '''
        return self.bench

    def get_all_pokemon_in_play(self) -> list[PokemonCard]:
        '''
        '''
        active = self.get_active()
        bench = self.get_bench()

        if not active and not bench:
            return []
        
        if not active:
            return self.bench
        
        if not bench:
            return [self.active]
        
        return [self.active] + self.bench
    
    def get_pokemon_in_hand(self) -> list[PokemonCard]:
        '''
        '''
        pokemon = []
        for card in self.hand:
            if isinstance(card, PokemonCard):
                pokemon.append(card)

        return pokemon
