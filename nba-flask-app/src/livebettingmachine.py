import sys, os, shelve, inspect
import statistics as stat



#moddirectory = os.path.dirname(inspect.getfile(inspect))

#dirs = os.path.split(moddirectory)


#print(dirs)


abspath = os.path.abspath('./')
print(abspath)
try:
    sys.path.append(abspath)
except:
    pass


import src.NBADataAnalysisTools as tools


#import data.livebettingdata as lbd

shelffile = shelve.open(abspath + '/data/livebettingdata')

data = shelffile['data']


def LiveBetSpread(quarter, time,  livelead, livespread, openspread): 
    
    similargames = findSimilarGames(quarter, time, livelead, openspread, 2, 2)

    results = []
    q1results = []
    q2results = []
    q3results = []


    for game in similargames:
        awayfinal, homefinal = tools.getFinalScore2(game['pbp'])
        result = awayfinal - homefinal
        results.append(result)
            
        q1score, q2score, q3score = tools.getScoreAtEndOfQuarters(game['pbp'])            
        q1results.append(q1score[0] - q1score[1])
        q2results.append(q2score[0] - q2score[1])
        q3results.append(q3score[0] - q3score[1])

        


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

        probability = count/len(results)

    return probability, results, q1results, q2results, q3results





def findSimilarGames(quarter, time, livelead, openspread, spsearchparameter, leadsearchparameter):

    failed = 0
    similargames = []

    for game in data:

        try:
    
            spread = game['sp']

            if spread == 'PK':
                spread = 0
                
            spreaddif = float(spread) - openspread

            if abs(spreaddif) < spsearchparameter:

                gameind = tools.findPlay2(game['pbp'], quarter, time)
                gameawayscore = game['pbp'][gameind][2]
                gamehomescore = game['pbp'][gameind][3]
                gamelead = gameawayscore - gamehomescore

                leaddif = gamelead - livelead

                if abs(leaddif) < leadsearchparameter:
                    #finalaway, finalhome = tools.getFinalScore2(game['pbp'])
                    #finalspread = finalaway - finalhome
                    similargames.append(game)             
        except Exception as e:
            failed +=1
            
    print('failed: ' + str(failed))
    return similargames
            


#LiveBetSpread(1, '12:00.0', 0, 0, 0)


