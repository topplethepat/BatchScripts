# goes through directory of JSON files, extracts words and writes to a txt file

# python get_txt_from_json.py /path_to_json_directory

word_List = []

def json2text_one(filepath):
	i = 0
	with open(filepath,'r') as jsonfile:
		jsondata = json.load(jsonfile)
		length_list = len(jsondata['transcript']['words'])
		print(length_list)
		
		while i < length_list:
			words = (jsondata['transcript']['words'][i]['w'])
			word_List.append(words)
			i += 1
			for word in word_List:
			
				with open (filepath + '.txt','a') as results_file:
				#print (results_file)
					text1 = re.sub(r'Agent','',word)
					text2 = re.sub(r'Caller','',text1)
					text3 = re.sub(r'Customer','',text2)			
					results_file.write(str(text3 + ' '))
							
			word_List[:] = []

def get_words_from_json(directory_path):
	for file in sorted(os.listdir(sys.argv[1])):

		if file.endswith(".json"):
			#try:
			filename = os.path.join(sys.argv[1], file)
			print (filename)
			#with io.open(filename, mode='r') as jsonfile:
			json2text_one(filename)



get_words_from_json(sys.argv[1])