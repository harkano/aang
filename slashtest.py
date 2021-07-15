"""
Copyright (C) 2021  Koviubi56
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import logging
import discord
#from traceback import print_exc
from discord_slash import context
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_button, create_actionrow

TOKEN = "ODY0MjQ1MTYzMDM1MDY2MzY4.YOypBw.Vql8DEqizKaztR7kSn3SAunA2m4"

logging.basicConfig(level=21,
                    format="[%(levelname)s %(name)s] %(message)s")
logging = logging.getLogger(__name__)
print("Loading...")


def log(msg: str) -> None:
    logging.log(21, msg)


def my_loading(msg: str) -> None:
    log(f"[LOAD] {msg}")


my_loading("Importing...")


my_loading("Settings...")

# ** SETTINGS **
# Import and use "dotenv"? Defaults to True
useDotenv = True
# ** SETTINGS **

my_loading("Settings: useDotenv...")

if useDotenv:
    from dotenv import load_dotenv
    load_dotenv()

my_loading("Creating client...")
client = discord.Client()
# Declares slash commands through the client.
my_loading("Creating slash...")
slash = SlashCommand(client, sync_commands=True)

my_loading("Making on_ready...")


@client.event
async def on_ready():
    print("Ready!")

my_loading("Making the poll command...")


@slash.slash(name="poll",
             description="Create a poll",
             options=[
                 create_option(
                     name="question",
                     description="What is your question?",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="showchoicesonbuttons",
                     description="Show the choice on buttons?",
                     option_type=5,
                     required=True
                 ),
                 create_option(
                     name="choice1",
                     description="The first choice. Please, do NOT use brackets!",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="choice2",
                     description="The second choice. Please, do NOT use brackets!",
                     option_type=3,
                     required=True
                 )
             ])
async def poll(ctx: context.SlashContext, question: str,
               showchoicesonbuttons: bool, choice1: str,
               choice2: str) -> None:
    """
    Creates a poll
    Args:
        ctx (discord_slash.context.SlashContext): The context
        question (str): The question
        showchoicesonbuttons (bool): Show choices on buttons?
        choice1 (str): The first choice
        choice2 (str): The second choice
    """
    log("Checking for ()...")
    if choice1.find("(") != -1 or choice1.find(")") != -1:
        await ctx.send("**ERROR!** Please, do NOT use brackets!")
        return
    if choice2.find("(") != -1 or choice2.find(")") != -1:
        await ctx.send("**ERROR!** Please, do NOT use brackets!")
        return
    log("Creating a poll...")
    # 🇦
    # 🇧
    pollEmbed = discord.Embed(
        title=question,
        description=f"\"{choice1}\" or \"{choice2}\"" if showchoicesonbuttons else f":regional_indicator_a: {choice1} \n:regional_indicator_b: {choice2}",
        # BringBackBlurple
        color=0x7289DA
    )

    buttons = [
        create_button(
            style=2,
            label=str(x) + " (0)",
            custom_id=str(y)
        )
        for y, x in enumerate([choice1, choice2], 1)
    ] if showchoicesonbuttons else [
        create_button(
            style=2,
            label="(0)",
            custom_id=str(y),
            emoji=x
        )
        for y, x in enumerate(["🇦", "🇧"], 1)
    ]
    pollComponents = [create_actionrow(*buttons)]
    log("Sending...")
    try:
        await ctx.send(embed=pollEmbed, components=pollComponents)
    except Exception:
        try:
            log("Error!")
            print_exc()
            log("Plan B...")
            await ctx.channel.send(embed=pollEmbed, components=pollComponents)
        except Exception:
            logging.error("Something went wrong! Infos:")
            print_exc()

my_loading("Making on_button_click...")


@client.event
async def on_component(ctx: context.ComponentContext):
    log("*Click*")
    myMsg = ctx.origin_message
    # mmt = My Message Things
    mmt = {
        "embed": myMsg.embeds[0],
        "comp": myMsg.components
    }

    # indexes are starting from 0
    # 1 2 3 4
    # * -1  *
    # 0 1 2 3
    myNum = ""
    good = False
    for j in ctx.component["label"]:
        if good and j == ")":
            good = False
        if good:
            myNum += j
        else:
            if j == "(":
                good = True
    myNum2 = int(myNum) + 1

    myNum3 = ""
    good = False
    id = int(ctx.custom_id) - 1
    if ctx.component["label"].startswith("("):
        myNum3 = ""
    else:
        for i, j in enumerate(ctx.component["label"]):
            if ctx.component["label"][i + 1] == "(":
                break
            myNum3 += j
        myNum3 += " "
    mmt["comp"][0]["components"][id]["label"] = f"{myNum3}({myNum2})"

    await ctx.edit_origin(embed=mmt["embed"], components=mmt["comp"])

my_loading("Running client...")

client.run(TOKEN)