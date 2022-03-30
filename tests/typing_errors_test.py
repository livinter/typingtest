import glob

from typing_errors import typing_errors
from utils import read_random_text_part


def test_get_next_letters():
    pass


def test_typing_errors_skip_correct():
    character_count = 50
    for i, text_file in enumerate(glob.glob(f"texts/*.txt")):
        example_text = read_random_text_part(character_count, file_select=i)
        time_passed = [(0.1, c) for c in example_text[:-10]]
        time_passed_e = typing_errors(time_passed, example_text)
        assert sum([not e for t, c, e in time_passed_e]) <= 0


def test_typing_errors_find_errors():
    example_text = "nie problams - slaabt wull"
    time_passed = [(0.1, c) for c in example_text]
    time_passed_e = typing_errors(time_passed, "Good day, nice problems, did you sleep also well?")
    assert sum([not e for t, c, e in time_passed_e]) == 9


def test_typing_errors_umlaute():
    example_text = "oh wie schön ist es auf den höhen..."
    time_passed = [(0.1, c) for c in example_text[:-3]]
    assert sum([not e for t, c, e in typing_errors(time_passed, example_text)]) <= 0
