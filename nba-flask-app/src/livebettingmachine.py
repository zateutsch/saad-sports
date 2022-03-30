import sys, os, shelve, inspect, pickle
import statistics as stat



#moddirectory = os.path.dirname(inspect.getfile(inspect))

#dirs = os.path.split(moddirectory)


#print(dirs)


abspath = os.path.abspath('./')
try:
    sys.path.append(abspath)
except:
    pass


import src.enginetools as tools


#import data.livebettingdata as lbd

#s1012 = shelve.open(abspath + '/data/livebettingdata10-12')
#s1315 = shelve.open(abspath + '/data/livebettingdata13-15')
#s1618 = shelve.open(abspath + '/data/livebettingdata16-18')
#s1922 = shelve.open(abspath + '/data/livebettingdata19-22')

pickle1 = open(abspath + '/data/lbd10-12.pickle', 'rb')
pickle2 = open(abspath + '/data/lbd13-15.pickle', 'rb')
pickle3 = open(abspath + '/data/lbd16-18.pickle', 'rb')
pickle4 = open(abspath + '/data/lbd19-22.pickle', 'rb')

data1 = pickle.load(pickle1)
data2 = pickle.load(pickle2)
data3 = pickle.load(pickle3)
data4 = pickle.load(pickle4)





data = data1 + data2 + data3 + data4


print(len(data))
def LiveBetSpread(quarter, time,  livelead, livespread, openspread, openoverunder,  possession): 
    
    similargames = findSimilarGames(quarter, time, livelead, openspread, openoverunder, 2, 180,  possession)

    results = []
    q1results = []
    q2results = []
    q3results = []


    for game in similargames:
        awayfinal, homefinal = tools.getFinalScore2(game['pbp'])
        result = int(awayfinal) - int(homefinal)
        results.append(result)
            
        q1score, q2score, q3score = tools.getScoreAtEndOfQuarters(game['pbp'])            
        q1results.append(int(q1score[0]) - int(q1score[1]))
        q2results.append(int(q2score[0]) - int(q2score[1]))
        q3results.append(int(q3score[0]) - int(q3score[1]))

        


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





def findSimilarGames(quarter, time, livelead, openspread, openoverunder, spsearchparameter, overunderparameter, possession):

    failed = 0
    similargames = []

    for game in data:

        try:
    
            spread = game['sp']

            if spread == 'PK' or spread == 'pk':
                spread = 0

            ou = game['ou']
                
            spreaddif = abs(float(spread) - openspread)
            oudif = abs(float(ou) - openoverunder)

            if spreaddif < spsearchparameter and oudif < overunderparameter:

                #gameind = tools.findPlay2(game['pbp'], quarter, time)
               # gameawayscore = game['pbp'][gameind][2]
                #gamehomescore = game['pbp'][gameind][3]
                #gamelead = gameawayscore - gamehomescore

                #leaddif = gamelead - livelead

                matchy, play = tools.findScoreMatch(game['pbp'], quarter, time, livelead, possession)

                if matchy == True:
                    #finalaway, finalhome = tools.getFinalScore2(game['pbp'])
                    #finalspread = finalaway - finalhome
                    similargames.append(game)       
        except Exception as e:
            failed +=1
            
    print('failed: ' + str(failed))
    return similargames





 
    
            
LiveBetSpread(2, '0:25.0', 2, -4.5, -8.5, 210, 1)
#LiveBetSpread(1, '4:20.0', 6, 0, -3.5, 205, 1)





