import requests
import json

# Your OpenAI API Key
API_KEY = 'YOUR_OPENAI_API_KEY'

# API endpoint
ENDPOINT_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"

# Function to ask GPT-4 a question
def ask_gpt4(question):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI-GPT-4-Client'
    }

    data = {
        "prompt": question,
        "max_tokens": 150  # You can adjust this based on your requirements
    }

    response = requests.post(ENDPOINT_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Test
email_content = """
Dear John,

After careful consideration, we regret to inform you that we have chosen to move forward with another candidate for the Software Engineer position.

Best regards,
XYZ Company
"""

result = ask_gpt4(f"Is this email a job application rejection, acceptance, follow-up, or irrelevant? {email_content}")
print(result)