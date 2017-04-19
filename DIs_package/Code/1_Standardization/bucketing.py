#!/usr/bin/env python

def bbucket():
    '''
    File name: Random.Number.py
    Author: Zhechen Yan
    Date created: 10/21/2016
    Date last modified: 10/21/2016
    Python Version: 3.5.2
    Desc: Generate 10,000 random numbers. Build a 10000.txt based on result.txt.
    input type:
    path : str
    fields : list of str
    output : .txt file
    '''
    __author__ = "Zhechen Yan"
    __copyright__ = "Copyright 2016, Fung institute of Engineering, UC Berkeley"
    __credits__ = ["Zhechen Yan", "Jiahuan Chen", "Liangjing Zhu",
                        "Guancheng Li", "Lee Fleming"]
    __version__ = "0.0.1"
    __maintainer__ = "Zhechen Yan"
    __email__ = "harry.yan@berkeley.edu"
    __status__ = "Research"
    # dictionary to store the patent_id in alphabet order, patent_id to store the patent_id.
    dictionary = {}
    dictionary2 = {} # to store assignee names
    patent_id = []
    assignee_name = []
    # load the patent_id
    with open("./data/result.txt", "r") as f:
        context = f.readlines()
    for i in range(len(context)):
        patent_id.append(context[i].split('\t')[0])
        assignee_name.append(context[i].split('\t')[1].upper())

    # build the dictionary in alphabet order 
    # get 10000 samples so set the pace to 29.
    for i in range(0, len(patent_id)):
        if assignee_name[i].strip()[0] not in dictionary:
            dictionary[assignee_name[i].strip()[0]] = [patent_id[i]]#if not included, build a list
        else:
            dictionary[assignee_name[i].strip()[0]].append(patent_id[i])#if included, append the list
        dictionary2[patent_id[i]] = assignee_name[i].split('+')[0] # use the first assignee name
    # write the result
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    # example of keys: ['D', 'I', 'N', 'C', 'L', 'T']
    # an example of values: [['7155851', '7155893'], ['7155871'], ['7155750'], ['7155779'], ['7155776'], ['7155865', '7155884']]
    for i in range(len(keys)):
        with open('./distributed/'+keys[i]+'.txt', 'w') as fw:
            for j in range(len(values[i])):
                fw.writelines(values[i][j] + '\t' + dictionary2[values[i][j]] + '\n')
bbucket()