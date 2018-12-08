#This program is an SEO tool which helps to analyze live WebPages for keyword density.
#The WebPages are analysed in batch mode and the result of each Webpage analysis is a table 
#of keywords along with their frequency and density in the webpage.The result
#is stored in a single table of a database .

import os.path
import sqlite3
import urllib.request
from bs4 import BeautifulSoup

#getStopWords() returns the set of words like "have,is,that,this,and,are etc" (known as stop words) that need to be excluded from the analyis
def getStopWords():
    f=open("C:\\Users\\kol-00530-facnode\\Desktop\\Webscraping\\StopWords.txt")   #opens the text file containting the stop words and reads the words into a list
    StopWordList=f.readlines()                      
    str="".join(StopWordList)                       #the stopwords read into the list has a trailing '\n' character ,so they are first joined to form single string
    StopWordSet=set(str.split("\n"))                #the string is split with '\n' as delimiter and the list of words formed is converted to a set and returned
    ##print(StopWordSet)
    return StopWordSet

#textFilter() takes a list of words as arguments and returns a list of unique keywords without duplicates
def textFilter(List1):
      SetA=set(List1)               #Converts list to set(dupicate words get removed)
      SetC=SetA-getStopWords()      #StopWords get removed
      List2=list(SetC)              #Set is converted to list and returned
      return List2

#createDictionary() takes  a small list and a large list as args
#small list contains unique words as items
#larger list contains the words in the smaller list repeated
#returns a dictionary with word in smaller list as key and the frequency and density of that particular word in the larger list as value    
def createDictionary(llist,slist):
      d1={};d2={}
      for word in slist:                                                  #iterating through smaller list
            count=llist.count(word)                                       #counts frequency of the word in larger list    
            d1.setdefault(word,count)                                     #adds word:frequency key,value pair to d1
            d2.setdefault(word,round((count/len(llist)*100),3))           #adds word:density key,value pair to d2
            d={i:j for i,j in zip(d1.keys(),zip(d1.values(),d2.values()))}#merges d1 and d2 into d with word:(frequency,denstiy) as key value pair
      return d

#scrapeUrl() takes Webpage Url (string) as argument and returns the list of words occuring
#in the webpage after scraping out the HTML content and all types of punctutations 
def scrapeUrl(UrlName):
     req = urllib.request.Request(UrlName, data=None, 
             headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' } 
                                      )                                                                  
     page=urllib.request.urlopen(req)               #opens the Url
     soup=BeautifulSoup(page,"html.parser")         #Creates a new bs4 object from the HTML data downloaded
     pgName=soup.title.string                       #Gets the content of the title tag of  the Webpage
     for script in soup(["script","style"]):        
         script.extract()                           #removes javascript and stylesheet code
         text=soup.get_text()                       #get text
     lines0=text.split()                            #Splits the string into words with " " as delimiter
     lines1=[]                                      #the word list is not fine as words are bundled together with '\n' and punctuation marks
     for x in lines0:                               #creates a new list,splitting words with '\n' as delim
         l=x.split("\n")                                      
         lines1.extend(l)
     lines2=[]      
     for x in lines1:                               #creates a new list,splitting words with '.' as delim
         l=x.split(".")
         lines2.extend(l)
     lines3=[]
     for x in lines2:                               #creates a new list,splitting words with ':' as delim
         l=x.split(":")
         lines3.extend(l)
     lines4=[]
     for x in lines3:                               #creates a new list,splitting words with ';' as delim
         l=x.split(";")
         lines4.extend(l)
     lines5=[]
     for x in lines4:                               #creates a new list,splitting words with '(' as delim
         l=x.split("(")
         lines5.extend(l)
     lines6=[]
     for x in lines5:                               #creates a new list,splitting words with ')' as delim
         l=x.split(")")
         lines6.extend(l)
     lines7=[]
     for x in lines6:                               #creates a new list,splitting words with '[' as delim
         l=x.split("[")
         lines7.extend(l)
     lines8=[]
     for x in lines7:                               #creates a new list,splitting words with ']' as delim
         l=x.split("]")
         lines8.extend(l)
     lines9=[]
     for x in lines8:                               #creates a new list,splitting words with '?' as delim
         l=x.split("?") 
         lines9.extend(l)
     lines10=[]
     for x in lines9:                               #creates a new list,splitting words with '/' as delim
         l=x.split("/")
         lines10.extend(l)
     lines11=[]
     for x in lines10:                              #creates a new list,splitting words with '\\' as delim
         l=x.split("\\")
         lines11.extend(l)
     lines12=[]
     for x in lines11:                              #creates a new list,splitting words with ''' as delim
         l=x.split("'") 
         lines12.extend(l)
     linesfin=[]
     for x in lines12:                              #creates a new list,splitting words with ',' as delim
         l=x.split(",")
         linesfin.extend(l)
     while "" in linesfin:linesfin.remove("")       #The final list of words contain numerous "" chars formed duto to prev splittings,they are removed
     ##print(lines5)
     return linesfin,pgName                         #returns list of words and pgName

#save() writes a Dictionary into a table of a database     
def save(conn,url,nm,D):
      for word in D.keys():          #iterates through the Dictionary keys
            freq=D[word][0]          #frequency of key
            dens=D[word][1]         #density of key
            conn.execute('''INSERT INTO WEBSCRAPING(KeyWord,Frequency,Density,Url)
                            VALUES(?,?,?,?)''',(word,freq,dens,url));#write (word,freq,dens,url) into database 
           # print(word,freq,dens,url)
            conn.commit()  
#Main program
FileName=input("Enter path to files where Urls are stored:")    #User inputs path to the .txt file where the batch of Webpage Url's are stored
fo=open(FileName)                                               #The .txt file is opened
DbName=input("Enter name of DataBase:")                         #User Inputs name of database
if(os.path.exists(DbName+".db")):                               #overwrites file if exists
    os.remove(DbName+".db")
    print("Previous instance of file was deleted")
db= sqlite3.connect(DbName+".db")                               #Database is created                                 
db.execute('''CREATE TABLE WEBSCRAPING                          
             (KeyWord STRING NOT NULL,
             Frequency INT,
             Density DOUBLE,
             Url STRING);''')                                   #table is created within the dbase with column names keyword,frequency,density,Url
db.commit()
UrlList=fo.readlines()                                          #reads each Url from file and stores them in UrlList        
for Url in UrlList:
    ListOfWords,SheetName=scrapeUrl(Url)                        #The Url is scraped and list of words and pagename is returned
    print(SheetName+":")
    print("")
    print("Number of Words:",len(ListOfWords))                  #prints out total number of words in the page
    UniqueWords=textFilter(ListOfWords)                         #Filters the list and removes duplicates
    print("Number of Unique Words :",len(UniqueWords))          #prints out total number of unique words on page
    MyDictionary=createDictionary(ListOfWords,UniqueWords)      #Creates the dictionary with word:(frequency,density) as key,value pair
    save(db,Url,SheetName,MyDictionary)                         #Saves the dictionary into the table
print("Database saved")
cursor=db.execute('SELECT * FROM WEBSCRAPING ORDER BY Frequency,Url')
for row in cursor:print(row) #prints the table in ascending order oof frequency
#print(MyDictionary)
