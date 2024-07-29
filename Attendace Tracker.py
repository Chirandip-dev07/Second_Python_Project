#Python Connector Code
import mysql.connector
conn = mysql.connector.connect(host='localhost',
                                password='password123', 
                                user='root', 
                                database='Attendance')
import pandas as pd
import datetime


if conn.is_connected()==False:
    print("ERROR connecting to database")
    

print("""WELCOME TO THE ATTENDANCE REGISTER DATABASE
      
      Rules:
      1. Previous data cannot be edited, it is under the control of localhost
      2. 1 means Present and 0 means Absent""")

cursor = conn.cursor()

students = [ ]
present = [ ]
classes = [ ]
cursor.execute("select * from attendancee")
data = cursor.fetchall()
count = cursor.rowcount
cursor.execute("select * from attendancee")
for j in range(count):
    data = cursor.fetchone()
    students.append(data[0])
    present.append(data[1])
    classes.append(data[2])


print("""What do you want to do?
      1. Enter the attendance for today
      2. Check the attendance for previous days
      3. Check the attendance history of a specific roll
      4. Check the entire attendance register till date""")
CHOICE = int(input("Enter your choice(1,2,3,4): "))

if CHOICE==1:
    x = (datetime.datetime.now())
    day = x.strftime("%d")
    month = x.strftime("%m")
    year = x.strftime("%y")
    y = str(day)+"_"+str(month)+"_"+str(year)
    prom = "ALTER TABLE attendancee ADD "+y+" integer "
    cursor.execute(prom)
    conn.commit()

    for i in range(count):
        print("Is ",students[i]," present? ")
        ans = input("(Y/N): ")
        
        if ans=="Y":
            cmd = "UPDATE attendancee SET "+y+" = 1 WHERE Roll = "+str(students[i])
            cursor.execute(cmd)
            conn.commit()
            cmd = "UPDATE attendancee SET Total = "+str(present[i]+1)+ " WHERE Roll = "+str(students[i])
            cursor.execute(cmd)
            conn.commit()
            cmd = "UPDATE attendancee SET Total_Classes = "+str(classes[i]+1)+ " WHERE Roll = "+str(students[i])
            cursor.execute(cmd)
            conn.commit()
        
        elif ans=="N":
            cmd = "UPDATE attendancee SET "+y+" = 0 WHERE Roll = "+str(students[i])
            cursor.execute(cmd)
            conn.commit()
            cmd = "UPDATE attendancee SET Total_Classes = "+str(classes[i]+1)+ " WHERE Roll = "+str(students[i])
            cursor.execute(cmd)
            conn.commit()

        else:
            print("ERROR")
        
    #Collection of data and storing it in text files
    da = "select * from attendancee"
    sql_query = pd.read_sql_query(da,conn)
    df = pd.DataFrame(sql_query)

    df.to_csv(r'a.csv', index=False)
    dff = pd.read_csv('a.csv')
    print(dff)

elif CHOICE==2:
    date = input("Enter the date in dd_mm_yy fromat : ")
    cmd = "SELECT * FROM attendancee WHERE "+date+" = 1"
    cursor.execute(cmd)
    data1 = cursor.fetchall()
    count1 = cursor.rowcount
    print("Present : ",count1,"\nAbsent : ",count - count1)

elif CHOICE==3:
    roll = input("Enter the roll number to be searched for : ")
    cmd = "select * from attendancee where Roll = "+roll
    cursor.execute(cmd)
    data1 = cursor.fetchall()
    print("Total Working Days : ",data1[0][2],"\nTotal No. of Days Present : ",data1[0][1])
    print("Attendance Percentage : ",(data1[0][1]/data1[0][2])*100,"%")

elif CHOICE==4:
    da = "select * from attendancee"
    sql_query = pd.read_sql_query(da,conn)
    df = pd.DataFrame(sql_query)

    df.to_csv(r'a.csv', index=False)
    dff = pd.read_csv('a.csv')
    print(dff)

else:
    print("Wrong Choice Entered")


print("\n")
print("I HOPE YOU LIKED IT")
