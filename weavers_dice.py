"""
weavers_dice.py - A Willie module for Weaver Dice
Copyright 2014, Gundor Gepein
Licensed under the GPL3.

Weaver Dice copyright 2013-2014, Wildbow
"""

import creation, triggers
from oauth2client.client import SignedJwtAssertionCredentials
import gspread
import willie

def tarot(factory):
    def outer(fn):
        def inner(bot, trigger):
            if trigger.group(2):
                i = int(trigger.group(2))
                if( i in range(1,23) ):
                    card = factory(i)
                else:
                    bot.reply("Invalid number!")
                    card = None
            else:
                card = factory()
            fn(bot, card)
        return inner
    return outer

def card_reply(bot, card):
    for line in str(card).split("\n"):
        if len(line) > 0 :
            bot.reply(line)

@willie.module.commands('luck','luckroll','character','char')
def character(bot, trigger):
    """
Generates the Tarot cards (advantages / disadvantages) for a Weaver Dice 
Character
    """
    for card in creation.character():
        card_reply(bot, card)

@willie.module.commands('advantage','adv')
@tarot(creation.advantage)
def advantage(bot, card):
    """
Prints the saved description of an advantage or generates one randomly
    """
    card_reply(bot, card)

@willie.module.commands('life_disadvantage','disadvantage_life','life_issue')
@tarot(creation.disadvantage_life)
def disadvantage_life(bot, card):
    """
Prints the saved description of a life disadvantage or generates one randomly
    """
    card_reply(bot, card)

@willie.module.commands('powers_disadvantage','disadvantage_powers','powers_issue')
@tarot(creation.disadvantage_powers)
def disadvantage_powers(bot, card):
    """
Prints the saved description of a powers disadvantage or generates one randomly
    """
    card_reply(bot, card)

@willie.module.commands('trigger','trigger_event')
def trigger_event(bot, trigger):
    """
Prints a trigger event from the sheet, either by number or randomly
    """
    if trigger.group(2):
        n = int(trigger.group(2))
    else:
        n = None
    cred = SignedJwtAssertionCredentials(
        bot.config.weavers_dice.google_service_account_name,
        google_private_key,
        ['https://www.googleapis.com/auth/drive','https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds'],
        bot.config.weavers_dice.google_private_key_password,
        "willie/"+willie.__version__)
    gc = gspread.authorize(cred)
    ts = triggers.TriggerSheet(gc, key=bot.config.weavers_dice.trigger_events_sheet)
    try:
        bot.msg( trigger.sender, ("%s: %s" %( trigger.nick, ts.event(n) )), 3 )
    except IndexError as e:
        bot.reply( e )

def setup(bot):
    global google_private_key
    pk_fn = bot.config.weavers_dice.google_private_key_file
    pk_file = open(pk_fn,'r')
    google_private_key = pk_file.read()
