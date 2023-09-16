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


# Defines the scope for Gmail and the endpoint URL for OpenAI's API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
ENDPOINT_URL = "https://api.openai.com/v1/chat/completions"




# Obtain Gmail API service with user authorization
def get_gmail_service():
    
    creds = None

    # Check if we already have stored credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If no (valid) credentials are available, let the user log in    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)




# Retrieve latest emails from Gmail account using Gmail API service
def fetch_latest_emails(service, max_emails=10):
    results = service.users().messages().list(userId='me', maxResults=max_emails).execute()
    messages = results.get('messages', [])
    return [service.users().messages().get(userId='me', id=message['id']).execute()['snippet'] for message in messages]




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
            "content": "You are a helpful assistant."
        }, {
            "role": "user",
            "content": question
        }],
        "max_tokens": 150
    }

    # Send POST request to OpentAI API
    response = requests.post(ENDPOINT_URL, headers=headers, data=json.dumps(data))
    response_data = response.json()
    
    # Check for valid response and extract the model's message content
    if response.status_code == 200:
        if ('choices' in response_data and len(response_data['choices']) > 0 
            and 'message' in response_data['choices'][0] 
            and 'content' in response_data['choices'][0]['message']):
            return response_data['choices'][0]['message']['content'].strip()
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