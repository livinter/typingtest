import numpy as np
from utils import _default_config, _load_config, get_config_value
from utils import read_random_text_part, linear_regression_get_beta, write_event, load_events
from unidecode import unidecode
import glob


def test_config():
    config = _load_config()
    for c in _default_config:
        assert c in config
    assert config["character_count"] > 10
    assert len(config["left_hand"]) > 0
    assert len(config["right_hand"]) > 0


def test_example_text_read():
    character_count = get_config_value("character_count")
    for text_file in list(glob.glob(f"texts/*.txt")):
        print(text_file)
        text_data = open(text_file).read()
        assert len(text_data) > 0
        text_data = unidecode(text_data)
        text_data = text_data * (1 + character_count // len(text_data))
        random_pos = len(text_data) - character_count
        assert len(text_data[random_pos:random_pos + character_count]) == character_count

    example_text = read_random_text_part(character_count=get_config_value("character_count"),
                                         convert_letters=0,
                                         language=get_config_value("language"))
    assert len(example_text) == get_config_value("character_count")
    example_text = read_random_text_part(character_count=get_config_value("character_count"),
                                         convert_letters=1)
    assert len(example_text) == get_config_value("character_count")


def test_linear_regression_get_beta():
    assert linear_regression_get_beta(np.array([4, 5, 6, 7, 8])) == 1
    assert linear_regression_get_beta([4., 4, 4, 4, 4]) == 0
