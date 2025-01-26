import streamlit as st
from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("APP_KEY")

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

flow_doubt = Flow(source="flow.yaml")  # For resolving doubts
flow_summary = Flow(source="flow1.yaml")  # For generating a summary
flow_framework = Flow(source="flow2.yaml")  # For creating a lecture framework

# Apply custom CSS for styling
st.markdown("""
    <style>
        /* Custom CSS for styling */
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        /* Add your other CSS here */
    </style>
""", unsafe_allow_html=True)

# Title
st.title("MIRA Edu Tool")

# Subheader
st.subheader("Provide the required input and choose the operation to perform.")

# Dropdown for input type
input_type = st.selectbox("Select Input Type:", ["Video URL", "PDF File"])

# Dropdown for operation
operation = st.selectbox("Select Operation:", ["Resolve Doubt", "Generate Summary", "Create Lecture plan"])

# Input logic for Video URL
if input_type == "Video URL":
    video_url = st.text_input("Enter the Video URL:")
    
    # Ensure correct video ID format
    if video_url.startswith('https://youtu.be/'):
        video_id = video_url.replace('https://youtu.be/', "")
    else:
        video_id = video_url.replace('https://www.youtube.com/watch?v=', "")
    
    if operation == "Resolve Doubt":
        doubt = st.text_input("Enter Your Doubt:")
    
    elif operation == "Create Lecture plan":
        lecture_duration = st.number_input("Enter the desired lecture duration (in minutes):", min_value=0, step=10)
    
    # Button to perform the selected operation
    if st.button("Process"):
        st.success("Processing your request...")
        plain_transcript = ""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            plain_transcript = " ".join([entry['text'] for entry in transcript])
        except Exception as e:
            st.error(f"An error occurred while fetching the transcript: {e}")
            plain_transcript = "Subtitles are unavailable for this video."
        
        if operation == "Resolve Doubt":
            input_dict = {"doubt": doubt, "transcript": plain_transcript}
            try:
                response = client.flow.test(flow_doubt, input_dict)
                if response and 'result' in response:
                    st.subheader("Explanation of your doubt")
                    st.write(response['result'])
                else:
                    st.error("No result or error in response.")
            except Exception as e:
                st.error(f"An error occurred while processing the doubt: {str(e)}")
        
        elif operation == "Generate Summary":
            input_dict = {"transcript": plain_transcript}
            try:
                response = client.flow.test(flow_summary, input_dict)
                if response and 'result' in response:
                    st.subheader("Summary")
                    st.write(response['result'])
                else:
                    st.error("No result or error in response.")
            except Exception as e:
                st.error(f"An error occurred while generating the summary: {str(e)}")
        
        elif operation == "Create Lecture plan":
            input_dict = {"transcript": plain_transcript, "duration": lecture_duration}
            try:
                response = client.flow.test(flow_framework, input_dict)
                if response and 'result' in response:
                    st.subheader("Lecture plan")
                    st.write(response['result'])
                else:
                    st.error("No result or error in response.")
            except Exception as e:
                st.error(f"An error occurred while creating the lecture plan: {str(e)}")

# Input logic for PDF File
elif input_type == "PDF File":
    pdf_file = st.file_uploader("Upload a PDF File:", type=["pdf"])
    if pdf_file:
        st.write(f"Uploaded file: {pdf_file.name}")
        try:
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            
            if operation == "Resolve Doubt":
                doubt = st.text_input("Enter Your Doubt:")
            
            elif operation == "Create Lecture plan":
                lecture_duration = st.number_input("Enter the desired lecture duration (in minutes):", min_value=0, step=10)
            
            # Button to perform the selected operation
            if st.button("Process"):
                if operation == "Resolve Doubt":
                    input_dict = {"doubt": doubt, "transcript": pdf_text}
                    try:
                        response = client.flow.test(flow_doubt, input_dict)
                        if response and 'result' in response:
                            st.subheader("Explanation of your doubt")
                            st.write(response['result'])
                        else:
                            st.error("No result or error in response.")
                    except Exception as e:
                        st.error(f"An error occurred while processing the doubt: {str(e)}")
                
                elif operation == "Generate Summary":
                    input_dict = {"transcript": pdf_text}
                    try:
                        response = client.flow.test(flow_summary, input_dict)
                        if response and 'result' in response:
                            st.subheader("Summary")
                            st.write(response['result'])
                        else:
                            st.error("No result or error in response.")
                    except Exception as e:
                        st.error(f"An error occurred while generating the summary: {str(e)}")
                
                elif operation == "Create Lecture plan":
                    input_dict = {"transcript": pdf_text, "duration": lecture_duration}
                    try:
                        response = client.flow.test(flow_framework, input_dict)
                        if response and 'result' in response:
                            st.subheader("Lecture plan")
                            st.write(response['result'])
                        else:
                            st.error("No result or error in response.")
                    except Exception as e:
                        st.error(f"An error occurred while creating the lecture plan: {str(e)}")
        
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
