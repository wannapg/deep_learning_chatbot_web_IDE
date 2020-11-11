import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer=LancasterStemmer()

import numpy
import tflearn 
import tensorflow
import random 
import json 
import pickle

with open("intents.json") as file: 
    data = json.load(file)
try:
    with open("data.pickle","rb") as f : 
        words,labels, training,output=pickle.load(f)
except: 
    words = []
    labels = []
    docs_x = [] #list of patterns 
    docs_y = []

    for intent in data["intents"]:
         for pattern in intent["patterns"]: 
            wrds=nltk.word_tokenize(pattern)
            words.extend(wrds)# add the words
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

         if intent["tag"] not in labels:
            labels.append(intent["tag"])
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    #one hot encoding word 가 존재하는지 안하는지 표시 
    training = []
    output = [] 

    out_empty = [0 for _ in range(len(labels))]

    for x,doc in enumerate(docs_x): 
         bag = [] 

    wrds = [stemmer.stem(w) for w in doc]

    for w in words: 
        if w in wrds: 
            bag.append(1) # bag 의 값이 존재해서 1 append
        else :
            bag.append(0) # bag의 단어가 존재하지 않는 경우
    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle","wb") as f : 
       pickle.dump((words,labels, training,output),f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None,len(training[0])]) #get shape of input
net = tflearn.fully_connected(net,8) #hidden layer
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]),activation="softmax")#get probabliites
net = tflearn.regression(net)

model = tflearn.DNN(net)

try: 
    model.load("model.tflearn")
except: 
    model.fit(training, output, n_epoch=1000,batch_size=8,show_metric=True) #
    model.save("model.tflearn")

#prediction 
#input of user words into bag of words
def bag_of_words(s, words): 
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s) #list of tokenized words
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words: 
        for i, w in enumerate(words):
            if w == se: #current word is equal to sth in our sentense
                bag[i] = 1

    return numpy.array(bag)


def chat():
    print("Start talking with the bot!(type quit to stop) ")
    while True:
        inp = input("You: ")
        if inp.lower()=="quit":
            break
        results = model.predict([bag_of_words(inp,words)])[0] #첫번째꺼 고르고
        results_index = numpy.argmax(results) #largest prediction 값 골라 
        tag = labels[results_index]
        
        if results[results_index]>0.7 : #70%의 정확도를 가질 경우만 
            for tg in data["intents"]:
                if tg['tag']==tag: 
                    responses = tg['responses']
        
            print(random.choice(responses))
        else:
            print("I didn't get that, try again. ")

chat()