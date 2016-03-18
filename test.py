import json
import math
import nltk

from pprint import pprint
from collections import defaultdict

with open('movies_pages_Action.json') as data_file:
    data = json.load(data_file)

numberOfMovies = 0
numberOfMoviesWithOutRate = 0
distributor = {}

#print(float(numberOfMoviesWithOutRate)/float(numberOfMovies))
#print(distributor)


def getNullPercentFrom(data, field):

    numberOfValues = 0
    numberOfNullValues = 0

    for movie in data:
        numberOfValues += 1
        if (data[movie][field] is None):
            numberOfNullValues += 1
    percentNull = round(float(numberOfNullValues)/float(numberOfValues), 2) * 100
    print(field + " has " + str(percentNull) + "% of null values")
    return percentNull


def getRateDistribution(data):

    rateDistribution = {}
    for movie in data:
        if (data[movie]["spectator_rate"] is not None):
            rate = math.ceil(data[movie]["spectator_rate"])
            try:
                rateDistribution[rate] += 1
            except:
                rateDistribution[rate] = 1
    print(rateDistribution)
    return rateDistribution


def getWordFrequency(data):

    wordFrequency = {}
    for movie in data:
        listOfWords = nltk.word_tokenize(data[movie]["summary"])
        for token in listOfWords:
            try:
                wordFrequency[token] += 1
            except:
                wordFrequency[token] = 1
    print(wordFrequency)
    return wordFrequency

'''
def getFieldDistribution(data, field):
'''


for key in data[data.keys()[0]].keys():
    getNullPercentFrom(data, key)

with open('rate.json', 'w') as fp:
    json.dump(getRateDistribution(data), fp)

getWordFrequency(data)
