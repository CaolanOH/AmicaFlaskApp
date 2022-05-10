import random
import json 
import pickle 
import numpy as np
import nltk
#Uncomment these on first run of this file to download these
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
#This loads the model from the chatbot_model.h5 file
from tensorflow.keras.models import load_model
# Getting working directory
from pathlib import Path 

# This stores whatever the working directory is to the variable working__directory
working_directory = Path(__file__).absolute().parent
# calling lemmatizer
lemmatizer = WordNetLemmatizer()
# opening intents json, word pickle file, tags pickle file, and loading in NN model
intents = json.loads(open(working_directory / 'intents.json').read())
words = pickle.load(open(working_directory / 'words.pkl', 'rb'))
tags = pickle.load(open(working_directory / 'tags.pkl','rb'))
model = load_model(working_directory / 'chatbot_model.h5')

# This function takes in a users message as a parameter and returns an of tokenized words
def tokenize_and_lemmatize_user_message(message):
    message_words = nltk.word_tokenize(message)
    message_words = [lemmatizer.lemmatize(word) for word in message_words]
    return message_words

# This function takes in the user message, tokenizes it, creates a bag of words of encoded words and returns a numpy array of the bag of words
def bag_of_words(message):
    # tokenizing user message
    message_words = tokenize_and_lemmatize_user_message(message)
    #Creating a bag of words equal to the number of words from the words.pkl file
    b_o_w = [0] * len(words)
    # encoding words in the bag of words. 
    for w in message_words:
        for i, word in enumerate(words):
            # if word is not in word python defaults the value to 0
            if word == w:
                b_o_w[i] = 1
    # return a numpy array so the model can read it
    return np.array(b_o_w)


context = {}
def predict_tag(message):
    bag = bag_of_words(message)
    res = model.predict(np.array([bag]))[0]
    error_threshold = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': tags[r[0]], 'probability': str(r[1])})
    print(f'This is the return list : {return_list}')
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            print(f'printing i : {i}')
            if 'context_set' in i:
                context['context'] = i['context_set']
                print(f'this is the current context : {context}')
                # check if this intent is contextual and applies to this user's conversation
                if not 'context_filter' in i or \
                        (context in context and 'context_filter' in i and i['context_filter'] == context['userID']):
                    result = {
                        "tag":i['tag'],
                        "response": random.choice(i['responses']),
                        "action": i['action']
                    }
                    break
            else:
                result = {
                    "response":random.choice(i['responses']),
                    "action":i['action']
                }
                    
    return result

# if not 'context_filter' in i or 'context' in context and 'context_filter' in i and i['context_filter'] == context['context']: 
#  if not 'context_filter' in i or \
#                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
#def chat():
#    print("*** Chat bot is ready to chat ****")
#    while True:
#        user_message = input("User : ")
#        if user_message.lower() == "quit":
#            break
#        results = model.predict([bag_of_words(user_message, words)])[0]
#        results_index = np.argmax(results)
#        tag = words_and_tags[results_index]
#
#        if results[results_index] > 0.7:
#            for tg in intents['intents']:
#                if tg['tag'] == tag:
#                    responses = tg['response']
#            print(random.choice(responses))
#        else:
#            print("I dont't understand")

# def get_response(ints, intents_json):
#     tag = ints[0]['intent']
#     list_of_intents = intents_json['intents']
#     for i in list_of_intents:
#         if(i['tag']== tag):
#             result = {
#                 "response": random.choice(i['responses']),
#                 "action": i['action']
#             }
#             break
#     return result

#chat() 
# def chat():
#     print("*** Chat bot is ready to chat ****")
#     print(tags)
#     while True:
#         user_message = input("User : ")
#         if user_message.lower() == "quit":
#             break
#         ints = predict_tag(user_message)
#         bot_response = get_response(ints, intents)
#         print(f'Bot : {bot_response}')

# chat()

def chat(message):
   tags = predict_tag(message)
   bot_response = get_response(tags, intents)
   return bot_response