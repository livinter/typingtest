import glob
import random
import numpy as np
import yaml
import json
import os
from unidecode import unidecode


def read_random_text_part(character_count, convert_letters=True, language=None):
    if language:
        language_filter = "." + language
    else:
        language_filter = ""
    text_files = list(glob.glob(f"texts/*{language_filter}.txt"))
    text_file = text_files[random.randint(0, len(text_files) - 1)]
    text_data = open(text_file).read()
    if convert_letters:
        text_data = unidecode(text_data)
    text_data = text_data * (1 + character_count // len(text_data))
    random_pos = random.randint(0, len(text_data) - 1) - character_count
    return text_data[random_pos:random_pos + character_count]


#  β = ∑ [(xi - ∅x) × (yi - ∅y)] / ∑(xi - ∅x)2
def linear_regression_get_beta(y):
    x = np.arange(len(y))
    y = np.array(y)
    return np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)


def load_config():
    with open(r'config.yaml') as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


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
