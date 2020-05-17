SEQUENCES = [
    {"text": "Bell Voucher", "value": [
        2.5, # Wait for menu and select item
        3, # Redeem ...?
        .75, # Confirm
        8, # Wait for item and receive
        2.5, # click through explanation
        4.5, # put item away and make another selection
        .75, # confirm dialog
    ]},
    {"text": "Craft Item", "value": [
        3, # Wait for menu and select item
        .75, # Craft it!
        .75, # Confirm
        7, # Make item and receive it
        .75, # Keep crafting
    ]},
    {"text": "Wish on Stars", "value": [
        1.5, # Wish on a possible star
    ]},
    {"text": "Debug", "value": [
        1, # Debug
    ]},
]
