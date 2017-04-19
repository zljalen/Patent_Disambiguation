# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 14:50:09 2016

@author: blowv6

Usage:

from vectorization import vectorize
vector = vectorize(input_fname = "*.txt" )


input: patent data(txt file)
output: a tuple contanting: 
        [0]   : vector array
        [1]   : list of vectors that are not merged
        [2]   :data that was vectorized
        [3]   :words for each dimension
        [4]   : vectorized column
input data format:
[0]ID [1]Assignee_name [2]date [3,4,5]location [6]citation [7]CPC [8]Inventors 
[9]Examiner 

vect_dic = {"name":0,"location":1,"citation":2,"cpc":3,"inventor":4,"examiner":5}
"""
import numpy
 
from sklearn.feature_extraction.text import CountVectorizer

def vectorize(input_fname = "result.txt", array_tpye = "int8",feature = ("name","location","citation","cpc","inventor","examiner")):
    with open(input_fname,encoding = 'utf-8') as fr:
        raw_patent_data = fr.readlines()
    
    #The patent_id and GranrtDate are not to be vectorized, named: not_vect.
    #The name, location, citing and reference are to be vectorized, 
    #named: need_vect.
    
    #skip if contain only 1 assignee
    if len(raw_patent_data) == 1:
        return 0;
        
    not_vect = [[],[]] #ID,name,date
    need_vect = [[] for i in range(6)] #name location cpc inventor examiner
    vect_dic = {"name":0,"location":1,"citation":2,"cpc":3,"inventor":4,"examiner":5}
    for line in raw_patent_data:
        line = line.strip()#delete the '\n'
        line = line.replace('nan','')
        line = line.replace('NULL','')
        line = line.replace('N/A', '')
        line = line.split('\t')
        #ID and date,[0,2]
        not_vect[0].append(line[0])
        not_vect[1].append(line[2])
        #Name[1]; choose the first assignee name
        names = str.split(line[1],'+')
        #delate " "
        #remove space
        need_vect[0].append(names[0].replace(' ', ''))
#        need_vect[0].append(names[0])
        #Location[3-5]; choose the first assignee location
        for i in range(3,6):
            line[i] = str.split(line[i],'+')[0]
        location = ' '.join(line[3:6])
        need_vect[1].append(location)
        #Citing[6]
        citing = line[6].replace('+', ' ')
        need_vect[2].append(citing)
        #CPC[7]
        cpc = line[7].replace('+', ' ')
        need_vect[3].append(cpc)
        #Inventor[8], "+": different inventors, ";": different names
        #last name1;first name1+last name2;first name2...
        #regard the l+f name as a single name
        inventor = line[8].replace('; ', '')
        inventor = inventor.replace(' ', '')
        inventor = inventor.replace('+', ' ')
        need_vect[4].append(inventor)
        #Examiner[9], same as Inventor
        examiner = line[9].replace('; ', '')
        examiner = examiner.replace(' ', '')
        examiner = examiner.replace('+', ' ')
        need_vect[5].append(examiner)
    #Extracting data finished
    
    first_name = need_vect[0][0]
    go_on = False
    
    #skip if names are all the same
    for n in need_vect[0]:
        if n != first_name:
            go_on = True
            break
    if not go_on:
        return 0
    
    
    #Vectorize 5 attributes respectively
    vectorizer = CountVectorizer(dtype = array_tpye,token_pattern='\\b\\w+\\b')
    vect = []
    words_in_bag = []
    vectorize_item = []
    for i in feature:
        vectorize_item.append(vect_dic[i])
    for i in vectorize_item:
        empty = True;
        #check if this string is empty, like "  " or " "
        for item in need_vect[i]:
            if len(item.replace(' ','')) != 0:
                empty = False
                break
        if not empty:
            X = vectorizer.fit_transform(need_vect[i])
            feature_vec = X.toarray()
            vect.append(feature_vec)
            words_in_bag.append(vectorizer.get_feature_names())
            
    #Merge vectors into a single array
    vecterized = vect[1];
    for i in range(2,len(vect)):
        #exclude citing
        vecterized  = numpy.concatenate((vecterized,vect[i]),axis = 1)
    return (vecterized,vect,need_vect,words_in_bag,vectorize_item)
