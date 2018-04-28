from wnlu.translate import WinogradSchema
import xml.etree.ElementTree as et

class WinogradLoader:
    def __init__(self):
        schemata = WinogradLoader.load_xml("datasets/winograd/WSCollection.xml")
        self.train_set = schemata[0:70]
        self.dev_set = schemata[70:140]
        self.test_set = schemata[140:]

    def get_train_set(self):
        return self.train_set

    def get_dev_set(self):
        return self.dev_set

    def get_test_set(self):
        return self.test_set

    @staticmethod
    def load_xml(winograd_xml_path):
        tree = et.parse(winograd_xml_path)
        root = tree.getroot()
        schemata = []
        for item in root.findall('./'):
            schema = item
            schemata.append(schema)
        records = []
        for idx,schema in enumerate(schemata):
            record = {"answers": [], "correct_answer": -1}
            for child in schema:
                if child.tag == "text":
                    for grandchild in child:
                        if grandchild.tag == "txt1":
                            record['premise_a'] = str.strip(grandchild.text.replace("\n"," "))
                        elif grandchild.tag == "pron":
                            record['premise_pronoun'] = str.strip(grandchild.text.replace("\n"," "))
                        elif grandchild.tag == "txt2":
                            record['premise_b'] = str.strip(grandchild.text.replace("\n"," "))
                # elif child.tag == "quote":
                elif child.tag == "answers":
                    for grandchild in child:
                        if grandchild.tag == "answer":
                            record['answers'].append(str.strip(grandchild.text.replace("\n"," ")))
                elif child.tag == "correctAnswer":
                    ca = str.strip(child.text)
                    if ca == "A." or ca == "A":
                        record["correct_answer"] = 0
                    elif ca == "B." or ca == "B":
                        record["correct_answer"] = 1
                    else:
                        print(ca)
            records.append(WinogradSchema.WinogradSchema("wino-"+str(idx), record['premise_a'], record['premise_pronoun'], record['premise_b'], record['answers'], record['correct_answer']))
        return records


