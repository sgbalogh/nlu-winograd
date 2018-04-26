from nltk import pos_tag, word_tokenize
import wnlu.translate

def accusative(pronoun):
	"""
	Method to convert a pronoun to accusative form
	"""
	if pronoun == 'she':
		return 'her'
	elif pronoun == 'he':
		return 'him'
	elif pronoun == 'they':
		return 'them'
	else:
		return pronoun
		
def nominative(pronoun):
	"""
	Method to convert a pronoun to nominative form
	"""
	if pronoun == 'her':
		return 'she'
	elif pronoun == 'him':
		return 'he'
	elif pronoun == 'them':
		return 'they'
	else:
		return pronoun


def make_noun(word):
	"""
	Method to convert retrieve nouns from variants such as possession 
	"""
	if word.endswith('\'s'):
		word = word.replace('\'s','',1)
	return word
	
	
def cleanup(sentence,connective):
	"""
	Method to properly format options by removing errors during paraphrasing, capitalising and lowercasing where appropriate 
	"""
	cleaned_sentence = sentence.replace('her\'s','her')
	cleaned_sentence = cleaned_sentence.replace('him\'s','his')
	cleaned_sentence = cleaned_sentence.replace('them\'s','their')
	cleaned_sentence = cleaned_sentence.replace('he\'s','his')
	cleaned_sentence = cleaned_sentence.replace('she\'s','her')
	cleaned_sentence = cleaned_sentence.replace('they\'s','their')
	cleaned_sentence = cleaned_sentence.strip()
	split = cleaned_sentence.split()
	if split[-1] == connective and connective != 'that':
		split = split[:-1]
	elif split[-2] + " " + split[-1] == connective:
		split = split[:-2]
	cleaned_sentence = ''
	for word in split:
		cleaned_sentence = cleaned_sentence + " " + word
	cleaned_sentence = cleaned_sentence.strip()
	if cleaned_sentence[-1] == ',':
		cleaned_sentence = cleaned_sentence[:-1] + '.'
	elif cleaned_sentence[-1] != '.':
		cleaned_sentence = cleaned_sentence + '.'
	pos = pos_tag(cleaned_sentence.split())
	cleaned_sentence = ''
	for i,word in enumerate(pos):
		if word[1] not in ['NNP','NNPS','JJ','VB','VBZ'] and i != 0 and word[0] not in ['I']:
			cleaned_sentence = cleaned_sentence + " " + word[0].lower()
		else:
			 cleaned_sentence = cleaned_sentence + " " + word[0]
	pos = pos_tag(cleaned_sentence.split())
	cleaned_sentence = ''
	for i,word in enumerate(pos):
		if word[0] in ['Then'] and i == 0:
			cleaned_sentence = cleaned_sentence
		else:
			cleaned_sentence = cleaned_sentence + " " + word[0]

	cleaned_sentence = cleaned_sentence.strip()
	cleaned_sentence = cleaned_sentence[:1].upper() + cleaned_sentence[1:] 
	return cleaned_sentence

def get_noun_phrase(noun,premise):
	"""
	Method to convert a noun as found in the truncated form of the hypothesis to its full form as found in the premise
	"""
	new_noun = ''
	m = noun.split()
	for i, word in enumerate(premise.split()):
		if len(m) > 1:
			if m[1] == word:
				pos = pos_tag([premise.split()[i-1],word])
				if pos[0][1] in ['JJ','NN']:
					new_noun = m[0] + " " + premise.split()[i-1] + " " + word
				elif pos[0][1] == 'PRP$':
					new_noun = premise.split()[i-1] + " " + word
	return new_noun

def get_options(f,dataset):
	"""
	Method to accumulate options for each premise-hypothesis pair under consideration
	"""
	for instance in dataset:
		i,k = 0,0
		string_end = True
		option1,option2,option3,option4 = '','','',''
		remainder,truncated,noun,new_noun,hypothesis,nounupper = [],[],[],[],[],[]
		remainder3 = ''
		for z in range(2):
			remainder.append('')
			truncated.append('')
			noun.append('')
			new_noun.append('')
			nounupper.append('')
			hypothesis.append('')
		premise = instance.get_premise()
		variant_generator = wnlu.SentenceVariants()
		if premise[-2] == ' ':
			premise = premise[:-2] + '.'
		if premise[-1] not in ['.','!']:
			premise = premise + '.'
	
		#format premise to remove redundant spaces
		if premise.count('.') == 2:
			sentence_split = premise.split('.')
			sentence_split[1] = sentence_split[1][:2].upper() + sentence_split[1][2:]
			premise = sentence_split[0] + "." + sentence_split[1] + "."
				
		premise_split = premise.split()
		possible_translations = instance.get_candidate_translations()
		
		#get pronoun reference to be solved
		for z in range(2):
			hypothesis[z] = possible_translations[z].split()
		for word in premise_split:
			if word == hypothesis[0][i]:
				i = i + 1
			else:
				break
		for j in range(i,len(hypothesis[0])):
			truncated[0] = truncated[0] + " " + hypothesis[0][j]
		for j in range(0,i):
			remainder[0] = remainder[0] + " " + premise_split[j]
		
		
		for word in premise_split:
			if word == hypothesis[1][k]:
				k = k + 1
			else:
				break
	
		for l in range(k,len(hypothesis[1])):
			truncated[1] = truncated[1] + " " + hypothesis[1][l]
		for l in range(0,k):
			remainder[1] = remainder[1] + " " + premise_split[l]
		
		for z in range(2):
			truncated[z] = truncated[z].strip()
			remainder[z] = remainder[z].strip()
		#pronoun_index = variant_generator.identify_pronoun_index(premise, possible_translations[0])
		pronoun = premise_split[i]
		pronoun = pronoun.strip()
		pronoun = pronoun.strip('.')
		
		#get connective of hypotheses
		connective = pos_tag(premise_split)[i-1]
		i = i - 1
		while '.' not in connective[0] and ',' not in connective[0] and (connective[0] in ['over','around','through','in'] or connective[1] not in ['IN','CC']):
			remainder3 = premise_split[i] + " " + remainder3
			i = i - 1
			connective = pos_tag(premise_split)[i]

		remainder3 = remainder3.strip()
		if remainder3 != '':
			for z in range(2):
				truncated[z] = remainder3 + " " + truncated[z]
				remainder[z] = remainder[z].replace(remainder3,'')
				remainder[z] = remainder[z].strip()
		for z in range(2):
			remainder[z] = remainder[z].strip()
			truncated[z] = truncated[z][:1].upper() + truncated[z][1:]
			
		#get the nouns the pronoun reference is referring to
		diff = len(hypothesis[0]) - len(premise_split)
		q = 0
		while diff > 0:
			noun[0] = noun[0] + " " + hypothesis[0][k + q]
			diff -= 1
			q += 1
		if diff <= 0:
			noun[0] = noun[0] + " " + hypothesis[0][k + q]
		
		diff = len(hypothesis[1]) - len(premise_split)
		q = 0
		while diff > 0:
			noun[1] = noun[1] + " " + hypothesis[1][k + q]
			diff -= 1
			q += 1
		if diff <= 0:
			noun[1] = noun[1] + " " + hypothesis[1][k + q]
		
		#replace truncated nouns with full noun phrases found in premise
		for z in range(2):
			noun[z] = noun[z].strip()
			noun[z] = noun[z].strip('.')
			nounupper[z] = noun[z][:1].upper() + noun[z][1:]
			if noun[z] not in premise:
				new_noun[z] = get_noun_phrase(noun[z],premise)
			if new_noun[z] != '':
				truncated[z] = truncated[z].replace(noun[z],new_noun[z])
				truncated[z] = truncated[z].replace(nounupper[z],new_noun[z])
				possible_translations[z] = possible_translations[z].replace(noun[z],new_noun[z])
				possible_translations[z] = possible_translations[z].replace(nounupper[z],new_noun[z])
				noun[z] = new_noun[z]
			noun[z] = noun[z].strip('.')
			truncated[z] = truncated[z][:-1]
		
		r = remainder[1].split(noun[1])
		if len(r) > 1:
			pos = pos_tag(r[1].split())
			string_end = False
			
		#Convert repeated nouns into pronouns 
		if noun[0].lower() in truncated[0].lower() or make_noun(noun[0].lower()) in truncated[0].lower():
			remainder[0] = remainder[0].replace(make_noun(noun[0]),nominative(pronoun),1)
			if noun[0] != nounupper[0]:
				remainder[0] = remainder[0].replace(nounupper[0],nominative(pronoun),1)
		if noun[1].lower() in truncated[1].lower() or make_noun(noun[1].lower()) in truncated[1].lower():
			if not string_end and pos[0][1] in ['VB','VBD','VBN','VBZ','VBG','VBP','MD']:
				remainder[1] = remainder[1].replace(make_noun(noun[1]),nominative(pronoun),1)
				if noun[1] != nounupper[1]:
					remainder[1] = remainder[1].replace(nounupper[1],nominative(pronoun),1)
			else:
				if accusative(pronoun) not in remainder[1].split() and '\'s' not in remainder[1]:
					remainder[1] = remainder[1].replace(make_noun(noun[1]),accusative(pronoun),1)
					if noun[1] != nounupper[1]:
						remainder[1] = remainder[1].replace(nounupper[1],accusative(pronoun),1)
		
		#If there are many commas in the remainders, get the clause from between the most recent commas
		for z in range(2):
			if ',' in remainder[z] and remainder[z].count(',') >= 2:
				remainder[z] = remainder[z].split(',')[1]
		
		#Remove so,too from truncations as they might distort the meaning
		pos = pos_tag(truncated[0].split())
		for z,word in enumerate(pos):
			if word[1] in ['JJ','JJR','RB']:
				if pos[z-1][0] in ['so','too']:
					truncated[0] = truncated[0].replace(' so ',' ',1)
					truncated[0] = truncated[0].replace(' too ',' ',1)
					truncated[1] = truncated[1].replace(' so ',' ',1)
					truncated[1] = truncated[1].replace(' too ',' ',1)
		
		#If the truncations repeat a noun, replace with pronoun	
		for z in range(2):
			if truncated[z].count(make_noun(noun[z])) > 1:
				truncated[z] = truncated[z].replace(noun[z],pronoun,1)
		
		#construct options based on connectives in hypotheses
		if connective[0] in ['because','since','as']:
			option1 = truncated[0] + " so " + remainder[0]
			option2 = truncated[1] + " so " + remainder[1]
			option1 = cleanup(option1,connective[0])
			option2 = cleanup(option2,connective[0])
			option3 = possible_translations[0]
			option4 = possible_translations[1]
			
		elif connective[0] in ['that']:
			option1 = truncated[0] + " so " + remainder[0]
			option2 = truncated[1] + " so " + remainder[1]
			option1 = cleanup(option1,connective[0])
			option2 = cleanup(option2,connective[0])
		
		elif connective[0] in ['hence','so','thus','therefore']:
			option1 = cleanup(truncated[0],connective[0])
			option2 = cleanup(truncated[1],connective[0])
		
		elif connective[0] in ['after']:
			option1 = truncated[0] + ", then " + remainder[0]
			option2 = truncated[1] + ", then " + remainder[1]
			option1 = cleanup(option1,connective[0])
			option2 = cleanup(option2,connective[0])
			option3 =  possible_translations[0]
			option4 =  possible_translations[1]
			
		elif connective[0] in ['then']:
			option1 = "After " + truncated[0] + ", " + remainder[0]
			option2 = "After " + truncated[1] + ", " + remainder[1]
			option1 = cleanup(option1,connective[0])
			option2 = cleanup(option2,connective[0])
			option3 =  possible_translations[0]
			option4 =  possible_translations[1]
		
		elif connective[0] in ['but']:
			option1 = cleanup(truncated[0],connective[0])
			option2 = cleanup(truncated[1],connective[0])

		elif premise_split[0] in ['If'] and connective[1] not in ['IN']:
			option1 = truncated[0] + " if " + remainder[0]
			option2 = truncated[1] + " if " + remainder[1]
			option1 = option1.replace('If','',1)
			option2 = option2.replace('If','',1)
			option1 = cleanup(option1,'')
			option2 = cleanup(option2,'')
			
		elif premise_split[0] in ['Because','Since','As'] and connective[1] not in ['IN']:
			option1 = truncated[0] + " because " + remainder[0]
			option2 = truncated[1] + " because " + remainder[1]
			option1 = option1.replace('Since','',1)
			option2 = option2.replace('Since','',1)
			option1 = option1.replace('Because','',1)
			option2 = option2.replace('Because','',1)
			option1 = option1.replace('As','',1)
			option2 = option2.replace('As','',1)
			option1 = cleanup(option1,'')
			option2 = cleanup(option2,'')
			option3 =  possible_translations[0]
			option4 =  possible_translations[1]
			
		elif connective[0] in ['until']:
			option1 = "Until " + truncated[0] + ", " + remainder[0]
			option2 = "Until " + truncated[1] + ", " + remainder[1]
			option1 = cleanup(option1,connective[0])
			option2 = cleanup(option2,connective[0])
			option3 =  possible_translations[0]
			option4 =  possible_translations[1]
			
		elif connective[0] == 'and':
			if premise.count(',') == 2:
				split = premise.split(',')
				truncated[0] = truncated[0][0].lower() + truncated[0][1:]
				truncated[1] = truncated[1][0].lower() + truncated[1][1:]
				option1 = split[1] + " and " + truncated[0]
				option2 = split[1] + " and " + truncated[1]
				option1 = cleanup(option1,connective[0])
				option2 = cleanup(option2,connective[0])
			else:
				option1 = possible_translations[0]
				option2 = possible_translations[1]
			
		elif connective[0] in ['though','although'] or (connective[0] == 'though' and premise_split[premise_split.index(connective[0]) - 1] == 'even'):
			option1 = truncated[0] + " but " + remainder[0]
			option2 = truncated[1] + " but " + remainder[1]
			if premise_split[premise_split.index(connective[0]) - 1] == 'even':
				connective = "even though"
			else:
				connective = connective[0]
			option1 = cleanup(option1,connective)
			option2 = cleanup(option2,connective)
			
		elif premise.count('.') == 1:
			option1 = possible_translations[0]
			option2 = possible_translations[1]


		#print premise-hypothesis options to file to be fed into the model
		if premise.count('.') == 1:
			f.write(premise + "\n")
			f.write(option1 + "\n")
			if instance.gold_answer_idx == 0:
				f.write('entailment\n')
			else:
				f.write('neutral\n')
			f.write(premise + "\n")
			f.write(option2 + "\n")
			if instance.gold_answer_idx == 1:
				f.write('entailment\n')
			else:
				f.write('neutral\n')
			
			if option3 != '':
				f.write(premise + "\n")
				f.write(option3 + "\n")
				if instance.gold_answer_idx == 0:
					f.write('entailment\n')
				else:
					f.write('neutral\n')
				f.write(premise + "\n")
				f.write(option4 + "\n")
				if instance.gold_answer_idx == 1:
					f.write('entailment\n')
				else:
					f.write('neutral\n')
			f.write("\n")

		
loader = wnlu.WinogradLoader()
f = open('traindev.txt','w')
train_set = loader.get_train_set()
dev_set = loader.get_dev_set()
test_set = loader.get_test_set()
get_options(f,train_set)
get_options(f,dev_set)
#get_options(f,test_set)