from __future__ import print_function
from email.mime.text import MIMEText
import base64
from fastapi import HTTPException
from app.models.email import EmailResponse

from app.core.config import SITE_URL

def create_message(sender, to, subject, message_text):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message_int(service, user_id, message) -> EmailResponse:
    """Send an email message.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.
    Returns:
      Sent Message.
    """
    try:
      message = (service.users().messages().send(userId=user_id, body=message)
                  .execute())
      return EmailResponse(status_detail="Email sent successfuly!")
    except Exception as e:
      raise HTTPException(status_code=500, detail="Unknown Error. Error raised trying to send message!")


import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from app.core.config import GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN, GMAIL_TOKEN, GMAIL_TOKEN_URI

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

from app.core.config import SERVER_EMAIL, ADMIN_EMAIL

def send_message(subject, message_text, to=ADMIN_EMAIL) -> EmailResponse:
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    else:
        creds = Credentials(
          token=GMAIL_TOKEN, 
          refresh_token=GMAIL_REFRESH_TOKEN,
          token_uri=GMAIL_TOKEN_URI,
          client_id=GMAIL_CLIENT_ID,
          client_secret=GMAIL_CLIENT_SECRET,
          scopes=SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    message = create_message(sender=SERVER_EMAIL, to=to, subject=subject, message_text=message_text)

    return send_message_int(service=service, user_id="me", message=message)


def create_confirm_link(token: str) -> str:
    # here should go url of our confirmation page
    # that page should send confirm request to server
    # if everything is good: 
    #     server responds with 200 and AuthResponse(verified=True)
    #     page displays all good
    # elif there is something wrong with verification (e.g. user doesn't exist anymore):
    #     server responds with coresponding error message
    #     page displays something gone wrong
    confirm_url = f"{SITE_URL}/email/confirm/{token}"

    return f"""
    <div style="position: absolute; left: 50%; bottom: 50%; transform: translate(50%, 50%)">
    <p><h1>Welcome! Thanks for signing up. Please follow this link to activate your account:<h1></p>
    <p><a href="{confirm_url}"><button style="background: light-blue">Confirm</button></a></p>
    <br>
    <p>Cheers!</p>
    </div>
    """

def create_confirm_code_msg(confirmation_code: int) -> str:

    return f"""
    <div style="position: absolute; left: 50%; bottom: 50%; transform: translate(50%, 50%)">
    <p><h1>Welcome! Thanks for signing up. Please follow this link to activate your account:<h1></p>
    <p>{confirmation_code}</p>
    <br>
    <p>Cheers!</p>
    </div>
    """