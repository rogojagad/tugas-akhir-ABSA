import pickle
import json
import numpy as np
from pprint import pprint
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

with open("D://Kuliah/TA/data/test/sentiment_analyze_result.pickle", "rb") as inp:
    results = pickle.load(inp)

with open("D://Kuliah/TA/data/test/aspect_sentiment_truth.pickle", "rb") as inp:
    truths = pickle.load(inp)

with open("dataset/test-dataset.json") as f:
    dataset = json.load(f)
#
error_counter = 0
missing = 0
aspect_count = 0
predictions = []
true_labels = []

for truth, result, data in zip(truths, results, dataset):
    for aspect, sentiment in truth["data"].items():
        aspect_count += 1
        try:
            predictions.append(result["data"][aspect])
            true_labels.append(sentiment)

            if result["data"][aspect] != sentiment:
                print(data["sentence"])
                print(result["id"])
                print(aspect)
                print("Truth")
                print(sentiment)
                print("Result")
                print(result["data"][aspect])
                print()
                error_counter += 1
        except KeyError:
            missing += 1
            continue

labels = {"positive": 0, "negative": 1, "neutral": 2}

predictions_np = np.array([labels[label] for label in predictions])
true_labels_np = np.array([labels[label] for label in true_labels])

print("Aspect count : {}".format(aspect_count))
print("Error : {}".format(error_counter))
print("Missing : {}".format(missing))
# print()
# print(
#     classification_report(
#         true_labels_np, predictions_np, target_names=["Positive", "Negative", "Neutral"]
#     )
# )
# print(confusion_matrix(true_labels_np, predictions_np, labels=[0, 1, 2]))
print("Accuracy : {}".format(accuracy_score(true_labels_np, predictions_np)))
