import math
import statistics

def num_won(met_goal, won):
    num_won = 0
    for i in met_goal:
        if won[i] == 1:
            num_won += 1
    return num_won

def met_two_goals(goal1, goal2):
    two_goals = [i for i in goal1 if i in goal2]
    return two_goals

def met_three_goals(goal1, goal2, goal3):
    three_goals = [i for i in goal1 if i in goal2]
    three_goals = [i for i in three_goals if i in goal3]
    return three_goals

def met_goal(offense, defense, special_teams):
    offense_n = []
    defense_n = []
    special_teams_n = []
    for i in range(len(offense)):
        if offense[i] >= 3:
            offense_n.append(i)
        if defense[i] >= 1:
            defense_n.append(i)
        if special_teams[i] >= 3:
            special_teams_n.append(i)
    return offense_n, defense_n, special_teams_n

def max_team(category):
    maximum = []
    max_val = -math.inf
    for i in range(len(category)):
        if category[i] > max_val:
            print(i)
            print(len(category))
            maximum = [i]
            max_val = category[i]
        elif category[i] == max_val:
            maximum.append(i)
    return maximum

def min_team(category):
    minimum = []
    min_val = math.inf
    for i in range(len(category)):
        if category[i] < min_val:
            minimum = [i]
            min_val = category[i]
        elif category[i] == min_val:
            minimum.append(i)
    return minimum

def get_teams(team, won, indexes):
    for i in indexes:
        
        if (i % 2) == 0:
            print(team[i] + ' vs ' + team[i+1])
            if won[i] == 1:
                print(team[i] + ' won.')
            else:
                print(team[i] + ' lost.')
            
        else:
            print(team[i] + ' vs ' +  team[i-1])
            if won[i] == 1:
                print(team[i] + ' won.')
            else:
                print(team[i] + ' lost.')

def sort_it(conference):
    offense = []
    defense = []
    special_teams = []
    won = []
    teams = []
    for result in conference:
        for team in result.keys():
            offense.append(result[team]['Offense'])
            defense.append(result[team]['Defense'])
            special_teams.append(result[team]['Special Teams'])
            won.append(result[team]['Won'])
            teams.append(team)
    return offense, defense, special_teams, teams, won


def calculate_max_and_min(offense, defense, special_teams, teams, won):
    offense_max = max_team(offense)
    offense_min = min_team(offense)
    defense_max = max_team(defense)
    defense_min = min_team(defense)
    special_teams_max = max_team(special_teams)
    special_teams_min = min_team(special_teams)
    print('The Max Value of Offense: ' + str(offense[offense_max[0]]))
    print('It occured in: ')
    get_teams(teams, won, offense_max)
    print('The Min Value of Offense: ' + str(offense[offense_min[0]]))
    print('It occured in: ')
    get_teams(teams, won, offense_min)
    print('The Max Value of Defense: ' + str(defense[defense_max[0]]))
    print('It occured in: ')
    get_teams(teams, won, defense_max)
    print('The Min Value of Defense: ' + str(defense[defense_min[0]]))
    print('It occured in: ')
    get_teams(teams, won, defense_min)
    print('The Max Value of Special Teams: ' + str(special_teams[special_teams_max[0]]))
    print('It occured in: ')
    get_teams(teams, won, special_teams_max)
    print('The Min Value of Special Teams: ' + str(special_teams[special_teams_min[0]]))
    print('It occured in: ')
    get_teams(teams, won, special_teams_min)

def calculate_stats(conference):
    sort = sort_it(conference)
    offense = sort[0]
    defense = sort[1]
    special_teams = sort[2]
    teams = sort[3]
    won = sort[4]
    calculate_max_and_min(offense, defense, special_teams, teams, won)
    num_met_goal = met_goal(offense, defense, special_teams)
    print('The Total Number of Teams is : ' + str(len(teams)))
    for i in range(len(num_met_goal)):
        if i == 0:
            phase = 'Offense'
        elif i == 1:
            phase = 'Defense'
        else:
            phase = 'Special Teams'
        print('The Number of Teams That Met The Goal on ' + phase + ' is: ' + str(len(num_met_goal[i])))
        print('The Number of Those Teams That Won is: ' + str(num_won(num_met_goal[i], won)))
    offense_defense = met_two_goals(num_met_goal[0], num_met_goal[1])
    print('The Number of Teams That Met The Goal on Offense and Defense is: '
            + str(len(offense_defense)))
    print('The Number of Those Teams That Won is: ' + str(num_won(offense_defense, won)))
    offense_specials = met_two_goals(num_met_goal[0], num_met_goal[2])
    print('The Number of Teams That Met The Goal on Offense and Special Teams is: ' 
            + str(len(offense_specials)))
    print('The Number of Those Teams That Won is: ' + str(num_won(offense_specials, won)))
    defense_specials = met_two_goals(num_met_goal[1], num_met_goal[2])
    print('The Number of Teams That Met The Goal on Defense and Special Teams is: ' 
            + str(len(defense_specials)))
    print('The Number of Those Teams That Won is ' + str(num_won(defense_specials, won)))
    all_three = met_three_goals(num_met_goal[0], num_met_goal[1], num_met_goal[2])
    print('The Number of Teams That Met The Goal in All Three Phases is: '
            + str(len(all_three)))
    print('The Number of Those Teams That Won is ' + str(num_won(all_three, won)))


