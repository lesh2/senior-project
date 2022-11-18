import sqlite3 as lite 
import sys

def conference_sort(conference):
    data_base = lite.connect('plusminus.db')
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
            
            

def add_to_table(conference, team):
    data_base = lite.connect('plusminus.db')
    with data_base:
        i = 0
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


def create_data_base():
    data_base = lite.connect('plusminus.db')
    with data_base:
        data_base.execute('CREATE TABLE UMAC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE SAA(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE WIAC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE NWC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE MIAC(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')
        data_base.execute('CREATE TABLE CCIW(Game INT, Team1 TEXT, Offense1 INT, Defense1 INT, SpecialTeams1 INT, Won1 INT,Team2 TEXT, Offense2 INT, Defense2 INT, SpecialTeams2 INT, Won2 INT)')



