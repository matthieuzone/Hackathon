from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import pandas as pd
import numpy as np
load_dotenv()

import streamlit as st

def run(name):
    llm = AzureChatOpenAI(azure_deployment='gpt-4')

    inst = """You are a personal wellness assistant, designed to help users track their mood and provide helpful resources.
        Your user have been awnsering questionaires the past few days, and here are their awnsers:
    """

    txtaws = ""

    with open("recomendations.txt", encoding='utf-8' ) as f:
        recomendations = f.read()

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
            Based on his awnsers, give recommendations to the user on how to improve his mental, physical and emotional health.
            here is a list of recomendations you can choose form: {recomendations}
            Your awnser sould only contain the recomendations you think are best for the user, and be a few sentences long.
            Please also provide a simple goal for the user to achieve in the day.
        """)
    ])

    def to_txt(msg):
        return msg.content

    ch = prompt | llm | to_txt
    

    prompt2 = ChatPromptTemplate.from_messages([
        ('system', inst),
        ('user', txtaws),
        ('system', f"""
            Based on his awnsers, reply 'yes' if the user's wellbeing is okay, and 'no' if something needs to be done about it.
        """)
    ])

    def alarm(msg):
        msg = msg.content.lower()
        if 'no' in msg:
            st.write("you don't seem to be in great shape, would you like to let your manager know?")
            if st.button("yes"):
                with open("data/alarms.txt", 'a') as f:
                    f.write(name + '\n')
            if st.button("no"):
                pass

    ch2 = prompt2 | llm | alarm

    ch2.invoke({})
    st.write(ch.invoke({}))

if __name__ == "__main__":
    run('test')