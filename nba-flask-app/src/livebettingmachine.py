import sys, os
import statistics as stat


abspath = os.path.abspath('../')

try:
    sys.path.append(abspath)
except:
    pass


import src.NBADataAnalysisTools as tools


import data.livebettingdata as lbd

data = lbd.data

def LiveBetSpread(quarter, time,  livelead, livespread, openspread): 
    similargameresults = []
    failed = 0
    for game in data:

        try:
    
            spread = game['sp']

            if spread == 'PK':
                spread = 0
                
            spreaddif = float(spread) - openspread

            if abs(spreaddif) < 2:

                gameind= tools.findPlay2(game['pbp'], quarter, time)
                gameawayscore = game['pbp'][gameind][2]
                gamehomescore = game['pbp'][gameind][3]
                gamelead = gameawayscore - gamehomescore

                leaddif = gamelead - livelead

                if abs(leaddif) < 2:
                    finalaway, finalhome = tools.getFinalScore2(game['pbp'])
                    finalspread = finalaway - finalhome
                    similargameresults.append(finalspread)             
        except Exception as e:
            failed += 1
            
    results = similargameresults

    su = 0
    count = 0

    for result in results:
        su += result
        if result > livespread:
            count += 1

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

