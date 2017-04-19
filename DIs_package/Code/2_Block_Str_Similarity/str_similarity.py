#### Divided a txt file into multiple txt file according to string similarity ###
#### For example, the b.txt can be divided into more than 400 txt files with names 'b1.txt' to 'b430.txt'
#### Then we can vectorize the data in a group to do clustering
#################
#	Read Me 	#
#################
# Note the input_path and output_path
import os
from fuzzywuzzy import fuzz
import numpy as np
import os.path

def find_filelist(input_path):
	filelist = []
	for (dirpath, dirnames, filenames) in os.walk(input_path):
		for fn in filenames:
			if fn[0] != "." :								# This is to ignore hidden files
				filelist.append(fn)
	return filelist


input_path = "./distributed_all_att/"
filelist = find_filelist(input_path)
for k in range(len(filelist)):
	patent_id = []
	assignee_name =[]
	with open(input_path+filelist[k],'r') as myfile:
		patent_assignee = myfile.readlines()
	for i in range(len(patent_assignee)):
		assignee_name.append(patent_assignee[i].split('\t')[1])
	##============= Diveded in multiple txt files===================
	assignee_list = []      # Build a list to check the grouped assignees
	group_number = 0		
	for i in range(len(assignee_name)):
		if assignee_name[i] not in assignee_list:		# Check whether the assignee is in the list
			assignee_list.append(assignee_name[i])
			group_number += 1
			mypath = os.getcwd() + '/' + filelist[k][0] + '/'
			if not os.path.isdir(mypath):
				os.makedirs(mypath)
			with open(mypath + filelist[k][0]+str(group_number)+'.txt','w') as fw:
				fw.write(patent_assignee[i])
				for j in range(i+1,len(assignee_name)):
					assignee1 = str.split(assignee_name[i],'+')[0]
					assignee2 = str.split(assignee_name[j],'+')[0]
					if fuzz.ratio(assignee1,assignee2) >= 80:  # We should consider more about this percent
						assignee_list.append(assignee_name[j])
						fw.write(patent_assignee[j])










	