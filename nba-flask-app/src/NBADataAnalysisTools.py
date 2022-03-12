import os, re

timereg = re.compile('(\d+):(\d+).(\d)')
rootdir = os.path.abspath('./NBAGamesDatabase')

#DOMAIN: year

#RANGE: array of [[boxscore location, pbp location,  DD/MM/YYYY], ...]


def getGameFiles(year):

    rootdir2 = rootdir + '/' + year

    games = []
    dirs1 = os.listdir(rootdir2)

    for dir1 in dirs1:

        fullpath1 = rootdir2 + '/' + dir1
        
        if os.path.isdir(fullpath1):
            
            dirs2 = os.listdir(fullpath1)
            
            for dir2 in dirs2:
                
                fullpath2 = fullpath1 + '/' + dir2
                
                if os.path.isdir(fullpath2):
                
                    dirs3 = os.listdir(fullpath2)
                    
                    for dir3 in dirs3:

                        fullpath3 = fullpath2 + '/' + dir3

                        if os.path.isdir(fullpath3):
                            boxloc = fullpath3 + '/' + 'boxscore.html'
                            pbploc = fullpath3 + '/' + 'pbp.html'
                            date = dir1 + '/' + dir2 + '/' + year
                            games.append([boxloc, pbploc, date])


    return games




#DOMAIN (quarter as int, time as mm:ss.s)
#RANGE seconds played


def convertTime(quarter, time):
    quarterseconds = (quarter -1 ) * 720
    tim = timereg.search(time)

    minutesleft = tim.group(1)

    secondsleft = tim.group(2)
    milly = tim.group(3)

    secondsplayedinq = 720 - (float(minutesleft)*60 + float(secondsleft) + float(milly)/10)
    return secondsplayedinq + quarterseconds



def findPlay(playbyplay, quarter, time):
    timmy = convertTime(quarter, time)
    if timmy > 2880 or timmy < 0:
        raise Exception('Out of bounds fool')

    nearbyplayindex = findNearbyPlay(playbyplay, quarter, time)

   
    


    found = False
    searchqrtr = playbyplay[nearbyplayindex]['quarter']
    searchtime = playbyplay[nearbyplayindex]['time']

    playindex = nearbyplayindex
    
    count = 0

    while not found and count < 100:
        count+= 1
        searchsecs = convertTime(searchqrtr, searchtime)
        
        dif = searchsecs - timmy
        #print(dif)

        oldp = playindex

        if dif > 0:
            playindex -= 1
            searchtime = playbyplay[playindex]['time']
            searchqrtr = playbyplay[playindex]['quarter']
        if dif < 0:
            playindex +=1
            searchtime = playbyplay[playindex]['time']
            searchqrtr = playbyplay[playindex]['quarter']


        newsearchsecs = convertTime(searchqrtr, searchtime)
        newdif = newsearchsecs - timmy
        #print('newdif: ' + str(newdif))

        if abs(newdif) >+ abs(dif):
            found = True


    return(oldp)
        
            
            
        

    
        
        
        

    

    return

    



#DOMAIN playbyplay data, quarter, time
# RANGE index of a play within 1 minute of the given time

def findNearbyPlay(playbyplay, quarter, time):

    uppersearchbound = len(playbyplay)
    lowersearchbound = 0
    searchindex = int(len(playbyplay)/2)
    found = False
    playtime = convertTime(quarter, time)
    count = 0

    while not found and count < 50:
        count += 1
        #print(count)
        searchtime = convertTime(playbyplay[searchindex]['quarter'], playbyplay[searchindex]['time'])
        if playtime > searchtime - 60 and playtime < searchtime + 60:
            found = True
        elif playtime > searchtime:
            tempind = searchindex
            searchindex = int((searchindex + uppersearchbound)/2)
            lowersearchbound = tempind
        else:
            tempind = searchindex
            searchindex = int((searchindex + lowersearchbound)/2)
            uppersearchbound = tempind
    
        
                
            
            
    
        

    return searchindex




def getFinalScore(playbyplay):

    endindex = len(playbyplay) - 1
    awayfinal = playbyplay[endindex]['awayscore']
    homefinal = playbyplay[endindex]['homescore']
    return [awayfinal, homefinal]

        




#print(convertTime(4, '11:00.7'))


#games = getGameFiles('2016')

#x = 0
#while x < 20:
 #   print(games[x])
   # x = x +1
                
                        
                        
