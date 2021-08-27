import re
import discord
import random
import logging

from utils import get_modified_num, get_moves, get_cap, get_move
from language_handler import get_translation
from config_interactions import get_raw_lang, get_dicedisplay
from playbook_interactions import get_character_ctx
from constants import LABELS, CONDITIONS, VALUE, dice, modifier_emojis

def parse (ctx, move, modifier=0):
 #   print (ctx)
    move_data = get_move(move)
 #   print (move_data)
 #   character = get_character_ctx(ctx)
    character = None
 #DISABLED FOR NOW UNTIL WE NEED CHARACTERS ###REENABLE ME
    embed=discord.Embed(title=f"{move_data['capital']}", colour=5450873)
    embed.set_footer(text=" ")
    embed.set_author(name=f"{ctx.author.name} {move_data['phrase']}")
    #embed.set_thumbnail(url=move_data['img']) this is the default aang logo
    embed.set_thumbnail(url=ctx.author.avatar_url) #use their logo instead!
    lang ='en'
    desc = get_translation(lang, 'description')
    embed.add_field(name=desc, value=f"{move_data['blob']}")
    addendum = None
    if move_data['requiresRolling']:
        addendum = handle_roll(character, embed, modifier, lang, ctx, move_data)
#       embed.set_footer(text=" ")
#       embed.set_author(name=f"{user} {phrase}")
        dicedisplay = True

        if dicedisplay:
            return embed, addendum
    return embed, ''

def handle_roll(character, embed, modifier, lang, ctx, move_data):
    #character = get_character(message) #get it higher up instead
    character_label = ''
    character_condition = ''
    char_mod = 0
    command_mod = ''

    if character:
        user = character['characterName']
        (char_mod, character_condition, character_label) = get_modifier_from_character(character[LABELS], character[CONDITIONS], move_data['label'], move_data['condition'], user, lang)
#        logger.info("Accessing " + character['characterName'])
    num_calc = get_modified_num(modifier)
    command_mod = num_calc #before the character mod is applied but after it's capped
    num_calc = get_cap(num_calc + char_mod)
    return add_result(embed, num_calc, modifier, lang, character_label, character_condition, command_mod)

def add_result (embed, num_calc, modifier, lang, character_label, character_condition, command_mod):
    """
    Rolls dice, mutates embed with result, returns emoji
    corresponding to the dice components of the result.
    """
    #do dice rolling
    result1 = random.randrange(1,7) ##first d6
    result2 = random.randrange(1,7) ##second d6
    die1 = get_die(result1)
    die2 = get_die(result2)
    mod_emoji = get_mod_emoji(num_calc)
    result_tot = result1 + result2 + num_calc

    if modifier > 0:
        modifier_to_show = ''
    else:
        modifier_to_show = f' {modifier}'

    calculation_title = get_translation(lang, 'dice_rolling.calculation_title')

    calculation = get_translation(lang, 'dice_rolling.calculation')(result1, result2, modifier_to_show, num_calc)
    #if character_condition: calculation = character_condition + calculation
    #if character_label: calculation = character_label + calculation
    result = get_translation(lang, 'dice_rolling.result')
    if command_mod: calculation = get_translation(lang, 'dice_rolling.command_modifier')(command_mod) + calculation
    embed.add_field(name=calculation_title, value=calculation, inline=False)
    embed.add_field(name=result, value=f"**{result_tot}**")

    return die1 + " " + die2 + " " + mod_emoji

def get_die (result):
    """
    Just does some sweet emoji lookups in the dictionary
    :param result: is the side of a 6 sided die you're looking for
    :return: is the id of the relevant emoji
    """
    for d in dice:
        if d[0] == result:
            emoji = f'<:{d[1]}:{d[2]}>'
    return emoji

def get_mod_emoji(mod_num):
    """
    :param mod_num: result form earlier command, lookup after being limited by cap and floor
    :return: modifier emoji
    """
    mod_emoji = ''
    for e in modifier_emojis:
        if e[0] == mod_num:
            mod_emoji = f'<:{e[1]}:{e[2]}>'
    return mod_emoji
