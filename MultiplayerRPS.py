import discord
from discord.ext import commands
import math

DEBUG = True

CHALLENGE_USAGE = "Usage: >>challenge [user] [choice]"
ACCEPT_USAGE = "Usage: >>accept [user] [choice]"

WIN = {"rock":"scissors", "paper":"rock", "scissors":"paper"}
OPTIONS = ["rock", "paper", "scissors"]

class Challenge:

    challenger = None
    challengee = None

    def __init__(self, challenger, challengee, bot):
        self.challenger = normalize(str(challenger), bot)
        self.challengee = normalize(str(challengee), bot)
        if DEBUG:
            print("Constructing challenge:", \
                  self.challenger, "vs", self.challengee)

    def __hash__(self):
        return len(str(self.challenger))

    def __eq__(self, other):
        return self.challenger == other.challenger \
               and self.challengee == other.challengee

    def __ne__(self, other):
        return not __eq__(other)

def normalize(user, bot):
    if user[-1] == ">":
        if DEBUG:
            if DEBUG:
                for member in bot.get_all_members():
                    print(member.id)
            try:
                for member in bot.get_all_members():
                    if int(user[2:-1]) == member.id:
                        user = str(member)
                        break
            except Exception:
                pass
    return user

class MultiplayerRPSCog:

    challenges = None
    bot = None
    
    def __init__(self, bot):
        self.challenges = {}
        self.bot = bot

    @commands.command()
    async def challenge(self, ctx):
        challenger = str(ctx.message.author)
        challengee = None
        choice = None
        try:
            message_split = ctx.message.content.split(' ')
            challengee = message_split[1]
            choice = message_split[2]
        except IndexError:
            await ctx.send(CHALLENGE_USAGE)
        if challengee != None:
            if Challenge(challenger, challengee, self.bot) \
               in self.challenges.keys():
                await ctx.send("You have already challenged " + challengee)
            elif Challenge(challenger, challengee, self.bot) \
                 in self.challenges.keys():
                await ctx.send(challengee + " has already challenged you.")
            else:
                if choice in OPTIONS:
                    self.challenges[Challenge(challenger, challengee, self.bot)] \
                                                          = choice
                    await ctx.send("Awaiting response from " + challengee)
                    if DEBUG:
                        print(challenger, "has challenged", challengee)
                else:
                    await ctx.send("You can't choose " + choice + ". Cheater.")

    @commands.command()
    async def accept(self, ctx):
        challengee = str(ctx.message.author)
        challenger = None
        choice = None
        try:
            message_split = ctx.message.content.split(' ')
            challenger = message_split[1]
            choice = message_split[2]
        except IndexError:
            await ctx.send(ACCEPT_USAGE)
        if challenger != None:
            if Challenge(challenger, challengee, self.bot) \
               in self.challenges.keys():
                challenger_choice = self.challenges[ \
                    Challenge(challenger, challengee, self.bot)]
                if choice in OPTIONS:
                    winner = challenger
                    if challenger_choice == WIN[choice]:
                        winner = challengee
                    elif challenger_choice == choice:
                        winner = None
                    winner_message = None
                    if winner == None:
                        winner_message = "It's a tie!"
                    else:
                        winner_message = winner + " wins!"
                    await ctx.send(challenger + " chose " + challenger_choice \
                                   + ". " + challengee + " chose " + choice \
                                   + ". " + winner_message)
                    del(self.challenges[Challenge(challenger, challengee, \
                                                  self.bot)])
                else:
                    await ctx.send("You can't choose " + choice + ". Cheater.")
            else:
                await ctx.send(challenger + " has not challenged you.")

    @commands.command()
    async def challengers(self, ctx):
        if DEBUG:
            print(ctx.message.author.name + " is checking challengers.")
        output = "You have been challenged by these users:"
        for challenge in self.challenges.keys():
            if challenge.challengee == str(ctx.message.author):
                output += "\n" + challenge.challenger
        await ctx.send(output)

    @commands.command()
    async def clear(self, ctx):
        self.challenges.clear()
        await ctx.send("Deleted all pending challenges.")

def setup(bot):
    bot.add_cog(MultiplayerRPSCog(bot))
