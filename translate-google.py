import json
import requests

def translate(api_key, text, source, target):
    api_endpoint = "https://translation.googleapis.com/language/translate/v2?key=" + api_key
    headers = {'Content-Type': 'application/json'}
    query = {
        'q': text,
        'source': source,
        'target': target,
        'format': 'text'
    }
    response = requests.post(api_endpoint, headers=headers, json=query)
    return response.json()

def paraphrase(api_key, text, via_language):
    translated_result = translate(api_key, text, "en", via_language)
    paraphrase = translate(api_key, translated_result['data']['translations'][0]['translatedText'], via_language, "en")
    return paraphrase['data']['translations'][0]['translatedText']

def create_paraphrases(api_key, path_to_input_text, path_to_output_text):
    f_out = open(path_to_output_text, "w")
    f = open(path_to_input_text, "r")
    for line in f:
        if line == "\n":
            continue
        else:
            wino_id = line.strip()
            premise = f.readline().strip()
            hypothesis = f.readline().strip()
            label = f.readline().strip()
            out = generate_paraphrase_output(wino_id, premise, hypothesis, label)
            f_out.write(out)
    f_out.close()

def generate_paraphrase_output(api_key, id,premise,hypothesis,label):
    lines = []
    languages = ['es','zh','hu','fr', 'eu', 'ja']
    for language in languages:
        lines.append(id)
        lines.append(premise)
        lines.append(paraphrase(api_key, hypothesis, language))
        lines.append(label)
        lines.append("")
    return "\n".join(lines)
