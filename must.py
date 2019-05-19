import pypyodbc
import csv
import bs4 as bs
import urllib.request
import pandas as pd
import pip
import linecache
import time
from time import gmtime, strftime

def max(line):
    str = 'http://weatherwatch.in.th/view.php?station=' + line
    print(str)
    return str

def update_data():
    con = pypyodbc.connect(
        'driver={SQL Server};' 'server=DESKTOP-7LS7KR8;' 'database=WEATHER_DATA;' 'trusted_connection=true')
    cur = con.cursor()
    csfile = open('modified_data.csv', encoding='utf-8', mode='r')

    csv_data = csv.reader(csfile)

    sql = """
    BULK INSERT [WEATHER_DATA].[dbo].[data]
    FROM 'C:/Users/appu/PycharmProjects/firstproj/modified_data.csv' WITH (
        FIELDTERMINATOR=',',
        ROWTERMINATOR='\n'
        );
    """
    try:
        cur.execute(sql)
        print("done")
    except Exception:
        print("tr")

    cur = cur.execute("SELECT * FROM [WEATHER_DATA].[dbo].[data]")
    for row in cur:
        print(row)

    cur.close()

    con.commit()

    con.close()
    time.sleep(30)

def executeSomething():
    r = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    len = sum(1 for line in open('name.txt'))
    print(len)
    df_list = []
    for m in range(len):
        m = m + 1
        line = linecache.getline('name.txt', m)
        print(line)
        sauce = urllib.request.urlopen(max(line)).read()
        soup = bs.BeautifulSoup(sauce, "html.parser")
        table = soup.find('table')
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            print(row)
            L = row
            L.extend((line, r))
            L = map(lambda s: s.strip(), L)
            df_list.append(L)
    df_list = pd.DataFrame(df_list)
    df_list.to_csv('book1.csv', mode='a', header=False)
    data = pd.read_csv('book1.csv')
    data.shape
    filldata = data.fillna("none")
    filldata.to_csv('modified_data.csv', mode='a', index=False)
    print(df_list)
    time.sleep(30)

while True:
    executeSomething()
    update_data()