from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk
import pymysql
from tkcalendar import Calendar
import tkinter as tk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict



# Connect to your MySQL database
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="travelmanagement",
#     database="crud"
# )

con=pymysql.connect(host='sql12.freesqldatabase.com',
                        user='sql12776990',
                        password='A22rYY62nK',
                        database='sql12776990',
                        port=3306)
mycursor= con.cursor()
    

    
    
# Create a cursor object to execute SQL queries
# mycursor = mydb.cursor()

# # Execute a query to fetch data from the 'graph' table
# mycursor.execute("SELECT date, profit FROM graph")
query='SELECT date, profit FROM graph'
mycursor.execute(query)
# Fetch all rows from the result set
result = mycursor.fetchall()


# Create a defaultdict to store the sum of 'profit' for each date
date_profit_sum = defaultdict(float)

# Create a dictionary to store the sum of 'profit' for each date


# Iterate through the result set and calculate the sum of 'profit' for each date
for date, profit in result:
    date_profit_sum[date] += profit

# Convert the dictionary to lists of dates and corresponding sums of 'profit'
dates = list(date_profit_sum.keys())
profit_sums = list(date_profit_sum.values())

# Plot the data
plt.figure(figsize=(8, 6))
plt.plot(dates, profit_sums, marker='o', linestyle='-')
plt.title('Total Profit over Time')
plt.xlabel('Date')
plt.ylabel('Total Profit')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()