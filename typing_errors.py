from itertools import count
from definitions import BACK


def get_next_letters(s:str, pattern:str):

    def get_matches(pattern, add=0):
        # make two letter pairs with index
        return [(i * 2 + add, c1 + c2) for c1, c2, i in zip(pattern[::2], pattern[1::2], count())]

    search = get_matches(pattern) + get_matches(pattern[1:], 1)
    text = list(dict(sorted(get_matches(s) + get_matches(s[1:], 1))).values())

    max_accepted_errors = 2 + len(pattern) // 4
    positions = []
    i = len(pattern)
    max_i = len(text)
    while i < max_i:
        text_search_range = text[i - len(pattern):i]
        score = 0
        for ii, sp in search:
            score += sp in text_search_range

        positions.append((score, i))

        # the less matches, the more move forward
        i += max((len(pattern) - score) - max_accepted_errors, 1)

    positions = sorted(positions, reverse=True)
    best_score = positions[0][0]
    return [s[p] for score, p in positions if score >= best_score - 1]



def typing_errors(time_passed: list, example_text: str):
    written_text = ""
    time_passed_with_error = []
    for t, c in time_passed:
        right = get_next_letters(example_text, written_text[-50:])
        if c == BACK:
            written_text = written_text[:-1]
        else:
            written_text += c
        time_passed_with_error.append((t, c, c in right))
    return time_passed_with_error