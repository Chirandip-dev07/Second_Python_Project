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

students = []

cursor.execute("SELECT Roll FROM students ORDER BY Roll")
data = cursor.fetchall()

for row in data:
    students.append(row[0])

count = len(students)


print("""What do you want to do?
      1. Enter the attendance for today
      2. Check the attendance for previous days
      3. Check the attendance history of a specific roll
      4. Check the entire attendance register till date""")
CHOICE = int(input("Enter your choice(1,2,3,4): "))

if CHOICE == 1:

    today = datetime.date.today()

    print("\nEntering attendance for:", today.strftime("%d_%m_%Y"))

    check_sql = """
        SELECT COUNT(*)
        FROM attendance
        WHERE Date = %s
    """

    cursor.execute(check_sql, (today,))
    attendance_count = cursor.fetchone()[0]

    if attendance_count > 0:

        print("\nERROR: Today's attendance has already been entered.")
        print("Date:", today.strftime("%d_%m_%Y"))
        print("Attendance records found:", attendance_count)
        print("You cannot enter attendance again today.")

    else:

        for roll in students:

            while True:
                ans = input(f"Is {roll} present? (Y/N): ").upper()

                if ans == "Y":
                    status = 1
                    break

                elif ans == "N":
                    status = 0
                    break

                else:
                    print("Invalid input. Please enter Y or N.")

            sql = """
                INSERT INTO attendance (Date, Roll, Status)
                VALUES (%s, %s, %s)
            """

            cursor.execute(sql, (today, roll, status))

        conn.commit()

        print("\nAttendance successfully recorded.")

elif CHOICE == 2:

    date_input = input("Enter the date (dd_mm_yyyy): ")

    try:
        date = datetime.datetime.strptime(
            date_input,
            "%d_%m_%Y"
        ).date()

    except ValueError:
        print("Invalid date format.")
        exit()

    cursor.execute("""
        SELECT Roll
        FROM attendance
        WHERE Date = %s
        AND Status = 1
        ORDER BY Roll
    """, (date,))

    present_students = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE Date = %s
    """, (date,))

    total = cursor.fetchone()[0]

    print("\nDate:", date_input)
    print("Present:", len(present_students))
    print("Absent:", total - len(present_students))

    print("\nPresent students:")

    for student in present_students:
        print(student[0])

elif CHOICE == 3:

    roll = input("Enter the roll number to be searched for: ")

    cursor.execute("""
        SELECT
            COUNT(*) AS total_classes,
            COALESCE(SUM(Status), 0) AS present
        FROM attendance
        WHERE Roll = %s
    """, (roll,))

    total_classes, present = cursor.fetchone()

    if total_classes == 0:
        print("No attendance records found.")
    else:
        percentage = (present / total_classes) * 100

        print("\nRoll Number:", roll)
        print("Total Working Days:", total_classes)
        print("Total Days Present:", present)
        print("Total Days Absent:", total_classes - present)
        print("Attendance Percentage:", round(percentage, 2), "%")

elif CHOICE == 4:

    query = """
        SELECT Date, Roll, Status
        FROM attendance
        ORDER BY Date, Roll
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        print("No attendance records found.")
    else:

        register = df.pivot(
            index="Date",
            columns="Roll",
            values="Status"
        )

        register.index = pd.to_datetime(register.index).strftime("%d_%m_%Y")

        print("\nENTIRE ATTENDANCE REGISTER\n")
        print(register.to_string())

        register.to_csv("attendance_register.csv")

else:
    print("Wrong Choice Entered")


print("\n")
print("I HOPE YOU LIKED IT")
