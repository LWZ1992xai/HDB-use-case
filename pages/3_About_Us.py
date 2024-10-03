import streamlit as st

# Set the title of the page
st.title("About Us")

with st.sidebar:
    st.markdown("---\nCreated by Lim Wei Zhong")

# Project Overview
st.header("Project Overview")
st.write("""
Welcome to the **HDB Flat Purchase Chatbot and Resale Price Dashboard**! This project aims to simplify the process of buying and selling HDB flats in Singapore by providing users with an interactive chatbot for instant guidance and a comprehensive dashboard for analyzing resale prices. Whether you’re a first-time buyer or a seasoned investor, the tools are designed to make your property journey smoother and more informed.
""")

# Project Scope
st.header("Project Scope")
st.write("""
This project consists of two primary components:

1. **HDB Flat Purchase Chatbot**: An interactive AI-driven chatbot that answers questions related to the purchasing and selling of HDB flats, covering topics like processes, required documents, and costs.

2. **Resale Price Dashboard**: A visual analytics dashboard that allows users to explore historical resale prices of HDB flats, filter data by town and year, and visualize trends through various graphs.

My goal is to provide a user-friendly experience that empowers users with the knowledge they need to make informed decisions in the HDB market.
""")

# Objectives
st.header("Objectives")
st.write("""
1. **User Empowerment**: Equip users with the information they need to navigate the HDB purchasing process confidently.

2. **Data Visualization**: Offer insightful data visualizations to help users understand market trends and pricing dynamics.

3. **Accessibility**: Ensure that the tools are easily accessible to all users, regardless of their technical expertise.

""")

# Data Sources
st.header("Data Sources")
st.write("""
This application utilizes a variety of data sources to ensure the accuracy and relevance of the information provided:

- **HDB Website**: Served as the official source to provide updated information. For each query submitted, the chatbot will refer to the website for the updated information.
         
- **HDB Resale Price Data**: Sourced from official government datasets, the resale price dashboard uses up-to-date historical data to offer insights on market trends since January 2017.

- **User Input**: The chatbot utilizes a sophisticated natural language processing model that learns from user interactions, improving its responses over time.
""")

# Features
st.header("Features")

st.subheader("HDB Flat Purchase Chatbot")
st.write("""
- **Natural Language Processing**: The chatbot understands user queries in natural language, providing accurate and contextually relevant responses.

- **Interactive Interface**: Users can easily type their questions and receive instant answers, making the process intuitive.

- **Guided Assistance**: The chatbot provides guidance on topics such as the purchasing process, necessary documentation, and financial considerations.
""")

st.subheader("Resale Price Dashboard")
st.write("""
- **Data Filtering**: Users can filter resale price data by town and year, allowing for tailored analysis based on their interests.

- **Key Metrics Display**: The dashboard showcases important metrics such as highest and lowest resale prices and total transaction counts for selected parameters.

- **Trend Visualization**: Users can visualize average resale prices and transaction counts over time through interactive charts, facilitating better market understanding.

- **Detailed Analysis by Flat Type**: The dashboard provides insights into average resale prices segmented by flat type, helping users make informed decisions.
""")

# Conclusion
st.header("Conclusion")
st.write("""
By combining an intuitive chatbot with a powerful data visualization dashboard, it aims to support buyers and sellers in their journey through the HDB market. I invite you to explore the tools and welcome any feedback that can help me improve!

Thank you for visiting my project!
""")
