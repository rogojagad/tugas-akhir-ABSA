import pycrfsuite
import pickle
import sys
from pprint import pprint
from custom_utils import *
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np

data_dir = "D:\Kuliah\TA\data"


def load_train_data():
    with open(data_dir + "\\train\\features.pickle", "rb") as inp:
        feature = pickle.load(inp)

    with open(data_dir + "\\train\\labels.pickle", "rb") as inp:
        labels = pickle.load(inp)

    return feature, labels


def train(X_train, y_train):
    trainer = pycrfsuite.Trainer()

    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({"feature.possible_states": True})

    trainer.train("crf.model")


def load_test_data():
    with open(data_dir + "\\test\\features.pickle", "rb") as inp:
        feature = pickle.load(inp)

    with open(data_dir + "\\test\\labels.pickle", "rb") as inp:
        labels = pickle.load(inp)

    return feature, labels


def predict(X_test):
    print("=========== NOW DETECTING ASPECT TERM ON TEST DATA ===============\n")

    tagger = pycrfsuite.Tagger("crf.model")

    tagger.open("crf.model")

    result = [tagger.tag(xseq) for xseq in X_test]

    print("===========               FINISH                   ===============\n")

    return result


def make_result(y_result):
    with open(data_dir + "\\test\\labelled_words.pickle", "rb") as inp:
        words = pickle.load(inp)

    prediction_result = []

    for data in zip(words, y_result):
        temp = []

        for i in range(len(data[0])):
            word = data[0][i][0]
            pos = data[0][i][1]
            label = data[1][i]

            temp.append((word, pos, label))

        prediction_result.append(temp)

    return prediction_result


def evaluate(y_test, y_pred):
    labels = {"B": 0, "I": 1, "O": 2}

    predictions = np.array([labels[tag] for row in y_pred for tag in row])
    truths = np.array([labels[tag] for row in y_test for tag in row])

    print(classification_report(truths, predictions, target_names=["B", "I", "O"]))

    print(confusion_matrix(truths, predictions, labels=[0, 1, 2]))


if __name__ == "__main__":
    xseq, yseq = load_train_data()

    train(xseq, yseq)

    X_test, y_test = load_test_data()

    y_result = predict(X_test)

    evaluate(y_test, y_result)

    export(y_result, "\\test\prediction_labels.pickle")

    prediction_result = make_result(y_result)

    export(prediction_result, "\\test\prediction_result.pickle")
