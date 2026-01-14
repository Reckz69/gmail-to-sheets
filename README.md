# Gmail to Google Sheets Automation

## 👤 Author
**Narendra Meshram**

---

## 🏗️ 1. High-Level Architecture


1.  **Gmail API**: Fetches unread messages from the inbox.
2.  **Logic Layer**: Parses email headers (From, Subject, Date) and sanitizes the body.
3.  **State Manager**: Compares Message IDs against `state.json` to prevent duplicates.
4.  **Sheets API**: Appends new unique email data as new rows.
![High-Level-Arch](https://github.com/user-attachments/assets/de35e5a6-54bd-402c-a6f6-2524653f38ce)

---

## 🚀 2. Step-by-Step Setup Instructions

### Prerequisites
* Python 3.10+ installed.
* A Google Cloud Project with Gmail and Sheets APIs enabled.

### Installation

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd gmail-to-sheets
```
2.  **Set Up Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Google Cloud & OAuth Configuration**:
    * Create a Google Cloud project
    * Enable the following APIs:
    * Gmail API
    * Google Sheets API
    * Configure OAuth Consent Screen (External)
    * Create OAuth Client ID (Desktop Application)
    * Download credentials.json
    * Place it in:
      ```bash
      credentials/credentials.json
      ```
    
5.  **Configure Google Sheet**:
    * Create a sheet with headers: `From`, `Subject`, `Date`, `Content`.
    * Copy the Spreadsheet ID into `config.py`.
    * Update config.py (located in the project root)

6. **Run the Script**:
    ```bash
     python src/main.py
    ```


---

## 🛠️ Explanation of Core Logic
## Explanation of Core Logic

### OAuth Flow Used
- OAuth 2.0 Desktop Application flow is used
- On the first run, the user is redirected to Google’s consent screen
- Access and refresh tokens are stored locally in `token.json`
- Tokens are reused on subsequent runs to avoid repeated authentication

### Duplicate Prevention Logic
- Each Gmail email has a unique message ID
- Processed message IDs are stored in `state.json`
- Emails already present in the state file are skipped
- This ensures idempotent execution across multiple runs

### State Persistence Method
- State is persisted using a local JSON file (`state.json`)
- The file stores processed Gmail message IDs
- This approach is simple, transparent, and sufficient for lightweight automation

---

## Challenges Faced and Solutions

### OAuth Scope Issues
- Initial OAuth tokens lacked Google Sheets permissions, causing authorization errors
- This was resolved by unifying Gmail and Google Sheets scopes and regenerating the OAuth token

### HTML and Image Content in Emails
- Emails often contained HTML tags and embedded images, cluttering the Google Sheet
- HTML cleaning was implemented to strip all tags and remove images, storing only plain text

### Google Sheets Cell Size Limit
- Google Sheets enforces a 50,000-character limit per cell
- Long email bodies caused API failures and were handled by safely truncating the content before insertion

---

## Limitations
- Large email bodies are truncated to meet Google Sheets character limits
- Email fetching is limited per run and can be extended using pagination
- Attachments are not processed
- State persistence is local and not shared across systems
- **Rate Limits**: The script is subject to Google API quota limits; processing thousands of emails at once may trigger a 429 error.
- **No Attachments**: The current version only parses the text body and does not download or link email attachments.

---

## Proof of Execution
Screenshots and a demo video are available in the `/proof` folder, including:
- Gmail inbox with unread emails
- Google Sheet populated by the script
- OAuth consent screen

*Note: The OAuth consent screen may display “No data available” because the application only requests Gmail and Google Sheets API scopes and does not access personal profile information.*

---
