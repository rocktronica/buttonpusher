REDEEM_NOOK_MILES_SEQUENCE = [
    {
        "seconds": 2.5,
        "description": 'Wait for menu and select item',
    },
    {
        "seconds": 3,
        "description": 'Redeem ...?',
    },
    {
        "seconds": .75,
        "description": 'Confirm',
    },
    {
        "seconds": 8,
        "description": 'Wait for item and receive',
    },
    {
        "seconds": 2.5,
        "description": 'click through explanation',
    },
    {
        "seconds": 4.5,
        "description": 'put item away and make another selection',
    },
    {
        "seconds": .75,
        "description": 'confirm dialog',
    },
]
CRAFT_SEQUENCE = [
    {
        "seconds": 3,
        "description": 'Wait for menu and select item'
    },
    {
        "seconds": .75,
        "description": 'Craft it!'
    },
    {
        "seconds": .75,
        "description": 'Confirm'
    },
    {
        "seconds": 7,
        "description": 'Make item and receive it'
    },
    {
        "seconds": .75,
        "description": 'Keep crafting'
    },
]
WISH_ON_A_STAR_SEQUENCE = [
    {
        "seconds": 1.5,
        "description": 'Wish on a possible star'
    },
]
DEBUG_SEQUENCE = [
    {
        "seconds": 1,
        "description": 'Debug'
    },
]

SEQUENCES = [
    {"text": "Redeem Nook Miles", "value": REDEEM_NOOK_MILES_SEQUENCE},
    {"text": "Craft item", "value": CRAFT_SEQUENCE},
    {"text": "Wish on a star", "value": WISH_ON_A_STAR_SEQUENCE},
    {"text": "Debug", "value": DEBUG_SEQUENCE},
]
