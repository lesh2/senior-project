import math
import statistics
import database
import matplotlib.pyplot as plt
import numpy as np
import models 
import databasenames as names

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

def new_goals(special_teams):
    plus_1 = []
    plus_2 = []
    for i in range(len(special_teams)):
        if special_teams[i] >= 2:
            plus_2.append(i)
        if special_teams[i] >= 1:
            plus_1.append(i)
    return plus_1, plus_2

def max_team(category):
    maximum = []
    max_val = -math.inf
    for i in range(len(category)):
        if category[i] > max_val:
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

def print_stats_one(num_met_goal, won, phase):
    print('The Number of Teams That Met The Goal on ' + phase + ' is: ' + str(len(num_met_goal)))
    print('The Number of Those Teams That Won is: ' + str(num_won(num_met_goal, won)))
    print('Thats a Clip of: ' + str(num_won(num_met_goal,won)/len(num_met_goal)))

def print_stats_two(num_met_goal, won, phase1, phase2):
    print('The Number of Teams That Met The Goal on ' + phase1 + ' and ' + phase2 + ' is: ' + str(len(num_met_goal)))
    print('The Number of Those Teams That Won is: ' + str(num_won(num_met_goal, won)))
    print('Thats a Clip of: ' + str(num_won(num_met_goal,won)/len(num_met_goal)))

def significance_test(r, size):
    x = (size-2)/(1 - (r*r))
    t = r * math.sqrt(x)
    print('Significance: ')
    print(t)

def calc_correlation(values, win_percent):
    frequencies = [1 for i in range(len(values))]
    vsm = calc_standard_dev(values, frequencies)
    wsm = calc_standard_dev(win_percent, frequencies)
    x = (len(values) - 1)*(vsm[0])*(wsm[0])
    n = 0
    for i in range(len(values)):
        n += (values[i] * win_percent[i])
    n = n - ((len(values)) * vsm[1] * wsm[1])
    r = n/x
    print('len: ')
    print(len(values))
    print('r value: ')
    print(r)
    significance_test(r, len(values))

def calc_standard_dev(values, frequencies):
    mean = 0
    num = 0
    for i in range(len(values)):
        mean += (values[i] * frequencies[i])
        num += frequencies[i]
    mean = (mean/num)
    print('mean: ')
    print(mean)
    dfm2 = []
    for i in range(len(values)):
        x = values[i] - mean
        x = (x * x)
        x = frequencies[i] * x
        dfm2.append(x)
    n = sum(dfm2)
    n = n/(num - 1)
    return math.sqrt(n), mean


def plot_against_wins(plusminus, wins, tag):
    plot = {}
    num4 = 0
    numm4 = 0
    for i in range(len(plusminus)):
        if plot.get(plusminus[i]) == None:
            plot[plusminus[i]] = [wins[i], 1]
        else:
            plot[plusminus[i]][0] += wins[i]
            plot[plusminus[i]][1] += 1
    print('Four Occured: ')
    print(num4)
    print('Minus Four Occured: ')
    print(numm4)
    score = []
    win_total = []
    frequency = []
    win_percent = []
    mode_freq = []
    mode_valf = 0
    mode_win = []
    mode_valw = 0
    for val in list(plot.keys()):
        if val == 5:
            print('Val 5: ')
            print(val)
            print(plot[val][1])
        if val == -5:
            print('Val -5: ')
            print(val)
            print(plot[val][1])
        if plot[val][1] > mode_valf:
            mode_valf = plot[val][1]
            mode_freq = [val]
        elif plot[val][1] == mode_valf:
            mode_freq.append(val)
        if plot[val][0] > mode_valw:
            mode_valw = plot[val][0]
            mode_win = [val]
        elif plot[val][0] == mode_valw:
            mode_valw = plot[val][0]
            mode_win.append(val)
        score.append(val)
        win_total.append(plot[val][0])
        frequency.append(plot[val][1])
        win_percent.append((plot[val][0])/plot[val][1])
    print('Frequency Dev: ')
    print(calc_standard_dev(score, frequency)[0])
    print('Win total Dev: ')
    print(calc_standard_dev(score, win_total)[0])
    calc_correlation(score, win_percent)
    print('Freq Mode: ')
    print(mode_freq)
    print('Val Freq Mode: ')
    print(mode_valf)
    print('Win Mode: ')
    print(mode_win)
    print('Val Win Mode: ')
    print(mode_valw)
    test_results = database.conference_sort('PAC', names.adjusted)
    print(len(test_results[1]))
    if tag == 'o':
        popt = models.best_fit(score, win_percent, models.sigmoid)
        print('offense test score:')
        print(models.test_model(test_results[1], test_results[4], popt, models.sigmoid))
    elif tag == 'd':
        print('defense test score:')
        popt = models.best_fit(score, win_percent, models.sigmoid)
        print(models.test_model(test_results[2], test_results[4], popt, models.sigmoid))
    else:
        print('specials test score:')
        print(score)
        popt = models.best_fit(score, win_percent, models.cos_curve)
        print(models.test_model(test_results[3], test_results[4], popt, models.cos_curve))
    models.regress_this(plusminus, wins)
    plt.scatter(score, win_total)
    plt.title('Special Teams Win Total')
    plt.xlabel('Special Teams Plus Minus')
    plt.ylabel('Win Total')
    plt.show()
    plt.scatter(score, frequency)
    plt.title('Special Teams Frequency')
    plt.xlabel('Special Teams Plus Minus')
    plt.ylabel('Frequency')
    plt.show()
    plt.scatter(score, win_percent)
    plt.title('Special Teams Win Percent')
    plt.xlabel('Special Teams Plus Minus')
    plt.ylabel('Win Percentage')
    plt.show()
    


def calculate_stats(conference, data_base):
    if conference == 'ALL':
        sort = database.get_all(data_base)
    else:
        sort = database.conference_sort(conference, data_base)
    teams = sort[0]
    offense = sort[1]
    defense = sort[2]
    special_teams = sort[3]
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
        print_stats_one(num_met_goal[i], won, phase)
    offense_defense = met_two_goals(num_met_goal[0], num_met_goal[1])
    print_stats_two(offense_defense, won, 'Offense', 'Defense')
    offense_specials = met_two_goals(num_met_goal[0], num_met_goal[2])
    print_stats_two(offense_specials, won, 'Offense', 'Special Teams')
    defense_specials = met_two_goals(num_met_goal[1], num_met_goal[2])
    print_stats_two(defense_specials, won, 'Defense', 'Special Teams')
    all_three = met_three_goals(num_met_goal[0], num_met_goal[1], num_met_goal[2])
    print('The Number of Teams That Met The Goal in All Three Phases is: '
            + str(len(all_three)))
    print('The Number of Those Teams That Won is ' + str(num_won(all_three, won)))
    print('Thats a Clip of: ' + str(num_won(all_three, won)/len(all_three)))
    print('With Special Teams Goal +1: ')
    new_goal = new_goals(special_teams)
    for goal in new_goal:
        print_stats_one(goal, won, 'Special Teams')
        offense_specials = met_two_goals(num_met_goal[0], goal)
        print_stats_two(offense_specials, won, 'Offense', 'Special Teams')
        defense_specials = met_two_goals(num_met_goal[1], goal)
        print_stats_two(defense_specials, won, 'Defense', 'Special Teams')
        all_three = met_three_goals(num_met_goal[0], num_met_goal[1], goal)
        print('The Number of Teams That Met The Goal in All Three Phases is: '
                + str(len(all_three)))
        print('The Number of Those Teams That Won is ' + str(num_won(all_three, won)))
        print('Thats a Clip of: ' + str(num_won(all_three, won)/len(all_three)))
    print('Offense SD: ')
    popt_o = plot_against_wins(offense, won, 'o')
    print('Defense SD: ')
    popt_d = plot_against_wins(defense, won, 'd')
    print('Combined Score: ')
    models.dual_prediction(offense, defense, won)
    print('Special Teams SD: ')
    plot_against_wins(special_teams, won, 's')
    #plt.scatter(offense, defense)
    #plt.show()
    #plt.scatter(offense, special_teams)
    #plt.show()
    #plt.scatter(defense, special_teams)
    #plt.show()
