"""
Common emoji code.
"""

import emoji

EMOJIS = set(emoji.emojize(emoji_code) for emoji_code in emoji.get_emoji_unicode_dict("en").values())

def is_emoji(c):
    return c in EMOJIS
