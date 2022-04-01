import os
import pymorphy2

logic = ["AND", "OR", "NOT"]


def to_normal_form(arr):
    morph = pymorphy2.MorphAnalyzer(lang='ru')

    normal_form = []

    for i, word in enumerate(arr):
        if word not in logic:
            p = morph.parse(word)[0]
            word_in_normal_form = p.normal_form
            normal_form.append(word_in_normal_form)
        else:
            normal_form.append(word)

    return normal_form


def create_index():
    files = [f"../2/tokenFiles/{i}.txt" for i in range(1, 101)]

    word_map_to_document = dict()

    for i, filename in enumerate(files):
        i += 1
        with open(f"{filename}", "r") as file:
            words = file.readline().split()
            for word in words:
                if word not in word_map_to_document:
                    word_map_to_document[word] = {i}
                else:
                    word_map_to_document.get(word).add(i)

    return word_map_to_document


def func_by_token(token, set_to_operate, set_to_insert):
    if token == logic[0]:
        set_to_operate.intersection_update(set_to_insert)

    if token == logic[1]:
        set_to_operate.update(set_to_insert)

    if token == logic[2]:
        set_to_operate.difference_update(set_to_insert)

    return set_to_operate


def parse(list_of_tokens, dict_of_words):

    list_of_tokens = to_normal_form(list_of_tokens)

    print(list_of_tokens)

    if list_of_tokens[0] != logic[2]:
        set_of_all_docs = set(dict_of_words[list_of_tokens[0]])
        i = 1
    else:
        set_of_all_docs = set(range(0, 100))
        set_of_all_docs.difference_update(dict_of_words[list_of_tokens[1]])
        i = 2

    while i < len(list_of_tokens) - 1:

        token = list_of_tokens[i]
        next_token = list_of_tokens[i + 1]

        if next_token != logic[2]:
            func_by_token(token, set_of_all_docs, dict_of_words[next_token])
            i += 2

        else:
            set_of_docs_without_next_token = set(range(1, 101)).difference(dict_of_words[list_of_tokens[i + 2]])
            func_by_token(token, set_of_all_docs, set_of_docs_without_next_token)
            i += 3

    return set_of_all_docs


def main():
    invert_index = create_index()
    file_result = open('index.txt', 'w', errors="ignore")
    file_result.write(str(invert_index))
    search1 = "федеральный OR казанский AND NOT подразделение"
    set1 = parse(search1.split(" "), invert_index)

    print(set1)


if __name__ == "__main__":
    main()
