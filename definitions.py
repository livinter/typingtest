default_config = {"language": "en",
                  "character_count": 500,
                  "left_hand": "`123456~!\#$%^qwertasdfgzxcvQWERTASDFGZXCV",
                  "convert_letters": 0,
                  "right_hand": "7890-=&*()_+yuiop[]\hjkl;'nm,./YUIOP{}|HJKL:BNM<>"
                  }

ESC = chr(27)
ENTER = chr(10)
BACK = chr(127)

CONFIG_FILE = "config.yaml"
RESULT_DIR = "results"
TEXT_DIR = "texts"
umlaut_dictionary = {u'Ä': 'Ae',
                    u'Ö': 'Oe',
                    u'Ü': 'Ue',
                    u'ä': 'ae',
                    u'ö': 'oe',
                    u'ü': 'ue',
                    u'ß': 'ss'
                    }
umap = {ord(key):val for key, val in umlaut_dictionary.items()}