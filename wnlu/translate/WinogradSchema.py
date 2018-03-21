from wnlu.translate.Utils import Utils

class WinogradSchema:
    def __init__(self, premise_A, pron, premise_B, answer_list, correct_answer):
        self.premise_A = str.strip(premise_A)
        self.pronoun = str.lower(str.strip(pron))
        self.premise_B = str.strip(premise_B)
        self.answers = list(map(lambda x: Utils.standardize_noun_phrase(str.strip(x)), answer_list))
        self.gold_answer_idx = correct_answer

    def get_premise(self):
        return self.premise_A + " " + self.pronoun + " " + self.premise_B

    # def get_translations_old(self):
    #     if (Utils.is_complete_sentence(self.premise_A)):
    #         return [
    #             self.premise_A + " " + Utils.capitalize_beginning(self.answers[0]) + " " + self.premise_B,
    #             self.premise_A + " " + Utils.capitalize_beginning(self.answers[1]) + " " + self.premise_B
    #         ]
    #     else:
    #         return [
    #             self.premise_A + " " + self.answers[0] + " " + self.premise_B,
    #             self.premise_A + " " + self.answers[1] + " " + self.premise_B
    #         ]

    def get_translations(self):
        translations = []
        for potential_answer in self.answers:
            pa = potential_answer
            if Utils.is_possessive_determiner(self.pronoun):
                pa = Utils.make_noun_phrase_possessive(potential_answer)
            if (Utils.is_complete_sentence(self.premise_A)):
                translations.append(self.premise_A + " " + Utils.capitalize_beginning(pa) + " " + self.premise_B)
            else:
                translations.append(self.premise_A + " " + pa + " " + self.premise_B)
        return translations

