import json
import numpy as np

winograd = []
correct = 0
count = 0
i = 0
real_entailment = []
neutral_entailment = []
diff = []

file = "../confidence_levels_winograd_devset.jsonl"
for line in open(file, 'r'):
	winograd.append(json.loads(line))

prev_premise = winograd[0]['premise']
while i != len(winograd):
	value = winograd[i:i+2]
	if prev_premise == value[0]['premise']:
		if value[0]['gold_label'] == 'entailment':
			real_entailment.append(value[0]['entailment_confidence'])
			neutral_entailment.append(value[1]['entailment_confidence'])
			diff.append(value[0]['entailment_confidence'] - value[1]['entailment_confidence'])
		else:
			real_entailment.append(value[1]['entailment_confidence'])
			neutral_entailment.append(value[0]['entailment_confidence'])
			diff.append(value[1]['entailment_confidence'] - value[0]['entailment_confidence'])
	else:
		count = count + 1
		print(prev_premise)
		real_entailment.append(sum(real_entailment))
		neutral_entailment.append(sum(neutral_entailment))
		print(real_entailment)
		print(neutral_entailment)
		print(diff)
		if sum(real_entailment) > sum(neutral_entailment):
			correct = correct + 1
			print("Correct")
		else:
			print("Wrong")
		real_entailment = []
		neutral_entailment = []
		diff = []	
		if value[0]['gold_label'] == 'entailment':
			real_entailment.append(value[0]['entailment_confidence'])
			neutral_entailment.append(value[1]['entailment_confidence'])
			diff.append(value[0]['entailment_confidence'] - value[1]['entailment_confidence'])
		else:
			real_entailment.append(value[1]['entailment_confidence'])
			neutral_entailment.append(value[0]['entailment_confidence'])
			diff.append(value[1]['entailment_confidence'] - value[0]['entailment_confidence'])
	prev_premise = value[0]['premise']
	i = i + 2


real_entailment.append(sum(real_entailment))
neutral_entailment.append(sum(neutral_entailment))
print(prev_premise)
print(real_entailment)
print(neutral_entailment)
print(diff)
if sum(real_entailment) > sum(neutral_entailment):
	correct = correct + 1
	print("Correct")
else:
	print("Wrong")
count = count + 1
print("Premise count: " + str(count))
print("Number of correct answers: " + str(correct))
print("Accuracy: " + str(correct/count))