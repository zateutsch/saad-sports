import sys, os

abspath = os.path.abspath('../')

try:
    sys.path.append(abspath)
except:
    pass


import NBADataAnalysisTools as tools, statistics as stat, gameresultsplotter as plt



try:
    import data.livebettingdata2021 as lb21
    print('2021 data imported')
except:
    print('2021 data import failed')
    lb21 = []
try:
    import data.livebettingdata2020 as lb20
    print('2020 data imported')
except:
    print('2020 data import failed')
    lb20 = []
import data.livebettingdata2019 as lb19
print('2019 data imported')
import data.livebettingdata2018 as lb18
print('2018 data imported') 
import data.livebettingdata2017 as lb17
print('2017 data imported')
import data.livebettingdata2016 as lb16
print('2016 data imported')
import data.livebettingdata2015 as lb15
print('2015 data imported')
import data.livebettingdata2014 as lb14
print('2014 data imported')
import data.livebettingdata2013 as lb13
print('2013 data imported')
import data.livebettingdata2012 as lb12
print('2012 data imported')
import data.livebettingdata2011 as lb11
print('2011 data imported')
import data.livebettingdata2010 as lb10
print('2010 data imported')







data = lb20.data + lb21.data + lb13.data + lb14.data + lb15.data + lb16.data + lb17.data + lb12.data + lb11.data + lb10.data + lb18.data + lb19.data
print(len(data))

def LiveBetSpread(quarter, time,  liveawayscore, livehomescore, livespread, openspread):

    
    similargameresults = []
    failed = 0
    for game in data:

        try:
            #print(game['overunder'])

            #oudif = float(game['overunder']) - openoverunder
            #print(oudif)
            #print(game['spread'])
            spread = game['spread']

            if spread == 'PK':
                spread = 0
                
            spreaddif = float(spread) - openspread
            #print(spreaddif)

            if abs(spreaddif) < 2:

                gameind= tools.findPlay(game['playbyplay'], quarter, time)
                gameawayscore = game['playbyplay'][gameind]['awayscore']
                gamehomescore = game['playbyplay'][gameind]['homescore']
                gamelead = float(gameawayscore) - float(gamehomescore)
                livelead = liveawayscore - livehomescore
                leaddif = gamelead - livelead

                #print(abs(leaddif))

                if abs(leaddif) <2:

                    #print('made it here')

                    #print(game['playbyplay'][gameind])
                    finalscore = tools.getFinalScore(game['playbyplay'])
                    #print('final: ' + str(finalscore))
                    finalspread = float(finalscore[0]) - float(finalscore[1])
                    #print('final spread: ' + finalspread)
                    similargameresults.append(finalspread)
        except Exception as e:
            failed += 1
            #print(game['month'] + '/' + game['day'] + '/' + game['year'])
            #print(game['awayteam'] + ' vs. ' + game['hometeam'])
            
            
                                


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






















    
    
            
            

            

        
    
    
