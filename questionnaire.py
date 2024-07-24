import streamlit as st
import pandas as pd
import time

st.write("Questionnaire")

# Lire les questions et les options à partir du fichier
with open("questions.txt") as f:
    questions = f.readlines()

# Charger les réponses précédentes
df = pd.read_csv("awnsers.csv", index_col=0)
awns = {}

day = time.strftime(r"%d/%m/%Y")

# Afficher les questions à choix multiple et les questions ouvertes
for q in questions:
    q_type, question = q.strip().split('|', 1)
    if q_type == 'multiple':
        question, options = question.split('|')
        options = options.split(',')
        awns[question] = st.selectbox(question, options, key=question)
    elif q_type == 'open':
        awns[question] = st.text_input(question, key=question)

# Ajouter les nouvelles réponses au dataframe
new = pd.DataFrame(awns, index=[day])
df = pd.concat([df, new], ignore_index=False)

# Afficher le dataframe mis à jour
st.write(df)

# Enregistrer les réponses lorsqu'on clique sur le bouton
if st.button("Save"):
    df.to_csv("awnsers.csv")
