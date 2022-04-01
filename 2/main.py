import string
import re
import pymorphy2
import cld2


def tokenize():
    setList = set()
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    for i in range(1, 101):
        file = open(f'files/{i}.txt', 'r', encoding='utf-8')
        text = file.read()

        for p in string.punctuation:
            if p in text:
                text = text.replace(p, '')

        text = re.sub(r'[^\w\s]+|[\d]+', r'', text).strip()
        words = text.split()
        tokens = open(f'tokenFiles/{i}.txt', 'w', encoding='utf-8')
        for word in words:
            if cld2.detect(word).details[1].language_name == 'RUSSIAN':
                continue
            try:
                normal_word = morph.parse(word)[0]
                tokens.write(str(normal_word.normal_form) + " ")
                setList.add(str(normal_word.normal_form))
            except UnicodeEncodeError:
                print(UnicodeEncodeError)
                pass
    return setList


def lemmatize(words):
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    obj = {}
    for word in words:
        word = word.lower()
        if cld2.detect(word).details[0].language_name == 'RUSSIAN':
            continue
        p = morph.parse(word)[0].normal_form
        if not p in obj.keys():
            obj[p] = [word]
        else:
            if not word in obj[p]:
                obj[p].append(word)
    lemmas = open(f'index.txt', 'w', encoding='utf-8')
    for elem in obj.keys():
        lemmas.write(elem + " - " + str(obj[elem]) + "\n")


if __name__ == "__main__":
    words = tokenize()
    lemmatize(words)
