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

    #print(nearbyplayindex)
    


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
       # print('pt: ' + str(playtime))
        
        count += 1
        #print(count)
        #print(playbyplay[searchindex]['quarter'])
        #print(playbyplay[searchindex]['time'])
        searchtime = convertTime(playbyplay[searchindex]['quarter'], playbyplay[searchindex]['time'])
        #print('st: ' + str(searchtime))
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
    
        
        #print(searchindex)      
            
            
    
        

    return searchindex



def findPlay2(shortpbp, quarter, time):


    closeindex = findNearbyPlay2(shortpbp, quarter, time)

    targettime = convertTime(quarter, time)

    searchtime = convertTime(shortpbp[closeindex][0], shortpbp[closeindex][1])
    #print(closeindex)
    #print(targettime)
    
    while searchtime <= targettime:
        #print('searchtime: ' + str(searchtime))
        if closeindex + 1 >= len(shortpbp):
            return closeindex

        nextplaytime = convertTime(shortpbp[closeindex + 1][0], shortpbp[closeindex][1])
        if nextplaytime > targettime:
            return closeindex
        else:
            closeindex += 1
            searchtime = convertTime(shortpbp[closeindex][0],
                                     shortpbp[closeindex][1])

    while searchtime > targettime:
        #print('searchtime: ' + str(searchtime))
        if closeindex -1 <= 0:
            return closeindex
        prevplaytime = convertTime(shortpbp[closeindex -1][0],
                                  shortpbp[closeindex -1][1])
        #print(prevplaytime)
        if prevplaytime <= targettime:
            tbr = closeindex -1
            #print('tbr: ' + str(closeindex - 1))
            return tbr
        else:
            closeindex -= 1
            searchtime = convertTime(shortpbp[closeindex][0],
                                     shortpbp[closeindex][1])
            
            
            
    
    



def findNearbyPlay2(shortpbp, quarter, time):

    targettime = convertTime(quarter, time)
    uppersearchbound = len(shortpbp)
    lowersearchbound = 0

    searchindex = int(uppersearchbound/2)

    found = False
    count = 0

    while not found and count < 20:
        count +=1
        searchtime = convertTime(shortpbp[searchindex][0],
                                 shortpbp[searchindex][1])
        #print('search: ' + str(searchtime))
        #print('target: ' + str(targettime))
        if abs(searchtime - targettime) < 60:
            found = True

        elif targettime > searchtime:
            #print(searchindex)
            lowersearchbound = searchindex
            searchindex = int((uppersearchbound + lowersearchbound)/2)

            #print('usb: ' + str(uppersearchbound))
            #print('lsb: ' + str(lowersearchbound))
            #print(searchindex)

        else:
            
            uppersearchbound = searchindex
            searchindex = int((uppersearchbound + lowersearchbound)/2)
 
        
    return searchindex




def getFinalScore(playbyplay):

    endindex = len(playbyplay) - 1
    awayfinal = playbyplay[endindex]['awayscore']
    homefinal = playbyplay[endindex]['homescore']
    return [awayfinal, homefinal]


def getFinalScore2(shortpbp):

    endindex = len(shortpbp) - 1
    awayfinal = shortpbp[endindex][2]
    homefinal = shortpbp[endindex][3]

    return awayfinal, homefinal


def getScoreAtEndOfQuarters(shortpbp):

    quarter1found = False
    quarter2found = False
    quarter3found = False
    quarter1score = []
    quarter2score = []
    quarter3score = []

    for i in range(0, len(shortpbp)):
        if quarter1found == False and shortpbp[i][0] > 1 :
            q1awayscore = shortpbp[i-1][2]
            q1homescore = shortpbp[i-1][3]
            quarter1score = [q1awayscore, q1homescore]
            quarter1found = True


        if  quarter2found == False and shortpbp[i][0] > 2:
            quarter2found = True
            q2awayscore = shortpbp[i-1][2]
            q2homescore = shortpbp[i-1][3]
            quarter2score = [q2awayscore, q2homescore]

        if quarter3found == False and shortpbp[i][0] > 3:
            quarter3found = True
            q3awayscore = shortpbp[i-1][2]
            q3homescore = shortpbp[i-1][3]
            quarter3score = [q3awayscore, q3homescore]
            

            
    return quarter1score, quarter2score, quarter3score
         
                        
            
        

    
def findScoreMatch(shortpbp, quarter, time, targetscore, possession):

    nearbyindex = findNearbyPlay2(shortpbp, quarter, time)

    searchtime = convertTime(quarter, time)
    
    index = nearbyindex
    #play = shortpbp[index]

    inbounds = True
    
    while inbounds and abs(convertTime(shortpbp[index][0], shortpbp[index][1]) - searchtime) < 120:

        scoredif = int(shortpbp[index][2]) - int(shortpbp[index][3])
        if scoredif == targetscore and shortpbp[index][4] == possession:
            return True, shortpbp[index]

        index +=1
        if index >= len(shortpbp):
            inbounds = False
        


    index = nearbyindex
    #play = shortpbp[index]
    inbounds = True
    while inbounds and abs(convertTime(shortpbp[index][0], shortpbp[index][1]) - searchtime) < 120 :
        
       
        scoredif = int(shortpbp[index][2]) - int(shortpbp[index][3])
        if scoredif == targetscore and shortpbp[index][4] == possession:
            return True, shortpbp[index]

        index -=1
        
        if index < 0:
            inbounds = False
            
  


    return False, ''


        

        
    
    

    


    
        




                
                        
                        
