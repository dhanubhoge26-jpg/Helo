import re
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Replace YOUR_MYSQL_PASSWORD with your MySQL root password.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "student_registration"
}

DEPARTMENTS = ["Information Technology", "Computer Engineering", "Mechanical", "Civil", "Electronics"]
YEARS = ["First year", "Second year", "Third year", "Final year"]
GENDERS = ["Female", "Male", "Other"]

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def setup_database():
    # Create database automatically if it does not exist.
    db = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS student_registration")
    cursor.close()
    db.close()

    # Create students table.
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            roll_no VARCHAR(20) NOT NULL UNIQUE,
            dob DATE NOT NULL,
            email VARCHAR(120) NOT NULL UNIQUE,
            phone VARCHAR(10) NOT NULL,
            department VARCHAR(80) NOT NULL,
            year VARCHAR(30) NOT NULL,
            gender VARCHAR(20) NOT NULL,
            hobbies VARCHAR(255),
            address VARCHAR(250) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    cursor.close()
    db.close()

def validate(data):
    errors = {}

    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]{2,49}", data["name"]):
        errors["name"] = "Enter a valid name (3 to 50 characters)."

    if not re.fullmatch(r"[A-Za-z0-9-]{3,20}", data["roll_no"]):
        errors["roll_no"] = "Use 3 to 20 letters, digits or hyphens."

    if not data["dob"]:
        errors["dob"] = "Select your date of birth."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", data["email"]):
        errors["email"] = "Enter a valid email address."

    if not re.fullmatch(r"[6-9][0-9]{9}", data["phone"]):
        errors["phone"] = "Enter a valid 10-digit mobile number."

    if data["department"] not in DEPARTMENTS:
        errors["department"] = "Select a valid department."

    if data["year"] not in YEARS:
        errors["year"] = "Select a valid year."

    if data["gender"] not in GENDERS:
        errors["gender"] = "Select your gender."

    if len(data["address"]) < 10 or len(data["address"]) > 200:
        errors["address"] = "Address must contain 10 to 200 characters."

    if not data["agree"]:
        errors["agree"] = "Please confirm that the details are correct."

    return errors

@app.route("/", methods=["GET", "POST"])
def register():
    values = {}
    errors = {}

    if request.method == "POST":
        fields = ["name", "roll_no", "dob", "email", "phone",
                  "department", "year", "gender", "address"]

        values = {key: request.form.get(key, "").strip() for key in fields}
        values["email"] = values["email"].lower()
        values["hobbies"] = request.form.getlist("hobbies")
        values["agree"] = request.form.get("agree", "")

        errors = validate(values)

        if not errors:
            db = get_db()
            cursor = db.cursor()

            try:
                cursor.execute("""
                    INSERT INTO students
                    (name, roll_no, dob, email, phone, department,
                     year, gender, hobbies, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    values["name"],
                    values["roll_no"],
                    values["dob"],
                    values["email"],
                    values["phone"],
                    values["department"],
                    values["year"],
                    values["gender"],
                    ", ".join(values["hobbies"]),
                    values["address"]
                ))

                db.commit()
                flash("Registration successful! Details saved in MySQL.", "success")
                return redirect(url_for("register"))

            except Error as error:
                db.rollback()
                if "Duplicate entry" in str(error) and "roll_no" in str(error):
                    errors["roll_no"] = "This roll number is already registered."
                elif "Duplicate entry" in str(error):
                    errors["email"] = "This email is already registered."
                else:
                    flash("Database error: " + str(error), "error")

            finally:
                cursor.close()
                db.close()

    return render_template(
        "registration.html",
        v=values,
        errors=errors,
        departments=DEPARTMENTS,
        years=YEARS,
        genders=GENDERS
    )

if __name__ == "__main__":
    try:
        setup_database()
        print("MySQL connected successfully.")
        print("Open http://127.0.0.1:5000")
        app.run(debug=True)
    except Error as error:
        print("MySQL connection error:", error)
        print("Check MySQL is running and DB_CONFIG password is correct.")
