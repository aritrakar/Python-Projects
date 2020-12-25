import os
import json
import nltk
import random
import pickle
import tflearn
import numpy as np
import tensorflow as tf
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

with open("intents.json") as file:
    data = json.load(file)

try:
    x
    print("FETCHING MODEL")
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    print("TRAINING MODEL")
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    # One-hot encoding
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])  # Input layer
# Add this fully connected layer to our neural network. 8 neurons in this hidden layer
net = tflearn.fully_connected(net, 8)  # Hidden layer 1
net = tflearn.fully_connected(net, 8)  # Hidden layer 2
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)  # Output layer

# Train the model
model = tflearn.DNN(net)

try:
    print("TRYING TO LOAD MODEL")
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def getResponse(s):
    prediction = model.predict([bag_of_words(s, words)])[0]
    prediction_index = np.argmax(prediction)
    tag = labels[prediction_index]
    #print("tag: ", tag)
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
    return (random.choice(responses), tag)
