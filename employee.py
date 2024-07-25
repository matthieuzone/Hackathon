import streamlit as st
import pandas as pd
import time
import questionnaire
import recomend
import os

if 'name' not in st.session_state:
    name = st.text_input("Please provide your name")
    if st.button("submit"):
        st.session_state.name = name
        st.rerun()
    st.stop()
else:
    name = st.session_state.name

if not os.path.exists(f"data/{name}.csv"):
    with open(f"data/{name}.csv", 'w') as f:
        f.write("t")

with open(f"data/{name}.csv", 'r') as f:
    aws = pd.read_csv(f, index_col=0).T

day = time.strftime(r"%d/%m/%Y")

if day in aws.columns:
    st.header("Thank you for awnsering the questionnaire today! Here are a few goal for today : ")
    recomend.run(name)
else:
    questionnaire.run(name)