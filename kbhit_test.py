def test_import():
    import os
    # Windows
    if os.name == 'nt':
        import msvcrt

    # Posix (Linux, OS X)
    else:
        import sys
        import termios
        import atexit
        from select import select


import kbhit


# def test_kbhit():
#     kb = kbhit.KBHit()
#     _ = kb.kbhit()
#     kb.set_normal_term()