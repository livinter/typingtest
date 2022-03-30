import glob

import numpy as np

from utils import default_config, _load_config, get_config_value
from utils import read_random_text_part, linear_regression_get_beta


def test_config():
    config = _load_config()
    for c in default_config:
        assert c in config
    assert config["character_count"] > 10
    assert len(config["left_hand"]) > 0
    assert len(config["right_hand"]) > 0


def test_example_text_read():
    character_count = get_config_value("character_count")
    for i, text_file in enumerate(glob.glob(f"texts/*.txt")):
        example_text = read_random_text_part(character_count, file_select=i)
        assert len(example_text) == character_count

    example_text = read_random_text_part(character_count=get_config_value("character_count"),
                                         convert_letters=False)
    assert len(example_text) == get_config_value("character_count")


def test_linear_regression_get_beta():
    assert linear_regression_get_beta(np.array([4, 5, 6, 7, 8])) == 1
    assert linear_regression_get_beta([4., 4, 4, 4, 4]) == 0
