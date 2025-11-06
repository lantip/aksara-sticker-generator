import re
from typing import Dict, List, Tuple
import unicodedata

class ScriptConverter:
    SCHEMES: Dict[str, Dict[str, Dict[str, str]]] = {
        'latin': {
            'ke': {
                'jawa': {
                    'virama': "꧀", 'pengapitAngka': "꧇", 'nglegena': {
                        "k": "ꦏ", "kh": "ꦏ꦳", "q": "ꦐ", "g": "ꦒ", "gh": "ꦒ꦳", "ng": "ꦔ", "c": "ꦕ", "j": "ꦗ", "z": "ꦗ꦳", "ny": "ꦚ", "th": "ꦛ", "dh": "ꦝ", "t": "ꦠ", "d": "ꦢ", "n": "ꦤ", "p": "ꦥ", "f": "ꦥ᳠", "b": "ꦧ", "m": "ꦩ", "y": "ꦪ", "r": "ꦫ", "l": "ꦭ", "w": "ꦮ", "v": "ꦮ᳠", "s": "ꦱ", "h": "ꦲ"
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
                }
            }
        }
    }

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
    def _make_regex(a: Dict) -> Dict[str, str]:
        n: Dict[str, str] = {}
        for e in a:
            g: List[str] = []
            for key in a[e].keys():
                g.append(ScriptConverter._reg_ex_backslash(key))
            g = ScriptConverter._sort_array(g)
            n[e] = ScriptConverter._array_to_regex(g)
        return n
    
    @staticmethod
    def transliterate_roman(text: str, scheme_name: str) -> str:        
        scheme = ScriptConverter.SCHEMES.get('latin', {}).get('ke', {}).get(scheme_name)
        if not scheme: 
            return text 

        if scheme_name != 'jawa':
            text = ScriptConverter._strip_diacritics(text)

        r = scheme
        
        text_lower = text.lower()
        if scheme_name == 'jawa':
            text_lower = text_lower.replace('è', 'é').replace('ě', 'e').replace('ê', 'e')
            text_lower = re.sub(r'([ié])([aiueéo])', r'\1y\2', text_lower)
            text_lower = re.sub(r'([u])([aieéo])', r'\1w\2', text_lower)
            text_lower = re.sub(r'([o])([aieé])', r'\1w\2', text_lower)
            text_lower = re.sub(r'r([ryl])', r'r \1', text_lower)
            text_lower = re.sub(r'l([r])', r'l \1', text_lower)
            text_lower = re.sub(r'n([cj])', r'ny\1', text_lower)
            text_lower = text_lower.replace('a ', 'a').replace('a\n', 'a')
            
        p = len(text_lower)
        u = 0
        k = ""
        
        all_patterns = []
        
        if scheme_name == 'jawa':
            all_patterns.append(("re", r['swara']['re'])) 
            all_patterns.append(("le", r['swara']['le'])) 

        for c_key, c_val in r['nglegena'].items():
            for v_key, v_val in r['sandhanganSwara'].items():
                all_patterns.append((c_key + v_key, c_val + v_val))
            for m_key, m_val in r.get('mandaswara', {}).items():
                for v_key, v_val in r['sandhanganSwara'].items():
                     all_patterns.append((c_key + m_key + v_key, c_val + m_val + v_val))

        for v_key, v_val in r['swara'].items():
             all_patterns.append((v_key, v_val))
        
        for c_key, c_val in r['nglegena'].items():
             all_patterns.append((c_key, c_val))

        panyigeg_patterns = []
        for p_key, p_val in r.get('panyigeg', {}).items():
             panyigeg_patterns.append((p_key, p_val))
             all_patterns.append((p_key, p_val))

        all_patterns.sort(key=lambda x: len(x[0]), reverse=True)
        panyigeg_patterns.sort(key=lambda x: len(x[0]), reverse=True)
        
        vowels = r['swara'].keys()
        
        while u < p:
            current_substring = text_lower[u:]
            matched_len = 0
            t = ""
            h = "" 
            matched = False
            
            for roman_panyigeg, script_panyigeg in panyigeg_patterns:
                if current_substring.startswith(roman_panyigeg):
                    next_char = text_lower[u + len(roman_panyigeg): u + len(roman_panyigeg) + 1]
                    is_followed_by_boundary = not next_char.isalnum() and not next_char.strip()
                    
                    if not next_char.strip() or is_followed_by_boundary:
                        h = roman_panyigeg
                        t = script_panyigeg
                        k += t
                        matched_len = len(h)
                        matched = True
                        break

            if matched:
                u += matched_len
                continue

            for roman_chunk, script_chunk in all_patterns:
                if current_substring.startswith(roman_chunk):
                    
                    if roman_chunk in r.get('panyigeg', {}):
                        continue 

                    h = roman_chunk
                    t = script_chunk
                    matched_len = len(h)
                    
                    is_bare_consonant_match = roman_chunk in r['nglegena'] and matched_len == len(roman_chunk) and not any(v in roman_chunk for v in vowels)
                    
                    if is_bare_consonant_match and scheme_name in ['jawa', 'sunda', 'bali']:
                        next_char = text_lower[u + len(h): u + len(h) + 1]
                        
                        if not next_char.strip() or (next_char.strip() and next_char not in vowels):
                            if scheme_name == 'jawa' and k.endswith(r['virama']):
                                pass 
                            else:
                                t += r['virama']

                    k += t
                    matched = True
                    break
            
            if not matched:
                
                num_match = re.match(r'^[0-9]+', current_substring)
                if num_match and scheme_name in ['jawa', 'sunda', 'bali', 'kawi', 'pegon']:
                    num_str = num_match.group(0)
                    h = num_str
                    t = r['pengapitAngka']
                    for digit in h:
                         t += r['angka'].get(digit, digit)
                    t += r['pengapitAngka']
                    k += t
                    matched_len = len(h)

                else:
                    char = current_substring[0]
                    k += char 
                    matched_len = 1
            
            u += matched_len
            if matched_len == 0 and u < p: 
                u += 1

        if scheme_name == 'jawa':
            k = k.replace(" ", "") 
            k = k.replace("꧀꧈", "꧀‌").replace("꧀꧉", "꧀꧈")
            
            for key, val in r['pepadan'].items():
                k = re.sub(key, val, k)

        return k

    @staticmethod
    def convert_to_script(text: str, scheme_name: str = 'jawa') -> str:
        return ScriptConverter.transliterate_roman(text, scheme_name=scheme_name)