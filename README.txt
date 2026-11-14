LP-II ASSIGNMENT 5 - REGISTRATION FORM WITH MYSQL

This version keeps the same registration form fields from your supplied project.
There is only ONE HTML file: templates/registration.html.
There is NO students listing page. Submitted records are checked directly in MySQL.

PROJECT FILES
- app.py
- requirements.txt
- templates/registration.html
- README.txt

RUN STEPS
1. Install Python and MySQL Server. Make sure MySQL Server is running.
2. Extract the ZIP and open the project folder in VS Code.
3. Open app.py and replace YOUR_MYSQL_PASSWORD with your actual MySQL root password.
   If your MySQL username is not root, change user in DB_CONFIG.
4. Open terminal in the project folder and install libraries:
       python -m pip install -r requirements.txt
5. Run the Flask application:
       python app.py
6. Open browser:
       http://127.0.0.1:5000
7. Fill in the registration form and click Register.
8. The page displays a success message. The record is saved in MySQL.

DATABASE
The program automatically creates:
- Database: student_registration
- Table: students

VIEW ENTRIES DIRECTLY IN MYSQL WORKBENCH
Open MySQL Workbench and run:
       USE student_registration;
       SELECT * FROM students;

To see selected columns:
       SELECT name, roll_no, email, phone FROM students;

IMPORTANT
- No separate HTML page displays student records.
- The only HTML page is registration.html.
- Flask is the backend that receives form values and inserts them into MySQL.
- The INSERT query uses parameterized placeholders (%s).
- Duplicate roll numbers and email addresses are rejected.
- Keep MySQL Server running while using the application.
- Stop the Flask server by pressing Ctrl+C in the terminal.
