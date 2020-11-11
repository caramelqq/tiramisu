import random
import binomial_calc

from discord.ext import commands

class probabilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def telosdrops(self, ctx, *args : str):
        """Calculates Telos unique drop chance given streak and enrage"""
        streak = 0
        enrage = 0
        lotd = 0

        try: 
            if len(args) < 2 or len(args) > 3:
                raise

            for s in args:
                if len(s) > 5:
                    raise

            if args[0] == '-l':
                lotd = 25
                streak = int(args[2])
                enrage = int(args[1])
                with_lotd = " with LoTD"
            else:
                lotd = 0
                streak = int(args[1])
                enrage = int(args[0])
                with_lotd = ""

            if streak > 201 or streak < 0:
                raise
            if enrage < 0 or enrage > 4000:
                raise

            denom = int((10000/(10 + 0.25*(enrage + lotd) + 3*streak)) // 1)
            if enrage < 100:
                denom *= 10
            if enrage < 25:
                denom *= 3

            await ctx.send("Chance of a Telos unique at **" + str(enrage) + "%** enrage and a **" + str(streak) + "** killstreak" + with_lotd + ": 1/**" + str(denom) + "**")
            return

        except Exception:
            await ctx.send("Usage:```telosdrops [-l <LotD>] enrage <[0, 4000]> streak <[0, 200]>```")
            return

    @commands.command()
    async def petchance(self, ctx, *args):
        """Calculates petchance"""
        #arg1 : pet, arg2 : kc, [arg3 : drops per kill (dpk)]
        args = ctx.message.content.split(' ')
        personal_message = ""

        try: 
            if not args: 
                raise
            if int(args[2]) < 0:
                raise

            # Local vars - chance : % chance, pet names
            chance = 0
            pet_names = ''

        except Exception:
            await ctx.send("Usage:```vitalis|gwd1|gwd2 <killcount >= 0 > [0 <= drops per kill <= 5]```")
            return

        if args[1] == 'vitalis':
            # Try converting args[3] (drops per kill) to int
            try:
                # vars: drops per kill, killcount
                dpk = float(args[3])
                kc = int(args[2])
                if dpk < 1 or dpk > 5:
                    raise
            except Exception:
                await ctx.send("Usage:```vitalis <killcount >= 0 > [0 <= drops per kill <= 5]```")
                return

            s = 's'
            # Variables : Threshold, drop rate denominator 
            thresh = 1000
            drate_denom = 5000

            chance = binomial_calc.binomial_calc(thresh, kc, drate_denom, dpk)

            # Construct output string
            if dpk == 1:
                s = ''
            await ctx.send('{}\nAfter **{}** kills with **{}** drop{} per kill, **{:.2f}%** of people would have obtained **Vitalis**.'.format(personal_message,args[2],dpk,s,chance))
            return

        if args[1] == 'gwd1':
            # Variables : Threshold, killcount, drop rate denominator 
            thresh = 1000
            kc = int(args[2])
            drate_denom = 5000
            pet_names = 'a GWD1 pet'

            chance = binomial_calc.binomial_calc(thresh, kc, drate_denom)

        if args[1] == 'gwd2':
            # Variables : Threshold, killcount, drop rate denominator 
            thresh = 400
            kc = int(args[2])
            drate_denom = 2000
            pet_names = 'a GWD2 pet'

            chance = binomial_calc.binomial_calc(thresh, kc, drate_denom)

        await ctx.send('{}\nAfter **{}** kills, **{:.2f}%** of people would have obtained **{}**.'.format(personal_message,args[2],chance,pet_names))


def setup(bot):
    bot.add_cog(probabilities(bot))
