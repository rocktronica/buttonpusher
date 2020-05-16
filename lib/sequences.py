REDEEM_NOOK_MILES_SEQUENCE = [
    2.5, # Wait for menu and select item
    3, # Redeem ...?
    .75, # Confirm
    8, # Wait for item and receive
    2.5, # click through explanation
    4.5, # put item away and make another selection
    .75, # confirm dialog
]
CRAFT_SEQUENCE = [
    3, # Wait for menu and select item
    .75, # Craft it!
    .75, # Confirm
    7, # Make item and receive it
    .75, # Keep crafting
]
WISH_ON_A_STAR_SEQUENCE = [
    1.5, # Wish on a possible star
]
DEBUG_SEQUENCE = [
    1, # Debug
]

SEQUENCES = [
    {"text": "Redeem Nook Miles", "value": REDEEM_NOOK_MILES_SEQUENCE},
    {"text": "Craft item", "value": CRAFT_SEQUENCE},
    {"text": "Wish on a star", "value": WISH_ON_A_STAR_SEQUENCE},
    {"text": "Debug", "value": DEBUG_SEQUENCE},
]
