import requests
import re
import datetime
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

class Get_vis_wax(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todays_combo = ''

    def get_forum_post():
        try:
            r = requests.get('https://secure.runescape.com/m=forum/sl=0/forums?75,76,331,66006366')
            return r.content
        except:
            return None

    def get_combo_from_post(requests_text):
        soup = BeautifulSoup(requests_text, 'html.parser')
        quoted_posts = str(soup.find_all(class_='quote')[0])
        return re.findall(r'>(-\s*[^<]*)', quoted_posts)
        
    def get_date_from_post(requests_text):
        soup = BeautifulSoup(requests_text, 'html.parser')
        quoted_posts = str(soup.find_all(class_='quote')[0])
        return re.findall(r'Combination\sfor\s(\w*)\sthe\s(\d*)(\w*)', quoted_posts)

    def post_vis_wax_combo():
        requests_response_text = get_forum_post()
        # Check date - if date doesn't equal today, return nothing
        d = get_date_from_post(requests_response_text)[0]
        if int(d[1]) != datetime.datetime.now().day:
            self.todays_combo = ''
            return None

        title = 'Combination for ' + d[0] + ' the ' + d[1] + d[2]
        combo = ''

        s = get_combo_from_post(requests_response_text)
        
        for i in range(len(s) - 1):
            if i == 0:
                combo += 'Slot 1:\n'
                combo += s[i]
                combo += '\n\nSlot 2:\n'
            if i >= 1:
                combo += s[i]
                combo += '\n'

        combo += '\nSlot 3:\n- Is random!'
        self.todays_combo = combo
        return [title, combo]

    @commands.command()
    async def wax(self, ctx):
        title, combo = post_vis_wax_combo()
        e = discord.Embed(type='rich', title='Vis Wax', color=int('e6ffff', 16))
        e.add_field(name=title, values=combo)

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Get_vis_wax(bot)))