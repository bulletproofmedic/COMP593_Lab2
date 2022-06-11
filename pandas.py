#-----------------------------------------------------
#   Lab 2, Pandas - COMP 593
#
#   Description:
#       Extracts info from .csv files to create new spreadsheets
#
#   Usage:
#       python pandas.py filename
#
#   Parameters:
#       Filename - Path to the .csv file
#
#   History:
#   Date        Author      Description
#   2022-06-09  A. Walker   Initial Creation
#-----------------------------------------------------

#Path of file > Get directory for new file > split data into individual orders

import os
import re
import pandas as pd

from sys import argv
from datetime import date
from xlsxwriter.utility import xl_rowcol_to_cell


#Ge the data to interpret
def get_sales_data():

    try:
        file = open(argv[1])
        sales_data_csv = argv[1]
        return sales_data_csv
        file.close()
    except IndexError:
        print("No file provided, please try again.")
        quit()
    except FileNotFoundError:
        print("The file provided does not exist.")
        quit()

#Define directory to save the files to
def get_order_directory(sales_data_csv):

    sales_directory = os.path.dirname(sales_data_csv)
    current_date = date.today().isoformat()
    order_directory_name = "Orders_" + current_date
    order_directory = os.path.join(sales_directory, order_directory_name)

    if not os.path.exists(order_directory):
        os.makedirs(order_directory)

    return order_directory

#Split sales into orders
def split_sales_to_orders(sales_data_csv, order_directory):


    sales_df = pd.read_csv(sales_data_csv)
    sales_df.insert(7, 'TOTAL PRICE', sales_df['ITEM QUANTITY'] * sales_df['ITEM PRICE'])
    sales_df.drop(columns=['ADDRESS', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY'], inplace=True)

    #Initiate loop to modify and save new files
    for order_id, order_df in sales_df.groupby('ORDER ID'):

        order_df.drop(columns=['ORDER ID'], inplace=True)
        order_df.sort_values(by='ITEM NUMBER', inplace=True)

        #Add grand total
        grand_total = order_df['TOTAL PRICE'].sum()
        grand_total_df = pd.DataFrame({'ITEM PRICE': ['GRAND TOTAL:'], 'TOTAL PRICE': [grand_total]})
        order_df = pd.concat([order_df, grand_total_df])

        #Order file save path
        customer_name = order_df['CUSTOMER NAME'].values[0]
        customer_name = re.sub(r'\W', '', customer_name)
        order_file_name = 'Order' + str(order_id) + '_' + customer_name + '.xlsx'
        order_file_path = os.path.join(order_directory, order_file_name)

        sheet_name = 'Order #' + str(order_id)
        order_df.to_excel(order_file_path, index=False, sheet_name=sheet_name)

        def fix_spreadsheets(xlsxfile):
    
            df = pd.read_excel(order_file_path)

            #Initiate writer
            writer = pd.ExcelWriter(order_file_path, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name=sheet_name)
            workbook = writer.book
            worksheet = writer.sheets['Order #' + str(order_id)]

            #Format money cells
            money_fmt = workbook.add_format({'num_format': '$#,##0', 'bold': True})
            worksheet.set_column('E:E', 14, money_fmt)
            worksheet.set_column('F:F', 13, money_fmt)
            worksheet.set_column('G:G', 11, money_fmt)

            #Format remaining cells
            worksheet.set_column('A:A', 11)
            worksheet.set_column('B:B', 13)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 13)
            worksheet.set_column('H:H', 7)
            worksheet.set_column('I:I', 24)

            #Save changes
            writer.save()

        fix_spreadsheets(order_file_path)

        



sales_data = get_sales_data()
order_directory = get_order_directory(sales_data)
split_sales_to_orders(sales_data, order_directory)
