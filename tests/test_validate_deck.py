import pandas as pd
from src.validate_deck import *

# run "python -m tests.test_validate_deck" in root file to view tests

check1 = check_deck('data/test_data/validate_deck/59_card_deck.csv')
print(check1, '\n')

check2 = check_deck('data/test_data/validate_deck/no_basic_deck.csv')
print(check2, '\n')

check3 = check_deck('data/test_data/validate_deck/5_count_deck.csv')
print(check3, '\n')