# About the script:
# This script is used to prepare the folders for BIDScoin
# The script will move the raw data into the new folder 
# and rename the subfolders' names

# The orginal data from collaborators include two folders:
# "./rawdata/MRI/xiafa1"  which include data from subject 1 to 25;
# "./rawdata/MRI/xiafa01", which include data from subject 31 to 53;

# Data from the other folders "xiafa002" and "xiafaCompare" are either
# from other experiments or derived from "xiafa1".

# Because the dicom data in "xiafa1" does not include the scanning time, and 
# subject's id, all the subject's id was identified by the session time from
# the eprime file by Dr. Zhuang, the information was saved in the file
# "rawdata_subj_ID_based_on_session_time.csv". This may need further check 
# in the future.
# The layout of the folder is as follows:
# ./rawdata/MRI/xiafa1
#   |--- folderName
#   |      |--- 3D
#   |      |      |--- dicom files
#   |      |--- BOLD
#   |      |      |--- dicom files
#   |      |--- DTI
#   |      |      |--- dicom files
#   |      |--- GRE
#   |      |      |--- dicom files
#   |      |--- REST
#   |      |      |--- dicom files
#   |--- ...

# data from "xiafa01" already has subject's id as folder names, so we directly 
# copy and rename the folder for BIDScoin.
# the layout of the folder is a flat dicom folder:
# ./rawdata/MRI/xiafa01
#   |--- folderName
#   |      |--- dicom files
#   |--- ...

# revision history of this script:
# Time         Author      Description
# 2023-04-12   hcp4715     organized the script for the first time
# 2023-04-15   hcp4715     Re-structured the folder, all in  DICOM flat, no more pt1, pt2 for raw data.

# get all folders in old_dir
import os
import shutil
import glob
import pandas as pd

# original folder
old_dir0 = r"./rawdata/MRI/xiafa1"
old_dir1 = r"./rawdata/MRI/xiafa01"
new_dir = r"./DataAnalyses/rawdata"

####  prepare rawdata for subject 1 to 25 ####


df = pd.read_csv("./rawdata/rawdata_subj_ID_based_on_session_time.csv")
df = df.dropna(how='all')  # delete all empty rows

# convert "Subject" column to interger and then to string
df["Subject"] = df["Subject"].astype(int).astype(str)

# remove space in "Folder_name" column
df["Folder_name"] = df["Folder_name"].str.replace(" ", "")

# Copy sub-folders from old_dir0 to new_dir, 
# based on the "Folder_name" column in df,
# rename the sub-folders by adding prefix to the "Subject" column 
# if the lenght of "Subject" column is 1, add prefix "sub-00" to the "Subject" column,
# if the lenght of "Subject" column is 2, add prefix "sub-0" to the "Subject" column.

for i in range(len(df)):
    if len(df["Subject"][i]) == 1:
        old_dir = os.path.join(old_dir0, df["Folder_name"][i])
        # print(old_dir)
        new_dir_sub = os.path.join(new_dir, "sub-00" + df["Subject"][i])
        # print(new_dir_sub)
        shutil.copytree(old_dir, new_dir_sub)
    elif len(df["Subject"][i]) == 2:
        old_dir = os.path.join(old_dir0, df["Folder_name"][i])
        # print(old_dir)
        new_dir_sub = os.path.join(new_dir, "sub-0" + df["Subject"][i])
        # print(new_dir_sub)
        shutil.copytree(old_dir, new_dir_sub)

# list all subfolders in "new_dir"
subfolders = os.listdir(new_dir)

# for each subfolder in "subfolders",
# check the sub-folders inside, if the sub-folder's names are in lower cases,
# change it to upper cases
# if no sub-folders inside, skip it
for subfolder in subfolders:
    subfolder_dir = os.path.join(new_dir, subfolder)
    if os.path.isdir(subfolder_dir):
        subfolders1 = os.listdir(subfolder_dir)
        for subfolder1 in subfolders1:
            subfolder1_dir = os.path.join(subfolder_dir, subfolder1)
            # print(subfolder1_dir)
            if os.path.isdir(subfolder1_dir):
                subfolder1_new = subfolder1.upper()
                print(subfolder1_new)
                subfolder1_new_dir = os.path.join(subfolder_dir, subfolder1_new)
                os.rename(subfolder1_dir, subfolder1_new_dir)

# Make the folder structure as DICOM flat
# for each sub-folder in new_dir, if it contains sub-folders, move all files to the parent folder
# and rename the files by the following rules:
# if it is the first sub-folder, use the original file name,
# if it is the second sub-folder, replace the original file name with
# "1_" + the number of all files in the first sub-folder,
# if it is the third sub-folder, replace the original file name with
# "1_" + the number of all files in the first two sub-folders,
# so on and so forth.


# create a dataframe to store the number of files in each sub-folder,
# save both the sub-folder's path and number of files in the dataframe

# get all subfolders' names in new_dir
flist = glob.glob(new_dir + "/*")

# create a list to store the parent folder names
parent_dir = []

# create a list to store the old file name
old_file_name = []

# create a list to store the subject id
subj_id = []

# create a list to store the sub-folder name
scan = []

# create a list to store the number of files in each subfolder
num_files = []

# create a list to store the file name
file_name = []

# for each subfolder in flist, get the number of files in the subfolder
for i in range(len(flist)):
    if os.path.isdir(flist[i]):
        subfolders = glob.glob(flist[i] + "/*")
        # get the number of files in the subfolder
        for subfolder1 in subfolders:

            # get the file names in subfolder1 to a list
            file_list = glob.glob(subfolder1 + "/*")

            # for each file name, get the string after "1_"  and before ".dcm " in the file name
            # and append it to the file_name
            for file in file_list:
                file_name.append(file.split(os.path.sep)[-1].split("1_")[-1].split(".dcm")[0])
                # print(file.split(os.path.sep)[-1].split("1_")[-1].split(".dcm")[0])

                # get the parent folder's name and append to "parent_dir"
                # print(flist[i])
                parent_dir.append(flist[i])
                
                # get old file name with full path and append to "old_file_name"
                # print(file)
                old_file_name.append(file)
                
                # get the number of files in "subfolder1"
                # print(len(glob.glob(subfolder1 + "/*")))
                num_files.append(len(glob.glob(subfolder1 + "/*")))

                # get subfolder name in flist[i]
                subj_id.append(flist[i].split(os.path.sep)[-1][-3:])
                # print(flist[i].split(os.path.sep)[-1][-3:])

                # get the subolder name in subfolder1
                # print(subfolder1.split(os.path.sep)[-1])
                scan.append(subfolder1.split(os.path.sep)[-1])

# create a dataframe to store the information
df_fnum = pd.DataFrame({"subj_id": subj_id, "scan":scan,
                        "parent_folder": parent_dir,"old_file_name": old_file_name, 
                        "num_files": num_files, "file_name": file_name})

# in "df_fnun", change the subj_id to integer and sort by subj_id and scan:
df_fnum["subj_id"] = df_fnum["subj_id"].astype(int)
df_fnum["file_name"] = df_fnum["file_name"].astype(int)
df_fnum = df_fnum.sort_values(by = ["subj_id", "scan", "file_name"]).reset_index(drop = True)

# select "subj_id", "scan", "num_files" from df_fnum as a new dataframe,
# and keep only the unique rows
df_fnum_subj = df_fnum[["subj_id", "scan", "num_files"]].drop_duplicates()

# create a new column "cum_num_files" to store the cumulative number of files
# for each sub-folder of each subj_id in df_fnum_subj
df_fnum_subj["cum_num_files"] = df_fnum_subj.groupby("subj_id")["num_files"].cumsum()

# create a new column "scan_idx" to store the index of each scan, start form 1 to n,
# and grouped by subj_id:
df_fnum_subj["scan_idx"] = df_fnum_subj.groupby("subj_id").cumcount() + 1


# merge df_fnum_subj with df_fnum on "subj_id" and "scan" as a new dataframe
df_fnum_new = pd.merge(df_fnum, df_fnum_subj, on = ["subj_id", "scan", "num_files"])

# create a new column in df_fnum_new based the following condition:
# grouped by "subj_id",
# if "scan_idx" is 1, using value from "file_name",
# if "scan_idx" is not 1, using value from "file_name" + value from "cum_num_files" 
# that corresponding to "scan_idx" - 1:
df_fnum_new["new_file_name"] = df_fnum_new.apply(lambda x: x["file_name"] if x["scan_idx"] == 1 else x["file_name"] + df_fnum_new[(df_fnum_new["subj_id"] == x["subj_id"]) & (df_fnum_new["scan_idx"] == x["scan_idx"] - 1)]["cum_num_files"].values[0], axis = 1)

# create a column for the new file name by the following rules:
# "parent_folder/" + "new_file_name" + ".dcm" 
df_fnum_new["new_file_name_dir"] = df_fnum_new["parent_folder"] + "/" + df_fnum_new["new_file_name"].astype(str) + ".dcm"

# check "new_file_name" for subj_id == 1
df_fnum_new[df_fnum_new["subj_id"] == 7]

# loop through df_fnum_new, move files from "old_file_name" as "new_file_name_dir"
for i in range(len(df_fnum_new)):
    shutil.move(df_fnum_new["old_file_name"].iloc[i], df_fnum_new["new_file_name_dir"].iloc[i])

# check the subfolders inside the subfolders of newdir, if they are empty
# remove them
for i in range(len(flist)):
    subfolder1 = flist[i]
    for root, dirs, files in os.walk(subfolder1, topdown=False):
        for name in dirs:
            os.rmdir(os.path.join(root, name))


#### prepare rawdata for subject 31 to 53 ####

# get the file path and add "3D" to the end of the path
flist1 = glob.glob(old_dir1 + "/*" + os.path.sep + "3D")

# copy all files in flist1 to new folder, flist 2 has a different structure
# and rename the subfolders' name by extracting substring from the older folder name
# without the layer of older of "3D".
# rename the files by removing "1_" from the beginning of the file name

for dir in flist1:
    # get the subfolder name before "3D"
    new_name = dir.split(os.path.sep)[-2]

    # extract the first two characters of the subfolder name
    new_name = new_name[0:2]

    # add "sub-0" to the beginning of the subfolder name
    new_name = "sub-0" + new_name

    # create new folder using the new name
    new_dir_tmp = os.path.join(new_dir, new_name + "/")

    # new_subfolder1 = new_dir + "/" + subfolder1.split(os.path.sep)[-2]
    # print(new_dir_tmp)

    if not os.path.exists(new_dir_tmp):
        os.makedirs(new_dir_tmp)
    for root, dirs, files in os.walk(dir):
        for name in files:
            old_file_name = os.path.join(root, name)
            new_file_name = os.path.join(new_dir_tmp, name[2:])
            # print(old_file_name)
            # print(new_file_name)
            shutil.copy(old_file_name, new_file_name)

# get all subfolders' names in new_dir and number of files in each subfolder,
# and save the information to a csv file

# get all subfolders' names in new_dir
flist = glob.glob(new_dir + "/*")

# create a list to store the subfolder names
subfolder = []

# create a list to store the number of files in each subfolder
num_files = []

# for each subfolder in flist, get the number of files in the subfolder
for i in range(len(flist)):
    subfolder.append(flist[i].split(os.path.sep)[-1])
    num_files.append(len(glob.glob(flist[i] + "/*")))

# create a dataframe to store the information
df2 = pd.DataFrame({"subfolder": subfolder, "num_files": num_files})

# sort the dataframe by the number of files and reset the index
df2 = df2.sort_values(by = "num_files", ascending = False).reset_index(drop = True)

# save the dataframe to a csv file
df2.to_csv("./DataAnalyses/Subj_num_files_new.csv", index = False)