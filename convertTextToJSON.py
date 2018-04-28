"""
This function takes the winograd translations and converts them to json format similar to MultiNLI json format

"""
import wnlu.translate
from nltk.parse.stanford import StanfordParser

import sys
import json
from nltk import Tree
from functools import reduce
count = 1

def binarize(tree):
    """
    Recursively turn a tree into a binary tree. Adapted from https://stackoverflow.com/questions/44742809/how-to-get-a-binary-parse-in-python
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
    
def get_json(input_file,output_file,parser,count):
    f = open(input_file,'r')
    f1 = open(output_file,'w')
    for line in f:
        if line == "\n":
            continue
        else:
            test = {}
            test["pairID"] = line.strip()
            test["sentence1"] = f.readline().strip()
            parse_string = remove_formatting(parser.raw_parse(test["sentence1"]))
            test["sentence1_parse"] = parse_string
            test["sentence1_binary_parse"] = format_binary_tree(Tree.fromstring(parse_string))
            test["sentence2"] = f.readline().strip()
            parse_string = remove_formatting(parser.raw_parse(test["sentence2"]))
            test["sentence2_parse"] = parse_string
            test["sentence2_binary_parse"] = format_binary_tree(Tree.fromstring(parse_string))
            test["gold_label"] = f.readline().strip()
            test = json.dumps(test)
            print(test)
            f1.write(test)
            f1.write("\n")
            count = count + 1
    f.close()
    f1.close()    
    
"""
Stanford PCFG Parser 3.9.1
Dan Klein and Christopher D. Manning. 2003. Accurate Unlexicalized Parsing. Proceedings of the 41st Meeting of the Association for Computational Linguistics, pp. 423-430.
"""
jar = 'apps/stanford-parser-full-2018-02-27/stanford-parser.jar'
model = 'apps/stanford-parser-full-2018-02-27/stanford-parser-3.9.1-models.jar'
parser = StanfordParser(model, jar, encoding='utf8')

get_json(sys.argv[1],sys.argv[2],parser,count)

