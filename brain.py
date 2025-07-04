import os
import datetime
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def authenticate_google():
    creds = None
    if not os.path.exists('credentials.json'):
        raise FileNotFoundError("❌ credentials.json not found. Cannot authenticate Google API.")
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_recent_emails():
    try:
        creds = authenticate_google()
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', maxResults=5).execute()
        messages = results.get('messages', [])
        email_summaries = []

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet = msg_data.get('snippet', '')
            email_summaries.append(snippet[:150])

        return "\n".join(email_summaries)
    except Exception as e:
        return f"⚠️ Failed to fetch emails: {e}"

def get_upcoming_events():
    try:
        creds = authenticate_google()
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=5, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return 'No upcoming events found.'

        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No Title')
            event_list.append(f"{start} - {summary}")

        return "\n".join(event_list)
    except Exception as e:
        return f"⚠️ Failed to fetch calendar events: {e}"


# Simple intent-based response function
def get_response(prompt):
    prompt_lower = prompt.lower()

    if "check my email" in prompt_lower or "read my gmail" in prompt_lower:
        return get_recent_emails()

    if "calendar" in prompt_lower or "my events" in prompt_lower:
        return get_upcoming_events()

    return "🧠 Sorry, I couldn’t find an answer. Please ask something else."