# CareerLens AI

CareerLens AI is a Streamlit-based career guidance assistant that helps students and job seekers analyze resumes, internship notices, job descriptions, and placement-related documents. It uses Google Gemini to extract key insights and generate actionable career preparation advice.

## Features

- Upload a resume, resume image, job description, or placement notice
- Analyze document type and target role
- Identify required skills and missing skills
- Check eligibility criteria
- Generate likely interview questions
- Create a 30-day preparation plan
- Provide career guidance and recommendations
- Send the prepared report via email

## Tech Stack

- Python
- Streamlit
- Google GenAI (Gemini)
- SMTP email integration

## Project Structure

- `app.py` - main Streamlit application
- `prompts.py` - system prompts and templates used for AI analysis
- `.streamlit/secrets.toml` - secret configuration for Gemini and Gmail credentials
- `requirements.txt` - Python dependencies

## Setup

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.streamlit/secrets.toml` file with the following keys:

```toml
GEMINI_API_KEY="your_gemini_api_key"
GMAIL_EMAIL="your_email@gmail.com"
GMAIL_APP_PASSWORD="your_gmail_app_password"
```

Note: for Gmail, use an app password if your account requires one.

## Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## How It Works

- The app collects the user's name and email on first launch.
- The user uploads a document or text input.
- The AI model analyzes the uploaded content.
- The result is shown in the chat interface.
- The user can generate and email a final report.

## Notes

This project is intended for career assessment and preparation support. It is most useful for resumes, internship posting analysis, and placement preparation workflows.
