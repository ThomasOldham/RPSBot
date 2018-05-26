#Coin Flip Function
#will output heads or tails at random when function is called

import discord
from discord.ext import commands
import math
import random
from random import randint

class coinFlip:
    def __init__(self, bot):
        self.bot = bot

    # coin flip command
    @commands.command()
    async def coin_flip(self, ctx):       
        x = random.randint(0, 1)
        headsOrTails = ""
        if x == 1:
            headsOrTails = "tails"
        else:
            headsOrTails = "heads"
        await ctx.send(headsOrTails)

# add this cog to the bot
def setup(bot):
    bot.add_cog(coinFlip(bot))
