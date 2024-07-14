#Python Connector Code
import mysql.connector
conn = mysql.connector.connect(host='localhost',
                                password='password123', 
                                user='root', 
                                database='shopping')
import pandas as pd


if conn.is_connected()==False:
    print("ERROR connecting to database")


cursor = conn.cursor()
print("Please enter 'P' for present and 'A' for absent ")
date = input("Enter the date in the format (dd_mm_yy): ")
cmd = "alter table attendance add "+date+" varchar(2);"
cursor.execute(cmd)
while True:
    da = "select * from attendance"
    sql_query = pd.read_sql_query(da,conn)
    df = pd.DataFrame(sql_query)
    
    df.to_csv(r'a.csv', index=False)
    dff = pd.read_csv('a.csv')
    print(dff) 
    break
    