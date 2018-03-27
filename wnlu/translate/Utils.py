from nltk.tag import pos_tag

class Utils:
    @staticmethod
    ## Checks to see if the given input ends with a period
    def is_complete_sentence(input):
        cleaned = str.strip(input)
        if len(cleaned) == 0:
            return False
        else:
            if cleaned[-1] == '.':
                return True
            else:
                return False

    @staticmethod
    ## Given a clause, capitalizes the first character of the first letter
    def capitalize_beginning(input):
        if len(input) == 0:
            return input
        else:
            return str.upper(input[0]) + input[1:]

    @staticmethod
    ## We want the canonical version of the noun phrase (for the answer)...
    ## If it is proper (e.g. 'Emma'), we want it with the correct capitalization ('Emma'),
    ## if it isn't (e,g. 'The dogs', then we want it converted to lower case ('the dogs')
    def standardize_noun_phrase(noun_phrase):
        tagged = Utils.tag_phrase(noun_phrase)
        modified_tokens = []
        if tagged[0][1] == "NNP":
            modified_tokens.append(tagged[0][0])
        elif tagged[0][1] == "NNS":
            modified_tokens.append(str.lower(tagged[0][0]))
        else:
            if len(tagged) == 1:
                modified_tokens.append(tagged[0][0])
            else:
                modified_tokens.append(str.lower(tagged[0][0]))
        for token,tag in tagged[1:]:
            modified_tokens.append(token)
        return " ".join(modified_tokens)

    @staticmethod
    def make_noun_phrase_possessive(noun_phrase):
        if (len(noun_phrase) == 0):
            return noun_phrase
        else:
            if noun_phrase[-1] == 's':
                return noun_phrase + "'"
            else:
                return noun_phrase + "'s"

    @staticmethod
    ## From https://dictionary.cambridge.org/grammar/british-grammar/pronouns/pronouns-possessive-my-mine-your-yours-etc
    def is_possessive_determiner(pronoun):
        if str.lower(pronoun) in ['my', 'your', 'his', 'her', 'its', 'our', 'their', 'one\'s']:
            return True
        else:
            return False

    @staticmethod
    def tag_phrase(phrase):
        return pos_tag(phrase.split())