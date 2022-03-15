import sys, os

abspath = os.path.abspath('../')

try:
    sys.path.append(abspath)
except:
    pass


import NBADataAnalysisTools as tools, statistics as stat, gameresultsplotter as plt

import data.livebettingdata as lbd

data = lbd.data

def LiveBetSpread(quarter, time,  liveawayscore, livehomescore, livespread, openspread):

    
    similargameresults = []
    failed = 0
    for game in data:

        try:
           

            #oudif = float(game['overunder']) - openoverunder
            #print(oudif)
    
            spread = game['sp']

            if spread == 'PK':
                spread = 0
                
            spreaddif = float(spread) - openspread
            #print('spread dif: ' + str(spreaddif))

            if abs(spreaddif) < 2:

                gameind= tools.findPlay2(game['pbp'], quarter, time)
                gameawayscore = game['pbp'][gameind][2]
                gamehomescore = game['pbp'][gameind][3]
                gamelead = gameawayscore - gamehomescore
                livelead = liveawayscore - livehomescore
                leaddif = gamelead - livelead

                #print('lead dif: ' + str(abs(leaddif)))

                if abs(leaddif) < 2:

                    #print('made it here')

                
                    finalaway, finalhome = tools.getFinalScore2(game['pbp'])
                    #print('final: ' + str(finalscore))
                    finalspread = finalaway - finalhome
                    #print('final spread: ' + finalspread)
                    similargameresults.append(finalspread)
        except Exception as e:
            failed += 1
            #print(e)
            #print(game['mnth'] + '/' + game['dy'] + '/' + game['yr'])
            #print(game['away'] + ' vs. ' + game['home'])
            
            
            
                                


    results = similargameresults


    su = 0
    count = 0

    for result in results:
        su += result
        #print(result)
        if result > livespread:
            count += 1

    #print('Game results: ' + str(results))
    results_count = len(results)
    probability = -1.0
    if(results_count > 0):
        print('avg: ' + str(su/len(results)))
        print('med: ' + str(stat.median(results)))

        print('num results: ' + str(len(results)))
        print('probability the away team covers: ' + str(count/len(results)))
        print('probility the home team covers: ' + str(1-count/len(results)))

        print('failed: ' + str(failed))
        probability = count/len(results)

    return probability, results








#p, res = LiveBetSpread(1, '7:10.0', 5, 0, 4.5, 3.5)


#LiveBetSpread(2,'5:00.0', 0, 4, 5.5, 11.5)


#warriors -11
#bucks +1.5
#bulls -5
#raptors -6.5





LiveBetSpread(2, '1:43.0', 0, 2, 5, 5)













    
    
            
            

            

        
    
    
