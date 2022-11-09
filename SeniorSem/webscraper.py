from bs4 import BeautifulSoup
import requests

def calcfieldposition(start, team): #calculate the field position for a team
    startpos = ''.join([i for i in start if i.isdigit()]) #get the yard line
    side = ''.join([i for i in start if not i.isdigit()]) #get the side of the field
    p = 0
    side = side.split()[0]
    if (side != team): #if on the other teams side then the number is going to be greater than 50 
        startpos = (50 - int(startpos)) + 50
    elif (startpos == '00' or startpos == '0'): #if its a touchback 
        startpos = 25
    return int(startpos)

def calcavgyards(avgyards, opponents, punt, kickoff): #calculate the average punt and kickoff yards
    for team in opponents:
       if (len(punt[team]) == 0): #if a team did not have to punt ensure they win (unless other team did not)
           val = 0
       else: # otherwise sum up the number of yards and divide by number of punts
           val = sum(punt[team])/(len(punt[team]))
       avgyards[team]['Punt'] = val
       val2 = sum(kickoff[team])/len(kickoff[team]) #sum up number of yards and divide by number of kickoffs
       avgyards[team]['Kickoff'] = val2
    return avgyards

def calcspecialplusminus(plusminus, avgyards, team1, team2): #calculate the special teams plusminus score
    if (avgyards[team1]['Kickoff'] > avgyards[team2]['Kickoff']): #determine which team (or neither) had a higher kick off average 
        plusminus[team1]['Special Teams'] += 1
        plusminus[team2]['Special Teams'] -= 1
        
    elif (avgyards[team2]['Kickoff'] > avgyards[team1]['Kickoff']): 
        plusminus[team2]['Special Teams'] += 1
        plusminus[team1]['Special Teams'] -= 1
        
    
    if (avgyards[team1]['Punt'] > avgyards[team2]['Punt']): #determine which team (or neither) had a higher punt average
        plusminus[team1]['Special Teams'] += 1
        plusminus[team2]['Special Teams'] -= 1
    elif(avgyards[team2]['Punt'] > avgyards[team1]['Punt']):
        plusminus[team2]['Special Teams'] += 1
        plusminus[team1]['Special Teams'] -= 1
    return plusminus
    
def catagorize(tableString):
    team = []
    started = []
    ended = []
    result = []
    began = []
    opponents = []
    for el in tableString: #Go through all the elements of the drive result sheet and add them to proper lists
        #print(el)
        if(el.attrs['data-label'] == 'Team'): #Determine what Team the drive corresponds to 
            team.append(el.text)
            if el.text not in opponents: #This is to get the name of both the teams that played (inefficient need to improve)
                opponents.append(el.text)
        elif(el.attrs['data-label'] == 'Started: Spot'): #Add the start location
            started.append(el.text)
        elif(el.attrs['data-label'] == 'Ended: Spot'): #Add the end location
            ended.append(el.text)
        elif(el.attrs['data-label'] == 'Ended: How'): #Add the result
            result.append(el.text)
        elif(el.attrs['data-label'] == 'Started: How'): #Add how drive started
            began.append(el.text)
    return team, started, ended, result, began, opponents #Return the 5 corresponding lists

def isPunt(team, punt, plusminus, touchdowns, start, i): #Determine the changes that need to occur from a punt
    punt[team[i]].append(start) #add the starting position to the punt
    if(start == 100): #this means they scored so adjust the plusminus and touchdowns
        for adversary in plusminus:
            if adversary == team[i]:
                plusminus[adversary]['Special Teams'] += 1
                touchdowns[adversary]['Special Teams'] += 1
            else:
                plusminus[adversary]['Special Teams'] -= 1
    return punt, plusminus, touchdowns

def isKickoff(result, team, kickoff, plusminus, touchdowns, turnovers, start, i, opponents):
    if (i != 0):
        if (result[i-1] == 'FUMB' or result[i-1] == 'INT'):
            if (team[i] == opponents[0]):
                plusminus[opponents[1]]['Defense'] += 2
                touchdowns[opponents[1]]['Defense'] += 1
                turnovers[opponents[1]] += 1
            else:
                plusminus[opponents[0]]['Defense'] += 2
                touchdowns[opponents[0]]['Defense'] += 1
                turnovers[opponents[0]] += 1
    kickoff[team[i]].append(int(start))
    if(start == 100):
        for adversary in plusminus:
            if adversary == team[i]:
                plusminus[adversary]['Special Teams'] += 1
                touchdowns[adversary]['Special Teams'] += 1
            else:
                plusminus[adversary]['Special Teams'] -= 1
    return kickoff, plusminus, touchdowns, turnovers

def soupIt(url):
    req = requests.get(url)
    content = req.text
    soup = BeautifulSoup(content)
    return soup

def scrape(url):   
    #url= 'https://rhodeslynx.com/sports/football/stats/2021/augustana-college-il-/boxscore/7826'
    soup = soupIt(url)
    driveChart = soup.find('section', {'id' : "drive-chart" })
    driveChart = driveChart.find('table')
    driveChart = driveChart.findAll('td')
    plays = soup.find('section', {'id' : "play-by-play"})
    playByPlay = {'1st' : [], '2nd' : [], '3rd' : [], '4th' : [], 'OT' : []}
    playByPlay['1st'] = (plays.find('section' , {'id' : '1st'})).findAll('table')
    playByPlay['1st'].pop(0)
    playByPlay['2nd'] = (plays.find('section' , {'id' : '2nd'})).findAll('table')
    playByPlay['3rd'] = (plays.find('section' , {'id' : '3rd'})).findAll('table')
    playByPlay['4th'] = (plays.find('section' , {'id' : '4th'})).findAll('table')
    OT = plays.find('section', {'id' : 'OT'})
    if OT:
        playByPlay['OT'] = OT.findAll('table')
    return driveChart, playByPlay
#print(type(find[22]))
#print(find[22].attrs)

def initializeTable(opponents):
    punt = {}
    kickoff = {}
    plusminus = {}
    avgyards = {}
    touchdowns = {}
    turnovers = {}
    for o in opponents:
        punt[o] = []
        kickoff[o] = []
        plusminus[o] = {'Offense' : 0, 'Defense': 0, 'Special Teams' : 0}
        avgyards[o] = {'Punt' : 0, 'Kickoff' : 0}
        touchdowns[o] = {'Offense' : 0, 'Defense' : 0, 'Special Teams' : 0}
        turnovers[o] = 0
    return punt, kickoff, plusminus, avgyards, touchdowns, turnovers

def calculateBlocks(playByPlay, plusminus, opponents, possession):
    driveCounter = 0
    for quarters in playByPlay.keys():
        for drives in playByPlay[quarters]:
            descriptions = drives.findAll('td')
            for string in descriptions:
                if len(string) > 0:
                    string = (string.text).replace(',', ' ').split()
                    for word in string:

                        if word.upper() == "BLOCKED":
                            team = possession[driveCounter]
                            if opponents[0] == team:
                                plusminus[team]['Special Teams'] -= 1
                                plusminus[opponents[1]]['Special Teams'] += 1
                            else:
                                plusminus[team]['Special Teams'] -= 1
                                plusminus[opponents[0]]['Special Teams'] += 1
            if drives.find('tfoot'):
                driveCounter += 1
    return plusminus

def calculatePlusMinus(driveChart, playByPlay):
    #print(tableString)
    #tableString = table.findAll('td') 
    categorized = catagorize(driveChart)
    possession = categorized[0]
    started = categorized[1]
    ended = categorized[2]
    result = categorized[3]
    began = categorized[4]
    opponents = categorized[5]
    initialized = initializeTable(opponents)
    punt = initialized[0]
    kickoff = initialized[1]
    plusminus = initialized[2]
    avgyards = initialized[3]
    touchdowns = initialized[4]
    turnovers = initialized[5]
    for i in range(len(possession)): #loop through every single possession
        start = calcfieldposition(started[i], possession[i]) #this is for starting field position
        if (began[i] == 'PUNT'): 
            punted = isPunt(possession, punt, plusminus, touchdowns, start, i) #send it to the function for a punt
            punt = punted[0] #change the dictionaries
            plusminus = punted[1]
            touchdowns = punted[2]
        elif (began[i] == 'KO'): #the next option for beginning of drive is kick off
            kicked = isKickoff(result, possession, kickoff, plusminus, touchdowns, turnovers, start, i, opponents) 
            kickoff = kicked[0] #change the dictionaries based off of kick off results
            plusminus = kicked[1]
            touchdowns = kicked[2]
            turnovers = kicked[3]
                    
        elif (began[i] == 'FUMB' or began[i] == 'INT'): #last option is it begins in a turnover
            if(result[i-1] != 'PUNT' and result[i-1] != 'KO'): #check to make sure turnover was not on special teams
                plusminus[possession[i]]['Defense'] += 1 #increase the plusminus for current teams defense and turnovers
                turnovers[possession[i]] += 1
                if (possession[i] == possession[i-1]):# This is incase they don't have a drive accounting for td
                    plusminus[possession[i]]['Defense'] += 1 #Check if the teams are the same which meant they scored
                    touchdowns[possession[i]]['Defense'] += 1
            #print(plusminus)
        if (result[i] == 'FUMB' or result[i] == 'INT'): #Check if the result of drive is turnover
            plusminus[possession[i]]['Offense'] -= 1 #Change plus minus accordingly 
            #print(plusminus)
        elif (result[i] == 'TD'): #other option is a TD
            if(start != 100): #make sure the score wasn't from defense or specials
                plusminus[possession[i]]['Offense'] += 1 #change plus minus accordingly 
                touchdowns[possession[i]]['Offense'] += 1
                if (possession[i] == opponents[0]): #change the defensive plusminus
                    plusminus[opponents[1]]['Defense'] -= 1
                else:
                    plusminus[opponents[0]]['Defense'] -= 1
            else:
                if(began[i] == 'FUMB' or began[i] == 'INT'):# This is incase they do have a drive accounting for td
                    plusminus[possession[i]]['Defense'] += 1
                    touchdowns[possession[i]]['Defense'] += 1

    
    avgyards = calcavgyards(avgyards, opponents, punt, kickoff) #calculate the average starting position
    
    plusminus = calcspecialplusminus(plusminus, avgyards, opponents[0], opponents[1]) #calculate who won punt and ko
    plusminus = calculateBlocks(playByPlay, plusminus, opponents, possession) #calculate blocks
    #print(result)
    #print(began)
    print(plusminus)
    #print(turnovers)
    #print(touchdowns)
    #print(avgyards)

def scrapeSchedule(url):
    soup = soupIt(url)
    web_page = url.split('/')
    web_page = web_page[2]
    box_scores = soup.findAll('li', {'class' : 'sidearm-schedule-game-links-boxscore'}) 
    for i in range(6, len(box_scores), 2):
        box_score_url = box_scores[i].find('a', href = True)
        scrapeGame('http://'+ web_page + box_score_url['href'])

def scrapeYears(url):
    soup = soupIt(url)
    web_page = url.split('/')
    web_page = web_page[2]
    diff_schedules = soup.find('select', {'id':'sidearm-schedule-select-season'})
    diff_schedules = diff_schedules.findAll('option', value = True)
    for i in range(5):
        new_url = diff_schedules[i]['value']
        scrapeSchedule('http://' + web_page + new_url)

def scrapeGame(url):
    scraped = scrape(url)
    calculatePlusMinus(scraped[0], scraped[1])

scrapeYears('https://rhodeslynx.com/sports/football/schedule/2022')
#scrapeSchedule('https://hendrixwarriors.com/sports/football/schedule/2022')
#main('https://rhodeslynx.com/sports/football/stats/2022/centre-college/boxscore/8340')
#main('https://rhodeslynx.com/sports/football/stats/2022/berry-college-ga-/boxscore/8341')
#main('https://rhodeslynx.com/sports/football/stats/2022/trinity-university-texas-/boxscore/8342')
#main('https://rhodeslynx.com/sports/football/stats/2022/millsaps-college/boxscore/8343')
#main('https://rhodeslynx.com/sports/football/stats/2022/sewanee/boxscore/8344')
#scrape('https://rhodeslynx.com/sports/football/stats/2021/hendrix-college/boxscore/7831')
#scrape('https://hendrixwarriors.com/sports/football/stats/2022/trinity-texas-/boxscore/3968')
