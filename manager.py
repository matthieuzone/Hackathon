import streamlit as st

employees = st.text_input("Please provide the names of your employees separated by commas")
if st.button("Submit"):
    employees = employees.split(',')
    employees = [e.strip() for e in employees]