import streamlit as st
import pandas as pd
import time
import random

st.write("Questionnaire")

# Lire les questions et les options à partir du fichier
with open("questions.txt") as f:
    questions = f.readlines()

# Séparer les questions obligatoires des questions optionnelles
mandatory_questions = []
optional_questions = []

for q in questions:
    parts = q.strip().split('|')
    q_type = parts[0]
    question_text = parts[2]
    
    if q_type == 'mandatory':
        mandatory_questions.append((parts[1], question_text, parts[3] if len(parts) > 3 else None))
    elif q_type == 'optional':
        optional_questions.append((parts[1], question_text, parts[3] if len(parts) > 3 else None))

# Charger les réponses précédentes
df = pd.read_csv("awnsers.csv", index_col=0)
awns = {}

day = time.strftime(r"%d/%m/%Y")

# Ajouter les questions obligatoires
for q_type, question_text, options in mandatory_questions:
    if q_type == 'multiple':
        options = options.split(',')
        awns[question_text] = st.selectbox(question_text, options, key=question_text)
    elif q_type == 'open':
        awns[question_text] = st.text_input(question_text, key=question_text)

# Sélectionner 3 questions aléatoires parmi les optionnelles
random_questions = random.sample(optional_questions, 3)

# Afficher les questions aléatoires
for q_type, question_text, options in random_questions:
    if q_type == 'multiple':
        options = options.split(',')
        awns[question_text] = st.selectbox(question_text, options, key=question_text)
    elif q_type == 'open':
        awns[question_text] = st.text_input(question_text, key=question_text)

# Ajouter les nouvelles réponses au dataframe
new = pd.DataFrame(awns, index=[day])
df = pd.concat([df, new], ignore_index=False)

# Afficher le dataframe mis à jour
st.write(df)

# Enregistrer les réponses lorsqu'on clique sur le bouton
if st.button("Save"):
    df.to_csv("awnsers.csv")
