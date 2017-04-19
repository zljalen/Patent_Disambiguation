#===== Label each file for all data after clustering ====
import os
import os.path

#=========== To find all files in a directory ==========
def find_filelist(input_path):
	filelist = []
	for (dirpath, dirnames, filenames) in os.walk(input_path):
		for fn in filenames:
			if fn[0] != "." :								# This is to ignore hidden files
				filelist.append(fn)
	return filelist

def label_to_file(clus_file,label_file):
	with open(clus_file,"r") as infile:
		content = infile.readlines()
	patent_id = []
	assignee_name = []
	st_name = []
	for i in range(len(content)):
		patent_id.append(content[i].split('\t')[0])
		assignee_name.append(content[i].split('\t')[1])
		st_name.append(content[i].split('\t')[2].rstrip())
	#==========No new label for now ========
	st_dict = {}
	st_name_check = []
	group_id = -1
	#========= Build a dictionary =======
	for i in range(len(content)):
		if st_name[i] not in st_name_check:
			st_name_check.append(st_name[i])
			group_id += 1
			st_dict[st_name[i]] = group_id
	#======== new file with group ID =====
	with open(label_file,"w") as outfile:
		for i in range(len(content)):
			outfile.write(str(st_dict[st_name[i]])+"\t"+patent_id[i]+"\t"+assignee_name[i]+"\t"+st_name[i]+"\n")
	return

if __name__ == "__main__":
	input_path = "./Clus/"

	dir_list1 = os.listdir(input_path)                        # list all directories (A,B,C,D)
	for directory in dir_list1:
		print(directory)
		filelist = find_filelist(input_path+directory)                    # list all files under each directory A/(A1,A2,A3)
		for file in filelist:
			input_file = input_path + directory + "/" + file
			output_path = "./Clus_Label/" + directory + "/"
			if not os.path.isdir(output_path):
				os.makedirs(output_path)
			output_file = output_path + file
			label_to_file(input_file,output_file)


