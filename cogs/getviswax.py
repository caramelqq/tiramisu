import requests
import re
import datetime
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

class getviswax(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todays_combo = [None, None, None, None, None]

    def get_forum_post(self):
        try:
            r = requests.get('https://secure.runescape.com/m=forum/sl=0/forums?75,76,331,66006366')
            return r.content
        except:
            return None

    def get_combo_from_post(self, requests_text):
        soup = BeautifulSoup(requests_text, 'html.parser')
        quoted_posts = str(soup.find_all(class_='quote')[0])
        return re.findall(r'>(-\s*[^<]*)', quoted_posts)
        
    def get_date_from_post(self, requests_text):
        soup = BeautifulSoup(requests_text, 'html.parser')
        quoted_posts = str(soup.find_all(class_='quote')[0])
        return re.findall(r'Combination\sfor\s(\w*)\sthe\s(\d*)(\w*)', quoted_posts)

    def post_vis_wax_combo(self):
        # Check if we already have the result
        if all(self.todays_combo) and self.todays_combo[0] == datetime.datetime.now().day:
            return self.todays_combo

        requests_response_text = self.get_forum_post()
        # Check date - if post is outdated (date doesn't equal today), invalidate current combo and return nothing
        d = self.get_date_from_post(requests_response_text)[0]
        if int(d[1]) != datetime.datetime.now().day:
            self.todays_combo = [None, None, None, None, None]
            return self.todays_combo

        title = 'Combination for ' + d[0] + ' the ' + d[1] + d[2]
        slot_1 = ''
        slot_2 = ''

        s = self.get_combo_from_post(requests_response_text)
        
        for i in range(len(s) - 1):
            if i == 0:
                slot_1 += s[i]
            if i >= 1:
                slot_2 += s[i]
                slot_2 += '\n'

        self.todays_combo = [int(d[1]), title, slot_1, slot_2]
        return self.todays_combo

    @commands.command()
    async def wax(self, ctx):
        day, title, slot_1, slot_2 = self.post_vis_wax_combo()
        e = discord.Embed(type='rich', title='Vis Wax', color=int('e6ffff', 16))
        if not day or not title or not combo:
            e.add_field(name='Combination not out yet')
        else:
            e.add_field(name=title)
            e.add_field(name='Slot 1:', value=slot_1)
            e.add_field(name='Slot 2:', value=slot_2)
            e.add_field(name='Slot 3:', value='- Is random!')

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(getviswax(bot))