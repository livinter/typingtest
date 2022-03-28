
def get_next_letters(s, pattern):

    def get_matches(pattern, add=0):
        # make two letter pairs with index
        return [(i * 2 + add, c1 + c2) for c1, c2, i in zip(pattern[::2], pattern[1::2], range(10000000))]

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