### Overview

#### Loading Winograd Schema Dev/Test Instances

The repository contains a copy of the [XML document](https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WSCollection.xml) provided by Ernest Davis. The local copy is located at `datasets/winograd/WSCollection.xml`.

From a command line, open a Python 3 shell in the home directory of this repository.

```python
import wnlu

## Initializing a translator class automatically
## parses all of the examples from the XML document:
translator = wnlu.WinogradTranslator()

## This loops through the instances and prints out
## the original premise content:
for instance in translator.schemata:
  print(instance.get_premise())

winograd_example = translator.schemata[0]
print(winograd_example.get_premise())

## Get a list of the two possible translations of the
## schema (i.e., the two ways of replacing the pronoun):
possible_translations = winograd_example.get_translations()

## To just view the possible answers:
winograd_example.answers

## If we want to see the GOLD label, we can get the index
## of it within the answers list (above) using:
winograd_example.gold_answer_idx
```
