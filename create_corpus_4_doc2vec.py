import json

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

structutr_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1,"structure.json"])
source_path = "/".join([train_dir,train_data_dir,rumor_dirs["ferguson"],ferguson_1,"source-tweet","498280126254428160.json"])



# filedic = {}
# with open(source_path,"r")as jsonfile:
# 	filedic= json.load(jsonfile)

# for k,v in filedic.items():
# 	print k
# 	print v
# 	print "\n"
