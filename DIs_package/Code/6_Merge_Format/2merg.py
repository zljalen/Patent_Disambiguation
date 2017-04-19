
import os
import os.path

##  Merge all files and convert it to csv file ####

input_path  = "./Clus_merge_fuzz/"



def find_filelist(input_path):
	filelist = []
	for (dirpath, dirnames, filenames) in os.walk(input_path):
		for fn in filenames:
			if fn[0] != "." :								# This is to ignore hidden files
				filelist.append(fn)
	return filelist

if __name__ =="__main__":
	dir_list = os.listdir(input_path)                        # list all directories
	dir_list.remove('.DS_Store')

	with open('result_fuzz.txt','w') as outfile:
		outfile.write("patent_id"+"\t"+"raw_name"+"\t"+"st_name"+"\t"+"1_or_0"+"\t"+"str_similar")
		for dirname in dir_list:
			filelist = find_filelist(input_path+dirname+"/")
			for fname in filelist:
				with open(input_path+dirname+"/"+fname,"r") as infile:
					for line in infile:
						outfile.write(line)



import pandas as pd
data = pd.read_csv("result_fuzz.txt",sep="\t")
data.to_csv("final_result.csv")


