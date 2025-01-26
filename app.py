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
        /* Center the app content */
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        /* Style the block container */
        .block-container {
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15);
            padding: 25px;
            border-radius: 15px;
            background-color: black;
            font-family: 'Roboto', sans-serif;
        }
        /* Style the title */
        h1 {
            color: #2E7D32;
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 15px;
            text-shadow: 1px 2px 3px rgba(0, 0, 0, 0.2);
        }
        /* Style the subheader */
        h2, h3 {
            color: #388E3C;
            font-family: 'Roboto', sans-serif;
            font-weight: 500;
            margin-bottom: 10px;
        }
        /* Style input fields */
        .stTextInput, .stNumberInput {
            width: 80% !important;
            margin: 15px auto;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 16px;
            box-shadow: inset 1px 1px 5px rgba(0, 0, 0, 0.1);
        }
        /* Style buttons */
        button {
            background-color: #66BB6A;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.15);
        }
        button:hover {
            background-color: #43A047;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        }
        /* Style dropdowns */
        .stSelectbox {
            width: 80% !important;
            margin: 15px auto;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
            background-color: #fff;
            box-shadow: inset 1px 1px 5px rgba(0, 0, 0, 0.1);
        }
        /* Highlight information boxes */
        .stAlert {
            margin: 15px 0;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.1);
            background-color: #333;
            color: #2E7D32;
            font-weight: bold;
        }
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
    video_id = video_url.replace('https://youtu.be/', "")
    
    if operation == "Resolve Doubt":
        doubt = st.text_input("Enter Your Doubt:")
    
    elif operation == "Create Lecture plan":
        lecture_duration = st.number_input("Enter the desired lecture duration (in minutes):", min_value=0, step=10)
    
    # Button to perform the selected operation
    if st.button("Process"):
        st.success("Processing your request...")
        plain_transcript = "......."
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            plain_transcript = " ".join([entry['text'] for entry in transcript])
        except Exception as e:
            print(f"An error occurred: {e}")
        
        if operation == "Resolve Doubt":
            input_dict = {"doubt": doubt, "transcript": plain_transcript}
            response = client.flow.test(flow_doubt, input_dict)
            st.subheader("Explanation of your doubt")
            st.write(response['result'])
        
        elif operation == "Generate Summary":
            input_dict = {"transcript": plain_transcript}
            response = client.flow.test(flow_summary, input_dict)
            st.subheader("Summary")
            st.write(response['result'])
        
        elif operation == "Create Lecture plan":
            input_dict = {"transcript": plain_transcript, "duration": lecture_duration}
            response = client.flow.test(flow_framework, input_dict)
            st.subheader("Lecture plan")
            st.write(response['result'])

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
                    response = client.flow.test(flow_doubt, input_dict)
                    st.subheader("Explanation of your doubt")
                    st.write(response['result'])
                
                elif operation == "Generate Summary":
                    input_dict = {"transcript": pdf_text}
                    response = client.flow.test(flow_summary, input_dict)
                    st.subheader("Summary")
                    st.write(response['result'])
                
                elif operation == "Create Lecture plan":
                    input_dict = {"transcript": pdf_text, "duration": lecture_duration}
                    response = client.flow.test(flow_framework, input_dict)
                    st.subheader("Lecture plan")
                    st.write(response['result'])
        
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
