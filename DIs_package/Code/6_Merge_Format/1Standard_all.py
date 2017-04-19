import os
import os.path
from collections import defaultdict
from fuzzywuzzy import fuzz

#####   Rewrite all data for final data format  ####
#####	Dataformat  ###
#####  patent_id	raw_name	standard_name	1_0		string_similarity   ####
#### change the input_path in main function

def find_filelist(input_path):
	filelist = []
	for (dirpath, dirnames, filenames) in os.walk(input_path):
		for fn in filenames:
			if fn[0] != "." :								# This is to ignore hidden files
				filelist.append(fn)
	return filelist

def lab_assignees(filename):
	with open(filename,"r") as infile:
		content = infile.readlines()
	label_list = []
	patent_id = []
	assignee_name = []
	for i in range(len(content)):
		label_list.append(content[i].split('\t')[0])
		patent_id.append(content[i].split('\t')[1])
		assignee_name.append(content[i].rstrip().split('\t')[2].split('+')[0])
	return patent_id,label_list, assignee_name

def dict_def(label_list,assignee_name):
	d = defaultdict(list)
	for i in range(len(label_list)):
		d[label_list[i]].append(assignee_name[i].rstrip())
	return d
	
def most_common(lst):
    return max(set(lst), key=lst.count)


if __name__ == "__main__":
	input_path = "./Clus_merge_fuzz/"
	dir_list = os.listdir(input_path)                        # list all directories
	for i in range(len(dir_list)):
		print(dir_list[i])
		filelist = find_filelist(input_path+dir_list[i])    # list all files under directory for initial data (A1,A2,A3)
		for j in range(len(filelist)):
			print(filelist[j])
			filename = input_path + dir_list[i] + "/" +filelist[j]
			if os.stat(filename).st_size > 0:
				patent_id,label_list,assignee_name = lab_assignees(filename)
				d = dict_def(label_list,assignee_name)
				with open(filename,'w') as myfile:
						for k in range(len(patent_id)):
							stardard_name = most_common(d[label_list[k]])
							if stardard_name == assignee_name[k]:
								myfile.write(patent_id[k]+'\t'+assignee_name[k]+'\t'+stardard_name+'\t'+'1'+'\t'+str(fuzz.ratio(stardard_name,assignee_name[k]))+'\n')
							else:
								myfile.write(patent_id[k]+'\t'+assignee_name[k]+'\t'+stardard_name+'\t'+'0'+'\t'+str(fuzz.ratio(stardard_name,assignee_name[k]))+'\n')
			else:
				with open("empty.txt",'a') as myfile2:
					myfile2.write(filelist[j]+'\n')


