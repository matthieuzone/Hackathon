import streamlit as st
import pandas as pd
import time

st.write("Questionnaire")

with open("questions.txt") as f:
    questions = f.readlines()

df = pd.read_csv("awnsers.csv", index_col=0)
awns = {}

day = time.strftime(r"%d/%m/%Y")

for q in questions:
    awns[q] = st.text_input(q, key=q)

new = pd.DataFrame(awns, index=[day])
df = pd.concat([df, new], ignore_index=False)

st.write(df)
if st.button("Save"):
    df.to_csv("awnsers.csv")
