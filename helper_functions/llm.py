import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken


if load_dotenv('.env'):
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_embedding(input, model='text-embedding-3-small'):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]


# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create( #originally was openai.chat.completions
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content


# Note that this function directly take in "messages" as the parameter.
def get_completion_by_messages(messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content


# This function is for calculating the tokens given the "message"
# ⚠️ This is simplified implementation that is good enough for a rough estimation
def count_tokens(text):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    return len(encoding.encode(text))


def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))


def process_user_message(user_input, debug=True):
    delimiter = "####"
    website = "https://www.hdb.gov.sg"

    # Step 1: Check input to see if it flags the Moderation API
    response = OpenAI().moderations.create(input=user_input)
    moderation_output = response.results

    if moderation_output[0].flagged:
        print("Step 1: Input flagged by Moderation API.")
        return "Sorry, we cannot process this request."

    if debug: print("Step 1: Input passed moderation check.")

    # Step 2: Answer the user question
    system_message = f"""You will be provided with customer service queries.
The customer service query will be delimited with {delimiter} characters.

Follow these internal steps to answer the customer queries, this is to help you answer their question better
do not output these out. 
Use step 1 ,2 3 and 4 to formulate your response and only show the final response in step 5 to the customer
The customer query will be delimited with four hashtags,
i.e. {delimiter}.

Step 1:{delimiter} decide whether the customer is
asking a question about performing a transaction or general enquries on the process.

Step 2:{delimiter} analyses the keywords and phrasing to understand the general intent.

Step 3:{delimiter} search the {website}, including all relevant pages within the website
for relevant articles, FAQs, or guides, tables based on the intent category. Only use information found 
within this {website}
prioritizes results that match the specific keywords and context identified earlier.
Check that the url is working and List down the website url and where you found it.

Step 4:{delimiter}: selects the most relevant information from the website to formulate a response.
The response could be a direct answer, a step-by-step guide, or a list of options for the customer.
If the response includes eligibility, list down the various eligibilty checks in table form.
for each step-by-step guide, provide links or articles that is useful for the user. 

Step 5:{delimiter}: offers the response to the customer and monitors their feedback (e.g., positive/negative response, further questions).
If the customer indicates dissatisfaction, you can:
Ask clarifying questions to refine its understanding of the issue.

Only show the final response in step 5 to the customer
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"}
    ]

    final_response = get_completion_by_messages(messages)
    if debug:print("Step 2: Generated response to user question.")

    # Step 3: Put the answer through the Moderation API
    response = OpenAI().moderations.create(input=final_response)
    moderation_output = response.results

    if moderation_output[0].flagged:
        if debug: print("Step 3: Response flagged by Moderation API.")
        return "Sorry, we cannot provide this information."

    if debug: print("Step 3: Response passed moderation check.")

    # Step 4: Ask the model if the response answers the initial user query well
    user_message = f"""
    Customer message: {delimiter}{user_input}{delimiter}
    Agent response: {delimiter}{final_response}{delimiter}

    Does the response sufficiently answer the question?
    """
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    evaluation_response = get_completion_by_messages(messages)
    if debug: print("Step 4: Model evaluated the response.")

    # Step 5: If yes, use this answer; if not, say that you will need more information to answer the question
    if "Y" in evaluation_response:
        if debug: print("Step 5: Model approved the response.")
        return final_response
    else:
        if debug: print("Step 5: Model disapproved the response.")
        neg_str = "I'm unable to provide the information you're looking for. Please provide more information on your query"
        return neg_str
