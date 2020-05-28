WISH_ON_STAR_INTERVAL = 1.5

SEQUENCES = [
    {
        "text": "Craft Item",
        "value": [
            3,  # Wait for menu and select item
            1,  # Craft it!
            1,  # Confirm
            7,  # Make item and receive it
            1,  # Keep crafting
        ],
    },
    {
        "text": "Bell Voucher",
        "value": [
            2.5,  # Wait for menu and select item
            3,  # Redeem ...?
            1,  # Confirm
            8,  # Wait for item and receive
            2.5,  # click through explanation
            4.5,  # put item away and make another selection
            1,  # confirm dialog
        ],
    },
    {
        "text": "Wish on Stars 1m",
        "value": [WISH_ON_STAR_INTERVAL] * int(60 / WISH_ON_STAR_INTERVAL),
    },
    {"text": "Debug", "value": [1,]},  # Debug
]
