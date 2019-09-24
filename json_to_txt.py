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
				items_to_remove = ['Agent', 'Customer', 'Caller']
				for j in items_to_remove:
					word = word.replace(j,'')
				with open (filepath + '.txt','a') as results_file:
					results_file.write(word + ' ')
				
			word_List[:] = []

def get_words_from_json(directory_path):
	for file in sorted(os.listdir(sys.argv[1])):

		if file.endswith(".json"):
			filename = os.path.join(sys.argv[1], file)
			print (filename)

			json2text_one(filename)



get_words_from_json(sys.argv[1])