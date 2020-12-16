
# ********** LET'S TRANSLATE SOME STUFF *****************
# SOURCE: https://github.com/lushan88a/google_trans_new
# Many thanks to puzpy, available at https://github.com/alexdej/puzpy

# TO-DO: fix ["First clue", "Second clue"] pattern


from google_trans_new import google_translator
import puz
import re
import random
import sys

# LANGUAGES
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'}

# SHORTER LIST OF LANGUAGES
LATIN_LANG = {
	'af': 'afrikaans',
    'eu': 'basque',
    'ca': 'catalan',
    'da': 'danish',
    'nl': 'dutch', 
    'fi': 'finnish',
    'fr': 'french',   
    'gl': 'galician',
    'de': 'german',   
    'is': 'icelandic',  
    'id': 'indonesian',
    'it': 'italian',   
    'ms': 'malay',
    'no': 'norwegian',    
    'pt': 'portuguese',
    'es': 'spanish',
    'sw': 'swahili',
    'sv': 'swedish'
}

# READING PUZ FILE
filename= sys.argv[1]

# NOTE: The .puz file to translate should be in a folder called "puztranslate"
p = puz.read(filename + ".puz")

old_clues = p.clues
new_clues = []

# TRANSLATING THAT BAD BOY
from multiprocessing.dummy import Pool as ThreadPool
import time

pool = ThreadPool(20) # Threads

def request(text):
    lang = "fr"
    t = google_translator(timeout=5)
    # TRANSLATES TO RANDOM LANGUAGES A RANDOM NUMBER OF TIMES
    num_translations = 4
    for i in range(num_translations):
        lang = random.choice(list(LATIN_LANG.keys()))
        text = t.translate(text, lang)
        text = t.translate(text, "en")
    translateFINAL = t.translate(text, "en")
    #translateFINAL = t.translate(translateFINAL, "la")
    #translateFINAL = t.translate(translateFINAL, "en")   
    translateFINAL = re.sub(u"(\u201c|\u201d)", "\"", translateFINAL)
    translateFINAL = re.sub(u"(\u2018|\u2019)", "'", translateFINAL)

    return translateFINAL

if __name__ == "__main__" :
    time1 = time.time()
    texts = p.clues
    print("Translating...")
    results = pool.map(request, texts)
    pool.close()
    pool.join()

    time2 = time.time()
    print("Translating %s clues, a total of %s s"%(len(texts),time2 - time1))

p.clues = results

p.save(filename + '_TRANSLATED.puz')