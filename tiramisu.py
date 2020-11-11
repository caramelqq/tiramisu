import datetime
import sys
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='~', description='Send me pastries and cake!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Executed: ' +  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('------')

if __name__ == '__main__':
    sys.path.insert(1, os.getcwd() + "/cogs/")

    for file in os.listdir(os.getcwd() + '/cogs'):
        if os.path.isfile(os.getcwd() + '/cogs/' + file) and file.endswith('.py'):
            try:
                bot.load_extension(file.split('.')[0])
                print('Loaded: ', file.split('.')[0])
            except Exception as error:
                print('{} not loaded. [{}]'.format(file, error))

    with open('key', 'r') as api_key:
        key = api_key.read()

    bot.run(key)
