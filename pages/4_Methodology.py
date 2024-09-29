import streamlit as st

# Set the title of the page
st.title("Methodology")

with st.sidebar:
    st.markdown("---\nCreated by Lim Wei Zhong")

# Introduction
st.header("Introduction")
st.write("""
This methodology page provides a comprehensive explanation of the data flows and implementation details of the HDB Flat Purchase Chatbot and Resale Price Dashboard. Our application aims to assist users in navigating the HDB property market through an interactive chatbot and a dynamic data dashboard.
""")

# Data Flows and Implementation Details
st.header("Data Flows and Implementation Details")

st.subheader("1. HDB Flat Purchase Chatbot")
st.write("""
The HDB Flat Purchase Chatbot is designed to interact with users and provide them with information regarding the purchasing and selling of HDB flats. The data flow for this component involves the following steps:
1. **User Input**: Users enter their queries regarding HDB flat purchases.
2. **Processing User Queries**: The input is sent to the natural language processing (NLP) model for interpretation.
3. **Data Retrieval**: Based on the processed query, relevant data is retrieved from the knowledge base or generated using the NLP model.
4. **Response Generation**: The chatbot formulates a response and sends it back to the user.
""")

st.subheader("2. HDB Resale Price Dashboard")
st.write("""
The Resale Price Dashboard allows users to analyze resale prices of HDB flats. The data flow for this component involves:
1. **Data Loading**: Historical resale price data is loaded from the CSV file into a pandas DataFrame.
2. **Data Filtering**: Users can filter data by town and year using the dashboard interface.
3. **Data Visualization**: Based on user selections, relevant data is processed, and visualizations are generated (charts, metrics).
4. **Display Metrics**: Key metrics and visualizations are presented to the user for insights on market trends.
""")

# Flowcharts
st.header("Flowcharts for Use Cases")

st.subheader("1. Chat with Information")
st.write("Below is the flowchart illustrating the process flow for the chatbot use case.")
st.image("path_to_chatbot_flowchart.png", caption="Flowchart for Chatbot Use Case")

st.subheader("2. Intelligent Search")
st.write("Below is the flowchart illustrating the process flow for the resale price dashboard use case.")
st.image("path_to_dashboard_flowchart.png", caption="Flowchart for Resale Price Dashboard Use Case")

# Conclusion
st.header("Conclusion")
st.write("""
This methodology outlines the essential processes and data flows within our HDB Flat Purchase Chatbot and Resale Price Dashboard. By following this structure, we aim to provide users with accurate, timely, and relevant information to support their property decisions. Continuous feedback and improvements will be integrated into both components to enhance user experience.
""")
