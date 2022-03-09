import random
import json
import pickle
import numpy as np
import nltk
#Run these on first run of this file to download these
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

from pathlib import Path 
# This stores whatever the working directory is to the variable working__directory
working_directory = Path(__file__).absolute().parent

## ****** NLP Text Processing on intents ******

# Initializing Lemmatizer from nltk
## Lemmatization is more complex than stemming but is more accurate and has less chances of error
lemmatizer = WordNetLemmatizer()

# Load in intents
intents = json.loads(open('intents.json').read())

# Arrays to break up data from intents file
words = []
tags = []
words_and_tags = []
ignored_characters = ["?","!",",","."]

# Looping through intents
for intent in intents['intents']:
    # Looping through the patterns array each intent
    for pattern in intent['patterns']:
        # Tokenize each word in the patterns array
        word_list = nltk.word_tokenize(pattern)
        # Add the tokekized words_list to the words array
        words.extend(word_list)
        # Appending the corresponding tags to the tokenized words in the documents array as a tuple
        words_and_tags.append((word_list, intent['tag']))
        if intent['tag'] not in tags:
            tags.append(intent['tag'])

# Comment this
words = [lemmatizer.lemmatize(word) for word in words if word not in ignored_characters]
words = sorted(set(words))
tags = sorted(set(tags))

pickle.dump(words, open('words.pkl', 'wb')) 
pickle.dump(words_and_tags, open('words_and_tags.pkl', 'wb')) 

# Creating the training array for the neural network to learn
training = []
# The output array should be the same length as however many tags there are in the intents file
output_empty = [0] * len(tags)

# Looping through words_tags to create a bag of words and encoding each word with a 1 or zero
for wt in words_and_tags:
    # b_o_w is the empty bag of words array
    b_o_w = []
    word_patterns = wt[0]
    # lemmatizing each word in the word_patterns
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    # encoding each word with a 1 or 0
    for word in words:
        b_o_w.append(1) if word in word_patterns else b_o_w.append(0)
    output_row = list(output_empty)
    output_row[tags.index(wt[1])] = 1
    training.append([b_o_w, output_row])

# Shuffling training data
random.shuffle(training)
# training data must be converted to a numpy array for the model 
training = np.array(training, dtype=object)

#Splitting data into traing sets
# explain the python array short hand
train_x = list(training[:, 0])
train_y = list(training[:, 1])

#Building model
## This is a sequential model because text is a sequence
model = Sequential()
# First layer is a standard 128 neurons. the shape is equal to train_x,  the activation function is a rectitified linear function
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
# Find out about drop out
model.add(Dropout(0.05))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
# Softmax gives us a probability percentage output, highest percentage is the best answer return by network
model.add(Dense(len(train_y[0]), activation='softmax'))
# This optimizer changes weights as the model learns in order to reduce losses
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# loss function is categorical crossentropy
model.compile(optimizer=sgd,loss="categorical_crossentropy",  metrics=['accuracy'])
# Fitting model
saved_model = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
# Saving model to h5 file
model.save('chatbot_model.h5', saved_model)
print("done")


