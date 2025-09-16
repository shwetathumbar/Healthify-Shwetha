import streamlit as st
import google.generativeai as genai
import os
import pandas as pd

api = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = 'AIzaSyCA2uu5GaTNoNUXeelsTv0G4rgzzjRL_Zs')
model = genai.GenerativeModel('gemini-2.5-flash-lite')

#lets create the UI
st.title("Healthify :- :blue[Your personal health assistant]")
st.markdown('''
            This application will assist you to have a better and healthy life.
            You can ask your health related questions and get personalized guidance 
            ''')
st.sidebar.header(':green[ENTER YOUR DETAILS]')
name = st.sidebar.text_input('Enter your Name')
tips='''
:blue[Follow the steps]
* Enter your details in the side bar.
* Enter your gender, age, height (cms), weight (kgs).
* Select the number on the fitness scale (0-5), 5-Fitness and 0-No Fitness at all'''
st.write(tips)

gender = st.sidebar.selectbox('Select your Gender',['Female','Male'])
age = st.sidebar.text_input('Enter your Age in years')
weight = st.sidebar.text_input('Enter your weight in kgs')
height = st.sidebar.text_input('Enter your height in cms')
bmi = pd.to_numeric(weight)/(pd.to_numeric(height)/100)**2
fitness = st.sidebar.slider('Rate your fitness between 0 to 5',0,5,1)
st.sidebar.write(f"{name} Your BMI is : {round(bmi,2)} kg/m^2")

user_query = st.text_input('Enter your question here')
# pronoun handling
if gender == "Male":
    pronoun = "his"
else:
    pronoun = "her"

prompt = f"""
Assume you are a health expert. You are required to answer the question asked by the user.

Use the following details provided by dearest user:
Name: {name}
Gender: {gender}
Age: {age} years
Weight: {weight} kg
Height: {height} cm
BMI: {bmi} kg/m²
Fitness rating: {fitness}

Please provide personalized health guidance considering {name}'s profile and {pronoun} lifestyle.

Your output should be in following format
* It should start by giving one or two line comment on the details that have been provided.
* It should explain what is the real problem based on the query asked by user.
* What could be the possible reason for the problem.
* What are the possible solutions for the problem.
* You can also mention what doctor to see (specialization) if required.
* Strictly do not or advice any medicine.
* Output should be in bullet points and use tables wherever required

here is the query from the user {user_query}
In the end,
give 5 to 7 lines of summary of everything that has been discussed
"""

response = model.generate_content(prompt)
if response:
    st.write(response.text)
