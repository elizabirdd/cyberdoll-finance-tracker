from datetime import datetime
import time

#AUTHENTICATION
import os
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

#authorizing gspread and reuses saved token if available
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", scope)
else:
    flow = InstalledAppFlow.from_client_secrets_file(
        r"C:\Users\yuxuan\Desktop\python projects\Business tracker\client_secret.json",
        scope
    )
    creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

client = gspread.authorize(creds)

#MAIN FUNCTION 
def main():
    #GLOBAL CONSTANTS (pathway to/from sheets)
    #open sheet 
    spreadsheet = client.open("Business expenses")
    sheet = spreadsheet.worksheet("Input")

    print("App running.. waiting for input.")

    #starting a loop so that the program will run when the submit button is pressed 
    while True: 
        expense_flag = sheet.acell("K3").value 
        income_flag = sheet.acell("K12").value

        #if arguments so that only expense functions run when expense button is pressed..
        if expense_flag == "RUN":
            expense = read_expense_input(sheet)
            clear_expense_input(sheet)
            write_expense_to_monthly_sheet(spreadsheet, expense)

            #resetting the button for reuse
            sheet.update("K3", [["READY"]])
            print("expense logged successfully!")

        #..vice versa.
        if income_flag == "RUN":
            income = read_income_input(sheet)
            variable_costs = read_current_variable_costs(sheet)
            variable_cost_per_entry = calculate_variable_cost_per_entry(variable_costs, income)
            clear_income_input(sheet)
            write_income_to_monthly_sheet(access_spreadsheet= spreadsheet,income_input= income, variable_cost = variable_cost_per_entry)
            sheet.update("K12", [["READY"]])
            print("income logged successfully!")

        time.sleep(5)


#INPUT 
 #reading expense input 
def read_expense_input(sheet):

    #enabling option to leave date section empty, to enable entry of both historical and current data with minimal effort 
    if not sheet.acell("I7").value:
        date = datetime.today()
    else: 
        date = datetime.strptime(sheet.acell("I7").value.strip(), "%d/%m/%Y")
    
    #creating a dictionary to store expense details
    expense_input = {
        "item description": (sheet.acell("I3").value or "").strip().capitalize(),
        "category": sheet.acell("I4").value.strip().capitalize(),
        "supplier": sheet.acell("I5").value.strip().title(),
        "amount paid": float(sheet.acell("I6").value.strip()),
        "date": date
    }
    return expense_input

#clearing expense input from the cells:
def clear_expense_input(sheet):
    sheet.batch_clear(["I3:I7"])

#reading income input 
def read_income_input(sheet):
    
    if not sheet.acell("I17").value:
        date = datetime.today()
    else: 
        date = datetime.strptime(sheet.acell("I17").value.strip(), "%d/%m/%Y")

    income_input = {
        "product name": (sheet.acell("I11").value or "").strip().capitalize(),
        "quantity": int((sheet.acell("I12").value or "1").strip()),
        "category": (sheet.acell("I13").value or "").strip().capitalize(),
        "shipping fee charged": float((sheet.acell("I14").value or "0").strip()),
        "actual shipping cost": float((sheet.acell("I15").value or "0").strip()),
        "amount received": float((sheet.acell("I16").value or "0").strip()),
        "date": date
    }
    return income_input

#clearing income input from the cells: 
def clear_income_input(sheet):
    sheet.batch_clear(["I11:I17"])

#WRITE EXPENSE TO MONTHLY SHEET 
def write_expense_to_monthly_sheet(access_spreadsheet, expense_input):
    #deriving sheet the data belongs to based on date provided 
    month = expense_input["date"].strftime("%B")
    
    monthly_sheet = access_spreadsheet.worksheet(month)

    #making variable so that prog can find the next row to fill in new data
    next_row = len(monthly_sheet.col_values(1))+1
    index = next_row - 2

    #add data using list within list 
    monthly_sheet.update(f"A{next_row}:F{next_row}", [
        [
            f"{index}.", 
            expense_input["date"].strftime("%d/%m/%y"),
            expense_input["item description"],
            expense_input["category"],
            expense_input["supplier"],
            expense_input["amount paid"]
        ]
    ])

#WRITE INCOME TO MONTHLY SHEET 
def write_income_to_monthly_sheet(access_spreadsheet, income_input, variable_cost):
    month = income_input["date"].strftime("%B")
    monthly_sheet = access_spreadsheet.worksheet(month)
    next_row = len(monthly_sheet.col_values(8))+1
    index = next_row - 2
    monthly_sheet.update(f"H{next_row}:P{next_row}", [
        [
            f"{index}.", 
            income_input["date"].strftime("%d/%m/%y"),
            income_input["product name"],
            income_input["quantity"],
            income_input["category"],
            income_input["amount received"],
            income_input["shipping fee charged"],
            income_input["actual shipping cost"],
            variable_cost
        ]
    ])

#READ CURRENT VARIABLE COSTS (as they are subject to change)
def read_current_variable_costs(sheet):
    
    current_variable_costs = {
        #per set 
        "metal case": float((sheet.acell("D20").value or "0").strip()),
        "tape": float((sheet.acell("D21").value or "0").strip()),
        "nail tips": float((sheet.acell("D22").value or "0").strip()),
        "nail file": float((sheet.acell("D24").value or "0").strip()),
        "alcohol wipes": float((sheet.acell("D25").value or "0").strip()),
        #per order 
        "paper box": float((sheet.acell("F20").value or "0").strip()),
        "wrapping paper": float((sheet.acell("F21").value or "0").strip()),
        "cuticle oil": float((sheet.acell("F23").value or "0").strip()),
        "cuticle pusher": float((sheet.acell("F24").value or "0").strip()),
        "sticky tabs": float((sheet.acell("F25").value or "0").strip()),
        "nail glue": float((sheet.acell("F26").value or "0").strip())
    }
    return current_variable_costs


#CALCULATE CURRENT VARIABLE COST OF EACH INCOME ENTRY 
def calculate_variable_cost_per_entry(current_variable_cost, income_input):
    
    #separating current vc data into per set and per order categories and add their values
    variable_cost_per_set = (
        current_variable_cost["metal case"] +
        current_variable_cost["tape"] +
        current_variable_cost["nail tips"] +
        current_variable_cost["nail file"] +
        current_variable_cost["alcohol wipes"]
    )

    variable_cost_per_order = (
        current_variable_cost["paper box"] +
        current_variable_cost["wrapping paper"] +
        current_variable_cost["cuticle oil"] +
        current_variable_cost["cuticle pusher"] +
        current_variable_cost["sticky tabs"] +
        current_variable_cost["nail glue"] 
    )

    #calculating vc for the entry
    variable_cost_for_income_entry = variable_cost_per_order + (variable_cost_per_set*income_input["quantity"])
    return variable_cost_for_income_entry



if __name__ == "__main__":
    main()