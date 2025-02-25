
# coding: utf-8

# In[1]:


import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


# In[2]:


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


# In[3]:


documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()


# In[4]:


word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


# In[5]:


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


# In[7]:


featuresets_f = open("pickled_algos/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()


# In[8]:


random.shuffle(featuresets)
print(len(featuresets))


# In[9]:


testing_set = featuresets[10000:]
training_set = featuresets[:10000]


# In[14]:


open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/BernouliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/SGDClassifier_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/SVC_classifier5k.pickle", "rb")
SVC_classifier = pickle.load(open_file)
open_file.close()

open_file = open("pickled_algos/NuSVC_classifier5k.pickle", "rb")
NuSVC_classifier = pickle.load(open_file)
open_file.close()


# In[25]:


voted_classifier = VoteClassifier(classifier,
                                  MNB_classifier,
                                  LogisticRegression_classifier,
                                  BernoulliNB_classifier,
#                                   SGDC_classifier,
                                  LinearSVC_classifier,
#                                   SVC_classifier, 
#                                   NuSVC_classifier
                                 )


# In[26]:


# print("Voted classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)


# In[27]:


def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
