import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import pickle

# Load the model, tokenizer, and encoder
# Load the LabelEncoder object from the file
with open("./algorithm/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)
model = load_model("./algorithm/tactic_classification_model.h5")
tokenizer = joblib.load("./algorithm/tokenizer.pkl")
enc = joblib.load("./algorithm/encoder.pkl")
with open('./algorithm/max_sequence_length.pkl', 'rb') as f:
    max_sequence_length = pickle.load(f)

# Load the new data
new_data = pd.read_csv("./data/cowrie.csv")


original_commands = new_data['Commands'].copy()

# Preprocess the data
new_data['Commands'] = new_data['Commands'].str.replace('[^\w\s]', '')

# Tokenize the Commands column
sequences = tokenizer.texts_to_sequences(new_data['Commands'])
X_new = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')


# Encode categorical features
enc_src_ip = enc.transform(new_data[['src_ip']]).toarray()

# Concatenate numeric and categorical features
X_new = np.column_stack((X_new, enc_src_ip, new_data[['hour', 'day', 'month']]))

# Make predictions for the new data
y_pred = model.predict(X_new)

# Add the predicted_probabilities column to the DataFrame
# new_data['predicted_probabilities'] = y_pred.tolist()


# After getting the predictions
predicted_indices = np.argmax(y_pred, axis=1)
predicted_tactics = le.inverse_transform(predicted_indices)

new_data['predicted_tactic'] = predicted_tactics
new_data['Commands'] = original_commands

# Save the DataFrame with the predicted tactics
new_data.to_csv("./data/cowrie.csv", index=False)
