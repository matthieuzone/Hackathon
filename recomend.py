from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import pandas as pd
import numpy as np
load_dotenv()

import streamlit as st

llm = AzureChatOpenAI(azure_deployment='gpt-4')

inst = """You are a personal wellness assistant, designed to help users track their mood and provide helpful resources.
    Your user have been awnsering questionaires the past few days, and here are their awnsers:
"""

txtaws = ""

aws = pd.read_csv("awnsers.csv", index_col=0).T

st.write(aws)

for day in aws.columns:
    txtaws += f"\n\n{day}:"
    for q in aws.index:
        a = aws.loc[q, day]
        if a not in ["", "nan", None, np.nan]:
            txtaws += f"\n{q}: {a}"
print(txtaws)
st.write(llm("I am feeling sad today").content)