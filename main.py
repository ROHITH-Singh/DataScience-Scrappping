import requests
import pymongo
from pymongo import MongoClient
import json
from bs4 import BeautifulSoup
cluster= MongoClient("mongodb+srv://admin:Rohit91138@cluster0.d4cq9.mongodb.net/Novelore?retryWrites=true&w=majority")
db=cluster["Novelore"]
collection=db["mangadex-scrap"]

url="https://mangadex.org"
data=list()
r=requests.get(url)
htmlcontent=r.content
#print(htmlcontent)

soup=BeautifulSoup(htmlcontent,'html.parser')
#print(soup.prettify)
#commonly used objects
#1 tag print(type(soup.title))
#2 navigable string print(type(title.string))
#3 Beautiful soup  print(type(soup))
#4 comment
#get all paras from html content instead of p use a for anchor tag
#paras =soup.find_all('p')
#print(paras)

#print(soup.find('p')['class'])

#get all the links on the page
anchors=soup.find_all('a')
all_links =set()


for link in anchors:
  if( link.get('href').startswith('/title')):
      linkText=("https://mangadex.org"+link.get('href'))
      all_links.add(linkText)



print(all_links)
s=list(all_links)
print(s)
for t in s:
   l =requests.get(t)
   htmlcontents=l.content
   soup1=BeautifulSoup(htmlcontents,'html.parser')

   sub_list=["MangaDex","-","(Title)","   ","<title>","</title>","Title ID:","\n","/"]
   author=list()
   titleid=list()
   img=list()
   for matter1 in soup1.find_all('div',{"class":"col-xl-9 col-lg-8 col-md-7"}):
     titleid=list(matter1.find('div',{"class":"row m-0 py-1 px-0"}).strings)
     author=list(matter1.find('a').strings)
   for matter2 in soup1.find_all('div',{"class":"col-xl-3 col-lg-4 col-md-5"}):
       img=(matter2.find('img',{"class":"rounded"}))
       img=img["src"]
   title_str=str(soup1.title)
   descrption =soup1.find('meta',{"name":"description"})
   descrption=(descrption["content"])
   author= ''.join(map(str,author))
   titleid= ''.join(map(str,titleid))
   for sub in sub_list:
    title_str=title_str.replace(sub,' ')
    titleid=titleid.replace(sub,'')
   titleid =titleid.replace(" ",'')
   n=len(title_str)
   title_name=title_str[1:n]
   # print(titleid)
   # print(title_name)
   # print(author)
   # print(descrption)
   title_link=title_name.replace(' ','-')
   title_link=title_link.replace('---','')
   # print(title_link)
   page_link_list = (soup1.find_all('a', {"class": "page-link"}))
   page_link=list()
   chapters = list()
   if(page_link_list):
       # print("page available")
       for pagelink_chapter in page_link_list:
           if (str(pagelink_chapter.get('href')).startswith('/title')):
               pagelink = ("https://mangadex.org"+str(pagelink_chapter.get('href')))
               page_link = [pagelink] + page_link
           for x in page_link:
             if page_link.count(x) > 1:
                page_link.remove(x)
       dspilt=''+page_link[0]
       dspilt=dspilt.split('chapters/',1)
       dspilt1=dspilt[1]
       # print(page_link[0])
       for sub in sub_list:
           dspilt1=dspilt1.replace(sub,'')
       numpages=int(dspilt1)
       # print(numpages)

       # for q in page_link:
       #     b=requests.get(q)
       #     htmlpagecontent=b.content
       #     soup3=BeautifulSoup(htmlpagecontent,'html.parser')
       #     page_link_list = (soup3.find_all('a', {"class": "page-link"}))
       #     for pagelink_chapter in page_link_list:
       #         if (str(pagelink_chapter.get('href')).startswith('/title')):
       #             pagelink = ("https://mangadex.org"+str(pagelink_chapter.get('href')))
       #             page_link =page_link +[pagelink]
       #
       # page_link=set(page_link)
       # page_link=list(page_link)
       #
       # print((page_link))

       for x in (range(1,numpages+1)):
           m="https://mangadex.org/title/"+titleid+"/"+title_link+"/chapters/"+str(x)+"/"
           # print(m)
           p=requests.get(m)
           htmlpagecontent=p.content
           soup2=BeautifulSoup(htmlpagecontent,'html.parser')
           anchors_chapter1 = (soup2.find_all('a', {"class": "text-truncate"}))
           allchapter_link1 = list()
           for link_chapter1 in anchors_chapter1:
               if (link_chapter1.get('href').startswith('/chapter')):
                   chapterlink1 = ("https://mangadex.org" + link_chapter1.get('href'))
                   chapters=chapters+[chapterlink1]
       # print(chapters)

   else:
        # print("notavailabele")
        anchors_chapter = (soup1.find_all('a',{"class":"text-truncate"}))
        allchapter_link=list()
        for link_chapter in anchors_chapter:
           if(link_chapter.get('href').startswith('/chapter')):
               chapterlink=("https://mangadex.org"+link_chapter.get('href'))
               chapters=chapters+[chapterlink]
        # print(chapters)

   data_set={"id":titleid ,"imgthmp":img,"Title":title_name,"description":descrption,"chapters":chapters}
   collection.insert_one(data_set)
   print(data_set)
   result= collection.find({"Title":"solo-leveling"})
   # data.append(data_set)
   # with open('data.txt', 'a') as outfile:
   #     json.dump(data, outfile)
   # print(data)

#mongodb+srv://admin:<password>@cluster0.d4cq9.mongodb.net/<dbname>?retryWrites=true&w=majority