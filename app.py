import streamlit as st
import google.generativeai as genai
import pdfplumber
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(uploaded_file, user_question,generative_model):
    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                pages = [page.extract_text() for page in pdf.pages]
                pdf_text = "\n".join(pages)

            input_prompt = f"""
                You are an AI trained to answer questions about PDF documents.

                Here is a PDF document: {pdf_text}

                Question: {user_question}
                Answer : 
                Reasoning:
                
                Answer the question accurately based on the information in the PDF document. Provide a clear and concise response along with reasoning.
                """
            
            response = generative_model.generate_content(
                [input_prompt]
                # max_tokens=200, temperature=0.7
            )
            return response.text
            #status.update(label="Response", state="complete")
        except Exception as e:
            raise Exception(str(e))

# Create an instance of the Gemini Pro model
generative_model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title='PDF Q&A App')
# App layout
st.title("PDF Q&A with Google Gemini")

uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
# Query text
user_question = st.text_input('Enter your question:', placeholder = 'Please provide a short summary.', disabled=not uploaded_file)

#with st.form('myform', clear_on_submit=True):
submitted = st.button('Get an Answer', disabled=not(uploaded_file and user_question))

if submitted:
    #with st.status("Fetching an answer...",expanded=True) as status:
    with st.spinner('Fetching an answer...'):
        try:
            answer = get_gemini_response(uploaded_file,user_question,generative_model)
        
            st.write("**Response:**")
            st.markdown("```\n" + answer + "\n```")

        except Exception as e:
            st.error(f"Error: {e}")

