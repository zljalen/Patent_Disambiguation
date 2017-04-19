#### K means clustering for each files in specific path
#### Also provide the standard name in clustring file 
#### Find the cluster numbers k before clustering
from sklearn.cluster import KMeans
import numpy as np
import os
import os.path
from collections import defaultdict

###########
# READ ME # Take care for the two input paths and output path in main function
########### 
#============= Function for building dictionary for label_list and assignee name =======
def dict_def(label_list,assignee_name):
	d = defaultdict(list)
	for i in range(len(label_list)):
		d[label_list[i]].append(assignee_name[i].rstrip())
	return d
#============= Function for finding the most common name in a group ======
def most_common(lst):
    return max(set(lst), key=lst.count)
#######################################
## Function about k-means start here ##
#######################################
#================Find the total distances under different cluster numbers=============
def total_distances(X,end):
	total_distances = []
	for i in range(1,end,1):
		kmeans = KMeans(n_clusters = i).fit(X)      	# Cluster under cluster numbers i
		total_distances.append(kmeans.inertia_)    		# Caculate the sum of samples' distance to cluster center
	return total_distances

#==============Find the number with the largest ratio===========
def k_find(dis_list):
	ratios = []                                    		# A list to store the ratio of two adjacent numbers
	for i in range(len(dis_list)-1):
		if dis_list[i+1] != 0:							# This condition is to remove the cluster numbers with total diatance = 0
			ratios.append(dis_list[i]/dis_list[i+1])
		else:
			ratios.append(1)
	if len(ratios) <= 1:
		k_index = len(dis_list)
	else:
		k_index = ratios.index(max(ratios))+1          		# Find the largest ratio and corresponding index in the total distances list
	return k_index 
#============== Cluster and Label accoring to original txt file and vector txt file ============
def Clustering(input_path1,input_path2,output_path,file_original,file_vector,file_Clustered):
	print(file_original)
	X = np.loadtxt(fname=(input_path2+file_vector),dtype="int8")		# Load vector file
	group_len = len(X)									# The length of vectors
	Y = total_distances(X,int(group_len))			    # Assume at most (group_len*0.5) clusters in a group
	k_cluster = k_find(Y) + 1							# Cluster numbers in a group
	kmeans_final = KMeans(n_clusters=k_cluster).fit(X)  # Cluster under number k_cluster
	label_list = kmeans_final.labels_ 					# Label list
	with open((input_path1+file_original),"r") as infile:
		patent_assignee = infile.readlines()
		patent_id = []
		assignee_name = []
		for i in range(len(patent_assignee)):
			patent_id.append(patent_assignee[i].split('\t')[0])
			assignee_name.append(patent_assignee[i].split('\t')[1])
	d = dict_def(label_list,assignee_name)             # For standard name
	#=========== Output lable index, patent id, assignee name in the clustered file ============ 
	# label_index = os.path.splitext(file_original)[0]		# Label index for different file, this is for final files merging
	# print(label_index)
	output_path_new = output_path+file_original[0]+"/"      # Put file under directory with initial letter
	if not os.path.isdir(output_path_new):
		os.makedirs(output_path_new)
	with open((output_path_new+file_Clustered),"w") as fw:
		for i in range(group_len):
			stardard_name = most_common(d[label_list[i]])
			#fw.write(str(label_index)+"_"+str(label_list[i])+"\t"+str(patent_id[i])+"\t"+str(assignee_name[i])+"\t"+stardard_name+"\n")
			fw.write(str(patent_id[i])+"\t"+str(assignee_name[i])+"\t"+stardard_name+"\n")
	return
#####################################
## Function about k-means end here ##
#####################################
#=============== For files no need to cluster ==================
def Copy_noclus_file(input_path1,output_path,file_original,file_Clustered):
	print(file_original)
	with open((input_path1+file_original),"r") as infile:
		patent_assignee = infile.readlines()
		patent_id = []
		assignee_name = []
		for i in range(len(patent_assignee)):
			patent_id.append(patent_assignee[i].split('\t')[0])
			assignee_name.append(patent_assignee[i].split('\t')[1])
	#=========== Output lable index, patent id, assignee name in the clustered file ============ 
	# label_index = os.path.splitext(file_original)[0]		# Label index for different file, this is for final files merging
	# print(label_index)
	group_len = len(assignee_name)
	output_path_new = output_path+file_original[0]+"/"      # Put file under directory with initial letter
	if not os.path.isdir(output_path_new):
		os.makedirs(output_path_new)
	with open((output_path_new+file_Clustered),"w") as fw:
		for i in range(group_len):
			stardard_name = assignee_name[0]       # In this situation, names in this file are all the same
			#fw.write(str(label_index)+"\t"+str(patent_id[i])+"\t"+str(assignee_name[i])+"\t"+stardard_name+"\n")
			fw.write(str(patent_id[i])+"\t"+str(assignee_name[i])+"\t"+stardard_name+"\n")

	return
#=========== To find all files in a directory ==========
def find_filelist(input_path):
	filelist = []
	for (dirpath, dirnames, filenames) in os.walk(input_path):
		for fn in filenames:
			if fn[0] != "." :								# This is to ignore hidden files
				filelist.append(fn)
	return filelist


if __name__ == "__main__":
	input_path1 = "./data_initial_letter/"
	input_path2 = "./vec_nospace/"
	output_path = "./Clus/"
	if not os.path.isdir(output_path):
		os.makedirs(output_path)
	dir_list1 = os.listdir(input_path1)                        # list all directories
	dir_list2 = os.listdir(input_path2)
	for i in range(len(dir_list1)):
		filelist1 = find_filelist(input_path1+dir_list1[i])    # list all files under directory for initial data (A1,A2,A3)
		vector_path = input_path2+dir_list1[i]+"vec/"          # vector path (Avec)
		filelist2 = find_filelist(vector_path)
		for j in range(len(filelist1)):
			vec_file = os.path.splitext(filelist1[j])[0] + "vec.txt"
			clus_file = os.path.splitext(filelist1[j])[0] + "Clus.txt"
			if vec_file in filelist2:									# Find a corresponding vector file 
				Clustering(input_path1+dir_list1[i]+"/",vector_path,output_path,filelist1[j],vec_file,clus_file)
			elif vec_file not in filelist2:
				Copy_noclus_file(input_path1+dir_list1[i]+"/",output_path,filelist1[j],clus_file)




