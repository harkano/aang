import os
import requests
import discord
from discord.ext import commands
from discord import guild
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

from dotenv import load_dotenv

from slash_parse import parse

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

buttons = [
        create_button(
            style=ButtonStyle.gray,
            label="Mark Fatigue"
        ),
        ]
from utils import get_moves
json_array = get_moves('en')

action_row = create_actionrow(*buttons)

@slash.slash(
    name="move",
    description="Use a move",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='move', description="Select core move", required=True, option_type=4, choices= [
            create_choice(name="Assess a situation", value=6),
            create_choice(name="Push your luck in a risky situation", value=12),
            create_choice(name="Rely on your skills and training", value=11),
            create_choice(name="Intimidate an NPC into backing off or giving in", value=8),
            create_choice(name="Trick an NPC", value=10),
            create_choice(name="Comfort or support another person", value=13),
            create_choice(name="Plead with an NPC who cares what you think", value=7),
            create_choice(name="Another move", value=9)]),
        create_option(name='modifier', description="What modifier are we adding to the dice roll?", required=False, option_type=4, choices= [
            create_choice(name='+4', value=4),
            create_choice(name='+3', value=3),
            create_choice(name='+2', value=2),
            create_choice(name='+1', value=1),
            create_choice(name='0', value=0),
            create_choice(name='-1', value=-1),
            create_choice(name='-2', value=-2),
            create_choice(name='-3', value=-3),
        ])
    ]
    )
async def move(ctx, move:str, modifier:int=0):
    embed, addendum = parse(ctx, move, modifier)
    await ctx.send(embed=embed, content=addendum)

@slash.slash(
    name="fight",
    description="Make a combat approach",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='move', description="Select core move", required=True, option_type=4, choices= [
            create_choice(name="Defend & Respond", value=17),
            create_choice(name="Advance & Attack", value=19),
            create_choice(name="Evade & Observe", value=18)]),
        create_option(name='modifier', description="What modifier are we adding to the dice roll?", required=False, option_type=4, choices= [
            create_choice(name='+4', value=4),
            create_choice(name='+3', value=3),
            create_choice(name='+2', value=2),
            create_choice(name='+1', value=1),
            create_choice(name='0', value=0),
            create_choice(name='-1', value=-1),
            create_choice(name='-2', value=-2),
            create_choice(name='-3', value=-3),
        ])
    ]
)
async def fight(ctx, move:str, modifier:int=0):
    embed, addendum = parse(ctx, move, modifier)
    await ctx.send(embed=embed, content=addendum)

@slash.slash(
    name="balance",
    description="Balance Moves",
    #guild_ids=[696999350726819931],
    options=[
        create_option(name='move', description="Select core move", required=True, option_type=4, choices= [
            create_choice(name="Live up to your principle", value=2),
            create_choice(name="Call someone out", value=3),
            create_choice(name="Deny a Callout", value=4),
            create_choice(name="Resist Shifting Your Balance", value=1),
            create_choice(name="Lose your balance", value=5)]),
        create_option(name='modifier', description="What modifier are we adding to the dice roll?", required=False, option_type=4, choices= [
            create_choice(name='+4', value=4),
            create_choice(name='+3', value=3),
            create_choice(name='+2', value=2),
            create_choice(name='+1', value=1),
            create_choice(name='0', value=0),
            create_choice(name='-1', value=-1),
            create_choice(name='-2', value=-2),
            create_choice(name='-3', value=-3),
        ])
    ]
)
async def balance(ctx, move:str, modifier:int=0):
    embed, addendum = parse(ctx, move, modifier)
    await ctx.send(embed=embed, content=addendum)





client.run(TOKEN)