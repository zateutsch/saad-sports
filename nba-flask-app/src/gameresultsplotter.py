import sys,  matplotlib.pyplot as plt,  numpy as np,  matplotlib.colors, os, statistics as stat
import time
#import livebettingmachine

#import scipy.stats.norm



rootdir = os.path.abspath('.')
#print(rootdir)

#input: array of game results
#output: location of histogram plot of those gameresults

def plotGames(results):
    t = time.localtime()
    current_time = time.strftime('%H:%M:%S', t)
    



    
    try:
        os.makedirs(rootdir + '/photos')
    except FileExistsError:
        pass


    sigma = stat.stdev(results)

    mu = stat.mean(results)
    
    
    n, bins, patches = plt.hist(results, 20,
                                density = 1,
                                color = 'green', alpha = .7)


    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))

    plt.plot(bins, y, '--', color = 'black')
    plt.xlabel('Game result')

    plt.ylabel('Percentage of Total Games')

    
    dirs = rootdir + '/photos/fig' + current_time + '.png'

    plt.savefig(dirs)

    plt.close()

    

    return(dirs)


#input: list of game results

# output: implied odds for spreads ranging from 0 to 2 times the median
# e.g ([0, odds], [1.5, odds], [2.5, odds], ... [10.5, odds]]




def getOdds(results):
    length = len(results)
    med = stat.median(results)
    print(med)
    checklist = [0]
    x = 1.5
    while x > 0 and x < abs(med*2) + 1:

        checklist.append(x)
        x += 1
    if med < 0:
        checklist = [-y for y in checklist]
        

    print(checklist)

    oddslist = []
    
    for spread in checklist:
        count = 0

        for result in results:
            if result > spread:
                count +=1
        try:

            odds = probabilityToOdds(count/length)

            oddslist.append([spread, odds])
        except:
            pass

    return oddslist        
        
        
        

    
        
    
 
    



def probabilityToOdds(x):

    

    if x <= .5:
        return '+' + str(int(100*(1-x)/x))

    if x > .5:

        return str(int(-100* x/(1-x)))






    
    
    
    



#prob, results = lbm.LiveBetSpread(1, '6:40.0', 3, 0 ,  -1.5, -4.5, 205)


#plotGames(results)

