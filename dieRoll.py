import discord
from discord.ext import commands
import math
import random
from random import randint

class dieRoll:
    def __init__(self, bot):
        self.bot = bot

    # die roll command
    @commands.command()
    async def die_roll(self, ctx):
        try:
            await ctx.send("You selected 'die_roll' ! How many sides is your die?")
            await ctx.send("Please enter any positive integer.")
            sides = ctx.message.content.split(" ")
            await ctx.send(sides)
            index = int(sides[1])
            x = random.randint(1, index)
            await ctx.send("Rolling...")
            await ctx.send(x)
        except Exception:
            await ctx.send("Error! Please enter a positive integer!")

# add this cog to the bot
def setup(bot):
    bot.add_cog(dieRoll(bot))
