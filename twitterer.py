#!/var/chroot/home/content/37/9387237/bin/python
import os
import re
import string
import pickle 
from twitter import *

#######################################for first round##########################
##################################### function #####################################
def generate_features(line):
    features = {}

    #num_difference
    count1 = 0
    count2 = 0
    splitWords = line.split()
    for splitWord in splitWords:
            if(splitWord.find('object1')!=-1):
                count1=count1+1;
            if(splitWord.find('object2')!=-1):
                count2=count2+1; 
    features['num_difference'] = abs(count1-count2)

    #hasQuestionMark
    #hasExclamation
    #hasBOTH
    hasQuestionMark = 0
    hasExclamation = 0
    hasBoth = 0
    if(line.find('?')!=-1):
        hasQuestionMark=1
    if(line.find('!')!=-1):
        hasExclamation=1
    if(line.find('both')!=-1):
        hasBoth=1
    #features['hasQuestionMark'] = hasQuestionMark
    #features['hasExclamation'] = hasExclamation
    #features['hasBoth'] = hasBoth

    #effectiveOR
    #effectiveAND
    effectiveAND = 0
    effectiveOR = 0
    object1List = [i for i, x in enumerate(splitWords) if x == 'object1']
    object2List = [i for i, x in enumerate(splitWords) if x == 'object2']

    #common case
    if len(object1List) == 1 and len(object2List) == 1:
        if object2List[0] - object1List[0] <= 5:
            for i in range(object1List[0]+1,object2List[0]):
                if splitWords[i] == 'and' or splitWords[i] == '&' or splitWords[i] == ',':
                    effectiveAND = 1
                if splitWords[i] == 'or' or splitWords[i] == '/' or splitWords[i] == 'vs':
                    effectiveOR = 1
                if splitWords[i] == 'i' or splitWords[i] == 'than' or splitWords[i] == '?' or splitWords[i] == '!':
                    effectiveAND = 0
                    effectiveOR = 0

    #if one object appears twice or more
    else:
        for index1 in object1List:
            for index2 in object2List:
                if abs(index1 - index2) <= 5:
                    if index1>index2:
                        preindex = index2
                        postindex = index1
                    else:
                        preindex = index1
                        postindex = index2
                    for i in range(preindex+1,postindex):
                        if splitWords[i] == 'and' or splitWords[i] == '&' or splitWords[i] == ',':
                            effectiveAND = 1
                        if splitWords[i] == 'or' or splitWords[i] == '/' or splitWords[i] == 'vs':
                            effectiveOR = 1
                        if splitWords[i] == 'i' or splitWords[i] == 'than' or splitWords[i] == '?' or splitWords[i] == '!':
                            effectiveAND = 0
                            effectiveOR = 0
    
        
    #features['effectiveAND'] = effectiveAND
    #features['effectiveOR'] = effectiveOR
    features['effectiveANDOR'] = effectiveOR or effectiveAND
    return features
################################## end of function ###############################################################
##################################end of function for first round############################


###################################for second round################################

unigramListInOneSubsentence = []
unigramListInSeparateSubsentence = []

negationList = ['why the fuck','kidding','not','never',"don't","doesn't","doesnt",'hardly','rarely',"won't","didn't","isn't"]
posVerbList = ['problem','switch to','work','works','move to','moved to','team','prefer','preferred','choose','buy','bought','i get','i got','need','I want','i want','wanted','love','loved','like','liked','I have','i have','use','i use','I use','using']
negVerbList = ['bore','fuck','hate','suck','sucks','f','get rid of','shit','shitty','sick','tired of']


r = open('unigramList_inOneSubsentence.txt')
while 1:
    line = r.readline()
    if not line:
        break
    line = line.strip('\n')
    unigramListInOneSubsentence.append(str(line))
r.close()


r = open('unigramList_inSeparateSubsentence.txt')
while 1:
    line = r.readline()
    if not line:
        break
    line = line.strip('\n')
    unigramListInSeparateSubsentence.append(str(line))
r.close()

################################### classifier function 1 #################################
def generate_features_inOneSubsentence(line):
    features = {}

    line = line.replace(',','.') 
    line = line.replace(';','.')
    line = line.replace('?','.')
    line = line.replace('!','.')
    lineElementList = line.split('.')

    #separate line by space
    wordList = line.split(' ')
    wordsInBetweenList = []

    periodList = []
    index = -1
    for word in wordList:
        index = index+1
        if word == '.':
            periodList.append(index)

    periodList.sort(reverse = True)
    #get list for words before object1 to check for negation
    beforeObj1List = []

    for lineElement in lineElementList:
        if lineElement.find('object1') != -1 and lineElement.find('object2') != -1:
            index1 = wordList.index('object1')
            index2 = wordList.index('object2')
            #get the list of words between object1 and object2
            wordsInBetweenList = wordsInBetweenList + wordList[index1+1:index2]

            #find index of the first period before object1
            firstPeriodBeforeIndex = -1
            for periodIndex in periodList:
                if periodIndex < index1:
                    firstPeriodBeforeIndex = periodIndex
                    break

            beforeObj1List = beforeObj1List + wordList[firstPeriodBeforeIndex+1:index1]

            negAfterObj2 = 0
            if wordList[index2+1] == 'sucks' or wordList[index2+1] == 'suck' or wordList[index2+1] == 'terrible':
                negAfterObj2 = 1
    
    #two keywords appear in one subsentece
    #features: occurranceOfUnigram
    i = 0
    for unigramElement in unigramListInOneSubsentence:
            i = i + 1
            count = wordsInBetweenList.count(unigramElement)
            features['occurranceOfUnigram'+str(i)] = count

    hasNegateWord = 0
    
    #write there is negation or not 
    for negationElement in negationList:
        if negationElement in beforeObj1List:
            hasNegateWord = (hasNegateWord+1)%2
    #features['hasNegateWord'] = hasNegateWord

    #write if there is positive verb or negative verb between object1 and object2
    hasPosVerbInBetween = 0
    hasNegVerbInBetween = 0
    
    for posVerb in posVerbList:
        if posVerb in wordsInBetweenList:
            hasPosVerbInBetween = 1
            break
    for negVerb in negVerbList:
        if negVerb in wordsInBetweenList:
            hasNegVerbInBetween = 1
            break

    if hasNegateWord == 1:
        hasPosVerbInBetween = 1-hasPosVerbInBetween
        hasNegVerbInBetween = 1-hasNegVerbInBetween

    #feature: hasPosVerbInBetween, hasNegVerbInBetween
    features['hasPosVerbInBetween'] = hasPosVerbInBetween
    features['hasNegVerbInBetween'] = hasNegVerbInBetween

    #write if there is positive verb or negative verb before object1
    hasPosVerbBeforeObj1 = 0
    hasNegVerbBeforeObj1 = 0
    for posVerb in posVerbList:
        if posVerb in beforeObj1List:
            hasPosVerbBeforeObj1 = 1
            break
    for negVerb in negVerbList:
        if negVerb in beforeObj1List:
            hasNegVerbBeforeObj1 = 1
            break
    if 'or' in wordsInBetweenList or ['and'] == wordsInBetweenList or ['&'] == wordsInBetweenList or ['/'] == wordsInBetweenList:
        hasNegVerbBeforeObj1 = 0
        hasPosVerbBeforeObj1 = 0

    if hasNegateWord == 1:
        hasPosVerbBeforeObj1 = 1-hasPosVerbBeforeObj1
        hasNegVerbBeforeObj1 = 1-hasNegVerbBeforeObj1
    
    #feature: hasPosVerbBeforeObj1, hasNegVerbBeforeObj1, negAfterObj2
    features['hasPosVerbBeforeObj1'] = hasPosVerbBeforeObj1
    features['hasNegVerbBeforeObj1'] = hasNegVerbBeforeObj1
    features['negAfterObj2'] = negAfterObj2
    return features
################################### end of function 1 ############################


################################### classifier function 2 #################################
def generate_features_inSeparateSubsentence(myObjectList):
    features = {}
    if len(myObjectList) != 0:
        i = 0
        for unigramElement in unigramListInSeparateSubsentence:
            i = i + 1
            count = myObjectList.count(unigramElement)
            features['occurranceOfUnigram'+str(i)] = count

        hasNegation = 0
        for negationElement in negationList:
            if negationElement in myObjectList:
                hasNegation = 1
                break

        hasPosVerb = 0
        hasNegVerb = 0
            
        for posVerb in posVerbList:
            if posVerb in myObjectList:
                hasPosVerb = 1
                break

        for negVerb in negVerbList:
            if negVerb in myObjectList:
                hasNegVerb = 1
                break

        if hasNegation==1:
            hasPosVerb = 1-hasPosVerb
            hasNegVerb = 1-hasNegVerb

        features['hasPosVerb'] = hasPosVerb
        features['hasNegVerb'] = hasNegVerb
        features['hasPosVerb'] = hasPosVerb
    else:
        print 'error! object name not exist'
    return features
    
################################### end of function 2 ############################



###################################end of function for second round###############3
query_term = os.environ['QUERY_STRING'] 
(query1,query2,query3) = query_term.split('&')
(term1,value1) = query1.split('=')
(term2,value2) = query2.split('=')
(term3,value3) = query3.split('=')
#print value


value1 = re.sub('\+',' ',value1)
value1 = re.sub('%20',' ',value1)
value2 = re.sub('\+',' ',value2)
value2 = re.sub('%20',' ',value2)

value1 = value1.lower()
value2 = value2.lower()
value = value1+" "+value2

if int(value3) > 10:
    value3 = 1

myQuery = value
myCountPerPage = 100
myPageNum = int(value3)

error = 0
w = open(myQuery+' searchResult.txt','w')
try:
    t = Twitter(
                auth=OAuth('823979988-iDDtJETGMy5iGNmOhIQkjBLQfv4G09M1fPosGnRS', 'YXd8cElXllotnsJxnVT9nIjioEoAdwappouwoOnyA',
                           'OkaarFhmqr27NI45Xqsg', 'VNpWT1YOWEOfqyy4m1egaDRxyTKOrvTs2c6mbknU')
               )
    last_id = 0

    for page in range(0,myPageNum):
        
        #get id of the last tweet
        
        
        if page == 0:
            dict = t.search.tweets(q=myQuery,count=myCountPerPage,lang="en",result_type="recent")
        else:
            dict = t.search.tweets(q=myQuery,count=myCountPerPage,lang="en",max_id=last_id,result_type="recent")

        if myCountPerPage > len(dict["statuses"]) :
            myCountPerPage = len(dict["statuses"])
            
        for i in range(1,myCountPerPage):
            #print '* '+dict["statuses"][i]['text']+'\n'
            w.write('* '+dict["statuses"][i]['text'].encode('ascii','ignore')+'\n')
            #print dict["statuses"][i]['id']
        last_id =  dict["statuses"][myCountPerPage-1]['id']
except:
    error = 1


w.close()


f = open('neutral_classifier.pickle')
classifier = pickle.load(f)
f.close()

print 'Content-Type: text/html\r\n\r\n'
print '<html>'
print "<head>"
print "<link rel='icon'  type='image/png' href='http://www.zhengchanghai.com/favicon.png'>"
print "<title>TwitterER search result</title>"
print "<script>"
print "function   show(obj){"
print "document.all.mydiv.style.display='block';"
print "obj.style.background='#FF9933';"
print "document.all.mydiv.style.left=event.x; "
print "document.all.mydiv.style.top=event.y+5; "
print "document.all.mydiv.innerText=txt; }"
print "function   hide(obj){ "
print "mydiv.style.display='none' "
print "obj.style.background='#FFFFFF';}   "
print "</script>"

print "<script type='text/javascript' src='https://www.google.com/jsapi'></script>"

print "<script type='text/javascript'>"
print "function inputCheck(){"
print "if (document.getElementById('query_term_1').value == '' || document.getElementById('query_term_2').value == '' ) "
print "{alert ('Please enter name of the two objects which you want to compare.');break;"
print "}"
print "if (document.getElementById('query_term_1').value != '' && document.getElementById('query_term_2').value != '' ){ document.getElementById('display').style.display =\"block\"; document.getElementById('form').action = 'http://www.zhengchanghai.com/cgi/twitterer.py';}"
print "}</script>"

print "<style>"
print "#error {position: absolute;left:70px;top: 80px;}"
print "body{ min-width:1024px;}"
print "#display {display:none;}"
print "p{font-family:Arial,Helvetica,sans-serif;}"
print "#box {position: absolute;left: 15px;top: 2px;}"
print "#logo {position: absolute;left: 2px;top: 4px;}"
print "#query_term_1 {position: absolute;left: 290px;top: 26px;color:#aaa;border:1px solid;padding:5px;}"
print "#query_term_2 {position: absolute;left: 505px;top: 26px;color:#aaa;border:1px solid;padding:5px;}"
print "#button {position: absolute;left: 710px;top: 25px;}"
print "#num_of_page {position: absolute;left: 790px;top: 25px;}"
print "#display {position: absolute; left: 950px;top: 34px;}"
print "td {padding-right: 10px;}"
print "#topright {position: absolute;left: 850px;top: 310px;}"
print "#A {font-family:Arial,Helvetica,sans-serif;}"
print "</style>"

print "</head>"
print "<body>"
print "<table id='box' border='0' ><tr><td>"
print "<a href='http://zhengchanghai.com/twitterer'><img id='logo' src='http://zhengchanghai.com/logo_s.jpg' width='270px'></a>"
print "</td><td>"
print "</br>"
print "<form id='form' method='get' action='' onSubmit='inputCheck()' align='center'>"
print "<div style='font-family:arial'> <p align='center'>"
print "<input  id='query_term_1' type='text' name='query_term_1' "
print "value = '"+value1+"'"
print " style='color:#aaa; height:23; width:200; border:1px solid;'   onkeydown=\"this.style.color='#000000'\"  onBlur=\"if (value ==''){value='"+value1+"';this.style.color='#aaa'}\" onFocus=\"if (value =='"+value1+"'){value =''} \" onmouseover=\"this.style.borderColor='#FF6600'\" onmouseout=\"this.style.borderColor='#aaa'\" >&nbsp;"
print "<input id='query_term_2' type='text' name='query_term_2' "
print "value = '"+value2+"'"
print "style='color:#aaa; height:23; width:200; border:1px solid;' onkeydown=\"this.style.color='#000000'\"  onBlur=\"if (value ==''){value='"+value2+"';this.style.color='#aaa'}\"  onFocus=\"if (value =='"+value2+"'){value =''} \" onmouseover=\"this.style.borderColor='#FF6600'\" onmouseout=\"this.style.borderColor='#aaa'\">"
print "<input id='button' type='submit' value='Compare'>"
print " &nbsp; "
print "<img id='display' src='http://www.zhengchanghai.com/loading.gif'>"
print " &nbsp; &nbsp; "
print "<font color='#aaa' size='1.2px'>size: &nbsp;</font> "
print "<select id='num_of_page' name='num_of_page' style='width:40'>"
print "<option selected='selected'>1</option> "
print "<option>2</option> "
print "<option>3</option> "
print "<option>4</option> "
print "<option>5</option> "
print "</select>"
print "<font color='#aaa' size='1.2px'> x100</font>"
print "</p></div></form></td></tr></table>"
print "</br></br></br></br></br></br>"

if error == 0:
    #print pie chart
    print "<div style='position:absolute; top:100; left:0'>"
    print "<div  id='chart_div' style='width: 500px; height: 300px;'></div></div>"
    print "<div style='position:absolute; top:100; left:400'>"
    print "<div id='chart_div2' style='width: 500px; height: 300px;'></div></div>"
    print "</br></br> </br></br> </br></br> </br></br> </br></br> </br></br> </br></br> </br></br>"
    print "<div id='topright'><table><tr> <td with='80px'></td> "
    print "<td   id='h'   onMouseOver='javascript:show(this);' onMouseOut=hide(this); style='cursor:hand'><font id='A' size=1 color=#585858>so, how to understand these graphs?</td>   "
    print "</tr></table>"
    print "<div    id='mydiv'   bgcolor='#FBFEFF' style='display:none;'> "
    print "<table style='position:relative;left:15px;' width='400'   border='0' cellpadding='0' cellspacing='1' bgcolor='#C1F0FF'>"
    print "<tr align='center' bgcolor='#DFF8FF'><td style='text-align:left'><font id='A' size=2>"
    textInside = "The graph on the left shows the percentage of the Twitter messages that imply preference of "+value1+", preference of "+value2+" and those that imply neutralism. The graph on the right do not take neutral tweets into account."
    print textInside
    print "</font></td></tr>"
    print "</table></div></div>"

###########################open saved classifiers####################
f = open('classifier_inOneSubsentence.pickle')
classifier_inOneSubsentence = pickle.load(f)
f.close()

f = open('classifier_inSeparateSubsentence.pickle')
classifier_inSeparateSubsentence = pickle.load(f)
f.close()

a = value1
b = value2

aCount = 0
bCount = 0
nCount = 0

#print result out
r = open(myQuery+' searchResult.txt')
while 1:
    line = r.readline()
    if not line:
        break
    line = line.strip('')
    if line[0] != '*':
        continue
    originalLine = line

    #to lower case
    line = line.lower()

    
    
    #pre-process each line of tweet
    tweet = line
    #change @XXXX and @XXX to 'USERNAME':
    tweet = re.sub('@\S+\s',' USERNAME ',tweet)

    #only take care of tweets that contain both the two objects
    if a.lower() not in tweet or b.lower() not in tweet:
        continue

    #print tweet+'</br>'
    
    #remove http link
    #for input file, need to make a new line in the end
    tweet = re.sub('http:\S+\s','',tweet) 
    
    #reduce repeated symbol
    tweet = re.sub('\.+','.',tweet)
    tweet = re.sub('\!+','!',tweet)
    tweet = re.sub('\?+','?',tweet)
    tweet = re.sub('\,+',',',tweet)
    #make special charactors visible, &, <, >, "
    CHAR_ENTITIES={'&nbsp;':' ','&lt;':'<','&gt;':'>','&amp;':'&','&quot;':'"'}
    for k, v in CHAR_ENTITIES.items():
        tweet=re.sub(k,v,tweet)
    #remove #
    tweet=re.sub("#", " ", tweet)
    #remove repeated characters
    tweet=re.sub(r"(\w)\1{2,}", r"\1", tweet)
    tweet = tweet.strip('\n') 
    
    #change two keywords to object1 and object2
    #to-do:add long list. Here is simple version
    #first, see which keyword appears first,
    ai = string.find(tweet,a)
    bi = string.find(tweet,b)
    if ai<bi:
        formerObj = a
    else:
        formerObj = b
    if formerObj == a:
        tweet = re.sub(a,' object1 ',tweet)
        tweet = re.sub(b,' object2 ',tweet)
    else:
        tweet = re.sub(b,' object1 ',tweet)
        tweet = re.sub(a,' object2 ',tweet) 
    #print tweet+'</br>'
    if 'object1' not in tweet or 'object2' not in tweet:
        continue
    
    #add extra space at both side of punctuation marks
    puncIList = []

    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\\',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\/',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\.',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\,',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\!',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\?',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\+',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\'',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\"',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\&',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\%',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\(',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\)',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\-',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\$',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\<',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\>',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\:',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\[',tweet)]
    puncIList =  puncIList+ [m.start() for m in re.finditer(ur'\]',tweet)]

    
  
    puncIList.sort(reverse = True) 
    for puncI in puncIList:
        if puncI>0:
            tweet = tweet[:puncI]+' '+tweet[puncI]+' '+tweet[puncI+1:]  
    
    #remove extra white space
    newWords=tweet.split()
    newString=""
    for x in newWords:
        newString=newString+x+" "

    #remove retweet
    irt = string.find(tweet,' rt  username ')
    if irt>0:
        #print tweet
        continue

    newString = newString[2:]
    if newString == '':
        continue
    myClass = classifier.classify(generate_features(newString))

    if myClass == "NEU":
        myClass = 'n'
    
    if myClass == "NON":
        #second round of classification on newString
        line = newString
        line = line.strip('\n')
        #deal with the tweets that two keyword come in one sub-sentence
        line = line.replace(',','.') 
        line = line.replace(';','.')
        line = line.replace('?','.')
        line = line.replace('!','.')
        lineElementList = line.split('.')
        appearInOneSubsentence = 0

        for lineElement in lineElementList:
            if lineElement.find('object1') != -1 and lineElement.find('object2') != -1:
                appearInOneSubsentence = 1

        if appearInOneSubsentence == 1:
            myClass = classifier_inOneSubsentence.classify(generate_features_inOneSubsentence(newString))

        else:
            #in separate sentences
            object1List = []
            object2List = []
            for lineElement in lineElementList:
                if 'object1' in lineElement:
                    #the subsentence has object1 but not object2
                    tempList = lineElement.split(' ')
                    tempList.remove('object1')
                    object1List = object1List + tempList 

                if 'object2' in lineElement:
                    #the subsentence has object1 but not object2
                    tempList = lineElement.split(' ')
                    tempList.remove('object2')
                    object2List = object2List + tempList

            if len(object1List) != 0:
                #get results for object1
                classFor1 = classifier_inSeparateSubsentence.classify(generate_features_inSeparateSubsentence(object1List))

            if len(object2List) != 0:
                #get results for object2
                classFor2 = classifier_inSeparateSubsentence.classify(generate_features_inSeparateSubsentence(object2List))

            #combine the results
            if classFor1 == 'like' and classFor2 == 'like':
                myClass = 'n'
            elif classFor1 == 'like' and classFor2 == 'notlike':
                myClass = 'a'
            elif classFor1 == 'notlike' and classFor2 == 'like':
                myClass = 'b'
            elif classFor1 == 'notlike' and classFor2 == 'notlike':
                myClass = 'n'


    if formerObj == a:
        laterObj = b
    elif formerObj == b:
        laterObj = a

    if myClass == "n":
        result = "neutral"
    elif myClass == "a":
        result = formerObj 
    elif myClass == "b":
        result = laterObj

    if result == a:
        aCount = aCount + 1
        print "<font color='#04B404'>"
    elif result == b:
        bCount = bCount + 1
        print "<font color='#FF6600'>"
    elif result == 'neutral':
        nCount = nCount + 1
        print "<font color='#0099FF'>"

    #make equal length
    alen = len(a)
    blen = len(b)
    maxLen = max(alen,blen,7)

    print "<p>&nbsp;&nbsp;&nbsp;<b>"

    print str(result)

    if len(result)<maxLen:
        distance = maxLen - len(result)
        for i in range(0,distance):
            print "&nbsp;"
    print "</b>"


        
                
 
        
    print "&nbsp;&nbsp;&nbsp;&nbsp;"
    #print newString + "</b>"
    print originalLine
    print "<br>"

    #print attribute    
    #print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+ str(generate_features(newString))+ "<br>"
    print "</p>"

    print "</font>"
    
r.close()
totalCount = aCount+bCount+nCount
no_results = 0
if totalCount == 0:
    print "<p id='error'>&nbsp;&nbsp;&nbsp;<b>No results</b></p>"
    no_results = 1

os.remove(myQuery+' searchResult.txt')

if no_results == 0:
    #print js for pie chart
    print "<script type='text/javascript'>"
    print "google.load('visualization', '1', {packages:['corechart']});"
    print "google.setOnLoadCallback(drawChart);"
    print "function drawChart() {"
    print "var data = google.visualization.arrayToDataTable(["
    print "['object', 'number of support'],"
    print "['"+a+"',"+str(aCount)+"],"
    print "['"+b+"',"+str(bCount)+"],"
    print "['neutral',"+str(nCount)+"],"
    print "]);"

    print "var data2 = google.visualization.arrayToDataTable(["
    print "['object', 'number of support'],"
    print "['"+a+"',"+str(aCount)+"],"
    print "['"+b+"',"+str(bCount)+"],"
    print "]);"

    print "var options = {"
    print "title: 'All Results',"
    print "titleTextStyle: {fontName:'Arial'},"
    print "colors: ['#04B404', '#FF6600', '#0099FF'], "
    print "is3D: true,"
    print "legend : {position:'top'}"
    print "};"

    print "var options2 = {"
    print "title: 'Non-neutral Results',"
    print "titleTextStyle: {fontName:'Arial'},"
    print "colors: ['#04B404', '#FF6600'], "
    print "is3D: true,"
    print "legend : {position:'top'}"
    print "};"


    print "var chart = new google.visualization.PieChart(document.getElementById('chart_div'));"
    print "chart.draw(data, options);"
    print "var chart2 = new google.visualization.PieChart(document.getElementById('chart_div2'));"
    print "chart2.draw(data2, options2);"

    print "}"
    print "</script>"
#delete useless files
with open('search_history.txt', 'a') as file:
    file.write(myQuery+'\n')
    





print "</body>"
print "</html>"


