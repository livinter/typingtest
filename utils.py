import glob
import random
import numpy as np
import yaml
import json
import os
import unicodedata

_default_config = {"language": "en",
                   "character_count": 500,
                   "left_hand": "123456~!#$%^qwertasdfgzxcvQWERTASDFGZXCV",
                   "convert_letters": 0,
                   "right_hand": '7890uiophjkl;nm,.<>'
                   }

_config = None

def _load_config():
    with open(r'config.yaml') as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def get_config_value(key):
    global _config
    if _config is None:
        _config = _load_config()
    return _config.get(key, _default_config[key])


def read_random_text_part(character_count, convert_letters=True, language=None):
    if language:
        language_filter = "." + language
    else:
        language_filter = ""
    text_files = list(glob.glob(f"texts/*{language_filter}.txt"))
    text_file = text_files[random.randint(0, len(text_files) - 1)]
    text_data = open(text_file, "rt", encoding="utf-8").read()
    if convert_letters:
        text_data = unicodedata.normalize("NFKC", text_data)
    text_data = text_data * (1 + character_count // len(text_data))
    random_pos = random.randint(0, len(text_data) - 1- character_count)
    return text_data[random_pos:random_pos + character_count]


#  β = ∑ [(xi - ∅x) × (yi - ∅y)] / ∑(xi - ∅x)2
def linear_regression_get_beta(y):
    x = np.arange(len(y))
    y = np.array(y)
    return np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)


def write_event(event):
    os.makedirs("results", exist_ok=True)
    with open(f'results/{event["start_time"]}.json', "wt") as file:
        print("writing event...")
        return json.dump(event, file)


def load_events():
    print("loading events...")
    events = []
    for event_file in sorted(list(glob.glob("results/*.json"))):
        with open(event_file) as file:
            events.append(json.load(file))
    return events
