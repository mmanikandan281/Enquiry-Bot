import gspread
import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    # Try env variable first (for Render deployment)
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if creds_json:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        # Fallback to local file (for local development)
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
    return sheet.sheet1

def save_lead(lead):
    try:
        sheet = get_sheet()
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            lead.get("name", "Unknown"),
            lead.get("email", "Not provided"),
            lead.get("phone", "Not provided"),
            "New Lead"
        ]
        sheet.append_row(row)
        print(f"✅ Lead saved: {lead}")
        return True
    except Exception as e:
        print(f"❌ Error saving lead: {e}")
        return False





# Local development instructions:

# import gspread
# import os
# from datetime import datetime
# from google.oauth2.service_account import Credentials
# from dotenv import load_dotenv

# load_dotenv()

# # Google Sheets setup
# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]

# def get_sheet():
#     creds = Credentials.from_service_account_file(
#         "credentials.json",
#         scopes=SCOPES
#     )
#     client = gspread.authorize(creds)
#     sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
#     return sheet.sheet1

# def save_lead(lead):
#     try:
#         sheet = get_sheet()
#         row = [
#             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             lead.get("name", "Unknown"),
#             lead.get("email", "Not provided"),
#             lead.get("phone", "Not provided"),
#             "New Lead"
#         ]
#         sheet.append_row(row)
#         print(f"✅ Lead saved: {lead}")
#         return True
#     except Exception as e:
#         print(f"❌ Error saving lead: {e}")
#         return False


