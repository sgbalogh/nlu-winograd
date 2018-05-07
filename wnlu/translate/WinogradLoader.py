from wnlu.translate import WinogradSchema
import xml.etree.ElementTree as et

class WinogradLoader:
    def __init__(self):
        schemata = WinogradLoader.load_xml("datasets/winograd/WSCollection.xml")
        self.rn_instances = WinogradLoader.load_rn(["datasets/rahman-ng-2012/test.c.txt", "datasets/rahman-ng-2012/train.c.txt"])
        self.train_set = schemata[0:70]
        self.dev_set = schemata[70:140]
        self.test_set = schemata[140:]

    def get_train_set(self):
        return self.train_set

    def get_dev_set(self):
        return self.dev_set

    def get_test_set(self):
        return self.test_set

    def get_rahman_ng_set(self):
        return self.rn_instances

    @staticmethod
    def load_rn(paths):
        records = WinogradLoader.read_rn(paths)
        converted = []
        for idx, record in enumerate(records):
            converted.append(WinogradLoader.rahman_to_winograd(record, idx))
        return converted

    @staticmethod
    def rahman_to_winograd(record, idx):
        premise_segments = list(map(lambda x: x.strip(), record['scheme'].split(record['pronoun'])))
        premise_A = premise_segments[0]
        premise_B = premise_segments[1]
        correct_index = record['options'].index(record['correct'])
        return WinogradSchema.WinogradSchema("rahman-ng-" + str(idx), premise_A, record['pronoun'],
                                      premise_B, record['options'], correct_index)



    @staticmethod
    def read_rn(paths):
        records = []
        for path in paths:
            lines = open(path, "r").read().splitlines()
            inner_idx = 0
            input = {}
            for idx, line in enumerate(lines):
                if inner_idx == 0:
                    input['scheme'] = line
                    inner_idx += 1
                elif inner_idx == 1:
                    input['pronoun'] = line
                    inner_idx += 1
                elif inner_idx == 2:
                    input['options'] = list(map(lambda x: x.strip(), line.split(",")))
                    inner_idx += 1
                elif inner_idx == 3:
                    input['correct'] = line
                    inner_idx += 1
                elif inner_idx == 4:
                    inner_idx = 0
                    input = {}
                if "correct" in input:
                    records.append(input)
        return records



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


