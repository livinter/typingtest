import glob
import json
import os
import random
import unicodedata

import numpy as np
import yaml

from definitions import RESULT_DIR, CONFIG_FILE, TEXT_DIR, default_config, umap

_config = None


def _load_config():
    with open(CONFIG_FILE) as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def get_config_value(key: str):
    global _config
    if _config is None:
        _config = _load_config()
    return _config.get(key, default_config[key])


def read_random_text_part(character_count: int, convert_letters: bool = True,
                          language: str = None, file_select: int = None) -> str:
    if language:
        language_filter = "." + language
    else:
        language_filter = ""
    text_files = list(glob.glob(f"{TEXT_DIR}/*{language_filter}.txt"))

    if file_select is None:
        file_select = random.randint(0, len(text_files) - 1)
    text_file = text_files[file_select]
    text_data = open(text_file, "rt", encoding="utf-8").read()
    text_data = unicodedata.normalize("NFKC", text_data)
    if convert_letters:
        text_data = text_data.translate(umap)
    text_data = text_data * (1 + character_count // len(text_data))
    random_pos = random.randint(0, len(text_data) - 1 - character_count)
    return text_data[random_pos:random_pos + character_count]


#  β = ∑ [(xi - ∅x) × (yi - ∅y)] / ∑(xi - ∅x)2
def linear_regression_get_beta(y: list):
    x = np.arange(len(y))
    y = np.array(y)
    return np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)


def write_event(event: dict):
    os.makedirs(RESULT_DIR, exist_ok=True)
    with open(f'{RESULT_DIR}/{event["start_time"]}.json', "wt") as file:
        print("writing event...")
        return json.dump(event, file)


def load_events() -> list:
    print("loading events...")
    events = []
    for event_file in sorted(list(glob.glob(f"{RESULT_DIR}/*.json"))):
        with open(event_file) as file:
            events.append(json.load(file))
    return events
