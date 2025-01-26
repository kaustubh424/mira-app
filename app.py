import os
import streamlit as st
from mira_sdk import MiraClient, Flow

# Hardcoded Mira API key
API_KEY = "your_mira_api_key_here"  # Replace with your actual Mira API key

# Initialize MiraClient with API key
client = MiraClient(api_key=API_KEY)

# Display title
st.title("Mira App Streamlit Deployment")

# Upload file and get transcript
uploaded_file = st.file_uploader("Upload PDF or Video Transcript", type=["pdf", "txt"])

if uploaded_file is not None:
    # Process the file (For example, extracting text from a PDF)
    if uploaded_file.type == "application/pdf":
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    else:
        text = uploaded_file.read().decode("utf-8")
    
    st.write("Extracted Text:")
    st.text_area("Transcript Text", text, height=300)

    # Initialize Flow for processing
    if st.button("Submit for Processing"):
        flow = Flow(client=client, flow_name="video-or-pdf-summarizer")
        response = flow.run(inputs={"transcript": text})
        
        st.write("Processed Output:")
        st.write(response)
