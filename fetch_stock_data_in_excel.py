from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import date, timedelta, datetime


def get_client_data():
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('google-excel-file.json', scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)
    return client


@api_view(["GET"])
def fetch_stock_value(request):
        # Date
        todays_date = date.today()

        # fetch Client data
        clinet_data = get_client_data()

        # Open Google Sheet by Title
        sheet = clinet_data.open('GoogleSheetTitle')

        # get the instance of the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(0)

        # update the cell value
        sheet_instance.update_cell(2, 2, '=GOOGLEFINANCE('+str("\u0022")+str("STOCK-SYMBOL")+str("\u0022")+')')

        # update the value at the specific cell
        sheet_instance.update_cell(2, 1, '=TODAY()')

        # get Data of specific cell
        get_cell_data = sheet_instance.cell(col=2,row=2)

        # Get Cell Value
        get_cell_value = get_cell_data.value
           
        data = {'status':200,'Stock_price':get_cell_value}
        return Response(data)




@api_view(["GET"])
def fetch_close_value(request):
        # Date
        todays_date = date.today()

        # fetch Client data
        clinet_data = get_client_data()

        # Open Google Sheet by Title
        sheet = clinet_data.open('GoogleSheetTitle')
        
        # get the instance of the first sheet of the Spreadsheet
        sheet_instance = sheet.get_worksheet(0)

         # update the cell value
        sheet_instance.update_cell(6, 1, '=GOOGLEFINANCE('+str("\u0022")+str("STOCK-SYMBOL")+str("\u0022") + "," +str("\u0022")+str("closeyest")+str("\u0022")+')')
        
        # get Data of specific cell
        get_cell_data = sheet_instance.cell(col=2,row=6)

        # Get Cell Value
        get_cell_value = get_cell_data.value
           
        data = {'status':200,'Stock_price':get_cell_value}
        return Response(data)





# Use below article to connect Google sheet and create JSON file 

# https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python