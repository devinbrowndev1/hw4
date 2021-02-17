#!/usr/bin/env python
# coding: utf-8

# In[15]:


import sys
import re
import numpy as np
import sklearn
import os
import nltk
from collections import Counter
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd
from copy import deepcopy
import scipy.stats
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import sklearn_crfsuite
import pprint

def feat_vector(ngram_l, unique_ngrams):
    #skeleton dictionary
    temp_dict = dict.fromkeys(unique_ngrams,0)
    temp_counter = Counter(ngram_l)
    for k in temp_counter:
        if k in temp_dict:
            temp_dict[k] = temp_counter[k]
        else:
            temp_dict['unk'] += temp_counter[k]
    return list(temp_dict.values())

        
def convert_to_ngrams(sentences):
    #convert text input to bigrams
    ngram_list = []

    for l in sentences:
        unigram_list = list(l.split()) # [[()()()], [()()()]]
        bigram_list = list(nltk.bigrams(l.split()))
        trigram_list = list(nltk.trigrams(l.split()))

        ngram_list.append(unigram_list + bigram_list + trigram_list)

    #get unique ngrams
    biglist = []
    for sentence in ngram_list:
        for ngram in sentence:
            biglist += ngram

    unique_ngrams = list(set(biglist))
    unique_ngrams.append("unk")

    return ngram_list, unique_ngrams



def create_intents_train_test(ngram_sentences, unique_ngrams):
    #initialize training set
    total_train = [feat_vector(l, unique_ngrams) for l in ngram_sentences]

    return total_train


# # TRAIN MODEL 

def train_intent_model(train_X, train_Y):
    model = sklearn.svm.SVC(kernel='linear')
    model.fit(train_X,train_Y)
    
    return model




# # CRF 

def process_data(filename):
    intent_labels = []
    intent_input = []

    utterances_annotated = []
    utterances_unannotated = []


    with open(filename) as f:
        for line in f:
            line = line.strip().split("\t")
            intent_labels.append(line[0])
            utterances_annotated.append(line[1])
            utterances_unannotated.append(re.sub('<[^>]*>','',line[1]))

            temp_sent = re.sub('<[^>]*>','',line[1])
            temp_sent = 'BOS {} EOS'.format(temp_sent)
            intent_input.append(temp_sent)

    return intent_labels, intent_input, utterances_annotated, utterances_unannotated
            



flavors = ["vegan", "hawaiian", "meat lovers", "4 cheese", "pepperoni", "veggie supreme"]
sizes = ["small", "medium", "large"]
crusts = ["thin", "regular", "gluten-free","gluten free", "deep-dish", "deep dish"]
toppings = ['spinach','kale','cheese','onions','olives','swiss cheese','pineapple','provolone cheese','anchovies','extra cheese','peppers','pepporoni','sausage','ham','mushrooms']
delivery = ['pickup','pick-up','delivery','delivered','pick up','take-out','take out']



def word2features(sent, i):
    word = sent[i][0]
    postag = nltk.pos_tag([sent[i][0]])[0][1]
    
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    
                         
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = nltk.pos_tag([sent[i-1][0]])[0][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = nltk.pos_tag([sent[i+1][0]])[0][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True
        
        
    for i, lexicon in enumerate([flavors, sizes, crusts, toppings,delivery]):
        if word.lower() in lexicon:
            if i == 0:
                features['flavors'] = True
            elif i == 1:
                features['sizes'] = True
            elif i == 2:
                features['crusts'] = True
            elif i == 3:
                features['toppings'] = True
            elif i == 4:
                features['delivery'] = True

    return features



# returns sentence tagged with BIO instead of html tags
def sent2BIO(sent):
    beginning = re.compile("<([^/]*)>([^<]*)")
    end = re.compile("(.*)</.*>")
    sent = re.sub(" </", "</", sent)

    sent = sent.split()
    inside = False
    inside_tag = ""
    bio_sent = []

    for word in sent:
        if not inside:
            if beginning.search(word) is not None:
                inside_tag = beginning.search(word).groups()[0]
                bio_sent.append((beginning.search(word).groups()[1], "B-"+inside_tag))
                inside = True

                if end.search(word) is not None:
                    inside = False

            else:
                bio_sent.append((word, "O"))
        else:
            if end.search(word) is not None:
                bio_sent.append((end.search(word).groups()[0], "I-"+inside_tag))
                inside = False
            else:
                bio_sent.append((word, "I-"+inside_tag))

    return bio_sent

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, label in sent]

def sent2tokens(sent):
    return [token for token, label in sent]


def train_crf(utterances_anno):

    train_sents = [sent2BIO(s) for s in utterances_anno] # change `sentences` to train input
    test_sents = [sent2BIO(s) for s in utterances_anno] # change `sentences` to test input

    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]


    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    # train
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=20,
        all_possible_transitions=False,
    )
    crf.fit(X_train, y_train);

    y_preds = crf.predict(X_test)
    labels = crf.classes_

    print(metrics.flat_f1_score(y_test, y_preds, average='weighted', labels=labels))

    return crf



if __name__ == "__main__":
    # read in the data

    intent_labels, intent_input, utterances_anno, utterances_unanno = process_data('group1_data.txt')

    # train the intents model
    intent_input, unique_ngrams = convert_to_ngrams(intent_input) # length = # of sentences (list of bigrams)

    intent_input = create_intents_train_test(intent_input, unique_ngrams) # length = # of sentences (list of features)

    intent_mod = train_intent_model(intent_input, intent_labels)

    # train the slots model
    slots_mod = train_crf(utterances_anno)

    # read from stdin

    in_value = ""

    while in_value != "q":
        print("Enter an utterance:")
        in_value = input()

        intent_val, trash = convert_to_ngrams(["BOS "+in_value+" EOS"])
        intent_val = feat_vector(intent_val[0], unique_ngrams)

        slots_val = sent2features([(w,) for w in in_value.split()])

        intent = intent_mod.predict([intent_val])
        slots = slots_mod.predict([slots_val])

        print("{}\t{}".format(intent, slots))





