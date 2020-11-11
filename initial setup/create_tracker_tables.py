from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect()

skill_names = 'Overall, Attack, Defence, Strength, Constitution, Ranged, Prayer, Magic, Cooking, Woodcutting, Fletching, Fishing, Firemaking, Crafting, Smithing, Mining, Herblore, Agility, Thieving, Slayer, Farming, Runecrafting, Hunter, Construction, Summoning, Dungeoneering, Divination, Invention'
skill_names_arr = [x.strip() for x in skill_names.split(',')]

session.execute('CREATE KEYSPACE tracker WITH replication = {\'class\': \'SimpleStrategy\', \'replication_factor\': \'1\'}  AND durable_writes = true;')
session.execute('USE tracker')

for skill in skill_names_arr:
	session.execute('CREATE TABLE ' + skill + ' (username varchar, time timestamp, exp bigint, rank int, PRIMARY KEY (username, time)) WITH CLUSTERING ORDER BY (time DESC);')


# create table xp_att (username varchar, time timestamp, exp int, rank int, PRIMARY KEY (username, time)) WITH CLUSTERING ORDER BY (time DESC);
# insert into xp_att (username, time, exp) values('bisca', toTimestamp(now()), 8500);
# select * from xp_att where username='ascendance' and time > '2019-07-21 22:09:50-0007';
print('SELECT * FROM overall WHERE username='ascendance' AND time > '2019-07-22 00:00:00-0007' AND time < '2019-07-22 23:59:59-0007';')
rows_old = session.execute('SELECT * FROM ' + 'overall' + ' WHERE username=\'' + 'bisca' + '\' AND time > \'2019-07-22 00:00:00-0007\' AND time < \'2019-07-22 23:59:59-0007\';')