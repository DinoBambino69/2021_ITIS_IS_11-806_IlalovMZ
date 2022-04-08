import math
import os

import numpy as np
import pandas as pd


def tf(vocab):
    tf_matrix = []
    all_docs = [f"../2/tokenFiles/{i}.txt" for i in range(1, 101)]

    for document_number, doc in enumerate(all_docs):
        arr = np.zeros(len(vocab))
        with open(f"{doc}") as f:
            words_in_document = f.readline().split()
            for i, word in enumerate(vocab):
                arr[i] = words_in_document.count(word)

        tf_matrix.append(list(map(lambda x: round(x / len(words_in_document), 5), arr)))

    return np.array(tf_matrix)


def idf(inverse_index, n_docs=100):
    idf_per_word_in_vocab = np.zeros(len(inverse_index))
    for i, word in enumerate(inverse_index.keys()):
        idf_per_word_in_vocab[i] = round(math.log(n_docs / len(inverse_index[word])), 5)

    return idf_per_word_in_vocab


def tf_idf(tf, idf):
    tf_idf_matrix = np.zeros((tf.shape[1], tf.shape[0]))

    for word_i, row in enumerate(tf.T):
        for doc_i, column in enumerate(row):
            tf_idf_matrix[word_i][doc_i] = round(column * idf[word_i], 5)

    return tf_idf_matrix


def to_df(arr, set_of_words):
    df = pd.DataFrame(arr)
    dict_of_indexes = dict()

    for i, word in enumerate(set_of_words):
        dict_of_indexes[i] = word

    return df.rename(index=dict_of_indexes)


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




if __name__ == "__main__":
    inverse_index = create_index()

    set_of_words = list(inverse_index.keys())

    tf_result = tf(set_of_words)

    tf_df = to_df(tf_result.T, set_of_words)
    tf_df.to_csv("tf.csv")

    idf_out = idf(inverse_index)
    idf_df = pd.DataFrame.from_dict({k: v for k, v in zip(inverse_index.keys(), idf_out)}, orient='index')
    idf_df.to_csv("idf.csv")

    tf_idf_out = tf_idf(tf_result, idf_out)
    tf_idf_df = to_df(tf_idf_out, set_of_words)
    tf_idf_df.to_csv("tf_idf.csv")
