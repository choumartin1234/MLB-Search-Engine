# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from collections import defaultdict
import json
import jieba
import time
class News:
    def __init__(self,title, date, content, link,tfidf = 0):
        self.title = title
        self.date = date
        self.content = content
        self.link = link
        self.tfidf = tfidf
class Team:
    def __init__(self, name, time, place,content, P,C,IF,OF,DH,link,num=0):
        self.name = name
        self.time = time
        self.place = place
        self.content = content
        self.P = P
        self.C=C
        self.IF=IF
        self.OF=OF
        self.DH=DH
        self.link = link
        self.num = num
        self.icon = ""

Teamlist = []
PATH = '../getNews/getNews/team.json'
TEAM = open(PATH,'r', encoding='utf_8').readlines()
for i in range(0,30):
    temp = json.loads(TEAM[i])
    team = Team(temp['name'],temp['time'],temp['place'],temp['content'],temp['P'],temp['C'], temp['IF'], temp['OF'],
                 temp['DH'],'/team/'+str(i))
    team.icon = "/static/"+str(i)+".png"
    Teamlist.append(team)

Newslist = []
n = 0
PATH = '../getNews/getNews/data.json'
NEWS = open(PATH,'r', encoding='utf_8').readlines()
for i in range(0,20000):
    temp = json.loads(NEWS[i])
    new = News(temp['title'],temp['date'],temp['content'],"/news/"+str(i))
    Newslist.append(new)

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖
        •·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
filterpunc = lambda s: ''.join(filter(lambda x: x not in punct, s))

#分詞 + 倒排索引
jieba.load_userdict('mlbdict.txt')
InvertedIndexMap = defaultdict(set)
for i in range(0,len(Newslist)):
    tit = Newslist[i].title
    content = Newslist[i].content
    twords = jieba.lcut(filterpunc(tit))
    for word in twords:
        InvertedIndexMap[word].add(i)
    for team in Teamlist:
        if content.find(team.name) != -1:
            InvertedIndexMap[team.name].add(i)

#tf-idf值
cnt = 0
tfidf = []
dic = {}
f = open('tfidf.txt','r',encoding = 'utf-8')
Lines = f.readlines()
for i in range(0,len(Lines)):
    if Lines[i].find('----') != -1:
        tfidf.append(dic)
        cnt += 1
        dic = {}
    else:
        words = Lines[i].split(',')
        words[1] = words[1].replace('\n',"")
        dic[words[0]] = float(words[1])
f2 = open('tfidf2.txt','r',encoding = 'utf-8')
Lines = f2.readlines()
for i in range(0,len(Lines)):
    if Lines[i].find('----') != -1:
        tfidf.append(dic)
        cnt += 1
        dic = {}
    else:
        words = Lines[i].split(',')
        words[1] = words[1].replace('\n',"")
        dic[words[0]] = float(words[1])
f3 = open('tfidf3.txt','r',encoding = 'utf-8')
Lines = f3.readlines()
for i in range(0,len(Lines)):
    if Lines[i].find('----') != -1:
        tfidf.append(dic)
        cnt += 1
        dic = {}
    else:
        words = Lines[i].split(',')
        words[1] = words[1].replace('\n',"")
        dic[words[0]] = float(words[1])

for i in range(0,len(Lines)):
    if Lines[i].find('----') != -1:
        tfidf.append(dic)
        cnt += 1
        dic = {}
    else:
        words = Lines[i].split(',')
        words[1] = words[1].replace('\n',"")
        dic[words[0]] = float(words[1])
class Item:
    def __init__(self,url,name):
        self.url = url
        self.name = name

tlist = [
    Item('/','首頁'),
    Item('/teamlist/','球隊一覽'),
    Item('/rank/','熱搜排行'),
    Item('/zex/','關於作者')
]
default_dic = {
    'toolbar':tlist,
}

related_news = []
related_num = []
#熱搜
for i in range(0,30):
    temp = []
    for j in InvertedIndexMap[Teamlist[i].name]:
        temp.append(Newslist[j])
    related_news.append(temp)
    related_num.append((len(temp),i))
    Teamlist[i].num = len(temp)

related_num.sort(reverse=True)

def rank(request):
    sorted_team = []
    for (i,j) in related_num:
        sorted_team.append(Teamlist[j])
        #print(i,j,Teamlist[j].name)
    dic = {
        'toolbar': tlist,
        'web_title':  "熱搜排行榜",
        'teams':sorted_team,
    }
    return render(request,'rank.html',dic)


def search(request):
    if request.POST.get('status') == "T":
        startscrape()
    elif request.POST.get('status') == 'F':
        endscrape()
    text = str(request.GET.get('input_text'))
    if 'page_num' in request.GET:
        page_num = int(request.GET.get('page_num'))
    else:
        page_num = 1

    words = jieba.lcut_for_search(text)
    ls = []
    start = time.time()
    for i in range(0,20000):
        num = 0
        for word in words:
            num += tfidf[i].get(word,0)
        if (num != 0):
            ls.append((num,i))
    end = time.time()
    lst = sorted(ls,reverse=True)
    #print(lst)
    if len(lst) <= (page_num - 1) * 10:
        return HttpResponse("已無更多搜索結果 !")
    startpos = (page_num - 1) * 10
    endpos = min(10 * page_num, len(lst))
    searchlist = []
    for i in range(startpos,endpos):
        (n,x) = lst[i]
        tp = Newslist[x]
        searchlist.append(News(tp.title,tp.date,tp.content,tp.link,n))

    for i in range(0,endpos-startpos):
        for keyword in words:
            keyword = str(keyword) #記得python中的string不可變, 要重新附值
            searchlist[i].title = searchlist[i].title.replace(keyword, "<span class = 'highlight'>" + keyword + "</span>")
            searchlist[i].content = searchlist[i].content.replace(keyword, "<span class = 'highlight'>" + keyword + "</span>")
            #print(searchlist[i].title)
            #print(Newslist[i].title)
    page_bef = max(1, page_num - 4)
    last = (len(lst)-1) // 10 + 1
    page_aft = min(last , page_num + 4)
    page_total = []
    if page_bef > 1:
        page_total.append(Item("/search?input_text={:s}&page_num=1".format(text),"首頁"))
    for num in range(page_bef, page_aft+1):
        page_total.append(Item("/search?input_text={:s}&page_num={:d}".format(text, num), str(num)))
    if page_aft < last:
        page_total.append(Item("/search?input_text={:s}&page_num={:d}".format(text, last), "末頁"))
    dic = {
        'toolbar': tlist,
        'web_title': request.GET['input_text'] + " 搜索结果",
        'search_count': str(len(lst)),
        'search_time': str(end-start),
        'news': searchlist,
        'page_total': page_total,
        'text':text,
    }
    return render(request, 'search.html', dic)

def home(request):
    if 'input_text' in request.GET:
        return search(request)
    else:
        return render(request,'home.html',default_dic)

def zex(request):
        return render(request,'zex.html',default_dic)

def news(request):
    num = (int)(request.path[6:])
    new = Newslist[num]
    par = new.content.split('\n')
    title = new.title
    text = ""
    for p in par:
        text = text+p+ "<br></br>"
    #替换关键词
    for team in Teamlist:
        url = team.link
        text = text.replace(team.name, "<a href="+url+">"+team.name+"</a>")
        for P in team.P:
            text = text.replace(P, "<a href=" + url + ">" + P + "</a>")
        for C in team.C:
            text = text.replace(C, "<a href=" + url + ">" + C + "</a>")
        for OF in team.OF:
            text = text.replace(OF, "<a href=" + url + ">" + OF + "</a>")
        for IF in team.IF:
            text = text.replace(IF, "<a href=" + url + ">" + IF + "</a>")
        for DH in team.DH:
            text = text.replace(IF, "<a href=" + url + ">" + DH + "</a>")
    dic = {
        'toolbar': tlist,
        'web_title': "新聞" + str(num),
        'title': title,
        'date': new.date,
        'text': text,
    }
    return render(request,'news.html',dic)




def team(request):
    num = (int)(request.path[6:])
    team = Teamlist[num]
    news = []
    for i in InvertedIndexMap[team.name]:
        tp = Newslist[i]
        news.append(News(tp.title,tp.date,tp.content[0:80]+"......",tp.link))
    if 'page_num' in request.GET:
        page_num = int(request.GET.get('page_num'))
    else:
        page_num = 1
    startpos = (page_num - 1) * 10
    endpos = min(10 * page_num, len(news))
    currentlist = []
    for i in range(startpos,endpos):
        currentlist.append(news[i])

    page_bef = max(1, page_num - 4)
    last = len(news) // 10 + 1
    page_aft = min(last, page_num + 4)
    page_total = []
    if page_bef > 1:
        page_total.append(Item("/team/"+str(num)+"?page_num=1", "首頁"))
    for n in range(page_bef, page_aft + 1):
        page_total.append(Item("/team/"+str(num)+"?page_num={:d}".format(n), str(n)))
    if page_aft < last:
        page_total.append(Item("/team/"+str(num)+"?page_num={:d}".format(last), "末页"))
    dic = {
        'toolbar': tlist,
        'web_title': "球隊" + str(num),
        'team':team,
        'num':num,
        'news':currentlist,
        'page_total': page_total,
    }
    return render(request,'team.html',dic)

def teamlist(request):
    dic = {
        'toolbar' : tlist,
        'web_title': "球隊一覽",
        "teams": Teamlist,
    }
    return render(request, 'teamlist.html',dic)