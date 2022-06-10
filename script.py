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


def get_sales_data():

    try:
        file = open(argv[1])
        sales_data_csv = argv[1]
        file.close()
    except IndexError:
        print("No file provided, please try again.")
        quit()
    except FileNotFoundError:
        print("The file provided does not exist.")
        quit()

def get_order_directory(sales_data_csv):

    sales_directory = os.path.dirname(sales_data_csv)
    current_date = date.today().isoformat()
    order_directory_name = "Orders_" + current_date
    order_directory = os.path.join(sales_directory, order_directory_name)

    if not os.path.exists(order_directory):
        os.makedirs(order_directory)

    return order_directory

#def sales_to_orders(sales_data_csv, order_directory):

#    grand_total = order_df['TOTAL PRICE'].sum()
#    grand_total_df = pd.DataFrame({'ITEM PRICE:' ['GRAND TOTAL:'], columns})
#    order_df = pd.concat([order_df, grand_total_df])

sales_data = get_sales_data()
order_dir = order_directory(order_directory)