import os.path
import json
import requests


# Google-specific imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# Local configuration imports
from config import OPENAI_API_KEY, GOOGLE_API_KEY

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Defines the scope for Gmail and the endpoint URL for OpenAI's API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
ENDPOINT_URL = "https://api.openai.com/v1/chat/completions"




# Obtain Gmail API service with user authorization
def get_gmail_service():
    
    creds = None

    # Check if we already have stored credentials
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json')
        except ValueError as e:
            print("Error reading token.json:", e)
            os.remove('token.json')  # Remove the faulty token file
            creds = None

    # If no (valid) credentials are available, let the user log in    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080, prompt='consent')  # Force a prompt

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)




# Retrieve latest emails from Gmail account using Gmail API service
def fetch_latest_emails(service, max_emails=10):
    results = service.users().messages().list(userId='me', maxResults=max_emails).execute()
    messages = results.get('messages', [])
    return [service.users().messages().get(userId='me', id=message['id']).execute()['snippet'] for message in messages]



def categorize_response(response_text):
    """
    Interpret the response from GPT-4 and categorize it into a single word.
    """
    if "rejection" in response_text.lower():
        return "rejection"
    elif "acceptance" in response_text.lower():
        return "acceptance"
    elif "follow-up" in response_text.lower():
        return "follow-up"
    else:
        return "irrelevant"



# Ask GPT-4 a question and retrieve the answer
def ask_gpt4(question):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI-GPT-4-Client'
    }
    data = {
        "model": "gpt-4", 
        "messages": [{
            "role": "system",
            "content": ("You are a helpful assistant tasked with classifying emails to determine if they are related to a current internship application. Only choose anything but irrelevant only if you can contextualize that the email is regarding a current internship status "
                        "Based on the email content provided, categorize it precisely as either: "
                        "'irrelevant', 'acceptance', 'rejection', or 'follow-up'. , If the email has nothing to do with a current internship application what so ever, and doesnt fit the categories, return irrelevant ")
        }, {
            "role": "user",
            "content": question
        }],
        "max_tokens": 150
    }

    # Send POST request to OpentAI API
    response = requests.post(ENDPOINT_URL, headers=headers, data=json.dumps(data))
    response_data = response.json()
    
    # Extract the model's message content
    if response.status_code == 200:
        if ('choices' in response_data and len(response_data['choices']) > 0 
            and 'message' in response_data['choices'][0] 
            and 'content' in response_data['choices'][0]['message']):
            detailed_response = response_data['choices'][0]['message']['content'].strip()
            return categorize_response(detailed_response)
        else:
            print(f"Unexpected response structure: {response_data}")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    



# Main function to retrieve emails and ask GPT-4 for analysis
def main():

    # Get Gmail API service
    service = get_gmail_service()

    # Fetch latest emails
    email_contents = fetch_latest_emails(service)

    # Ask GPT-4 for email categorization and print results
    for email_content in email_contents:
        result = ask_gpt4(f"Is this email a job application rejection, acceptance, follow-up, or irrelevant? {email_content}")
        print(result)

if __name__ == "__main__":
    main()


@app.route('/process_emails', methods=['POST'])
def process_emails():
    data = request.json
    token = data['token']

    # Use this token to authenticate Gmail
    creds = Credentials.from_authorized_user(token)
    service = build('gmail', 'v1', credentials=creds)

    email_contents = fetch_latest_emails(service)

    results = []
    for email_content in email_contents:
        result = ask_gpt4(f"Is this email a job application rejection, acceptance, follow-up, or irrelevant? {email_content}")
        results.append(result)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)