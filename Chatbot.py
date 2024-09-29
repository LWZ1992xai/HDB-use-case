import streamlit as st
import pandas as pd
from helper_functions import llm
from helper_functions.utility import check_password  

# Set up and run this Streamlit App
st.set_page_config(
    layout="centered",
    page_title="HDB Flat Purchase Chatbot",
    page_icon="🏡"
)

# Check if the password is correct.  
if not check_password():  
    st.stop()
# ------------------

# Title
st.title("🏡 HDB Flat Purchase/Selling Chatbot")
st.markdown("### Your guide to buying and selling HDB flats")

# Sidebar with creator info and instructions
with st.sidebar:
    st.markdown("### How to Use:")
    st.write(
        """
        - Ask about flat purchasing processes and procedures.
        - You can ask questions like:
            - What is the process of buying a flat?
            - What documents do I need?
            - What is stamp duty?
        """
    )
    st.markdown("### 🚀 Get Started:")
    st.markdown("Type your question below and hit **Submit**.")
    st.divider()
    st.markdown("#### Created by Lim Wei Zhong")
    st.markdown("##### Updated on 1 Oct 2024")

# Spacer to enhance layout
st.write("<br>", unsafe_allow_html=True)

# Form for user input
form = st.form(key="form")
user_prompt = form.text_area("Enter your question here:", height=150, placeholder="Type your question about HDB flats...")

# Submit button
if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    
    # Divider for layout separation
    st.divider()

    # Process the user's question and get a response
    response = llm.process_user_message(user_prompt)

    # Display the response
    st.markdown("### Chatbot Response:")
    st.success(response)

    # Additional divider for layout separation
    st.divider()

# Important Notice Expander
with st.expander("IMPORTANT NOTICE", expanded=False):
    st.write(
        """
        This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
        
        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
        
        Always consult with qualified professionals for accurate and personalized advice.
        """
    )