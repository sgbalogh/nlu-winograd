# nlu-winograd.py
Models and code for addressing the Winograd Schema Challenge with training data from the SNLI/MultiNLI corpora.

## Acknowledgements

For convenience, this repository pre-packages some dependency code and data not created by the authors.

- The dataset of Winograd Schemas at `./datasets/winograd/WSCollection.xml` is taken from [Ernest Davis's (NYU) website](https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html).
- We package a modified implementation of the [baseline NLI models](https://github.com/nyu-mll/multiNLI) from the Machine Learning for Language Group at NYU, which is stored in `./model`


## Overview

### General Environment Setup

First, install Python 3. Then, start by cloning this repository:

```bash
git clone https://github.com/sgbalogh/nlu-winograd
cd nlu-winograd
```

Pre-requisites can be installed simply with:

```bash
make
```

Optionally, you can run the test suite with:
```bash
make test
```

### Model Training Environment Setup

In order to run the TensorFlow NLI model implementations, some datasets need to be downloaded first.

Create a `data` directory in `./model` containing an additional nested directory `winograd`; additionally, create a `logs` directory within `./model`:

```bash
mkdir -p ./model/data/winograd
mkdir -p ./model/logs
cd ./model/data
```

Then download and unzip SNLI, MNLI, and GloVe:
```bash
wget https://www.nyu.edu/projects/bowman/multinli/multinli_0.9.zip
wget https://nlp.stanford.edu/projects/snli/snli_1.0.zip
wget http://nlp.stanford.edu/data/glove.840B.300d.zip
unzip ./*.zip
```

We also need the Stanford Parser, which should be stored in ./apps

```bash
cd nlu-winograd
mkdir -p ./apps
cd apps
wget https://nlp.stanford.edu/software/stanford-parser-full-2018-02-27.zip
unzip ./*.zip
```

Now you should be all set.

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
for instance in loader.get_train_set():
  print(instance.get_premise())

winograd_example = loader.get_train_set()[0]
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

### Working With Winograd -> NLI Translation

Two scripts are provided for two different interfaces from Winograd translation into JSONL format necessary for input to the NLI models.

- `convertToJSON.py` uses the translation interface specified within the `wnlu` module to generate dev and test outputs directly
- `convertTextToJSON.py` performs a similar function, but reads in from a text file, making it more suitable for experimentation with different translation strategies; it needs to be passed a path to the input text file, followed by a path to the output JSON -- the input format expected is:

```
<Premise>
<Hypothesis>
<GOLD label>

<Premise>
<Hypothesis>
<GOLD label>

...
```
