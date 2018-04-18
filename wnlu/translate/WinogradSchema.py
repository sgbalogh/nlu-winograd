from wnlu.translate.Utils import Utils

####
## This class provides an encapsulization for a schema, which is characterized by:
## 1) A "premise" string, containing a sentence (or potentially sequence of sentences).
## 2) A reference to an ambiguous pronoun within the premise.
## 3) Two potential noun options for that ambigous pronoun.
## For labeled instances, there is also an index to which noun option correctly removes the
## ambiguity in the premise.
####

class WinogradSchema:
    def __init__(self, premise_A, pron, premise_B, answer_list, correct_answer=None):
        self.premise_A = str.strip(premise_A)
        self.pronoun = str.lower(str.strip(pron))
        self.premise_B = str.strip(premise_B)
        self.answers = list(map(lambda x: Utils.standardize_noun_phrase(str.strip(x)), answer_list))
        self.gold_answer_idx = correct_answer

    ## Returns the original "premise" string, containing the pronoun in question
    def get_premise(self):
        return self.premise_A + " " + self.pronoun + " " + self.premise_B

    ## Returns versions of the premise string with the candidate answers swapped-
    ## in for the ambiguous pronoun
    def get_candidate_translations(self):
        translations = []
        for potential_answer in self.answers:
            pa = potential_answer
            if Utils.is_possessive_determiner(self.pronoun):
                pa = Utils.make_noun_phrase_possessive(potential_answer)
            if (Utils.is_complete_sentence(self.premise_A)):
                translations.append(self.premise_A + " " + Utils.capitalize_beginning(pa) + " " + self.premise_B)
            else:
                translations.append(self.premise_A + " " + pa + " " + self.premise_B)
                
            # remove space before the period, if any
            if translations[-1][-2] == " ":
                translations[-1] = translations[-1][0:-2] + "."
                
        return translations
