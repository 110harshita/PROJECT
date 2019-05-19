from flask import Flask
from os import environ
from datetime import datetime
from flask import render_template

import pypyodbc

from flask import render_template, redirect, request

app = Flask(__name__)

# creating connection Object which will contain SQL Server Connection
connection = pypyodbc.connect(
    'driver={SQL Server};' 'server=DESKTOP-7LS7KR8;' 'database=WEATHER_DATA;')  # Creating Cursor

cursor = connection.cursor()
cursor.execute("SELECT * FROM [WEATHER_DATA].[dbo].[data]")
#cursor.execute("DELETE FROM [WEATHER_DATA].[dbo].[data]")
s = "<table style='border:1px solid red'><tr><th>sr_no</th><th>sensor</th><th>measurement</th><th>unit</th><th>station_id</th><th>date_time</th></tr>"
for row in cursor:
    s = s + "<tr>"
    for x in row:
        s = s + "<td>" + str(x) + "</td>"
    s = s + "</tr>"

connection.close()

@app.route('/')
def index():

    return'homepage'

@app.route('/home')
def home():

    return "<html><body>" + s + "</body></html>"

if __name__=="__main__":
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 8000
    app.run(HOST, PORT)

