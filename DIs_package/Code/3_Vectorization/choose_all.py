# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:56:30 2016

@author: blowv6
"""
import numpy
import time
import os
import os.path

from vectorization_nospace import vectorize

# Add your input and output path.
input_path = "../../test8_1119/"
output_path = "../../test8_1119/vec_nospace/"
#input_path = "test/"
#output_path = "test_vect/"
error = []
skip_list = []
chosen_feature=("name","location","cpc","inventor","examiner")

#check and generate path
if not os.path.exists(output_path):
    os.makedirs(output_path)

input_subpath = []
output_subpath = []
for parent,dirnames,filenames in os.walk(input_path):
    for n in dirnames:
        p = os.path.join(parent,n)
        if len(p) == 18:
            input_subpath.append(p)
            output_subpath.append(output_path+p[-1]+"vec")
            if not os.path.exists(output_subpath[-1]):
                os.makedirs(output_subpath[-1])

letter = 0
for i in input_subpath:         
    count = 0
    #walk through 
    for parent,dirnames,filenames in os.walk(i):
        for n in filenames:
            fn = os.path.join(parent,n)
            try:
                vec = vectorize(fn,feature=chosen_feature)
                if vec:
                    numpy.savetxt(output_path + n[0]+"vec/"+ n[0:-4]+'vec'+n[-4:],X=vec[0],fmt = '%.0e')
                else:
                    skip_list.append(n+'\n')
    # show the progress
                if not count%100:
                    print(count*1./len(filenames)+letter)
                count += 1
            except:
                # print failed file name
                print(n)
                error.append(n)
    letter += 1

#write skipped file
with open(output_path+"skip.txt","w") as fr:
    fr.write(time.strftime('%Y-%m-%d,%H:%m',time.localtime()))
    fr.write('\n')
    fr.writelines(skip_list)
#write error file
with open(output_path+"errors.txt","w") as fr:
    fr.writelines(error)