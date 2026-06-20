import pandas as pd

CARDS = pd.read_csv('data/EN_Card_Data.csv')

slot1 = CARDS.groupby('Card ID').nth(0)
slot2 = CARDS.groupby('Card ID').nth(1)
slot3 = CARDS.groupby('Card ID').nth(2)

slot2 = slot2[['Card ID', 'Move Name' , 'Cost', 'Damage', 'Effect Explanation']]
slot3 = slot3[['Card ID', 'Move Name' , 'Cost', 'Damage', 'Effect Explanation']]

slot1 = slot1.rename(columns = {
    'Move Name': 'slot1_name',
    'Cost': 'slot1_cost',
    'Damage': 'slot1_dmg',
    'Effect Explanation': 'slot1_effect'
})
slot2 = slot2.rename(columns = {
    'Move Name': 'slot2_name',
    'Cost': 'slot2_cost',
    'Damage': 'slot2_dmg',
    'Effect Explanation': 'slot2_effect'
})
slot3 = slot3.rename(columns = {
    'Move Name': 'slot3_name',
    'Cost': 'slot3_cost',
    'Damage': 'slot3_dmg',
    'Effect Explanation': 'slot3_effect'
})

final_card_list = slot1.merge(slot2, on = 'Card ID', how = 'left')
final_card_list = final_card_list.merge(slot3, on = 'Card ID', how = 'left')

final_card_list.to_csv('data/final_legal_card_list.csv', index = False)
