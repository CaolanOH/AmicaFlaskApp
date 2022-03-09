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
# opeing intents json, word pickle file, words_and_tags pickle file, and loading in RNN model
intents = json.loads(open('intents.json').read())
print(f'This is the intents json {intents}')
words = pickle.load(open('words.pkl', 'rb'))
print(f'This is the words pickle {words}')
words_and_tags = pickle.load(open('words_and_tags.pkl','rb'))
print(f'This is the words and tags pickle {words_and_tags}')
model = load_model('chatbot_model.h5')

# This function takes in a users message as a parameter and returns an of tokenized words
def tokenize_and_lemmatize_user_message(message):
    message_words = nltk.word_tokenize(message)
    message_words = [lemmatizer.lemmatize(word) for word in message_words]
    return message_words

# This function takes in the user message, tokenizes it, creates a bag of words of encoded words and return a numpy array of the bag of words
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
            
        print(f'This is the users bag of words encoded : {b_o_w}')
    # return a numpy array so the model can read it
    return np.array(b_o_w)

def predict_tag(message):
    bag = bag_of_words(message)
    res = model.predict(np.array([bag]))[0]
    error_threshold = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': words_and_tags[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    print(f'This is the tag{tag}')
    list_of_intents = intents_json['intents']
    print(f'This is the list_of_intents{list_of_intents}')
    for i in list_of_intents:
        print(f'This is i {i}')
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result
        
def chat():
    print("*** Chat bot is ready to chat ****")
    while True:
        user_message = input("User : ")
        if user_message.lower() == "quit":
            break
        ints = predict_tag(user_message)
        bot_response = get_response(ints, intents)
        print(f'Bot : {bot_response}')

chat() 

#def chat(message):
#    print(message)
#
#    tags = predict_tag(message)
#    bot_response = get_response(tags, intents)
#    print(f'This is from chatbot.py chat function :{bot_response}')
#    return bot_response