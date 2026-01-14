SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify"
]


from googleapiclient.discovery import build
from auth import get_credentials


def get_gmail_service():
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify"
]

TOKEN_PATH = "token.json"
CREDENTIALS_PATH = "credentials/credentials.json"



def get_gmail_service():
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)

def fetch_unread_emails(service, max_results=10):
    response = service.users().messages().list(
        userId="me",
        q="is:unread in:inbox",
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])
    return messages


def get_email_details(service, message_id):
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    return message


def mark_email_as_read(service, message_id):
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
