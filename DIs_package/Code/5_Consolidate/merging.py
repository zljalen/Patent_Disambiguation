# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:48:37 2016

@author: blowv6

Post-process.
Eliminate the over-splitted patents.
steps:
    1. find over-lapped patents
    2. choose a best-fit bucket(the smallest distance unless 0)
    3. delete from other buckets
Output:
    cluster files that are changed
    
*Deal with all data at once. May have memory problem
"""

import os
import os.path
from sklearn.cluster import KMeans
import numpy
import time

from vectorization_nospace import vectorize

start = time.clock()
label_path = "../../data/Clus/"

#load labeled imfromation

#record block path
input_subpath = []
for (dirpath, dirnames, filenames) in os.walk(label_path):
    for n in dirnames:
        p = os.path.join(dirpath,n)
        input_subpath.append(p)

#patent ID(string): files path(list)
over_lap = {}

#file(string):number of clusters(int)
clusters = {}

#iterate each Block(A,B,C,...)
for i in input_subpath:
    count = 0
    patent_id = {}
    #record patent IDs, and find duplicate patents
    for (dirpath, dirnames, filenames) in os.walk(i):
        if dirpath[-1] != None:
            for n in filenames:
                #string:string
                p = os.path.join(dirpath,n)
                with open(p) as f:
                    lines = f.readlines()
                max_cluster = 1
                for l in lines:
                    # format: label, patent ID, name
                    l = l.strip().split('\t')
                    max_cluster = max(max_cluster,int(l[0])+1)
                    clusters[p.split("Clus")[1].split("\\")[1]] = max_cluster
                    if l[1] not in patent_id:
                        patent_id[l[1]] = p.split("Clus")[1].split("\\")[1]
                    else:
                        # this patent is overlapped with and previous one
                        # if it is has not been recorded, add previous
                        # then, update the record
                        if l[1] not in over_lap:
                            over_lap[l[1]] = [patent_id[l[1]]]
                        over_lap[l[1]].append(p.split("Clus")[1].split("\\")[1])
            
                #show progress
                if not count%100:
                    print(dirpath[-1], count*1./len(filenames))
                count += 1
# all the duplicate patents are recond in over_lap

#update label

count = 0
for patent in over_lap:
    if not count%10:
        print(count*1./len(over_lap))
    count += 1
    # the param file_index is the index of over_lap file 
    file_index = 0
    merge_lines = []

    for fn in over_lap[patent]:
        if file_index == 0:
            # this is the first file
            # find the maxium label
            target_file_name = fn
            # the file formate is:
            #    label  ID  raw_name
            label = 0
            with open(label_path+fn[0]+'/'+fn+'Clus.txt','r') as f:
                lines = f.readlines()
            for line in lines:
                split_line = line.strip().split('\t')
                label = max(label,int(split_line[0]))
        else:
            label = str(int(label)+1)
            #other file
            with open(label_path+fn[0]+'/'+fn+'Clus.txt','r') as f:
                lines = f.readlines()
            #find the group that need to be delated
            for line in lines:
                split_line = line.strip().split('\t')
                if split_line[1] == patent:
                    delate_label = split_line[0]
                    break
            #new_lines stored the patents remains in the backet
            #merge_lines stored the patents added to the first file
            new_lines = []
            for line in lines:
                split_line = line.strip().split('\t')
                if split_line[0] != delate_label:
                    new_lines.append(line)
                else:
                    split_line[0] = str(label)
                    line = '\t'.join(split_line)
                    line += '\n'
                    merge_lines.append(line)
            label = str(int(label)+1) 
            #write the new file
            with open(label_path+fn[0]+'/'+fn+'Clus.txt','w') as f:
                f.writelines(new_lines)
                
        file_index += 1
    #write the fisrt file
    exist_patent=[]
    with open(label_path+fn[0]+'/'+target_file_name+'Clus.txt','r') as f:
        lines = f.readlines()
    with open(label_path+fn[0]+'/'+target_file_name+'Clus.txt','a') as f:
        for line in lines:
            split_line = line.strip().split('\t')
            exist_patent.append(split_line[1])
        for line in merge_lines:
            split_line = line.strip().split('\t')
            if split_line[1] not in exist_patent:
                f.writelines(line)
                exist_patent.append(split_line[1])
            
    
 
end = time.clock()
computing_time = end - start
print(computing_time)