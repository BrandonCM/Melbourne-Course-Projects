#GeoLocation Typos
import re

#NeedleMan Algorithm
def needleMan(str_f: str, str_t: str):
    if len(str_f) > len(str_t):                     
        str_t += ' ' * (len(str_f) - len(str_t))
    if len(str_f) < len(str_t):                                    
        str_f += ' ' * (len(str_t) - len(str_f))
    A = [[0 for x in range(len(str_f)+1)] for y in range(len(str_t)+1)]
    A[0][0] = 0     
      
    for j in range (1,len(str_t)+1):
        A[j][0] = j * -1 
         
    for k in range (1, len(str_f)+1):
        A[0][k] = k * -1 
         
    for j in range (1,len(str_t)+1):
        for k in range (1, len(str_f)+1):
            if str_f[k-1] == str_t[j-1]: 
                A[j][k] = A[j-1][k-1] + 1
            else:   
                A[j][k] = max(A[j][k-1],A[j-1][k],A[j-1][k-1]) - 1
                 
    return A[len(str_f)][len(str_t)]

  
def findClosestMatch(tweet):
    bestMatch = {}          #words w/ best score
    topScore = -1000000000
    gedScore = 0
    
    for i in range(2, len(tweet)-2):
        print("parsing: ", tweet[i])
        bestMatch.clear()
        if tweet[i] not in locations:           
            for city in locations:
                city = city.split()
                if len(city) == 1:              
                    gedScore = needleMan(tweet[i], city[0])
                else:
                    gedScore = 0
                    for j in range(len(city)):
                        gedScore += needleMan(tweet[i+j], city[j])
                        if gedScore < -2:
                            gedScore = -10000000000
                            break                        
                if gedScore == topScore:                                
                    bestMatch[str(city)] = gedScore
                if gedScore > topScore:                                 
                    bestMatch.clear()
                    bestMatch[str(city)] = gedScore
                    topScore = gedScore  

        else:
            continue
             
        writeToFile(tweet[i], str(bestMatch))
        topScore = -1000000000
    return None

 
def polishData(singleTweet):
    print(type(singleTweet), "inside PolishData")
    singleTweet = re.sub(r"http\S+", "", singleTweet)       #removes any links
    singleTweet = re.sub(r"www\S+", "", singleTweet)        #removes any links
    singleTweet = re.sub(r"@\S+", "", singleTweet)          #removes Usernames
    singleTweet = re.sub(r"#\S+", "", singleTweet)          #removes hashtags
    return singleTweet

 
def writeToFile(tweetword,bestMatch):
    results = open("Results.txt", 'a')
    results.write(tweetword)
    results.write("->")
    results.write(bestMatch)
    results.write("\n")
    results.close()
    return
         
#~~~~~~~~~~~~~~Storing cities within set object called 'locations'~~~~~~~~~~~~~~~~~~~~~~~~        
locations = set()
 
locationsFile = open("US-loc-names.txt", encoding="utf8")
 
for line in locationsFile:
    locations.add(line.strip())
 
locationsFile.close()
#~~~~~~~~~~~~~Place tweet file in a list~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tweetsFile = open("bcabrera_tweets.txt", encoding="utf8")
 
tweets = list()
 
for line in tweetsFile:
    tweets.append(line)
     
tweetsFile.close()
     
#~~~~~~~~~~~~~Tokenize tweet and store it in 'singleTweet'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
for i in range(len(tweets)):
    singleTweet = polishData(tweets[i])
    singleTweet = singleTweet.split()
    findClosestMatch(singleTweet)
