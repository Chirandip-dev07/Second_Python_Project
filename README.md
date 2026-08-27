# Attendance Tracker

A simple command-line attendance management system built with Python and MySQL. The project records daily attendance, allows users to check attendance for previous dates, view the attendance history of a specific roll number, and display the complete attendance register.

## Technologies Used

- **Python**
- **MySQL**
- **mysql.connector** — connects Python to the MySQL database
- **Pandas** — retrieves, processes, pivots, and exports attendance data
- **datetime** — extracts and handles the current date

## Database Design

The project uses a MySQL database named `Attendance`.

The attendance data is stored in a normalized structure rather than creating a new database column for every date.

### `students` table

The `students` table stores the roll numbers of students. The roll number itself acts as the student ID.

| Roll | Name |
|---:|---:|
| 101 | Student_101 |
| 102 | Student_102 |
| 103 | Student_103 |
| 104 | Student_104 |
| 105 | Student_105 |
| 106 | Student_106 |
| 107 | Student_107 |
| 108 | Student_108 |
| 109 | Student_109 |
| 110 | Student_110 |

### `attendance` table

The `attendance` table stores one record for each student's attendance on a particular date.

| Date | Roll | Status |
|---|---:|---:|
| 2026-08-28 | 101 | 1 |
| 2026-08-28 | 102 | 1 |
| 2026-08-28 | 103 | 0 |
| 2026-08-29 | 101 | 1 |

- `Date` — date on which attendance was recorded
- `Roll` — student's roll number/student ID
- `Status` — `1` for Present and `0` for Absent
- `PRIMARY KEY (Date, Roll)` — prevents duplicate attendance entries for the same student on the same day

This design ensures that a new day is stored as new records instead of modifying the database schema.

## Features

The program can perform four main tasks:

### 1. Enter Today's Attendance

The program extracts the current date from the local computer using Python's `datetime` module and asks for the attendance of each student.

- `Y` → Present (`1`)
- `N` → Absent (`0`)
- A student cannot have duplicate attendance records for the same date.
- The program checks whether today's attendance has already been entered before starting the entry process.

### 2. Check Attendance for Previous Days

The user can enter a date in `DD_MM_YYYY` format and view the number of students who were present and absent on that date.

### 3. Check Attendance History of a Specific Roll Number

The user can enter a roll number to view:

- Total working days recorded
- Total days present
- Total days absent
- Attendance percentage

These values are calculated from the attendance records rather than being stored separately.

### 4. Display the Complete Attendance Register

The normalized attendance records are converted into a register-style table using Pandas.

The database stores data in this form:

| Date | Roll | Status |
|---|---:|---:|
| 2026-08-28 | 101 | 1 |
| 2026-08-28 | 102 | 1 |
| 2026-08-28 | 103 | 0 |

The program can display it in the following format:

| Date | 101 | 102 | 103 | 104 |
|---|---:|---:|---:|---:|
| 28_08_2026 | 1 | 1 | 0 | 1 |
| 29_08_2026 | 1 | 0 | 1 | 1 |

The register can also be exported as `attendance_register.csv`.
