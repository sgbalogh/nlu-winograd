from nltk import pos_tag, word_tokenize, Tree
from nltk.parse.stanford import StanfordParser
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from wnlu.translate.Utils import Utils
from random import randint

class SentenceVariants:

	jar = 'apps/stanford-parser-full-2018-02-27/stanford-parser.jar'
	model = 'apps/stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar'
	parser = StanfordParser(model, jar, encoding='utf8')

	keywords_all = ['NN', 'VB', 'VBD', 'VBN', 'VBP', 'VBZ',' JJ', 'RB']
	keywords_verbs = ['VB', 'VBD', 'VBN', 'VBP', 'VBZ']
	keywords_adjuncts = ['JJ', 'RB']
	function_verbs = ['is', 'was', 'were', 'would', 'could', 'might', 'may', 'can', 'will', 'be']
	punctuation_list = [';', ',', '.', '!']

	@staticmethod
	def replace_key_words(sentence):
		"""
		Main method to semantically paraphase a sentence by substituting its key words
		"""

		tagged_sentence = pos_tag(word_tokenize(sentence))
		new_sentence = ''

		for pair_num in range(len(tagged_sentence)):
			pair = tagged_sentence[pair_num]

			# modifications for formatting
			if pair[0] == 'n\'t':
				new_sentence = new_sentence[0:-1] + pair[0] + ' '
				continue
			elif pair[1] == '.':
				new_sentence = new_sentence[0:-1] + '.'
				continue
			# modifications for content words
			if (pair[1] in SentenceVariants.keywords_all) and (len(wn.synsets(pair[0],SentenceVariants.convert_pos(pair[1]))) != 0):
				# get the words in a +-7 word window from the target word
				context_indexes = [x for x in range(max(pair_num-15,0),min(pair_num+16,len(tagged_sentence)))]
				context = [tagged_sentence[x][0] for x in context_indexes]
				# if word is a noun, return its hypernym
				if (pair[1] == ('NN')):
					wn_pos = SentenceVariants.convert_pos(pair[1])
					hypernym = SentenceVariants.get_hypernym(pair[0],wn_pos,context)
					new_sentence += (hypernym + ' (replaced:%s) '%pair[0])
					continue
				# if word is a verb return its definition
				elif (pair[1] in SentenceVariants.keywords_verbs) and (pair[0].lower() not in SentenceVariants.function_verbs):
					wn_pos = SentenceVariants.convert_pos(pair[1])
					definition = SentenceVariants.get_definition(pair[0],wn_pos,context)
					new_sentence += (definition + ' (replaced: %s) '%pair[0])

				# if word is an adjective or adverb (ie. an adjunct) remove it entirely
				elif (pair[1] in SentenceVariants.keywords_adjuncts):
					continue
				else:
					new_sentence += pair[0] + ' '
					continue
			# if word does not fit modification criteria, leave it alone
			else:
				new_sentence += pair[0] + ' '

		return new_sentence

	@staticmethod
	def get_definition(word, wn_pos, context):
		"""
		Method to obtain a word's WordNet definition given its WordNet part of speech and context
		"""

		# use lesk to disambiguate the word meaning
		word = lesk(context, word, wn_pos)
		raw_definition = word.definition()
		cleaned_definition = ''
		for char in raw_definition:
			if char not in SentenceVariants.punctuation_list:
				cleaned_definition += char
			else:
				break
		return cleaned_definition


	# def get_synonym(word, nltk_pos):
	# 	# first convert pos from nltk tagged form to wordnet form
	# 	wn_pos = SentenceVariants.convert_pos(nltk_pos)

	# 	synonyms = wn.synsets(word, pos)
		
	# 	# choose one of the random meanings of the word
	# 	word = synonyms[randint(0,len(synonyms)-1)]
	# 	return word

	@staticmethod
	def get_hypernym(word, wn_pos, context):
		"""
		Method to obtain a word's hypernym given its WordNet part of speech and context
		"""

		# use lesk to disambiguate the word meaning
		word = lesk(context, word, wn_pos)   
		if len(word.hypernyms()) != 0:
			# return the first hypernym if it exists
			hypernym = word.hypernyms()[0].lemma_names()[0].lower()

			if "_" in hypernym:
				hypernym = hypernym.split("_")
				hypernym = " ".join(hypernym)
		else:
			hypernym = word.lemma_names()[0].lower()

		return hypernym

	@staticmethod
	def convert_pos(pos):
		"""
		Method to convert part of speech from nltk form to WordNet form
		"""
		# dictionary of pos tags (keys are in nltk form, values are wordnet form)
		pos_conversions = dict.fromkeys(['NN', 'NNS'], 'n')
		pos_conversions.update(dict.fromkeys(['VB', 'VBD', 'VBN', 'VBP', 'VBZ'], 'v'))
		pos_conversions.update(dict.fromkeys(['JJ'], 'a'))
		pos_conversions.update(dict.fromkeys(['RB'], 'r'))

		new_pos = pos_conversions[pos]

		return new_pos

	@staticmethod
	def identify_pronoun_index(premise, hypothesis):
		"""
		Method to identify the word that is different between two sentences
		Returns the index of that word
		"""
		i = 0
		new_premise = ""
		new_hypothesis = ""

		# first add spaces before punctuation marks
		# this is to be consistent with how our parser treats punctuation
		for char in premise:
			if char in SentenceVariants.punctuation_list:
				new_premise += " " + char
			else:
				new_premise += char
		for char in hypothesis:
			if char in SentenceVariants.punctuation_list:
				new_hypothesis += " " + char
			else:
				new_hypothesis += char

		new_premise = new_premise.split(" ")
		new_hypothesis = new_hypothesis.split(" ")

		while (i < len(new_premise)):
			if new_premise[i] != new_hypothesis[i]:
				break
			i += 1
		# print(i)
		return i

	@staticmethod
	def truncate(sentence, index):
		"""
		Method to truncate only the important part of the sentence
		Returns a string
		"""
		parsed_sentence = list(SentenceVariants.parser.raw_parse(sentence))[0]
		treeposition = parsed_sentence.leaf_treeposition(index)

		# look up the tree to see if there is an S or SBAR layer, which signifies an embedded sentence.
		# if so, cut everything below off and return the truncated bit.
		# the treatment for S and SBAR is only slightly different because of trinary branching
		for i in range(0,len(treeposition)):
			constituent = parsed_sentence[treeposition[:-i]]
			# print(constituent)
			# print(constituent.label())

			if (constituent.label() == 'S'):
				# series of transformation steps to get it back into string form
				constituent = [word for word in constituent.leaves()]
				for word in constituent:
					if word == "n't":
						constituent[constituent.index(word)-1] += word
						constituent.remove(word)
					if word in SentenceVariants.punctuation_list:
						constituent[constituent.index(word)-1] += word
						constituent.remove(word)
				constituent = " ".join(constituent)
				constituent = Utils.capitalize_beginning(constituent)
				# remove space before the period, if any
				if constituent[-2] == " ":
					constituent = constituent[0:-2] + "."
				if constituent[-1] != ".":
					constituent += "."
				print(constituent)
				break

			elif (constituent.label() == 'SBAR'):
				# series of transformation steps to get it back into string form
				constituent = [word for word in constituent.leaves()]
				constituent = constituent[1:]
				for word in constituent:
					if word == "n't":
						constituent[constituent.index(word)-1] += word
						constituent.remove(word)
					if word in SentenceVariants.punctuation_list:
						constituent[constituent.index(word)-1] += word
						constituent.remove(word)
				constituent = " ".join(constituent)
				constituent = Utils.capitalize_beginning(constituent)
				# remove space before the period, if any
				if constituent[-2] == " ":
					constituent = constituent[0:-2] + "."
				if constituent[-1] != ".":
					constituent += "."
				print(constituent)
				break

		return constituent
		
		