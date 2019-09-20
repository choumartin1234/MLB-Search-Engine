# coding:utf-8
import jieba
import jieba.posseg as pseg
import os
import sys
import json
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer



punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖
        •·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
filterpunc = lambda s: ''.join(filter(lambda x: x not in punct, s))

PATH = '../getNews/getNews/data.json'
LINES = open(PATH,'r', encoding='utf-8').readlines()
corpus = []
for i in range(20000,25000):
    temp = json.loads(LINES[i])
    t = jieba.lcut(filterpunc(temp['title']))
    c = jieba.lcut(filterpunc(temp['content']))
    s = ""
    for w in t:
    	s = s + w + " "
    for w in c:
    	s = s + w + " "
    corpus.append(s)
vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
f = open('tfidf4.txt','w',encoding='utf-8')
for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    f.write("-------这里输出第{}类文本的词语tf-idf权重------\n".format(i+20000))
    for j in range(len(word)):
    	if weight[i][j]!=0.0:
        	f.write("{},{}\n".format(word[j],weight[i][j]))
