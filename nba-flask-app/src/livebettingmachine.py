import src.NBADataAnalysisTools as tools, statistics as stat, os


#abspath = os.path.abspath('./livebettingdata2')

import data.livebettingdata2017 as lba2017
print('2017 data imported')
import data.livebettingdata2016 as lba2016
print('2016 data imported')
import data.livebettingdata2015 as lba2015
print('2015 data imported')
import data.livebettingdata2014 as lba2014
print('2014 data imported')
import data.livebettingdata2013 as lba2013
print('2013 data imported')


data = lba2013.data + lba2014.data + lba2015.data + lba2016.data + lba2017.data


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

            if abs(spreaddif) < 1.5:

                gameind= tools.findPlay(game['playbyplay'], quarter, time)
                gameawayscore = game['playbyplay'][gameind]['awayscore']
                gamehomescore = game['playbyplay'][gameind]['homescore']
                gamelead = float(gameawayscore) - float(gamehomescore)
                livelead = liveawayscore - livehomescore
                leaddif = gamelead - livelead

                #print(abs(leaddif))

                if abs(leaddif) <= 2:

                    #print('made it here')

                    #print(game['playbyplay'][gameind])
                    finalscore = tools.getFinalScore(game['playbyplay'])
                    #print('final: ' + str(finalscore))
                    finalspread = float(finalscore[0]) - float(finalscore[1])
                    #print('final spread: ' + finalspread)
                    similargameresults.append(finalspread)
        except Exception as e:
            #print(e)
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

    #print('avg: ' + str(su/len(results)))
    #print('med: ' + str(stat.median(results)))

    #print('num results: ' + str(len(results)))
    #print('probability the away team covers: ' + str(count/len(results)))

    if(len(results) != 0):
        return str(count/len(results))
    else:
        return ""
    #print('failed: ' + str(failed))

