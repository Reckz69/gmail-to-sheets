from gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email_details,
    mark_email_as_read
)
from sheets_service import get_sheets_service, append_row
from email_parser import parse_email
from state_manager import load_state, save_state, is_processed, mark_processed
from config import SPREADSHEET_ID, SHEET_NAME


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    messages = fetch_unread_emails(gmail_service)
    state = load_state()

    print(f"Unread emails found: {len(messages)}")

    for msg in messages:   # 👈 msg IS DECLARED HERE
        message_id = msg["id"]

        if is_processed(message_id, state):
            print("Skipping duplicate email")
            continue

        message = get_email_details(gmail_service, message_id)
        email_data = parse_email(message)

        MAX_CELL_LENGTH = 49000  # buffer below 50k limit

        content = email_data["content"]
        if len(content) > MAX_CELL_LENGTH:
            content = content[:MAX_CELL_LENGTH] + "\n\n[TRUNCATED]"

        row = [
            email_data["from"],
            email_data["subject"],
            email_data["date"],
            content
        ]


        append_row(
            sheets_service,
            SPREADSHEET_ID,
            f"{SHEET_NAME}!A:D",
            row
        )

        mark_email_as_read(gmail_service, message_id)
        mark_processed(message_id, state)

        print(f"Processed email: {email_data['subject']}")

    save_state(state)


if __name__ == "__main__":
    main()
