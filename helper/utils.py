import re
from typing import Dict, List, Tuple
import unicodedata

class ScriptConverter:
    SCHEMES: Dict[str, Dict[str, Dict[str, str]]] = {
        'latin': {
            'ke': {
                'jawa': {
                    'virama': "꧀", 'pengapitAngka': "꧇", 'nglegena': {
                        "k": "ꦏ", "kh": "ꦏ꦳", "q": "ꦐ", "g": "ꦒ", "gh": "ꦒ꦳", "ng": "ꦔ", "c": "ꦕ", "j": "ꦗ", "z": "ꦗ꦳", "ny": "ꦚ", "th": "ꦛ", "dh": "ꦝ", "ḍ": "ꦣ", "ṭ": "ꦛ", "t": "ꦠ", "d": "ꦢ", "n": "ꦤ", "p": "ꦥ", "f": "ꦥ᳠", "b": "ꦧ", "m": "ꦩ", "y": "ꦪ", "r": "ꦫ", "l": "ꦭ", "w": "ꦮ", "v": "ꦮ᳠", "s": "ꦱ", "h": "ꦲ"
                    }, 'swara': {
                        "a": "ꦄ", "i": "ꦆ", "u": "ꦈ", "é": "ꦌ", "e": "ꦄꦼ", "eu": "ꦲꦼꦴ", "o": "ꦎ", "re": "ꦉ", "reu": "ꦉ᳠", "le": "ꦊ", "leu": "ꦋ"
                    }, 'mandaswara': {"y": "ꦾ", "r": "ꦿ"}, 'panyigeg': {"ng": "ꦁ", "h": "ꦃ", "r": "ꦂ"}, 'sandhanganSwara': {
                        "a": "", "i": "ꦶ", "u": "ꦸ", "é": "ꦺ", "e": "ꦼ", "eu": "ꦼ᳠", "o": "ꦺꦴ", "re": "ꦽ", "reu": "ꦽ᳠", "le": "꧀ꦭꦼ", "leu": "ꦭꦼ᳠"
                    }, 'pepadan': {"[.]": "꧉", "[,]": "꧈"}, 'angka': {
                        "0": "꧐", "1": "꧑", "2": "꧒", "3": "꧓", "4": "꧔", "5": "꧕", "6": "꧖", "7": "꧗", "8": "꧘", "9": "꧙"
                    }, 'lainnya': {}
                },
                'sunda': {
                    'virama': "᮪", 'pengapitAngka': "|", 'nglegena': {
                        "k": "ᮊ", "q": "ᮋ", "x": "ᮟ", "g": "ᮌ", "ng": "ᮍ", "c": "ᮎ", "j": "ᮏ", "z": "ᮐ", "ny": "ᮑ", "t": "ᮒ", "d": "ᮓ", "n": "ᮔ", "p": "ᮕ", "f": "ᮖ", "b": "ᮘ", "m": "ᮙ", "y": "ᮚ", "r": "ᮛ", "l": "ᮜ", "w": "ᮝ", "v": "ᮗ", "s": "ᮞ", "h": "ᮠ"
                    }, 'swara': {
                        "a": "ᮃ", "i": "ᮄ", "u": "ᮅ", "é": "ᮆ", "e": "ᮈ", "eu": "ᮉ", "o": "ᮇ", "reu": "ᮻ", "leu": "ᮼ"
                    }, 'mandaswara': {"y": "ᮡ", "r": "ᮢ", "l": "ᮣ"}, 'panyigeg': {"ng": "ᮀ", "h": "ᮂ", "r": "ᮁ"}, 'sandhanganSwara': {
                        "a": "", "i": "ᮤ", "u": "ᮥ", "é": "ᮦ", "e": "ᮨ", "eu": "ᮩ", "o": "ᮧ"
                    }, 'pepadan': {}, 'angka': {
                        "0": "᮰", "1": "᮱", "2": "᮲", "3": "᮳", "4": "᮴", "5": "᮵", "6": "᮶", "7": "᮷", "8": "᮸", "9": "᮹"
                    }, 'lainnya': {}
                },
                'batak': {
                    'virama': "᯲", 'pengapitAngka': "", 'nglegena': {
                        "k": "ᯃ", "q": "ᯂ", "g": "ᯎ", "ng": "ᯝ", "c": "ᯡ", "j": "ᯐ", "z": "ᯐ", "ny": "ᯠ", "t": "ᯖ", "d": "ᯑ", "n": "ᯉ", "nd": "ᯢ", "p": "ᯇ", "f": "ᯇ", "b": "ᯅ", "m": "ᯔ", "mb": "ᯣ", "y": "ᯛ", "r": "ᯒ", "l": "ᯞ", "w": "ᯋ", "v": "ᯇ", "s": "ᯘ", "h": "ᯂ"
                    }, 'swara': {
                        "a": "ᯀ", "i": "ᯤ", "u": "ᯥ"
                    }, 'mandaswara': {}, 'panyigeg': {"ng": "ᯰ", "h": "ᯱ"}, 'sandhanganSwara': {
                        "a": "", "i": "ᯪ", "u": "ᯮ", "é": "ᯩ", "e": "ᯧ", "o": "ᯬ"
                    }, 'pepadan': {}, 'angka': {}, 'lainnya': {}
                },
                'bali': {
                    'virama': "᭄", 'pengapitAngka': "", 'nglegena': {
                        "k": "ᬓ", "q": "ᬓ", "g": "ᬕ", "gh": "ᬖ", "ng": "ᬗ", "c": "ᬘ", "j": "ᬚ", "z": "ᬚ", "ny": "ᬜ", "dh": "ᬥ", "t": "ᬢ", "d": "ᬤ", "n": "ᬦ", "p": "ᬧ", "ph": "ᬨ", "f": "ᬧ᬴", "b": "ᬩ", "bh": "ᬪ", "m": "ᬫ", "y": "ᬬ", "r": "ᬭ", "l": "ᬮ", "w": "ᬯ", "v": "ᬧ", "s": "ᬲ", "h": "ᬳ"
                    }, 'swara': {
                        "a": "ᬅ", "i": "ᬇ", "u": "ᬳᬸ", "é": "ᬳᬾ", "e": "ᬳᬾ", "o": "ᬳᭀ", "re": "ᬋ", "le": "ᬍ"
                    }, 'mandaswara': {}, 'panyigeg': {"ng": "ᬂ", "h": "ᬄ", "r": "ᬃ"}, 'sandhanganSwara': {
                        "a": "", "ai": "ᬿ", "au": "ᭁ", "i": "ᬶ", "u": "ᬸ", "é": "ᬾ", "e": "ᭂ", "o": "ᭀ", "re": "ᬺ", "le": "ᬼ"
                    }, 'pepadan': {"[.]": "᭟", "[,]": "᭞"}, 'angka': {
                        "0": "᭐", "1": "᭑", "2": "᭒", "3": "᭓", "4": "᭔", "5": "᭕", "6": "᭖", "7": "᭗", "8": "᭘", "9": "᭙"
                    }, 'lainnya': {}
                },
                'rejang': {
                    'virama': "꥓", 'pengapitAngka': "", 'nglegena': {
                        "k": "ꤰ", "g": "ꤱ", "ng": "ꤲ", "c": "ꤹ", "j": "ꤺ", "ny": "ꤻ", "t": "ꤳ", "d": "ꤴ", "n": "ꤵ", "nd": "ꥄ", "p": "ꤶ", "b": "ꤷ", "m": "ꤸ", "mb": "ꥂ", "y": "ꤿ", "r": "ꤽ", "l": "ꤾ", "w": "ꥀ", "s": "ꤼ", "h": "ꥁ"
                    }, 'swara': {
                        "a": "ꥆ", "i": "", "u": "", "é": "", "e": "", "eu": "", "o": "", "re": ""
                    }, 'mandaswara': {}, 'panyigeg': {"n": "ꥐ", "ng": "ꥏ", "h": "ꥒ", "r": "ꥑ"}, 'sandhanganSwara': {
                        "a": "", "ai": "ꥊ", "au": "ꥌ", "i": "ꥇ", "u": "ꥈ", "é": "ꥎ", "e": "ꥉ", "eu": "ꥍ", "o": "ꥋ"
                    }, 'pepadan': {}, 'angka': {}, 'lainnya': {}
                },
                'kawi': {
                    'virama': "𑽁", 'pengapitAngka': "𑼃", 'nglegena': {
                        "k": "𑼒", "kh": "𑼓", "q": "𑼒𑽋", "x": "𑼒", "g": "𑼔", "gh": "𑼕", "ng": "𑼖", "c": "𑼗", "j": "𑼙", "z": "𑼙𑽋", "ny": "𑼛", "th": "𑼝", "dh": "𑼟", "t": "𑼡", "d": "𑼣", "n": "𑼠", "p": "𑼦", "ph": "𑼧", "f": "𑼦𑽋", "b": "𑼨", "bh": "𑼩", "m": "𑼪", "y": "𑼫", "r": "𑼬", "l": "𑼭", "w": "𑼮", "v": "𑼮𑽋", "s": "𑼱", "h": "𑼲"
                    }, 'swara': {
                        "a": "𑼄", "i": "𑼆", "u": "𑼈", "é": "𑼎", "e": "𑼄𑽀", "eu": "𑼄𑽀", "o": "𑼐"
                    }, 'mandaswara': {"r": "𑼊", "l": "𑼌"}, 'panyigeg': {"m": "𑼀", "ng": "𑼁", "h": "𑼃", "r": "𑼺"}, 'sandhanganSwara': {
                        "a": "", "ai": "𑼿", "i": "𑼶", "u": "𑼸", "é": "𑼾", "e": "𑽀", "eu": "𑽀", "o": "𑼾𑼴", "re": "𑼺"
                    }, 'pepadan': {"[.]": "𑽉"}, 'angka': {
                        "0": "𑽐", "1": "𑽑", "2": "𑽒", "3": "𑽓", "4": "𑽔", "5": "𑽕", "6": "𑽖", "7": "𑽗", "8": "𑽘", "9": "𑽙"
                    }, 'lainnya': {}
                },
                'pegon': {
                    'virama': "ْ", 'pengapitAngka': "", 'nglegena': {
                        "k": "ك", "kh": "خ", "q": "ق", "x": "خ", "g": "ڮ", "gh": "غ", "ng": "ڠ", "c": "چ", "j": "ج", "z": "ز", "ny": "ۑ", "th": "ث", "dh": "ض", "t": "ت", "d": "د", "n": "ن", "p": "ڤ", "f": "ف", "b": "ب", "m": "م", "y": "ي", "r": "ر", "l": "ل", "w": "و", "v": "ڤ", "s": "س", "sy": "ش", "h": "ح"
                    }, 'swara': {
                        "'a": "ع", "a": "اَ", "i": "اِ", "u": "اُ", "é": "اَيْ", "e": "اࢗ", "eu": "اࢗ‌", "o": "اَوْ"
                    }, 'mandaswara': {}, 'panyigeg': {}, 'sandhanganSwara': {
                        "a": "ا", "i": "ي", "u": "و", "é": "َيْ", "e": "ࢗ", "eu": "ࢗ‌", "o": "َوْ"
                    }, 'pepadan': {"[?]": "؟", ";": "؛", "%": "٪", "[(]": "﴿", "[)]": "﴾"}, 'angka': {
                        "0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤", "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"
                    }, 'lainnya': {}
                },
                'lontara': {
                    'virama': "",
                    'pengapitAngka': "",
                    'nglegena': {
                        "ka": "ᨀ", "ga": "ᨁ", "nga": "ᨂ", "ngka": "ᨃ",
                        "pa": "ᨄ", "ba": "ᨅ", "ma": "ᨆ", "mpa": "ᨇ",
                        "ta": "ᨈ", "da": "ᨉ", "na": "ᨊ", "nra": "ᨋ",
                        "ca": "ᨌ", "ja": "ᨍ", "nya": "ᨎ", "nca": "ᨏ",
                        "ya": "ᨐ", "ra": "ᨑ", "la": "ᨒ", "wa": "ᨓ",
                        "sa": "ᨔ", "a": "ᨕ", "ha": "ᨖ"
                    },
                    'swara': {
                        "a": "ᨕ", "i": "ᨕᨗ", "u": "ᨕᨘ", "é": "ᨕᨙ", "o": "ᨕᨚ", "e": "ᨕᨛ"
                    },
                    'sandhanganSwara': {
                        "a": "", "i": "ᨗ", "u": "ᨘ", "é": "ᨙ", "o": "ᨚ", "e": "ᨛ"
                    },
                    'pepadan': {
                        "[.]": "᨞", "[,]": "᨟"
                    },
                    'angka': {
                        "0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9"
                    },
                    'lainnya': {}
                }
            }
        }
    }

    _LONTARA_VOWEL_CHARS = "AaEeÈèÉéIiOoUuÊêĚěXxôāīūō"
    _LONTARA_CONSONANT_CHARS = "BCDfGHJKLMNPRSTVWYZbcdfghjklmnpqrstvwxyzḌḍṆṇṢṣṬṭŊŋÑñɲ"
    _LONTARA_SPECIAL_CHARS = "KkPpGgHhRrYy"
    _LONTARA_PUNCT_CHARS = ",.><?/+=-_}{[]*&^%$#@!~`\"\\|:;()"

    _LONTARA_CONSONANT_MAP = {
        "A": "ᨕ", "B": "ᨅ", "C": "ᨌ", "D": "ᨉ", "E": "ᨕᨛ", "F": "ᨄ", "G": "ᨁ",
        "H": "ᨖ", "I": "ᨕᨗ", "J": "ᨍ", "K": "ᨀ", "L": "ᨒ", "M": "ᨆ", "N": "ᨊ",
        "O": "ᨕᨚ", "P": "ᨄ", "Q": "ᨀ", "R": "ᨑ", "S": "ᨔ", "T": "ᨈ", "U": "ᨕᨘ",
        "V": "ᨄ", "W": "ᨓ", "X": "ᨕᨙ", "Y": "ᨐ", "Z": "ᨍ",
        "\u200b": "ᨕ",
        "a": "ᨕ", "b": "ᨅ", "c": "ᨌ", "d": "ᨉ", "e": "ᨕᨛ", "f": "ᨄ", "g": "ᨁ",
        "h": "ᨖ", "i": "ᨕᨗ", "j": "ᨍ", "k": "ᨀ", "l": "ᨒ", "m": "ᨆ", "n": "ᨊ",
        "o": "ᨕᨚ", "p": "ᨄ", "q": "ᨀ", "r": "ᨑ", "s": "ᨔ", "t": "ᨈ", "u": "ᨕᨘ",
        "v": "ᨄ", "w": "ᨓ", "x": "ᨕᨙ", "y": "ᨐ", "z": "ᨍ",
        "È": "ᨕᨙ", "É": "ᨕᨙ", "è": "ᨕᨙ", "é": "ᨕᨙ"
    }

    _LONTARA_PRESERVE_COMBINING = {
        'COMBINING ACUTE ACCENT',
        'COMBINING GRAVE ACCENT',
        'COMBINING CIRCUMFLEX ACCENT',
        'COMBINING MACRON',
    }

    _LONTARA_PRE_REPLACE = {
        'ñ': 'ny', 'Ñ': 'Ny',
        'ṅ': 'ng', 'Ṅ': 'Ng',
    }

    _LONTARA_MATRA_MAP = {
        "e": "ᨛ", "è": " ᨙ", "é": " ᨙ", "x": " ᨙ", "i": "ᨗ", "o": "ᨚ", "u": "ᨘ",
        "A": "ᨕ", "E": "ᨕᨛ", "È": "ᨕᨙ", "É": "ᨕᨙ", "X": "ᨕᨙ", "I": "ᨕᨗ", "O": "ᨕᨚ", "U": "ᨕᨘ"
    }

    @staticmethod
    def _lontara_super_trim(s):
        s = s or ''
        s = s.strip()
        s = re.sub(r'\s+', ' ', s)
        return s

    @staticmethod
    def _lontara_findstr(s, tofind):
        return tofind in s

    @staticmethod
    def _lontara_is_digit(a):
        return a in "0123456789"

    @staticmethod
    def _lontara_is_punct(a):
        return a in ScriptConverter._LONTARA_PUNCT_CHARS

    @staticmethod
    def _lontara_is_vowel(a):
        return a in ScriptConverter._LONTARA_VOWEL_CHARS

    @staticmethod
    def _lontara_is_consonant(a):
        return a in ScriptConverter._LONTARA_CONSONANT_CHARS

    @staticmethod
    def _lontara_is_special(a):
        return a in ScriptConverter._LONTARA_SPECIAL_CHARS

    @staticmethod
    def _lontara_get_matra(s):
        if len(s) < 1:
            return "ᨛ"
        i = 0
        while i < len(s) and s[i] == 'h':
            i += 1
        if i < len(s):
            s = s[i:]
        return ScriptConverter._LONTARA_MATRA_MAP.get(s, "")

    @staticmethod
    def _lontara_get_shift(s):
        sl = s.lower()

        if sl.startswith("nk"):
            return {"CoreSound": "ᨃ", "len": 2}
        elif sl.find("k") == 1:
            return {"CoreSound": ScriptConverter._lontara_get_core_sound(sl[0])["CoreSound"] + "ᨛᨀ", "len": 2}
        elif sl.find("k") > 1:
            sound, length = "", 0
            for c in sl:
                if not ScriptConverter._lontara_is_vowel(c):
                    sound += ScriptConverter._lontara_resolve_char(c)
                    length += 1
                else:
                    break
            return {"CoreSound": sound, "len": length}

        if sl.startswith("mp"):
            return {"CoreSound": "ᨇ", "len": 2}
        elif sl.find("p") == 1:
            return {"CoreSound": ScriptConverter._lontara_get_core_sound(sl[0])["CoreSound"] + "ᨛᨄ", "len": 2}
        elif sl.find("p") > 1:
            sound, length = "", 0
            for c in sl:
                if not ScriptConverter._lontara_is_vowel(c):
                    sound += ScriptConverter._lontara_resolve_char(c)
                    length += 1
                else:
                    break
            return {"CoreSound": sound, "len": length}

        if sl.startswith("ng"):
            return {"CoreSound": "ᨂ", "len": 2}
        elif sl.find("g") == 1:
            return {"CoreSound": ScriptConverter._lontara_get_core_sound(sl[0])["CoreSound"] + "ᨛᨁ", "len": 2}
        elif sl.find("g") > 1:
            sound, length = "", 0
            for c in sl:
                if not ScriptConverter._lontara_is_vowel(c):
                    sound += ScriptConverter._lontara_resolve_char(c)
                    length += 1
                else:
                    break
            return {"CoreSound": sound, "len": length}

        if sl.startswith("ny"):
            return {"CoreSound": "ᨎ", "len": 2}
        elif sl.find("y") == 1:
            return {"CoreSound": ScriptConverter._lontara_get_core_sound(sl[0])["CoreSound"] + "ᨛᨐ", "len": 2}
        elif sl.find("y") > 1:
            sound, length = "", 0
            for c in sl:
                if not ScriptConverter._lontara_is_vowel(c):
                    sound += ScriptConverter._lontara_resolve_char(c)
                    length += 1
                else:
                    break
            return {"CoreSound": sound, "len": length}

        if sl.startswith("nr"):
            return {"CoreSound": "ᨋ", "len": 2}
        elif sl.find("r") == 1:
            return {"CoreSound": ScriptConverter._lontara_get_core_sound(sl[0])["CoreSound"] + "ᨛᨑ", "len": 2}
        elif sl.find("r") > 1:
            sound, length = "", 0
            for c in sl:
                if not ScriptConverter._lontara_is_vowel(c):
                    sound += ScriptConverter._lontara_resolve_char(c)
                    length += 1
                else:
                    break
            return {"CoreSound": sound, "len": length}

        if sl.startswith("nc"):
            return {"CoreSound": "ᨏ", "len": 2}
        elif sl.find("c") == 1:
            return {"CoreSound": ScriptConverter._lontara_get_core_sound(sl[0])["CoreSound"] + "ᨛᨌ", "len": 2}
        elif sl.find("c") > 1:
            sound, length = "", 0
            for c in sl:
                if not ScriptConverter._lontara_is_vowel(c):
                    sound += ScriptConverter._lontara_resolve_char(c)
                    length += 1
                else:
                    break
            return {"CoreSound": sound, "len": length}

        return {"CoreSound": None, "len": 1}

    @staticmethod
    def _lontara_get_core_sound(s):
        h_shift = ScriptConverter._lontara_get_shift(s)
        if h_shift["CoreSound"] is None:
            core = ScriptConverter._LONTARA_CONSONANT_MAP.get(s[0], s[0])
            return {"CoreSound": core, "len": 1}
        return h_shift

    @staticmethod
    def _lontara_resolve_char(c):
        s = str(c)
        if ScriptConverter._lontara_is_digit(c):
            return c
        elif ScriptConverter._lontara_is_consonant(s[0]):
            return ScriptConverter._lontara_get_core_sound(s)["CoreSound"] + "ᨛ"
        else:
            return ScriptConverter._lontara_get_core_sound(s)["CoreSound"]

    @staticmethod
    def _lontara_get_sound(s):
        s = ScriptConverter._lontara_super_trim(s)
        if not s:
            return ""
        if len(s) == 1:
            return ScriptConverter._lontara_resolve_char(s[0])
        core_sound = ScriptConverter._lontara_get_core_sound(s)
        matra = ScriptConverter._lontara_get_matra(s[core_sound["len"]:]) if core_sound["len"] >= 1 else ""
        return core_sound["CoreSound"] + matra

    @staticmethod
    def _lontara_normalize(text: str) -> str:
        for k, v in ScriptConverter._LONTARA_PRE_REPLACE.items():
            text = text.replace(k, v)
        nfd = unicodedata.normalize('NFD', text)
        result = ''
        for ch in nfd:
            if unicodedata.category(ch) == 'Mn':
                if unicodedata.name(ch, '') in ScriptConverter._LONTARA_PRESERVE_COMBINING:
                    result += ch
            else:
                result += ch
        return unicodedata.normalize('NFC', result)

    @staticmethod
    def transliterate_lontara(text: str) -> str:
        vowel_prev = False
        i = 0
        ret = ""
        pi = 0
        vowel_flag = False

        s = ScriptConverter._lontara_super_trim(ScriptConverter._lontara_normalize(text))

        char_list = list(s)
        idx = 0
        while idx < len(char_list):
            if idx > 0 and ScriptConverter._lontara_is_vowel(char_list[idx]) and ScriptConverter._lontara_is_vowel(char_list[idx - 1]):
                char_list.insert(idx, '\u200b')
            idx += 1
        s = ''.join(char_list)

        i = 0
        pi = 0
        vowel_flag = False

        while i < len(s):
            c = s[i]
            if ScriptConverter._lontara_is_special(c) and not vowel_flag:
                pass
            elif (c == 'h' and vowel_flag) or (not ScriptConverter._lontara_is_vowel(c) and i > 0) or (c == ' ') or ScriptConverter._lontara_is_punct(c) or ScriptConverter._lontara_is_digit(c) or ((i - pi) > 5):
                ret += ScriptConverter._lontara_get_sound(s[pi:i])
                if c == ' ':
                    ret += ' '
                if ScriptConverter._lontara_is_punct(c):
                    ret += c
                    pi = i + 1
                else:
                    pi = i
                vowel_flag = False
            elif ScriptConverter._lontara_is_vowel(c) and c != 'h':
                vowel_flag = True

            if pi > 0 and ScriptConverter._lontara_is_vowel(s[pi - 1]):
                vowel_prev = True
            else:
                vowel_prev = False

            i += 1

        if pi < i:
            ret += ScriptConverter._lontara_get_sound(s[pi:i])

        return ScriptConverter._lontara_super_trim(ret)

    _JAWA_PRE_REPLACE = {
        'ñ': 'ny', 'Ñ': 'Ny',
        'ṅ': 'ng', 'Ṅ': 'Ng',
        'ṇ': 'ny', 'Ṇ': 'Ny',
        'ĕ': 'e',  'Ĕ': 'E',
        'ā': 'a',  'Ā': 'A',
        'ī': 'i',  'Ī': 'I',
        'ū': 'u',  'Ū': 'U',
    }

    _JAWA_PRESERVE_CHARS = {'é', 'è', 'ḍ', 'Ḍ', 'ṭ', 'Ṭ'}

    @staticmethod
    def _jawa_normalize(text: str) -> str:
        for k, v in ScriptConverter._JAWA_PRE_REPLACE.items():
            text = text.replace(k, v)
        preserve_combining = {'COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT'}
        nfd = unicodedata.normalize('NFD', text)
        result = ''
        i = 0
        while i < len(nfd):
            ch = nfd[i]
            if unicodedata.category(ch) == 'Mn':
                if unicodedata.name(ch, '') in preserve_combining:
                    result += ch
            else:
                base = ch
                j = i + 1
                combining = ''
                while j < len(nfd) and unicodedata.category(nfd[j]) == 'Mn':
                    combining += nfd[j]
                    j += 1
                composed = unicodedata.normalize('NFC', base + combining)
                if composed in ScriptConverter._JAWA_PRESERVE_CHARS:
                    result += composed
                    i = j
                    continue
                else:
                    result += base
            i += 1
        return result

    @staticmethod
    def _strip_diacritics(text: str) -> str:
        normalized_text = unicodedata.normalize('NFD', text)
        stripped_text = ''.join(
            char for char in normalized_text
            if unicodedata.category(char) != 'Mn'
        )
        return stripped_text

    @staticmethod
    def _sort_array(a: List[str]) -> List[str]:
        return sorted(a, key=len, reverse=True)

    @staticmethod
    def _array_to_regex(a: List[str]) -> str:
        return "|".join(a)

    @staticmethod
    def _reg_ex_backslash(a: str) -> str:
        if a in "[]().\\+-":
            return "\\" + a
        return a

    @staticmethod
    def _make_regex(scheme_part: dict) -> dict:
        res = {}
        for key, val in scheme_part.items():
            arr = [ScriptConverter._reg_ex_backslash(k) for k in val.keys()]
            arr = ScriptConverter._sort_array(arr)
            res[key] = ScriptConverter._array_to_regex(arr)
        return res

    _JAVA_WYANJANA: Dict[str, str] = {
        'b': 'ꦧ', 'bh': 'ꦨ', 'c': 'ꦕ', 'ch': 'ꦖ', 'd': 'ꦢ', 'dh': 'ꦝ',
        'ḍ': 'ꦣ', 'ḍh': 'ꦞ', 'dz': 'ꦢ꦳', 'f': 'ꦥ꦳', 'g': 'ꦒ', 'gh': 'ꦒ꦳',
        'g̣': 'ꦓ', 'h': 'ꦲ', 'j': 'ꦗ', 'jh': 'ꦙ', 'k': 'ꦏ', 'ḳ': 'ꦑ',
        'kh': 'ꦏ꦳', 'l': 'ꦭ', 'm': 'ꦩ', 'n': 'ꦤ', 'ng': 'ꦔ', 'ŋ': 'ꦔ',
        'ny': 'ꦚ', 'ñ': 'ꦚ', 'ṇ': 'ꦟ', 'p': 'ꦥ', 'ph': 'ꦦ', 'q': 'ꦐ',
        'r': 'ꦫ', 'ṛ': 'ꦬ', 's': 'ꦱ', 'ś': 'ꦯ', 'ṣ': 'ꦰ', 't': 'ꦠ',
        'th': 'ꦛ', 'ṭ': 'ꦡ', 'ṭh': 'ꦜ', 'v': 'ꦮ꦳', 'w': 'ꦮ', 'x': 'ꦏ꧀ꦱ',
        'y': 'ꦪ', 'z': 'ꦗ꦳',
    }

    _JAVA_SWARA: Dict[str, str] = {
        'a': 'ꦄ', 'ā': 'ꦄꦴ', 'aa': 'ꦄꦴ', 'ô': 'ꦄ', 'ôô': 'ꦄꦴ',
        'ai': 'ꦍ', 'ôi': 'ꦍ', 'au': 'ꦎꦴ', 'ôu': 'ꦎꦴ',
        'i': 'ꦆ', 'ï': 'ꦅ', 'ii': 'ꦇ', 'ī': 'ꦇ',
        'u': 'ꦈ', 'ū': 'ꦈꦴ', 'uu': 'ꦈꦴ',
        'e': 'ꦌ', 'é': 'ꦌ', 'ê': 'ꦄꦼ', 'o': 'ꦎ',
    }

    _JAVA_MURDA: Dict[str, str] = {
        'n': 'ꦟ', 'k': 'ꦑ', 'kh': 'ꦑ꦳', 't': 'ꦡ', 's': 'ꦯ', 'p': 'ꦦ',
        'f': 'ꦦ꦳', 'ny': 'ꦘ', 'ñ': 'ꦘ', 'g': 'ꦓ', 'gh': 'ꦓ꦳', 'b': 'ꦨ',
    }

    _JAVA_SANDHANGAN_WYANJANA: Dict[str, str] = {
        'r': 'ꦿ', 'ṛ': 'ꦽ', 'y': 'ꦾ',
    }

    _JAVA_SANDHANGAN_PANYIGEG: Dict[str, str] = {
        'r': 'ꦂ', 'h': 'ꦃ', 'ng': 'ꦁ',
    }

    _JAVA_SANDHANGAN_SWARA: Dict[str, str] = {
        'a': '', 'ô': '', 'aa': 'ꦴ', 'ai': 'ꦻ', 'au': 'ꦻꦴ', 'ôô': '',
        'ā': 'ꦴ', 'i': 'ꦶ', 'ii': 'ꦷ', 'ī': 'ꦷ', 'u': 'ꦸ', 'uu': 'ꦹ',
        'ū': 'ꦹ', 'e': 'ꦺ', 'è': 'ꦺ', 'é': 'ꦺ', 'ê': 'ꦼ', 'ě': 'ꦼ',
        'êu': 'ꦼꦴ', 'ěu': 'ꦼꦴ', 'o': 'ꦺꦴ',
    }

    _JAVA_ANGKA: Dict[str, str] = {
        '0': '꧐', '1': '꧑', '2': '꧒', '3': '꧓', '4': '꧔',
        '5': '꧕', '6': '꧖', '7': '꧗', '8': '꧘', '9': '꧙',
    }

    _JAVA_PADA: Dict[str, str] = {' ': '', '.': '꧉', ',': '꧈'}

    _JAVA_WYANJANA_PASANGAN_RIGHT = {'ꦥ', 'ꦥ꦳', 'ꦲ', 'ꦏ꧀ꦱ', 'ꦰ', 'ꦱ', 'ꦦ'}

    _KAWI_SIGNS: Dict[str, str] = {
        'ꦀ': '𑼀', 'ꦁ': '𑼁', 'ꦂ': '𑼂', 'ꦃ': '𑼃', 'ꦾ': '𑽂𑼫', 'ꦿ': '𑽂𑼬',
    }
    _KAWI_INDEPENDENT_VOWELS: Dict[str, str] = {
        'ꦄ': '𑼄', 'ꦄꦴ': '𑼅', 'ꦅ': '𑼆', 'ꦆ': '𑼆', 'ꦇ': '𑼇',
        'ꦈ': '𑼈', 'ꦈꦴ': '𑼉', 'ꦉ': '𑼊', 'ꦉꦴ': '𑼋', 'ꦊ': '𑼌',
        'ꦋ': '𑼍', 'ꦌ': '𑼎', 'ꦍ': '𑼏', 'ꦎ': '𑼐',
    }
    _KAWI_CONSONANTS: Dict[str, str] = {
        'ꦏ': '𑼒', 'ꦑ': '𑼓', 'ꦒ': '𑼔', 'ꦓ': '𑼕', 'ꦔ': '𑼖',
        'ꦕ': '𑼗', 'ꦖ': '𑼘', 'ꦗ': '𑼙', 'ꦙ': '𑼚', 'ꦚ': '𑼛',
        'ꦛ': '𑼜', 'ꦜ': '𑼝', 'ꦝ': '𑼞', 'ꦞ': '𑼟', 'ꦟ': '𑼠',
        'ꦠ': '𑼡', 'ꦡ': '𑼢', 'ꦢ': '𑼣', 'ꦣ': '𑼤', 'ꦤ': '𑼥',
        'ꦥ': '𑼦', 'ꦦ': '𑼧', 'ꦧ': '𑼨', 'ꦨ': '𑼩', 'ꦩ': '𑼪',
        'ꦪ': '𑼫', 'ꦫ': '𑼬', 'ꦭ': '𑼭', 'ꦮ': '𑼮', 'ꦯ': '𑼯',
        'ꦰ': '𑼰', 'ꦱ': '𑼱', 'ꦲ': '𑼲', 'ꦘ': '𑼳',
    }
    _KAWI_DEPENDENT_VOWELS: Dict[str, str] = {
        'ꦴ': '𑼴', 'ꦵ': '𑼵', 'ꦶ': '𑼶', 'ꦷ': '𑼷', 'ꦸ': '𑼸',
        'ꦹ': '𑼹', 'ꦽ': '𑼺', 'ꦺ': '𑼾', 'ꦻ': '𑼿', 'ꦼ': '𑽀',
    }
    _KAWI_VIRAMAS: Dict[str, str] = {'꧀': '𑽂'}
    _KAWI_PUNCTUATIONS: Dict[str, str] = {
        '꧈': '𑽃', '꧉': '𑽄', '꧃': '𑽅', '꧄': '𑽆', '꧅': '𑽆',
        '꧁': '𑽇', '꧂': '𑽇',
    }
    _KAWI_DIGITS: Dict[str, str] = {
        '꧐': '𑽐', '꧑': '𑽑', '꧒': '𑽒', '꧓': '𑽓', '꧔': '𑽔',
        '꧕': '𑽕', '꧖': '𑽖', '꧗': '𑽗', '꧘': '𑽘', '꧙': '𑽙',
    }

    _KAWI_PRE_REPLACE: Dict[str, str] = {
        'ñ': 'ny', 'Ñ': 'Ny',
        'ṅ': 'ng', 'Ṅ': 'Ng',
        'ṇ': 'ny', 'Ṇ': 'Ny',
        'ĕ': 'ê',  'Ĕ': 'Ê',
        'ā': 'aa', 'Ā': 'Aa',
        'ī': 'ii', 'Ī': 'Ii',
        'ū': 'uu', 'Ū': 'Uu',
    }

    _KAWI_PRESERVE_CHARS_SET = {'é', 'è', 'ê', 'Ê', 'ḍ', 'Ḍ', 'ṭ', 'Ṭ', 'ś', 'Ś', 'ṣ', 'Ṣ', 'ṛ', 'Ṛ'}

    @staticmethod
    def _kawi_normalize(text: str) -> str:
        for k, v in ScriptConverter._KAWI_PRE_REPLACE.items():
            text = text.replace(k, v)
        preserve_combining = {'COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT'}
        nfd = unicodedata.normalize('NFD', text)
        result = ''
        i = 0
        while i < len(nfd):
            ch = nfd[i]
            if unicodedata.category(ch) == 'Mn':
                if unicodedata.name(ch, '') in preserve_combining:
                    result += ch
            else:
                base = ch
                j = i + 1
                combining = ''
                while j < len(nfd) and unicodedata.category(nfd[j]) == 'Mn':
                    combining += nfd[j]
                    j += 1
                composed = unicodedata.normalize('NFC', base + combining)
                if composed in ScriptConverter._KAWI_PRESERVE_CHARS_SET:
                    result += composed
                    i = j
                    continue
                else:
                    result += base
            i += 1
        zws = '\u200b'
        result = re.sub('([aiueoéèê])(h)([aiueoéèê])', r'\g<1>h' + zws + r'\g<3>', result)
        return result

    @staticmethod
    def _java_is_consonant(s: str) -> bool:
        return s.lower() in ScriptConverter._JAVA_WYANJANA

    @staticmethod
    def _java_is_vowel(s: str) -> bool:
        return s.lower() in ScriptConverter._JAVA_SANDHANGAN_SWARA

    @staticmethod
    def _java_is_vowel_swara(s: str) -> bool:
        return s.lower() in ScriptConverter._JAVA_SWARA

    @staticmethod
    def _java_is_panyigeg(s: str) -> bool:
        return s.lower() in ScriptConverter._JAVA_SANDHANGAN_PANYIGEG

    @staticmethod
    def _java_is_wyanjana_val(v: str) -> bool:
        return v in ScriptConverter._JAVA_WYANJANA.values()

    @staticmethod
    def _java_is_swara_val(v: str) -> bool:
        return v in ScriptConverter._JAVA_SWARA.values()

    @staticmethod
    def _java_is_sandhangan_wyanjana_val(v: str) -> bool:
        return v in ScriptConverter._JAVA_SANDHANGAN_WYANJANA.values()

    @staticmethod
    def _java_is_sandhangan_panyigeg_val(v: str) -> bool:
        return v in ScriptConverter._JAVA_SANDHANGAN_PANYIGEG.values()

    @staticmethod
    def _java_is_pasangan_below(v: str) -> bool:
        return (ScriptConverter._java_is_wyanjana_val(v) and
                v not in ScriptConverter._JAVA_WYANJANA_PASANGAN_RIGHT)

    @staticmethod
    def _latin_to_java(text: str, ignore_space: bool = False,
                       diphthong: bool = False, aksara_swara: bool = True,
                       murda: bool = False) -> str:
        W = ScriptConverter._JAVA_WYANJANA
        SW = ScriptConverter._JAVA_SWARA
        MU = ScriptConverter._JAVA_MURDA
        SWY = ScriptConverter._JAVA_SANDHANGAN_WYANJANA
        SPY = ScriptConverter._JAVA_SANDHANGAN_PANYIGEG
        SSW = ScriptConverter._JAVA_SANDHANGAN_SWARA
        ANG = ScriptConverter._JAVA_ANGKA
        PAD = ScriptConverter._JAVA_PADA

        is_con = ScriptConverter._java_is_consonant
        is_vow = ScriptConverter._java_is_vowel
        is_vow_swara = ScriptConverter._java_is_vowel_swara
        is_panyigeg = ScriptConverter._java_is_panyigeg
        is_wyanjana_val = ScriptConverter._java_is_wyanjana_val
        is_swara_val = ScriptConverter._java_is_swara_val
        is_sandhangan_wyanjana_val = ScriptConverter._java_is_sandhangan_wyanjana_val
        is_sandhangan_panyigeg_val = ScriptConverter._java_is_sandhangan_panyigeg_val
        is_pasangan_below = ScriptConverter._java_is_pasangan_below

        def is_vowel_a(s): return s.lower() in ('a', 'ô')
        def is_vowel_pepet(s): return s.lower() in ('ê', 'ě')
        def is_vowel_wulu(s): return s.lower() == 'i'
        def is_vowel_suku(s): return s.lower() == 'u'
        def is_vowel_taling(s): return s.lower() in ('e', 'é', 'è')
        def is_vowel_taling_tarung(s): return s.lower() == 'o'
        def is_pangkon(s): return s == '꧀'
        def is_cakra(s): return s == 'ꦿ'
        def is_whitespace(s): return s in (' ', '\u200b', ' ︀')
        def is_angka(s): return s in ANG
        def is_pada(s): return s in PAD

        str_list = list(text)
        length = len(str_list)
        output = []
        murda_included = False
        already_stacked = False
        i = 0

        while i < length:
            c = str_list[i]

            if i + 1 < length:
                cc = c + str_list[i + 1]

                if is_con(cc) or is_con(cc.lower()):
                    i += 1
                    if cc == cc.upper() and cc != cc.lower():
                        cc = cc.lower()

                    if is_panyigeg(cc):
                        already_stacked = False
                        if i - 2 >= 0 and i + 1 < length:
                            cb = str_list[i - 2]
                            ca = str_list[i + 1]
                            if is_vow(cb) and not is_vow(ca):
                                output.append(SPY[cc.lower()])
                                i += 1
                                continue
                        if i - 2 >= 0 and i == length - 1:
                            cb = str_list[i - 2]
                            if is_vow(cb):
                                output.append(SPY[cc.lower()])
                                i += 1
                                continue

                    if len(output) >= 2:
                        lo = output[-1]
                        lo2 = output[-2]
                        if is_pangkon(lo) and is_pasangan_below(lo2):
                            if already_stacked:
                                output.pop(); output.pop()
                                output.append('\u200b')
                                output.append(lo2); output.append(lo)
                                already_stacked = False
                            else:
                                already_stacked = True

                    if murda and not murda_included and cc.lower() in MU:
                        output.append(MU[cc.lower()])
                        murda_included = True
                    else:
                        output.append(W[cc.lower()])
                    output.append('꧀')
                    i += 1
                    continue

            if is_panyigeg(c):
                already_stacked = False
                is_spy = False
                if i - 1 >= 0 and i + 1 < length:
                    cb = str_list[i - 1]
                    ca = str_list[i + 1]
                    if is_vow(cb) and not is_vow(ca):
                        is_spy = True
                if i - 1 >= 0 and i == length - 1:
                    cb = str_list[i - 1]
                    if is_vow(cb):
                        is_spy = True
                if is_spy:
                    if output and is_pangkon(output[-1]):
                        output.pop()
                    output.append(SPY[c.lower()])
                    i += 1
                    continue

            if c.lower() in SWY:
                already_stacked = False
                is_swy = False
                if i - 2 >= 0:
                    cb2 = str_list[i - 2] + str_list[i - 1]
                    if is_con(cb2) and not is_sandhangan_panyigeg_val(output[-1] if output else ''):
                        is_swy = True
                if not is_swy and i - 1 >= 0:
                    cb = str_list[i - 1]
                    if is_con(cb) and not is_sandhangan_panyigeg_val(output[-1] if output else ''):
                        is_swy = True
                if is_swy:
                    if output and is_pangkon(output[-1]):
                        output.pop()
                    output.append(SWY[c.lower()])
                    i += 1
                    continue

            if is_con(c) or is_con(c.lower()):
                if c == c.upper() and c != c.lower():
                    c = c.lower()

                if len(output) >= 2:
                    lo = output[-1]
                    lo2 = output[-2]
                    if is_pangkon(lo) and is_pasangan_below(lo2):
                        if already_stacked:
                            output.pop(); output.pop()
                            output.append('\u200b')
                            output.append(lo2); output.append(lo)
                            already_stacked = False
                        else:
                            already_stacked = True

                if murda and not murda_included and c.lower() in MU:
                    output.append(MU[c.lower()])
                    murda_included = True
                else:
                    output.append(W[c.lower()])
                output.append('꧀')
                i += 1
                continue

            if is_vow(c) and i + 1 < length:
                c2 = str_list[i + 1]
                if is_vowel_wulu(c) and is_vow(c2) and not is_vowel_wulu(c2):
                    str_list.insert(i + 1, 'y')
                    length += 1
                elif is_vowel_suku(c) and is_vow(c2) and not is_vowel_suku(c2):
                    str_list.insert(i + 1, 'w')
                    length += 1
                elif is_vowel_taling(c) and is_vowel_a(c2):
                    str_list.insert(i + 1, 'y')
                    length += 1
                elif is_vowel_taling(c) and is_vowel_taling_tarung(c2):
                    str_list.insert(i + 1, 'y')
                    length += 1
                elif is_vowel_taling_tarung(c) and is_vowel_a(c2):
                    str_list.insert(i + 1, 'w')
                    length += 1
                elif is_vowel_taling_tarung(c) and is_vowel_taling(c2):
                    str_list.insert(i + 1, 'w')
                    length += 1

            if aksara_swara and is_vow_swara(c):
                cb = str_list[i - 1] if i - 1 >= 0 else ''
                last_empty = len(output) == 0
                last_valid = False
                last_swara = False
                if output:
                    lo = output[-1]
                    last_swara = is_swara_val(lo)
                    if len(output) >= 2:
                        lo2 = output[-2]
                        last_valid = not (
                            (is_wyanjana_val(lo2) and is_pangkon(lo)) or
                            (is_wyanjana_val(lo2) and is_sandhangan_wyanjana_val(lo))
                        )

                if last_empty or last_swara or last_valid:
                    already_stacked = False
                    if i + 1 < length and is_vow(str_list[i + 1]):
                        cc = c + str_list[i + 1]
                        if is_vow_swara(cc):
                            output.append(SW[cc.lower()])
                            i += 2
                            continue
                    output.append(SW[c.lower()])
                    i += 1
                    continue

            if is_vow(c):
                already_stacked = False

                if is_vowel_pepet(c):
                    if output and is_cakra(output[-1]):
                        output.pop()
                        output.append('ꦽ')
                        i += 1
                        continue
                    if i - 1 >= 0:
                        cb = str_list[i - 1]
                        if cb.lower() == 'l':
                            output.pop(); output.pop()
                            output.append('ꦊ')
                            i += 1
                            continue
                        if cb.lower() == 'r':
                            output.pop(); output.pop()
                            output.append('ꦉ')
                            i += 1
                            continue

                if diphthong and is_vowel_suku(c):
                    if i - 2 >= 0:
                        c2b = str_list[i - 2]
                        cb = str_list[i - 1]
                        if c2b.lower() == 'l' and is_vowel_pepet(cb):
                            output.pop()
                            output.append('ꦋ')
                            i += 1
                            continue
                        if c2b.lower() == 'r' and is_vowel_pepet(cb):
                            output.pop()
                            output.append('ꦉꦴ')
                            i += 1
                            continue

                if i - 1 >= 0 and is_con(str_list[i - 1]):
                    if output and is_pangkon(output[-1]):
                        output.pop()
                    output.append(SSW[c.lower()])
                else:
                    output.append(W['h'])
                    output.append(SSW[c.lower()])

                if diphthong and i + 1 < length and is_vow(str_list[i + 1]):
                    c2 = str_list[i + 1]
                    if is_vowel_a(c) and is_vowel_a(c2):
                        output.append(SSW['aa']); i += 1; continue
                    if is_vowel_a(c) and is_vowel_wulu(c2):
                        output.append(SSW['ai']); i += 1; continue
                    if is_vowel_a(c) and is_vowel_suku(c2):
                        output.append(SSW['au']); i += 1; continue
                    if is_vowel_wulu(c) and is_vowel_wulu(c2):
                        output.pop(); output.append(SSW['ii']); i += 1; continue
                    if is_vowel_suku(c) and is_vowel_suku(c2):
                        output.pop(); output.append(SSW['uu']); i += 1; continue
                    if is_vowel_pepet(c) and is_vowel_suku(c2):
                        output.pop(); output.append(SSW['êu']); i += 1; continue

                i += 1
                continue

            if is_angka(c):
                already_stacked = False
                output.append(ANG[c])
                i += 1
                continue

            if is_pada(c):
                already_stacked = False
                if is_whitespace(c):
                    output.append(PAD[c] if ignore_space else c)
                else:
                    output.append(PAD[c])
                i += 1
                continue

            already_stacked = False
            output.append(c)
            i += 1

        res = ''.join(output)
        res = res.replace('ꦤ꧀ꦗ', 'ꦚ꧀ꦗ')
        res = res.replace('ꦤ꧀ꦕ', 'ꦚ꧀ꦕ')
        return res

    @staticmethod
    def _java_to_kawi(java_text: str) -> str:
        whitespaces = {' ', '\u200b', '\t', '\n'}
        dictionary = {}
        dictionary.update(ScriptConverter._KAWI_SIGNS)
        dictionary.update(ScriptConverter._KAWI_INDEPENDENT_VOWELS)
        dictionary.update(ScriptConverter._KAWI_CONSONANTS)
        dictionary.update(ScriptConverter._KAWI_DEPENDENT_VOWELS)
        dictionary.update(ScriptConverter._KAWI_VIRAMAS)
        dictionary.update(ScriptConverter._KAWI_PUNCTUATIONS)
        dictionary.update(ScriptConverter._KAWI_DIGITS)

        result = []
        inp = java_text
        n = len(inp)
        i = 0
        while i < n:
            c = inp[i]

            if c == '꧀':
                if i == n - 1 or inp[i + 1] in whitespaces:
                    result.append('𑽁')
                    i += 1
                    continue

            if c == 'ꦃ' and i < n - 1:
                result.append('𑼲𑽂')
                i += 1
                continue

            if i + 1 < n:
                cc = c + inp[i + 1]
                if cc in dictionary:
                    result.append(dictionary[cc])
                    i += 2
                    continue

            if c in dictionary:
                result.append(dictionary[c])
            else:
                result.append(c)
            i += 1

        return ''.join(result)

    @staticmethod
    def transliterate_roman(text: str, scheme_name: str) -> str:
        if scheme_name == 'lontara':
            return ScriptConverter.transliterate_lontara(text)

        if scheme_name == 'kawi':
            normalized = ScriptConverter._kawi_normalize(text)
            java_text = ScriptConverter._latin_to_java(normalized)
            return ScriptConverter._java_to_kawi(java_text)

        scheme = ScriptConverter.SCHEMES.get('latin', {}).get('ke', {}).get(scheme_name)
        if not scheme:
            return text

        if scheme_name not in ['jawa', 'kawi']:
            text = ScriptConverter._strip_diacritics(text)

        obj_regex = ScriptConverter._make_regex({
            'nglegena': scheme['nglegena'],
            'mandaswara': scheme.get('mandaswara', {}),
            'swara': scheme['swara'],
            'panyigeg': scheme.get('panyigeg', {}),
            'sandhanganSwara': scheme['sandhanganSwara'],
        })

        def sigeg(c):
            panyigeg = scheme.get('panyigeg', {})
            if c in panyigeg:
                return panyigeg[c]
            return scheme['nglegena'].get(c, c) + scheme['virama']

        PATT_KRVK = 1
        PATT_KRV = 2
        PATT_KVK = 3
        PATT_KV = 4
        PATT_VK = 5
        PATT_V = 6
        PATT_O = 0

        if scheme_name == 'jawa':
            text = ScriptConverter._jawa_normalize(text)

        i_str = text.lower()

        if scheme_name == 'jawa':
            i_str = i_str.replace('è', 'é').replace('ě', 'e').replace('ê', 'e')
            i_str = re.sub(r'([aiueoéè])(h)([aiueoéè])', r'\1h h\3', i_str)
            i_str = re.sub(r'([ié])([aiueéo])', r'\1y\2', i_str)
            i_str = re.sub(r'([u])([aieéo])', r'\1w\2', i_str)
            i_str = re.sub(r'([o])([aieé])', r'\1w\2', i_str)
            i_str = re.sub(r'r([ryl])', r'r \1', i_str)
            i_str = re.sub(r'l([r])', r'l \1', i_str)
            i_str = re.sub(r'n([cj])', r'ny\1', i_str)

        ng_pat = obj_regex.get('nglegena', '')
        man_pat = obj_regex.get('mandaswara', '')
        sw_pat = obj_regex.get('swara', '')
        pan_pat = obj_regex.get('panyigeg', '')

        c1_group = f'({ng_pat})?' if ng_pat else '()?'
        r_group = f'({man_pat})?' if man_pat else '()?'
        v_group = f'({sw_pat})' if sw_pat else '()'
        c2_group = f'({ng_pat}|{pan_pat})?' if (ng_pat and pan_pat) else (f'({ng_pat})?' if ng_pat else '()?')
        vr_group = f'({man_pat}|{sw_pat})?' if (man_pat and sw_pat) else (f'({sw_pat})?' if sw_pat else '()?')

        SYLLABLE = f'^{c1_group}{r_group}{v_group}{c2_group}{vr_group}'

        c_only_pat = f'^({ng_pat}|{pan_pat})' if (ng_pat and pan_pat) else (f'^({ng_pat})' if ng_pat else None)

        o_str = ''
        i_length = len(i_str)
        idx = 0

        while idx < i_length:
            cur_idx = idx
            suku = ''
            aksara = ''

            m = re.match(SYLLABLE, i_str[idx:])
            if m and m.group(0):
                mC1 = m.group(1)
                mR = m.group(2)
                mV = m.group(3)
                mC2 = m.group(4)
                mVR = m.group(5)

                if mC1:
                    if mC2:
                        if mR:
                            pattern = PATT_KRVK if not mVR else PATT_KRV
                        else:
                            pattern = PATT_KVK if not mVR else PATT_KV
                    else:
                        pattern = PATT_KRV if mR else PATT_KV
                else:
                    if mC2:
                        pattern = PATT_V if mVR else PATT_VK
                    else:
                        pattern = PATT_V

                if pattern == PATT_KRVK:
                    suku = mC1 + (mR or '') + mV + mC2
                    aksara = (scheme['nglegena'].get(mC1, '') +
                              scheme.get('mandaswara', {}).get(mR, '') +
                              scheme['sandhanganSwara'].get(mV, '') +
                              sigeg(mC2))
                elif pattern == PATT_KRV:
                    suku = mC1 + (mR or '') + mV
                    aksara = (scheme['nglegena'].get(mC1, '') +
                              scheme.get('mandaswara', {}).get(mR, '') +
                              scheme['sandhanganSwara'].get(mV, ''))
                elif pattern == PATT_KVK:
                    suku = mC1 + mV + mC2
                    combined = mC1 + mV
                    if combined in scheme['swara']:
                        aksara = scheme['swara'][combined] + sigeg(mC2)
                    else:
                        aksara = (scheme['nglegena'].get(mC1, '') +
                                  scheme['sandhanganSwara'].get(mV, '') +
                                  sigeg(mC2))
                elif pattern == PATT_KV:
                    suku = mC1 + mV
                    combined = mC1 + mV
                    if combined in scheme['swara']:
                        aksara = scheme['swara'][combined]
                    else:
                        aksara = (scheme['nglegena'].get(mC1, '') +
                                  scheme['sandhanganSwara'].get(mV, ''))
                elif pattern == PATT_VK:
                    suku = mV + mC2
                    aksara = scheme['swara'].get(mV, '') + sigeg(mC2)
                else:
                    suku = mV
                    aksara = scheme['swara'].get(mV, '')

                o_str += aksara

            else:
                matched = False
                if c_only_pat:
                    m2 = re.match(c_only_pat, i_str[idx:])
                    if m2 and m2.group(0):
                        p1 = m2.group(1)
                        suku = p1
                        aksara = scheme['nglegena'].get(p1, scheme.get('panyigeg', {}).get(p1, p1)) + scheme['virama']
                        o_str += aksara
                        matched = True

                if not matched:
                    m3 = re.match(r'^([0-9]+)', i_str[idx:])
                    if m3 and scheme_name in ['jawa', 'sunda', 'bali', 'kawi', 'pegon']:
                        num_str = m3.group(1)
                        suku = num_str
                        aksara = scheme['pengapitAngka']
                        for digit in num_str:
                            aksara += scheme['angka'].get(digit, digit)
                        aksara += scheme['pengapitAngka']
                        o_str += aksara
                    else:
                        suku = i_str[idx]
                        o_str += suku

            if suku:
                idx += len(suku)
            else:
                idx += 1

        if scheme_name == 'jawa':
            o_str = re.sub(r'[^\S\n]+', '', o_str)

        for key, val in scheme.get('pepadan', {}).items():
            o_str = re.sub(key, val, o_str)

        if scheme_name == 'jawa':
            o_str = o_str.replace("꧀꧈", "꧀\u200C")
            o_str = o_str.replace("꧀꧉", "꧀꧈")

        return o_str

    @staticmethod
    def convert_to_script(text: str, scheme_name: str = 'jawa') -> str:
        return ScriptConverter.transliterate_roman(text, scheme_name=scheme_name)


if __name__ == "__main__":
    tests = ["ana", "bola", "sulawesi", "makassar", "bugis", "nggambar", "mpa", "nka", "nya"]
    for t in tests:
        print(f"{t} -> {ScriptConverter.convert_to_script(t, 'lontara')}")