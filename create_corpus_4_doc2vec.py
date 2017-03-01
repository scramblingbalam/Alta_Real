import json
import os

train_dir = "Data/semeval2017-task8-dataset"
train_dic_dir = "traindev"

train_data_dir ="rumoureval-data"
rumor_dirs =    {"charlie_hebdo": "charliehebdo",
				 "ebola-essien": "ebola-essien",
				 "ferguson": "ferguson",
				 "germanwings-crash": "germanwings-crash",
				 "ottawa_shooting": "ottawashooting",
				 "prince-toronto": "prince-toronto",
				 "putinmissing": "putinmissing",
				 "sydney_siege": "sydneysiege" 
				}

ferguson_1 = "498280126254428160"
ferguson_2 = "498430783699554305"

structutr_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1,"structure.json"])
source_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_2,"source-tweet","498280126254428160.json"])
ferg_1_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1])
ferg_2_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_2])


top_path = "/".join([train_dir,train_data_dir])
top_path = ferg_1_path 

walk = os.walk(top_path)
for current_dir in walk:
	last_dir = current_dir[0].split("\\")[-1]
	if last_dir == "source-tweet" or last_dir == "replies":
		for json_path in current_dir[-1]:
			with open(current_dir[0]+"\\"+json_path,"r")as jsonfile:
				filedic = json.load(jsonfile)
				print filedic["text"].encode("UTF-8")
				print filedic["id"]
				# for k,v in filedic.items():
				# 	print k
				# 	print v
				# 	print "\t",last_dir

# for k,v in filedic.items():
# 	print k
# 	print v
# 	print "\n"
