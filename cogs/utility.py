import discord

from discord.ext import commands

class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joined(self, ctx, member : str):
        """Says when a member joined."""
        if str(ctx.message.author.id) != '194972515460710400':
            return

        if len(member) > 20:
            await ctx.send('Invalid ID.')
            return
        try:
            member_obj = await commands.MemberConverter().convert(ctx, member)
        except:
            await ctx.send('User not found.')
            return

        icon_url = member_obj.avatar_url_as()
        e = discord.Embed(type='rich', title='User Details', color=int('e6ffff', 16))
        e.set_thumbnail(url=icon_url)
        e.add_field(name='Name', value=str(member_obj))
        e.add_field(name='ID', value=member_obj.id)
        e.add_field(name='Nickname', value=member_obj.nick)
        e.add_field(name='Date Joined', value=member_obj.joined_at.strftime("%c"))
        s = ', '.join([role.name for role in member_obj.roles[1:]])
        e.add_field(name='Roles', value=s)

        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(utility(bot))



