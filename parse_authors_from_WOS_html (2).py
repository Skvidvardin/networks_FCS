
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
from collections import defaultdict


# In[2]:

path_from = '/Users/edward/Downloads/art/'
path_to = '/Users/edward/Downloads/'


# In[3]:

all_authors = {}


# In[13]:

"""
In the script below the html pages with articles are being parsed. It takes as an input the 
folder with all html pages (each contains 500 articles). For each page the following info is available:
 * name - YES
 * institution YES
 * coauthors YES
 * papers with coauthors YES
 * n papers YES

To identify researches and prevent collisions - the pair of Name and Surname + first part of institution 
(till the comma) is used. 

Script iterates over articles and  creates a value for each author ,
It checks  whether a researched is already added or not, and if he was added to dict previously,
then he is info is updated ( coauthors, articles list, number of publications).
"""


# In[12]:

# for each author 
# * name - YES
# * institution YES
# * coauthors YES
# * papers with coauthors YES
# * num cited NO
# * h index NO 
# * n papers YES


# In[4]:

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(path_from) if isfile(join(path_from, f))]


# In[5]:

def parse_doc(path): #path ='savedrecs.html'
    soup = BeautifulSoup(open(path, encoding='utf-8'), "html.parser")
    lines = soup.find_all("hr") 
    for i in range(len(lines)):
        get_filled(i,lines)


# In[6]:

def get_filled(k,lines):
    article = lines[k].find_next()
    authors_full = []

    try:
        a = article.find(text="AF ").find_next()
        authors_full = a.get_text().split("\n   ")
    except:
        authors_full.append("NaN")

    authors = []

    try:
        a = article.find(text="AU ").find_next()
        authors = a.get_text().split("\n   ")
    except:
        authors.append("NaN") 


    auth_ints = {}
    try:
        a = article.find(text="C1 ").find_next()
        t = a.get_text()
        new_text = t.replace('\n', '').replace('[', '|').replace(']', '--')[1:]

        for i in new_text.split('|'):
            auth_ints[i.split('--')[0]]=i.split('--')[1].strip()

        authors_with_inst = []
        for k in range(len(authors_full)):
            for group in list(auth_ints.keys()):
                if authors_full[k] in group or authors[k] in group:
                    authors_with_inst.append(authors_full[k] +'--'+auth_ints[group] )
                    break  
        authors_with_inst_short = []
        for k in range(len(authors_full)):
            for group in list(auth_ints.keys()):
                if authors_full[k] in group or authors[k] in group:
                    authors_with_inst_short.append(authors_full[k] +'--'+auth_ints[group].split(',')[0] )
                    break                      
        #print(authors_with_inst)
        total_authors  = dict(zip(authors_with_inst_short, authors_with_inst))
        try:
            title = article.find(text="TI ").find_next().get_text()
        except:
            title = "NaN" 
        for i in total_authors.keys():
            j = total_authors[i]
            local_full = authors_full.copy()
            local_full.remove(j.split("--")[0])
            all_coauthors = set(local_full)
            current_articles = [(title,local_full)]
            to_add = {}
            to_add['articles'] = current_articles
            to_add['name'] = j.split("--")[0]
            to_add['organisation'] = j.split("--")[1]
            to_add['num_articles'] = 1
            to_add['coauthors'] =  all_coauthors

            try: 
                xx = all_authors[i]
                xx['num_articles'] += 1
                xx['coauthors'] =  xx['coauthors'].union(to_add['coauthors'])
                xx['articles'].append(to_add['articles'][0])
                all_authors[i] = xx
            except:
                all_authors[i]=to_add    
    except:
        pass
#         print(article)
#         print('----')


# In[7]:

# LONGEST PART - LIMIT HERE TO TEST
for doc  in onlyfiles:
    parse_doc(path_from+doc)


# In[8]:

for i in list(all_authors.keys()):
    all_authors[i]['coauthors']=list(all_authors[i]['coauthors'])


# In[10]:

from json import dumps
json = dumps(list(all_authors.values()))
f = open(path_to+"authors_wos.json","w")
f.write(json)
f.close()

# from json import dumps
# json = dumps(all_authors)
# f = open("authors_wos.json","w")
# f.write(json)
# f.close()


# In[11]:

# for i in all_authors.keys():
#     if all_authors[i]['num_articles']>1:
#         print(all_authors[i])
        

