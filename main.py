import os.path
import json
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config import OPENAI_API_KEY, GOOGLE_API_KEY



SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
ENDPOINT_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"



def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('path_to_your_downloaded_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)



def fetch_latest_emails(service, max_emails=10):
    results = service.users().messages().list(userId='me', maxResults=max_emails).execute()
    messages = results.get('messages', [])
    return [service.users().messages().get(userId='me', id=message['id']).execute()['snippet'] for message in messages]



def ask_gpt4(question):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI-GPT-4-Client'
    }
    data = {
        "prompt": question,
        "max_tokens": 150
    }
    response = requests.post(ENDPOINT_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    

def main():
    service = get_gmail_service()
    email_contents = fetch_latest_emails(service)

    for email_content in email_contents:
        result = ask_gpt4(f"Is this email a job application rejection, acceptance, follow-up, or irrelevant? {email_content}")
        print(result)

if __name__ == "__main__":
    main()