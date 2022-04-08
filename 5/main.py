import pandas as pd
import numpy as np
import pymorphy2
from sklearn.metrics.pairwise import cosine_similarity


logic = ["AND", "OR", "NOT"]


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


def tf(vocab, list_of_words):

    tf_matrix = []

    arr = np.zeros(len(vocab))

    for i, word in enumerate(vocab):
        arr[i] = list_of_words.count(word)

    tf_matrix.append(list(map(lambda x: x / len(list_of_words), arr)))

    return np.array(tf_matrix)


def tf_idf(tf, idf):
    tf_idf_matrix = np.zeros((tf.shape[1], tf.shape[0]))

    for word_i, row in enumerate(tf.T):
        for doc_i, column in enumerate(row):
            tf_idf_matrix[word_i][doc_i] = column * idf[word_i]

    return tf_idf_matrix


def search(text):
    list_of_words = to_normal_form(text.lower().split(" "))
    inverse_index = create_index()
    set_of_words = list(inverse_index.keys())
    tf_of_search = tf(set_of_words, list_of_words)

    idf = pd.read_csv("../4/idf.csv").to_numpy().T[1]

    tf_idf_of_search = tf_idf(tf_of_search, idf).T[0]

    tf_idf_of_all_docs = pd.read_csv("../4/tf_idf.csv").to_numpy().T

    cosines = list(zip(range(1, 101), cosine_similarity(tf_idf_of_all_docs[1:], tf_idf_of_search.reshape(1, -1)).T[0]))

    return sorted(cosines, key=lambda tup: tup[1], reverse=True)


def get_relevant_docs(text, top_n):
    relevant_docs = search(text)
    return relevant_docs[:top_n]


if __name__ == "__main__":

    text = "структура кфу"

    print(get_relevant_docs(text, 100))