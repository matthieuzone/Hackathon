import streamlit as st
import pandas as pd
import time
import random
import os

# Function to load custom CSS
def load_css():
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Default styles will be applied.")

def load_questions():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'questions.txt')
    
    with open(file_path) as f:
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
    
    return mood_questions, ghq_questions

def run(name):
    load_css()
    st.title("Daily Mental Health Questionnaire")
    
    # Load questions
    mood_questions, ghq_questions = load_questions()

    # Load previous answers
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    try:
        df = pd.read_csv(os.path.join(data_dir, f"{name}.csv"), index_col=0)
    except FileNotFoundError:
        df = pd.DataFrame()

    # Initialize session state
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.answers = {}
        st.session_state.current_ghq_index = int(time.strftime("%j")) % len(ghq_questions)  # Cycle through GHQ questions
        st.session_state.ghq_question = ghq_questions[st.session_state.current_ghq_index]

    # Get current question
    all_questions = [st.session_state.ghq_question] + mood_questions
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
            st.rerun()
    else:
        day = time.strftime(r"%d/%m/%Y")
        new = pd.DataFrame(st.session_state.answers, index=[day])
        df = pd.concat([df, new], ignore_index=False)
        
        st.write(df)
        
        if st.button("Save"):
            df.to_csv(os.path.join(data_dir, f"{name}.csv"))
            st.success("Responses saved successfully!")
            st.session_state.question_index = 0
            st.session_state.answers = {}
            st.session_state.current_ghq_index = (st.session_state.current_ghq_index + 1) % len(ghq_questions)
            st.session_state.ghq_question = ghq_questions[st.session_state.current_ghq_index]

if __name__ == "__main__":
    run('test')
