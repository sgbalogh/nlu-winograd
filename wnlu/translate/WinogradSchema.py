class WinogradSchema:
    def __init__(self, premise_A, pron, premise_B, answer_list, correct_answer):
        self.premise_A = premise_A
        self.pronoun = pron
        self.premise_B = premise_B
        self.answers = answer_list
        self.gold_answer_idx = correct_answer

    def get_premise(self):
        return self.premise_A + " " + self.pronoun + " " + self.premise_B

    def get_translations(self):
        if (WinogradSchema.is_complete_sentence(self.premise_A)):
            return [
                self.premise_A + " " + self.answers[0] + " " + self.premise_B,
                self.premise_A + " " + self.answers[1] + " " + self.premise_B
            ]
        else:
            return [
                self.premise_A + " " + str.lower(self.answers[0]) + " " + self.premise_B,
                self.premise_A + " " + str.lower(self.answers[1]) + " " + self.premise_B
            ]

    @staticmethod
    def is_complete_sentence(input):
        cleaned = str.strip(input)
        if len(cleaned) == 0:
            return False
        else:
            if cleaned[-1] == '.':
                return True
            else:
                return False
