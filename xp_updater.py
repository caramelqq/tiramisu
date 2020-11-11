#!/usr/bin/python3

from cassandra.cluster import Cluster
import urllib.request
import time
import datetime

def getstats(username):
    # Get user's exp
    if not username:
        return

    try:
        httpresponse_obj = urllib.request.urlopen("https://secure.runescape.com/m=hiscore/index_lite.ws?player=" + username)
    except:
        return

    skill_names = 'Overall, Attack, Defence, Strength, Constitution, Ranged, Prayer, Magic, Cooking, Woodcutting, Fletching, Fishing, Firemaking, Crafting, Smithing, Mining, Herblore, Agility, Thieving, Slayer, Farming, Runecrafting, Hunter, Construction, Summoning, Dungeoneering, Divination, Invention'
    skill_names_arr = [x.strip() for x in skill_names.split(',')]

    s = httpresponse_obj.read().decode("utf-8")   

    return s.split('\n')



def insert(names):
    #cluster = Cluster()
    cluster = Cluster(['172.31.10.41'])

    session = cluster.connect('tracker')

    skill_names = 'Overall, Attack, Defence, Strength, Constitution, Ranged, Prayer, Magic, Cooking, Woodcutting, Fletching, Fishing, Firemaking, Crafting, Smithing, Mining, Herblore, Agility, Thieving, Slayer, Farming, Runecrafting, Hunter, Construction, Summoning, Dungeoneering, Divination, Invention, Archaeology'
    skill_names_arr = [x.strip() for x in skill_names.split(',')]

    for name in names:
        name = '%20'.join(name.split(' '))
        s_arr = getstats(name)
        name = ' '.join(name.split('%20'))

        if not s_arr:
            print("Failed to update " + name)
            continue

        for i in range(len(skill_names_arr)):
            # x = rank, level, exp

            x = s_arr[i].split(',')
            session.execute('INSERT INTO ' + skill_names_arr[i] + ' (username, time, exp, rank) VALUES (%s, toTimestamp(now()), %s, %s)', [name, int(x[2]), int(x[0])])

        print("Updated: " + name)
        time.sleep(1)
    return

if __name__ == "__main__":
    names = []

    with open("names.txt") as f:
        for line in f:
            names.append(line.strip())

    insert(names)
    print("Executed on: " +  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


