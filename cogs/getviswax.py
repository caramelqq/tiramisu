import requests
import re
import datetime
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

class getviswax(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todays_combo = [None, None, None, None]

    def get_forum_posts(self):
        try:

            headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Dest': 'document',
                'Accept-Encoding': 'gzip, deflate'
            }
            base_url = 'https://secure.runescape.com/m=forum/sl=0/forums?75,76,331,66006366'
            r = requests.get(base_url, headers=headers)
            return r.content
        except:
            return None

    def get_combo_from_post(self, requests_text):
        soup = BeautifulSoup(requests_text, 'html.parser')
        try:
            quoted_posts = str(soup.find_all(class_='forum-post__body')[0])
            return re.findall(r'>(-\s*[^<]*)', quoted_posts)
        except:
            return None

        
    def get_date_from_post(self, requests_text):
        soup = BeautifulSoup(requests_text, 'html.parser')
        try:
            quoted_posts = str(soup.find_all(class_='forum-post__body')[0])
            return re.findall(r'Combination\sfor\s(\w*)\sthe\s(\d*)(\w*)', quoted_posts)
        except:
            return None
            
    def post_vis_wax_combo(self):
        try:
            # Check if we already have the result
            if all(self.todays_combo) and self.todays_combo[0] == datetime.datetime.now(datetime.timezone.utc).day:
                return self.todays_combo

            requests_response_text = self.get_forum_posts()
            # Check date - if post is outdated (date doesn't equal today), invalidate current combo and return nothing
            d = self.get_date_from_post(requests_response_text)[0]
            if int(d[1]) != datetime.datetime.now(datetime.timezone.utc).day:
                self.todays_combo = [None, None, None, None]
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

            # Escape the '*' character
            slot1.replace(('*', '\*'))
            slot2.replace(('*', '\*'))

            self.todays_combo = [int(d[1]), title, slot_1, slot_2]
            return self.todays_combo
        except:
            self.todays_combo = [None, None, None, None]
            return self.todays_combo

    @commands.command()
    async def vis(self, ctx):
        day, title, slot_1, slot_2 = self.post_vis_wax_combo()
        e = discord.Embed(type='rich', color=int('e6ffff', 16))
        if not day or not title or not slot_1 or not slot_2:
            e.title = 'Combination not out yet'
            e.add_field(name='Vis Wax FC', value='https://secure.runescape.com/m=forum/sl=0/forums?75,76,331,66006366')
        else:
            e.title = 'Vis Wax ' + title
            e.add_field(name='Slot 1:', value=slot_1, inline=False)
            e.add_field(name='Slot 2:', value=slot_2, inline=False)
            e.add_field(name='Slot 3:', value='- Is random!', inline=False)

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(getviswax(bot))