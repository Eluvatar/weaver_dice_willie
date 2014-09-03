"""
weavers_dice.py - A Willie module for Weaver's Dice
Copyright 2014, Gundor Gepein
Licensed under the GPL3.

Weaver's Dice copyright 2013-2014, Wildbow
"""

import creation
import willie

@willie.module.commands('luck','luckroll','character','char')
def character(bot, trigger):
    """
Generates the Tarot cards (advantages / disadvantages) for a Weaver's Dice 
Character
    """
    for card in creation.character():
        for line in str(card).split("\n"):
            if len(line) > 0 :
                bot.reply(line)
