import pandas as pd

# Deck Rules
# - Exactly 60 cards
# - No more than 4 copies of cards with the same name
# - Must contain atleast 1 basic pokemon
# - Energy cards are not limited to 4
#   - Special energy cards are limited to 4 

LEGAL_CARDS = pd.read_csv('data/final_legal_card_list.csv')
LEGAL_CARDS = LEGAL_CARDS[['Card ID', 'Stage (Pokémon)/Type (Energy and Trainer)']]

def load_deck(deck_path: str) -> pd.DataFrame:
    '''
    '''
    deck = pd.read_csv(deck_path, header = None)

    deck.columns = ['Card ID']

    return deck

def load_deck_info(deck_path: str) -> pd.DataFrame:
    '''
    '''

    deck = load_deck(deck_path)

    deck = deck.merge(LEGAL_CARDS, on = 'Card ID', how = 'left')

    deck['count'] = deck.groupby('Card ID').transform('size')

    deck = deck.drop_duplicates()

    return deck

def check_deck(deck_path: str) -> tuple[pd.DataFrame, bool]:
    '''
    '''
    is_legal = True

    deck = load_deck_info(deck_path)

    deck_no_energy = deck[deck['Stage (Pokémon)/Type (Energy and Trainer)'] != 'Basic Energy']
    if deck['count'].sum() != 60:
        print('Invalid Deck: Deck does not have exactly 60 cards')
        is_legal = False
    
    exceeds_per_card_limit = (deck_no_energy['count'] > 4).any()
    if exceeds_per_card_limit:
        print('Invalid Deck: Deck contains more the 4 copies of a single card')
        is_legal = False
    
    contain_basic = (deck_no_energy['Stage (Pokémon)/Type (Energy and Trainer)'] == 'Basic Pokémon').any()
    if not contain_basic:
        print('Invalid Deck: Deck does not contain any basic pokemon')
        is_legal = False
    
    return (deck, is_legal)
    

