Mira-App

Mira-App is an educational web tool that allows users to process video URLs (YouTube) or PDF files to perform tasks like resolving doubts, generating summaries, and creating lecture frameworks. The app uses the MIRA API to provide these services, and it is built using Streamlit, Mira SDK, and other useful libraries.
Features:

    Resolve Doubts: Users can input a doubt related to the content of a YouTube video or a PDF, and the tool will provide an explanation.
    Generate Summaries: The tool can generate a concise summary of the content of a YouTube video or PDF file.
    Create Lecture Framework: Based on the content, the app can generate a lecture framework and even allow users to specify the desired lecture duration.

Requirements

Make sure you have the following libraries installed:

    Streamlit – For the web app interface.
    Mira SDK – For interacting with the MIRA API.
    python-dotenv – For managing environment variables.
    youtube-transcript-api – To extract transcripts from YouTube videos.
    PyPDF2 – To extract text from PDF files.

Installation

    Clone the repository:

git clone https://github.com/1404Samyak/Mira-App.git

Navigate to the project directory:

cd Mira-App

Install the required dependencies:

    pip install -r requirements.txt

Environment Setup

This project requires an API key for MIRA. Follow these steps to set it up:

    Create a .env file in the root directory of the project.
    Add your MIRA API key in the .env file as shown below:

    MIRA_KEY=your_mira_api_key_here

Make sure to replace your_mira_api_key_here with your actual MIRA API key.
Usage

    Run the Application
    After installing dependencies and setting up the .env file, run the app with the following command:

    streamlit run app.py

    Access the Web Interface
    Open your browser and go to the address shown in the terminal (typically http://localhost:8501/).

    Select Input Type
    Choose the input type you would like to use:
        Video URL: Paste the URL of a YouTube video.
        PDF File: Upload a PDF file directly.

    Select Operation
    Choose from the following operations:
        Resolve Doubt: Enter a doubt or question related to the content of the video or PDF.
        Generate Summary: Get a summary of the content.
        Create Lecture Framework: Generate a lecture framework with a specified duration.

    Click "Process"
    After providing the necessary input, click the "Process" button to see the result:
        Resolve Doubt: Displays an explanation of the doubt.
        Generate Summary: Displays the summary of the content.
        Create Lecture Framework: Displays the generated lecture framework.

Example

    Video URL: Enter a YouTube URL (e.g., https://youtu.be/abcdefghijk).
    Operation: Select one of the operations (Resolve Doubt, Generate Summary, Create Lecture Framework).
    Processing: The app processes the content and displays the appropriate result.

Contributing

Feel free to contribute to this project! You can:

    Open an issue if you encounter a bug or have a feature request.
    Submit a pull request with your improvements or fixes.


