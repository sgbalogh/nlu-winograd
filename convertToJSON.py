"""
This function takes the winograd translations and converts them to json format similar to MultiNLI json format

"""
import wnlu.translate
from nltk.parse.stanford import StanfordParser

import json
from nltk import Tree
from functools import reduce
count = 1

def binarize(tree):
    """
    Recursively turn a tree into a binary tree.
    """
    if isinstance(tree, str):
        return tree
    elif len(tree) == 1:
        return binarize(tree[0])
    else:
        return reduce(lambda x, y: (binarize(x), binarize(y)), tree)
          
def remove_formatting(tree):
    parse_string = ''
    parse_string1 = ''
    for u in tree:
        parse_string1 = str(u).split("\n")
    for parse in parse_string1:
        parse_string = parse_string + parse
    parse_string = " ".join(parse_string.split())
    return parse_string

def format_binary_tree(tree):
    tree.chomsky_normal_form()
    string = str(binarize(tree))
    string = string.replace("\'","")
    string = string.replace("\"s\"","'s")
    string = string.replace("\"nt\"","n't")
    string = string.replace("\"m\"","'m")
    string = string.replace("\"d\"","'d")
    string = string.replace("\"ve\"","'ve")
    string = string.replace(",,","|")
    string = string.replace(",","")
    string = string.replace("|",",")
    string = string.replace(" (","(")
    string = string.replace(") ",")")
    string = string.replace("("," ( ")
    string = string.replace(")"," ) ")
    string = string.replace("  "," ")
    return string
    
def get_json(dataset,f,parser,count):
    for instance in dataset:
        test = {}
        possible_translations = instance.get_candidate_translations()
        test["pairID"] = str(count) + 'a'
        test["sentence1"] = instance.get_premise()
        parse_string = remove_formatting(parser.raw_parse(instance.get_premise()))
        test["sentence1_parse"] = parse_string
        test["sentence1_binary_parse"] = format_binary_tree(Tree.fromstring(parse_string))
        test["sentence2"] = possible_translations[0]
        parse_string = remove_formatting(parser.raw_parse(possible_translations[0]))
        test["sentence2_parse"] = parse_string
        test["sentence2_binary_parse"] = format_binary_tree(Tree.fromstring(parse_string))
        if instance.gold_answer_idx == 0:
            test["gold_label"] = 'entailment'
        else:
            test["gold_label"] = 'neutral'
        test = json.dumps(test)
        f.write(test)
        f.write("\n")
        
        test = {}
        test["pairID"] = str(count) + 'b'
        test["sentence1"] = instance.get_premise()
        parse_string = remove_formatting(parser.raw_parse(instance.get_premise()))
        test["sentence1_parse"] = parse_string
        test["sentence1_binary_parse"] = format_binary_tree(Tree.fromstring(parse_string))
        test["sentence2"] = possible_translations[1]
        parse_string = remove_formatting(parser.raw_parse(possible_translations[1]))
        test["sentence2_parse"] = parse_string
        test["sentence2_binary_parse"] = format_binary_tree(Tree.fromstring(parse_string))
        if instance.gold_answer_idx == 1:
            test["gold_label"] = 'entailment'
        else:
            test["gold_label"] = 'neutral'
        test = json.dumps(test)
        f.write(test)
        f.write("\n")
        count = count + 1
    f.close()
    return count
    
    
loader = wnlu.WinogradLoader()
jar = 'apps/stanford-parser-full-2018-02-27/stanford-parser.jar'
model = 'apps/stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar'
parser = StanfordParser(model, jar, encoding='utf8')

f = open("winograd_dev_set.jsonl",'w')
count = get_json(loader.get_dev_set(),f,parser,count)

f = open("winograd_test_set.jsonl",'w')
get_json(loader.get_test_set(),f,parser,count)
