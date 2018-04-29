import json
import sys

input_file = sys.argv[1]

winograd = []
premises = {}
wino_to_premise = {}

correct_via_entailment_conf = 0
correct_via_entailment_and_neutral_conf = 0
correct_via_neutral_and_contra_conf = 0
correct_via_contra_conf = 0

def mean_scores(instances):
    sum_entailment_confidence = 0.0
    sum_neutral_confidence = 0.0
    sum_contradiction_confidence = 0.0
    for instance in instances:
        sum_entailment_confidence += instance['entailment_confidence']
        sum_neutral_confidence += instance['neutral_confidence']
        sum_contradiction_confidence += instance['contradiction_confidence']
    return {
        "entailment": sum_entailment_confidence / len(instances),
        "neutral": sum_neutral_confidence / len(instances),
        "contradiction": sum_contradiction_confidence / len(instances),
    }

for line in open(input_file, 'r'):
    winograd.append(json.loads(line))

for instance in winograd:
    wino_id = instance['pairID']
    wino_to_premise[wino_id] = instance['premise']
    if wino_id in premises:
        premises[wino_id][instance['gold_label']].append(instance)
    else:
        premises[wino_id] = {"entailment": [], "neutral": []}
        premises[wino_id][instance['gold_label']].append(instance)

## Now we have all of the model results stored in the premises dictionary

for premise, results in premises.items():
    gold_entailment = results['entailment']
    gold_neutral = results['neutral']
    g_entailment_agg = mean_scores(gold_entailment)
    g_neutral_agg = mean_scores(gold_neutral)
    if g_entailment_agg['entailment'] > g_neutral_agg['entailment']:
        correct_via_entailment_conf += 1
    if g_entailment_agg['entailment'] + g_entailment_agg['neutral'] > g_neutral_agg['entailment'] + g_neutral_agg[
        'neutral']:
        correct_via_entailment_and_neutral_conf += 1
    if g_entailment_agg['entailment'] == g_neutral_agg['entailment']:
        print("Match Entailment")
    if g_entailment_agg['contradiction'] < g_neutral_agg['contradiction']:
        correct_via_contra_conf += 1
    if g_entailment_agg['contradiction'] + g_entailment_agg['neutral'] < g_neutral_agg['contradiction'] + g_neutral_agg[
        'neutral']:
        correct_via_neutral_and_contra_conf += 1
    if g_entailment_agg['contradiction'] == g_neutral_agg['contradiction']:
        print("Match Contradiction")

print("Total # of Winograd Schemas: ", len(premises))
print("# Correct (via entailment only): ", correct_via_entailment_conf)
print("# Correct (via entailment + neutral only): ", correct_via_entailment_and_neutral_conf)
print("# Correct (via contradiction only): ", correct_via_contra_conf)
print("# Correct (via contradiction + neutral only): ", correct_via_neutral_and_contra_conf)
print("Accuracy (via entailment only): ", correct_via_entailment_conf / len(premises))
print("Accuracy (via entailment + neutral only): ", correct_via_neutral_and_contra_conf / len(premises))
print("Accuracy (via contradiction only): ", correct_via_contra_conf / len(premises))
print("Accuracy (via contradiction + neutral only): ", correct_via_neutral_and_contra_conf / len(premises))
