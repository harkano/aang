# bot.py
from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Client(intents=Intents.default())
slash = SlashCommand(bot)

bot.load_extension("cog")
bot.run(TOKEN)

# cog.py
from discord import Embed
from discord_slash import cog_ext, SlashContext


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="Embed Test")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Slash(bot))