from wnlu.translate import WinogradSchema
import xml.etree.ElementTree as et
import numpy as np

class WinogradLoader:
    def __init__(self):
        schemata = WinogradLoader.load_xml("datasets/winograd/WSCollection.xml")
        # self.dev_set = schemata[0:141]
        # self.test_set = schemata[141:]

        # perm = np.random.permutation(283)
        # dev_indices = np.sort(perm[:141])
        # test_indices = np.sort(perm[141:])
        # np.save('dev_indices', dev_indices)
        # np.save('test_indices', test_indices)

        dev_lst = np.load('dev_indices.npy').tolist()
        test_lst = np.load('test_indices.npy').tolist()

        self.dev_set = [schemata[i] for i in dev_lst]
        self.test_set = [schemata[i] for i in test_lst]



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
        for schema in schemata:
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
            records.append(WinogradSchema.WinogradSchema(record['premise_a'], record['premise_pronoun'], record['premise_b'], record['answers'], record['correct_answer']))
        return records


