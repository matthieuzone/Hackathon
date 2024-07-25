import streamlit as st
import pandas as pd
import time
import random

def load_questions():
    with open("questions.txt") as f:
        questions = f.readlines()

    mood_questions = []
    ghq_questions = []

    for q in questions:
        parts = q.strip().split('|')
        q_type = parts[0]
        question_text = parts[2]
        
        if q_type == 'mood':
            mood_questions.append((parts[1], question_text, parts[3] if len(parts) > 3 else None))
        elif q_type == 'ghq':
            ghq_questions.append((parts[1], question_text, parts[3] if len(parts) > 3 else None))

# Charger les réponses précédentes
df = pd.read_csv(f"data/{name}.csv", index_col=0)
awns = {}

def run(name):
    st.write("Questionnaire")

    # Load questions
    mood_questions, ghq_questions = load_questions()

    # Load previous answers
    try:
        df = pd.read_csv(f"data/{name}.csv", index_col=0)
    except FileNotFoundError:
        df = pd.DataFrame()

    # Initialize session state
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.answers = {}
        st.session_state.random_questions = random.sample(ghq_questions, 3)

    # Get current question
    all_questions = mood_questions + st.session_state.random_questions
    question_index = st.session_state.question_index

    if question_index < len(all_questions):
        q_type, question_text, options = all_questions[question_index]
        if q_type == 'multiple':
            options = options.split(',')
            st.session_state.answers[question_text] = st.selectbox(question_text, options, key=question_text)
        elif q_type == 'open':
            st.session_state.answers[question_text] = st.text_input(question_text, key=question_text)

        if st.button("Next"):
            st.session_state.question_index += 1
    else:
        day = time.strftime(r"%d/%m/%Y")
        new = pd.DataFrame(st.session_state.answers, index=[day])
        df = pd.concat([df, new], ignore_index=False)
        
        st.write(df)
        
        if st.button("Save"):
            df.to_csv(f"data/{name}.csv")
            st.success("Responses saved successfully!")

if __name__ == "__main__":
    run('test')
