import urllib.request
import datetime

from discord.ext import commands
from cassandra.cluster import Cluster

class hiscore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.skill_names = 'Overall, Attack, Defence, Strength, Constitution, Ranged, Prayer, Magic, Cooking, Woodcutting, Fletching, Fishing, Firemaking, Crafting, Smithing, Mining, Herblore, Agility, Thieving, Slayer, Farming, Runecrafting, Hunter, Construction, Summoning, Dungeoneering, Divination, Invention, Archaeology'
        self.skill_names_arr = [x.strip() for x in self.skill_names.split(',')]
        self.cluster = Cluster(["172.31.10.41"])
        self.session = self.cluster.connect('tracker')
        self.arch_release_date = datetime.date(2020, 3, 30)

    async def validate_name(self, ctx, username):
        if not all((x.isalnum() or x.isspace()) for x in username):
            await ctx.send('Username not found.')
            return None

        username = ' '.join(username)

        if len(username) > 12 or len(username) == 0:
            await ctx.send('Username not found.')
            return None

        return username

    async def get_stats(self, ctx, ironman, username):
        username = username.replace(' ', '%20')
        if ironman == False:
            try:
                httpresponse_obj = urllib.request.urlopen("https://secure.runescape.com/m=hiscore/index_lite.ws?player=" + username)
            except:
                await ctx.send('Username \"' + username + '\" not found.')
                await ctx.send('Spaces break this for some reason')
                return None
        else:
            try:
                httpresponse_obj = urllib.request.urlopen("https://secure.runescape.com/m=hiscore_ironman/index_lite.ws?player=" + username)
            except:
                await ctx.send('Username \"' + username + '\" not found.')
                return None

        s = httpresponse_obj.read().decode("utf-8")
        return s.split('\n')

    @commands.command()
    async def stats(self, ctx, *args : str):
        """
        Get stats for a user
        """
        if not args:
            await ctx.send('Usage: ?stats [-i  <ironman>] *name*')
            return

        if args[0] == '-i':
            ironman = True
            title_label = 'Ironman stats: '
        else:
            ironman = False
            title_label = 'Overall stats: '

        username = await self.validate_name(ctx, args[ironman:])

        if not username:
            return

        s_arr = await self.get_stats(ctx, ironman, username)

        if not s_arr:
            return

        response = '```╔' + '═'*49 + '╗\n'
        response += '║' + '{:^49}'.format(title_label + username) + '║\n'
        response += '╠' + '═'*15 + '╦' + '═'*9 + '╦' + '═'*7 + '╦' + '═'*15 + '╣\n'
        response += '║' + '{:^15}'.format('Skill')
        response += '║' + '{:^9}'.format('Rank')
        response += '║' + '{:^7}'.format('Level') 
        response += '║' + '{:^15}'.format('Experience') + '║\n'
        response += '╠' + '═'*15 + '╬' + '═'*9 + '╬' + '═'*7 + '╬' + '═'*15 + '╣\n'

        for i in range(len(self.skill_names_arr)):
            x = s_arr[i].split(',')
            response += '║' + '{:<15}'.format(" " + self.skill_names_arr[i])
            response += '║' + '{:>9,d}'.format(int(x[0]))
            response += '║' + '{:>7,d}'.format(int(x[1])) 
            response += '║' + '{:>15,d}'.format(int(x[2])) + '║\n'
        response += '╚' + '═'*15 + '╩' + '═'*9 + '╩' + '═'*7 + '╩' + '═'*15 + '╝```'

        await ctx.send(response)

    @commands.command()
    async def gains(self, ctx, *args):
        """
        Show xp difference between the present and x days prior
        """
        if len(args) < 1 or len(args) > 20:
            await ctx.send('Usage: ```?gains username days\n0 <= days <= 365```')
            return
            
        try:
            days_ago = int(args[-1])
            if days_ago > 365 or days_ago < 0:
                raise Exception()
        except:
            await ctx.send('Usage: ```?gains username days\n0 <= days <= 365```')
            return

        username = await self.validate_name(ctx, args[:-1])

        if not username:
            return

        s_arr = await self.get_stats(ctx, False, username)

        if not s_arr:
            return

        today = datetime.date.today()
        prev_date = today - datetime.timedelta(days_ago)

        response = '```╔' + '═'*54 + '╗\n'
        response += '║' + '{:^54}'.format("XP Difference for: " + username) + '║\n'
        response += '╠' + '═'*13 + '╦' + '═'*13 + '╦' + '═'*13 + '╦' + '═'*12 + '╣\n'
        response += '║' + '{:^13}'.format('Skill')
        response += '║' + '{:^13}'.format(str(prev_date))
        response += '║' + '{:^13}'.format("Current")
        response += '║' + '{:^12}'.format('Δ') + '║\n'
        response += '╠' + '═'*13 + '╬' + '═'*13 + '╬' + '═'*13 + '╬' + '═'*12 + '╣\n'

        for i in range(len(self.skill_names_arr)):
            rows_old = self.session.execute('SELECT * FROM ' + self.skill_names_arr[i] + ' WHERE username=\'' + username + '\' AND time > \'' + str(prev_date) + ' 00:00:00-0000\' AND time < \'' + str(prev_date) + ' 23:59:59-0000\';')

            x = s_arr[i].split(',')

            if not rows_old:
                if self.skill_names_arr[i] == 'Archaeology' and prev_date < self.arch_release_date:
                    old_exp = 0
                else:
                    # print('Not found: ' + self.skill_names_arr[i])
                    await ctx.send('```No exp logged for ' + str(prev_date) + '```')
                    return
            else:
                old_exp = int(rows_old.one().exp)

            new_exp = int(x[2])
            response += '║' + '{:<13}'.format(self.skill_names_arr[i])
            response += '║' + '{:>13,d}'.format(old_exp)
            response += '║' + '{:>13,d}'.format(new_exp) 
            response += '║' + '{:>12,d}'.format(new_exp - old_exp) + '║\n'
        response += '╚' + '═'*13 + '╩' + '═'*13 + '╩' + '═'*13 + '╩' + '═'*12 + '╝```'

        await ctx.send(response)

    @commands.command()
    async def delta(self, ctx, *args):
        """
        Show xp differences between two dates
        """
        
        # Take in username, days OR username, new-date, old-date
        if len(args) < 3 or len(args) > 20:
            await ctx.send('Usage: ```?delta username new-date old-date\ndate is in mm/dd/yyyy format\nnew-date must be ahead of old-date```')
            return

        # Input validation - Username, dates
        username = await self.validate_name(ctx, args[:-2])
        if not username:
            return

        try:
            date_new_arr = [int(x) for x in args[-2].split('/')]
            date_old_arr = [int(x) for x in args[-1].split('/')]

            date_new = datetime.date(date_new_arr[2], date_new_arr[0], date_new_arr[1])
            date_old = datetime.date(date_old_arr[2], date_old_arr[0], date_old_arr[1])
            if date_new < date_old:
                raise Exception()
        except:
            await ctx.send('Usage: ```?delta username new-date old-date\ndate is in mm/dd/yyyy format\nnew-date must be ahead of old-date```')
            return

        response = '```╔' + '═'*54 + '╗\n'
        response += '║' + '{:^54}'.format("XP Difference for: " + username) + '║\n'
        response += '╠' + '═'*13 + '╦' + '═'*13 + '╦' + '═'*13 + '╦' + '═'*12 + '╣\n'
        response += '║' + '{:^13}'.format('Skill')
        response += '║' + '{:^13}'.format(args[-1])
        response += '║' + '{:^13}'.format(args[-2]) 
        response += '║' + '{:^12}'.format('Δ') + '║\n'
        response += '╠' + '═'*13 + '╬' + '═'*13 + '╬' + '═'*13 + '╬' + '═'*12 + '╣\n'

        for i in range(len(self.skill_names_arr)):
            rows_new = self.session.execute('SELECT * FROM ' + self.skill_names_arr[i] + ' WHERE username=\'' + username + '\' AND time > \'' + str(date_new) + ' 00:00:00-0000\' AND time < \'' + str(date_new) + ' 23:59:59-0000\';')
            rows_old = self.session.execute('SELECT * FROM ' + self.skill_names_arr[i] + ' WHERE username=\'' + username + '\' AND time > \'' + str(date_old) + ' 00:00:00-0000\' AND time < \'' + str(date_old) + ' 23:59:59-0000\';')

            if not rows_new:
                if i == len(self.skill_names_arr) - 1: #Archaeology
                    if date_new < self.arch_release_date:
                        new_exp = 0
                    else:
                        await ctx.send('```No exp logged for ' + str(args[-2]) + '```')
                        return
                else:
                    await ctx.send('```No exp logged for ' + str(args[-2]) + '```')
                    return
            else:
                new_exp = int(rows_new.one().exp)

            if not rows_old:
                if i == len(self.skill_names_arr) - 1: #Archaeology
                    if date_old < self.arch_release_date:
                        old_exp = 0
                    else:
                        await ctx.send('```No exp logged for ' + str(args[-1]) + '```')
                        return
                else:
                    await ctx.send('```No exp logged for ' + str(args[-1]) + '```')
                    return
            else:
                old_exp = int(rows_old.one().exp)

            #old_exp = int(rows_old.one().exp)
            #new_exp = int(rows_new.one().exp)

            response += '║' + '{:<13}'.format(self.skill_names_arr[i])
            response += '║' + '{:>13,d}'.format(old_exp)
            response += '║' + '{:>13,d}'.format(new_exp)
            response += '║' + '{:>12,d}'.format(abs(new_exp - old_exp)) + '║\n'
        response += '╚' + '═'*13 + '╩' + '═'*13 + '╩' + '═'*13 + '╩' + '═'*12 + '╝```'

        await ctx.send(response)

def setup(bot):
    bot.add_cog(hiscore(bot))
