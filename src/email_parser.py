
from bs4 import BeautifulSoup
import base64



def _get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def _decode_base64(data):
    if not data:
        return ""
    decoded_bytes = base64.urlsafe_b64decode(data.encode("utf-8"))
    return decoded_bytes.decode("utf-8", errors="ignore")


def _extract_body(payload):
    # Case 1: Simple email (no parts)
    if "body" in payload and payload["body"].get("data"):
        return _decode_base64(payload["body"]["data"])

    # Case 2: Multipart email
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            body = part.get("body", {}).get("data")

            # Prefer plain text
            if mime_type == "text/plain" and body:
                return _decode_base64(body)

        # Fallback: HTML
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            body = part.get("body", {}).get("data")

            if mime_type == "text/html" and body:
                return _decode_base64(body)

    return ""

def clean_html(text):
    if not text or not isinstance(text, str):
        return ""

    soup = BeautifulSoup(text, "html.parser")

    # Remove images
    for img in soup.find_all("img"):
        img.decompose()

    return soup.get_text(separator=" ", strip=True)


def parse_email(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])


    content = _extract_body(payload).strip
    content = clean_html(content)

    email_data = {
        "from": _get_header(headers, "From"),
        "subject": _get_header(headers, "Subject"),
        "date": _get_header(headers, "Date"),
        "content": content
    }

    return email_data
