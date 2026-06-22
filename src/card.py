class Card:
    '''
    '''
    def __init__(self, 
                 card_id: int, 
                 card_name: str, 
                 card_type: str):
        '''
        '''
        self.card_id = card_id
        self.card_name = card_name
        self.card_type = card_type

class Attack:
    '''
    '''
    def __init__(self, 
                 name: str, 
                 damage: int = 0, 
                 cost: list[str] = None, 
                 effect: str = None):
        '''
        '''
        self.name = name
        self.damage = damage
        self.cost = cost if cost is not None else []
        self.effect = effect

        self.effect_id = None
        
class Ability:
    '''
    '''
    def __init__(self,
                 name: str,
                 effect: str,
                 once_per_turn: bool = False
                 ):
        '''
        '''
        self.name = name
        self.effect = effect
        self.once_per_turn = once_per_turn

        self.used = False
        self.effect_id = None
        

class PokemonCard(Card):
    '''
    '''
    def __init__(self, 
                 card_id: int, 
                 card_name: str, 
                 card_type: str,
                 pokemon_type: str,
                 hp: int,
                 stage: int, # Basic = 0, Stage 1 = 1, Stage 2 = 2
                 retreat_cost: int,
                 tera: bool = False,
                 ability: Ability = None,
                 attacks: list[Attack] = None,
                 weakness: str = None,
                 resistance: str = None,
                 ):
        '''
        '''
        super().__init__(card_id, card_name, card_type)
        self.pokemon_type = pokemon_type
        self.hp = hp
        self.stage = stage
        self.tera = tera 
        self.ability = ability 
        self.attacks = attacks if attacks is not None else []
        self.weakness = weakness
        self.resistance = resistance
        self.retreat_cost = retreat_cost

        self.damage = 0
        self.attached_energy = []
        self.tool = None
        self.status_cond = False

class TrainerCard(Card):
    '''
    '''
    def __init__(self, 
                 card_id: int, 
                 card_name: str, 
                 card_type: str,
                 trainer_type: str, 
                 effect: str):
        '''
        '''
        super().__init__(card_id, card_name, card_type)
        self.trainer_type = trainer_type
        self.effect = effect
        self.effect_id = None

class EnergyCard(Card):
    '''
    '''
    def __init__(self, 
                 card_id: int, 
                 card_name: str, 
                 card_type: str,
                 energy_type: str):
        '''
        '''
        super().__init__(card_id, card_name, card_type)
        self.energy_type = energy_type

        