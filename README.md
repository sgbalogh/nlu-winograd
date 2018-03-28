# nlu-winograd.py
Models and code for addressing the Winograd Schema Challenge with training data from the SNLI/MultiNLI corpora.

## Overview

### Environment Setup

First, install Python 3. Then, start by cloning this repository:

```bash
git clone https://github.com/sgbalogh/nlu-winograd
cd nlu-winograd
```
Next, make sure to grab a copy of the MultiNLI corpus and place it in `datasets/multinli`.

```bash
wget https://www.nyu.edu/projects/bowman/multinli/multinli_1.0.zip -P datasets/multinli
cd datasets/multinli
unzip multinli_1.0.zip
```

Pre-requisites can be installed simply with:

```bash
make
```

Optionally, you can run the test suite with:
```bash
make test
```

### Loading Winograd Schema Dev/Test instances

The repository contains a copy of the [XML document](https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WSCollection.xml) provided by Ernest Davis. The local copy is located at `datasets/winograd/WSCollection.xml`.

From a command line, open a Python 3 shell in the home directory of this repository.

```python
import wnlu

## Initializing a translator class automatically
## parses all of the examples from the XML document:
loader = wnlu.WinogradLoader()

## This loops through the dev set instances and prints out
## the original premise content:
for instance in loader.get_dev_set():
  print(instance.get_premise())

winograd_example = loader.get_dev_set()[0]
print(winograd_example.get_premise())

## Get a list of the two possible translations of the
## schema (i.e., the two ways of replacing the pronoun):
possible_translations = winograd_example.get_candidate_translations()

## To just view the possible answers:
winograd_example.answers

## If we want to see the GOLD label, we can get the index
## of it within the answers list (above) using:
winograd_example.gold_answer_idx
```
