import streamlit as st
import pandas as pd
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

employees = st.text_input("Please provide the names of your employees separated by commas")
if st.button("Submit"):
    employees = employees.split(',')
    employees = [e.strip() for e in employees]
else:
    st.stop()

llm = AzureChatOpenAI(azure_deployment='gpt-4')

inst = """You are a personal wellness assistant, designed to help managers create a better work environment for their employees.
    the employees have been awnsering questionaires the past few days, and here are their awnsers:
"""

txtaws = ""

for i,name in enumerate(employees):
    txtaws += f"\n\n\nEmployee{i}:"
    aws = pd.read_csv(f"data/{name}.csv", index_col=0).T
    #st.write(aws)
    for day in aws.columns:
        txtaws += f"\n\n{day}:"
        for q in aws.index:
            a = aws.loc[q, day]
            if not pd.isna(a):
                txtaws += f"\n{q}: {a}"

prompt = ChatPromptTemplate.from_messages([
    ('system', inst),
    ('user', txtaws),
    ('system', f"""
        Based on their awnsers, give a report to the manager of the wellbeing of his team, and recommendations how he can improve the work environment for their employees.
    """)
])

def to_txt(msg):
    return msg.content

ch = prompt | llm | to_txt
st.write(ch.invoke({}))