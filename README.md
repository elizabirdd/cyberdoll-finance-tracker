# Cyberdoll Finance Tracker

A Python automation tool I built to manage the finances of my small 
press-on nail business, Cyber Doll (@cyberdoll.nails). I built this tool partially as a 
portfolio project to demonstrate my understanding of accounting principles and 
practical Python skills applied to a real business I own and operate, and 
also to prevent myself from procrastinating.

## What it does
- Reads expense and income data entered into a custom Google Sheets input form (separately)
 <img width="1101" height="676" alt="image" src="https://github.com/user-attachments/assets/bfd397ef-ff7f-4f24-b796-4cc9b007becf" />

  *Variable cost values have been redacted to protect business information.*

- Clear input form for next entry
- Automatically routes entries to the correct monthly sheet based on date entry
  <img width="1773" height="916" alt="image" src="https://github.com/user-attachments/assets/2e5a76f1-5e2e-4b6d-8551-fc169ed79da1" />

- Calculates variable costs per order based on an adjustable cost table
 <img width="1463" height="674" alt="image" src="https://github.com/user-attachments/assets/e309151e-41ab-405a-91e3-cf594f343f44" />

 *Every time the "Submit" button is pressed, Python reads the cost table; hence costs can be changed at any time without touching code.*
- Tracks actual shipping costs separately to accommodate free shipping promotions, although manual entry and calculation is required
- Populates a financial overview with revenue, expenses, and profit metrics (This is done on Sheets itself.)
- Runs on an infinite loop and is triggered to run when the "Submit" button is pressed, hence fully operated on Sheets 
- Supports historical data entry by allowing manual date input
- Automatically fills in the date if left empty (If the entry was today, and I felt lazy)

## Why I built it
As a student running a small business, I needed a simple way to track 
my finances without spending too much time on manual data entry. I built 
this tool to automate the bookkeeping process while learning Python, and designed it 
so I can continue using it with minimal effort during busy periods like 
exam season. Above all else, creating solutions that bring genuine benefit to me 
or the people around me brings me great satisfaction. 

## Tech stack
- Python 3
- gspread (Google Sheets API)
- Google OAuth 2.0
- Google Apps Script (button triggers)

## How it works
1. Fill in the expense or income form in the Google Sheets Input tab
2. Click the Submit button next to the relevant section
3. Apps Script detects the click and writes a flag to a trigger cell
4. Python polling loop detects the flag every 5 seconds
5. Data is automatically written to the correct monthly sheet
6. Variable costs are calculated per order based on quantity
7. The input form is cleared and the flag is reset
8. The overview section updates automatically via Google Sheets formulas

## Project structure
```
business_tracker.py     # main application
client_secret.json      # Google OAuth credentials (not included — see setup)
token.json              # saved auth token (not included — generated on first run)
```

## How to run
1. Clone the repository:
   git clone https://github.com/elizabirdd/cyberdoll-finance-tracker.git
2. Install dependencies:
   pip install gspread google-auth-oauthlib
3. Set up Google Sheets API credentials:
   - Go to Google Cloud Console
   - Create a project and enable the Google Sheets and Google Drive APIs
   - Download your credentials as client_secret.json
   - Place it in the project folder
4. Run the program:
   python business_tracker.py
5. Complete the OAuth flow in the browser on first run
6. Leave the program running in the background while you work in Google Sheets

## Google Sheets structure
- **Input tab** — expense and income entry forms with submit buttons
- **Monthly tabs** (January–December) — auto-populated expense and income logs
- **Overview section** — summary metrics including total revenue, expenses, 
  variable costs, actual shipping, and profit for the month
- **Variable costs table** — adjustable cost breakdown used for per-order calculations

## Variable cost structure
Each order incurs a fixed per-order cost plus a per-set cost multiplied by quantity:
- Per order: paper box, wrapping paper, cuticle oil, cuticle pusher, sticky tabs, nail glue
- Per set: metal case, tape, nail tips, nail file, alcohol wipes

## What I learned
- Integrating Python with external APIs (Google Sheets via gspread)
- Making a real world data pipeline (read → process → write)
- Handling authentication and token reuse with OAuth 2.0
- Structuring a project with modular functions
- Using Google Apps Script to bridge Sheets and Python
- Applying basic accounting concepts (variable costs, profit margins) in code
 *Note: No cost allocation is currently implemented for fixed assets 
(tools, polishes etc.) for simplicity. This is a planned future improvement 
as the business grows.*
- Debugging API responses and handling edge cases

## Improvements in the future
- Cost allocation for fixed assets across months
- Annual summary sheet with cross-month calculations
- Product tracking and buyer habits
- Automated monthly email summary report
- Token refresh handling for long running sessions
- Automated inventory count 

