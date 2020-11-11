import discord
from numpy.random import choice

from discord.ext import commands

class decide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whatpvmshallwedo(self, ctx):
        await ctx.send(choice(
            ['Solak', 'Vorago', 'AoD', 'ED1', 'ED2', 'ED3', 'RotS', 'Raids', 'w54'],
            p=[.30, .25, .01, .08, .08, .08, .01, .10, .09 ]
            ))
        
def setup(bot):
    bot.add_cog(decide(bot))
