import streamlit as st
import pandas as pd
import time
import questionnaire
import recomend



aws = pd.read_csv("awnsers.csv", index_col=0).T
day = time.strftime(r"%d/%m/%Y")

if day in aws.columns:
    st.write("Thank you for awnsering the questionnaire today!, here are your some recomendations for you : ")
    recomend.run()
else:
    questionnaire.run()