#!/var/chroot/home/content/37/9387237/bin/python
import re
print "Content-Type: text/html\r\n"

print "<html>"
print "<head>"
print "<link rel='icon' type='image/png' href='http://www.zhengchanghai.com/favicon.png'>"

print "<title>TwitterER</title>"
print "<script>"
print "function   show(obj){obj.style.background='#FF9933';}"
print "function   hide(obj){obj.style.background='#FFFFFF';}"
print "</script>"
print "<script type='text/javascript'>"
print "function getVS()"
print "{ if (document.getElementById('query_term_1').value == 'enter name of one object (e.g. iPhone)' ) "
print "alert('Please enter name of the object.');"
print "else {document.getElementById('form').action = 'http://www.zhengchanghai.com/cgi/twitterer2.py';"
print " document.getElementById('form').submit();}}"

print "function inputCheck(){"
print "if (document.getElementById('query_term_1').value == 'object 1  (e.g. iPhone)' || document.getElementById('query_term_2').value == 'object 2  (e.g. Galaxy)' )"
print " alert ('Please enter name of the two objects which you want to compare.');"
print "else if(document.getElementById('num_of_page').value == 1024)"
print "{alert ('You are right. The more pages you analyze, the accurate the results, at the cost of longer processing time. But, 1024 pages? Are you kidding?'); }"
print "else {document.getElementById('display').style.display ='block';"
print "document.getElementById('form').action = 'http://www.zhengchanghai.com/cgi/twitterer.py' ;}}"

print "function clearInput(){window.location.reload();}"
print "</script>"

print "<style>"
print "body{min-width:1024px;}"
print "#display {display:none;}"
print "#query_term_1{color:#aaa;border:1px solid;padding:5px;} "
print "#query_term_2{color:#aaa;border:1px solid;padding:5px;} "
print "p,a {font-family:Arial,Helvetica,sans-serif;}"
print "input {font-family:Arial,Helvetica,sans-serif;}"
print "#right {font-family:Arial,Helvetica,sans-serif;font-size: 80%;float:right;}"
print "#vsinfo {font-size:80%; color:#FF6600;}"
print "#orange {color:#585858;}"
print "</style></head>"

print "<body onpageshow='if (event.persisted) clearInput();' > "
print "<div id='right'><a  href='http://zhengchanghai.com/whatistwitterer.html'>"
print "<font color='#FF6600'>what is TwitterER?</font></a>&nbsp;&nbsp;</div>"
print "</br></br></br>"
print "<p  align='center'><a href='http://zhengchanghai.com/twitterer'><img src='http://zhengchanghai.com/logo_s.jpg'  width='400px'></a></br><font color='#aaa' size='2px'>easy to compare, easy for life</font></p>  </br>"
print "<table id='vsinfo' align='center'><tr><td>"
print "<p><b><font color='#FF6600'>Pairs for reference (click for results)</font></b></p></td></tr>"

import os
from bs4 import BeautifulSoup
import urllib2

query_term = os.environ['QUERY_STRING']
querylist = query_term.split('&')
query1 = querylist[0]
(term1,value1) = query1.split('=')

query = value1

try:
    req = urllib2.Request('http://www.bing.com/search?q='+query+'+vs') 
    #req = urllib2.Request('http://www.bing.com/search?q='+query+'+vs&go=&qs=n&form=QBRE&pq=subaru+vs&sc=8-7&sp=-1&sk=') 
    response = urllib2.urlopen( req )
except:
    print "error"
page_source = response.read()



soup = BeautifulSoup(page_source)

txt = soup.find(text='Related searches')
#print txt.parent

if txt is not None:
    content = txt.find_parent('div')
    #print content.parent
    #print a
    #new_tag = soup.new_tag('div')
    #new_tag.string = '\n'
    #print content.li.a
    lilist = content.parent.parent.find_all('li')
    for li in lilist:
        #li.insert_before(new_tag)
        pair = li.get_text() 
        if pair.find('vs') == -1 and pair.find('Vs') == -1 and pair.find('VS') == -1 and pair.find('Vs.') == -1 and pair.find('vs.') == -1 and pair.find('VS.') == -1:
            continue
        if pair.find('Vs.') > 0:
            pairlist = pair.split(' Vs. ')
        elif pair.find('vs.') > 0:
            pairlist = pair.split(' vs. ')
        elif pair.find('VS.') > 0:
            pairlist = pair.split(' VS. ')
        elif pair.find('vs') > 0:
            pairlist = pair.split(' vs ')
        elif pair.find('Vs') > 0:
            pairlist = pair.split(' Vs ')
        elif pair.find('VS') > 0:
            pairlist = pair.split(' VS ')
       
        if len(pairlist) != 2:
            continue
        obj1 = pairlist[0]
        obj2 = pairlist[1]
        url= "http://www.zhengchanghai.com/cgi/twitterer.py?query_term_1="+obj1+"&query_term_2="+obj2+"&num_of_page=2"
        url = re.sub('%20','+',url)
        print "<tr><td onMouseOver='javascript:show(this);' onMouseOut=hide(this); style='cursor:hand'>"
        print "<a id='orange' style='text-decoration : none;' href= '"+url+"'>"+obj1 + " vs " + obj2 + "</a>"
        print "</td></tr>"
    #print content
    #print content.get_text()
else:
    print '<tr><td>No result</td></tr>'

print "</table>"
print "</p>"
print "<form id='form' method='get' action='' onSubmit='inputCheck()' align='center'>"
print "<div style='font-family:arial'>"
print "<p align='center'>"
print "<input  id='query_term_1' type='text' name='query_term_1' style='width:500' value='enter name of one object (e.g. iPhone)' onkeydown=\"this.style.color='#000000'\" "
print "onmouseover=\"this.style.borderColor='#FF6600'\" onmouseout=\"this.style.borderColor='#aaa'\" onFocus=\"if (value =='enter name of one object (e.g. iPhone)'){value =''} \" onBlur=\"if (value =='')"
print "{value='enter name of one object (e.g. iPhone)';this.style.color='#aaa'}\" >"
print "</br></br>"
print "<input type='button' value='find related pairs' onclick='getVS()'></br><a style='text-decoration : none;' href='http://zhengchanghai.com/twitterer/'><font color='#aaa' size='1px'>Home</font></a>"
print "</br></br>"

print "</p></div></form></br>"
print "<p id='display' align='center'><img src='http://zhengchanghai.com/loading.gif'></p>"
print "<noscript></body></html>"
