import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import joblib
import pickle

# Load the dataset
data = pd.read_csv("log.csv")

# Preprocess the data
data['Commands'] = data['Commands'].str.replace('[^\w\s]', '')

# Tokenize the Commands column
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['Commands'])
vocab_size = len(tokenizer.word_index) + 1
sequences = tokenizer.texts_to_sequences(data['Commands'])
max_sequence_length = max([len(seq) for seq in sequences])
X = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')

# Encode categorical features
enc = OneHotEncoder(handle_unknown='ignore')
enc_src_ip = enc.fit_transform(data[['src_ip']]).toarray()

# Encode the 'Tactic' column as integer labels
le = LabelEncoder()
data['Tactic'] = le.fit_transform(data['Tactic'])

# Concatenate numeric and categorical features
X = np.column_stack((X, enc_src_ip, data[['hour', 'day', 'month']]))

# Split the dataset into training and testing sets
y = to_categorical(data['Tactic'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Number of LSTM layers
num_lstm_layers = 2

# Number of units in each LSTM layer
num_units = [64, 128]

# Dropout rate
dropout_rate = 0.3

# Create an LSTM model
model = Sequential()
model.add(Embedding(vocab_size, 128, input_length=max_sequence_length + enc_src_ip.shape[1] + 3))

for i, units in enumerate(num_units):
    return_sequences = (i < num_lstm_layers - 1)
    model.add(LSTM(units, dropout=dropout_rate, recurrent_dropout=dropout_rate, return_sequences=return_sequences))

model.add(Dense(32, activation='relu'))
model.add(Dropout(dropout_rate))
model.add(Dense(len(np.unique(data['Tactic'])), activation='softmax'))

# Compile the model with a different optimizer
model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['accuracy'])

# Train the model with a different batch size
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=64)


# Make predictions for the test set
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Convert one-hot encoded y_test to class labels
y_test_classes = np.argmax(y_test, axis=1)

# Print classification report
print(classification_report(y_test_classes, y_pred_classes))

# Save the model, tokenizer, and encoders
model.save("tactic_classification_model.h5")
joblib.dump(tokenizer, "tokenizer.pkl")
joblib.dump(enc, "encoder.pkl")
# joblib.dump(le, "label_encoder.pkl")
with open("max_sequence_length.pkl", "wb") as f:
    pickle.dump(max_sequence_length, f)

# Save the LabelEncoder object to a file
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)
