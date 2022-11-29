import sqlite3 as lite 
import sys
import databasenames as names

# this function combines all of the data returned by each table in the database into giant lists so I can study the entirity of the ncca instead of individual conferences. 
def get_all(database):
    data_base = lite.connect(database)
    teams = []
    offense = []
    defense = []
    special_teams = []
    won = []
    with data_base:
        #this gets the table names from the sqlite_master schema. It then places them into the conference sort function which allows me to then extend the current list with all of the elements. 
        results = data_base.execute("SELECT name FROM sqlite_master WHERE type = 'table' and name != 'PAC'").fetchall()
        for conference in results:
            lists = conference_sort(conference[0], database)
            teams.extend(lists[0])
            offense.extend(lists[1])
            defense.extend(lists[2])
            special_teams.extend(lists[3])
            won.extend(lists[4])
    return teams, offense, defense, special_teams, won

# this function gets all the data stored in a table and puts it into the proper lists. It gets all the returns from select as tuples and then just iterates through them and appends in the proper order 1st, then 2nd. Returns the lists so they can be used in either get all or statistics.
def conference_sort(conference, database):
    data_base = lite.connect(database)
    teams = []
    offense = []
    defense = []
    special_teams = []
    won = []
    with data_base:
        results = data_base.execute('SELECT * FROM ' + conference).fetchall()
        for result in results:
            t1 = result[1]
            o1 = result[2]
            d1 = result[3]
            s1 = result[4]
            w1 = result[5]
            t2 = result[6]
            o2 = result[7]
            d2 = result[8]
            s2 = result[9]
            w2 = result[10]
            teams.append(t1)
            teams.append(t2)
            offense.append(o1)
            offense.append(o2)
            defense.append(d1)
            defense.append(d2)
            special_teams.append(s1)
            special_teams.append(s2)
            won.append(w1)
            won.append(w2)
    return teams, offense, defense, special_teams, won
            
            
# this function adds the python dictionary returned by the webscraper to the table 
def add_to_table(conference, team, database):
    data_base = lite.connect(database)
    with data_base:
        i = 0 #turns the python dict string into SQL so it can be quickly added the i is used to keep track of the game number.
        for result in conference:
            teams = list(result.keys())
            offense1 = result[teams[0]]['Offense']
            defense1 = result[teams[0]]['Defense']
            specials1 = result[teams[0]]['Special Teams']
            won1 = result[teams[0]]['Won']
            offense2 = result[teams[1]]['Offense']
            defense2 = result[teams[1]]['Defense']
            specials2 = result[teams[1]]['Special Teams']
            won2 = result[teams[1]]['Won']
            data_base.execute('INSERT INTO '+ "'" + team + "'" + ' VALUES(' + str(i) + ',' + "'" + teams[0] + "'"  + ','                + str(offense1) + ',' + str(defense1) + ',' + str(specials1) + ',' + str(won1) + ',' + "'" + teams[1] +                 "'" + ',' + str(offense2) + ',' + str(defense2) + ',' + str(specials2) + ',' + str(won2) + ')')
            i += 1


def add_table(database, conference):
    data_base = lite.connect(database)
    with data_base:
        data_base.execute('CREATE TABLE ' + conference + '(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')

#This function is used to create a new data base (it can also be done through command line, but quicker to have python code that does it all incase of deletion. Creates a table for each conference and stores the game number, the teams, and the offense, defense, and special teams plusminus score for each one. 
def create_data_base(database): 
    data_base = lite.connect(database)
    with data_base:
        data_base.execute('CREATE TABLE UMAC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE SAA(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE WIAC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE NWC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE MIAC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE CCIW(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE ASC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE E8(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE OAC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')

