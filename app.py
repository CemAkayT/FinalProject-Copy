from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL
from password_validation import is_password_strong
import bcrypt
import bleach

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


app = Flask(__name__)
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.secret_key = os.getenv("SECRET_KEY")

mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/om/")
def om():
    return render_template("om.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        results = cur.fetchone()

        if results:
            stored_password = results[2]
            if bcrypt.checkpw(
                password.encode("utf-8"), stored_password.encode("utf-8")
            ):
                flash("You logged in successfully", "success")
                return redirect("/")
            else:
                flash("Login failed. Please check your credentials.", "danger")
                return render_template("login.html")
        else:
            flash("There are no records with that email", "warning")

    return render_template("login.html")


@app.route("/opret", methods=["GET", "POST"])
def opret():
    if request.method == "POST":
        # santitizing user input with bleach
        email = bleach.clean(request.form.get("email"))
        password = request.form.get("password")  # .encode("utf-8")

        # user input validation
        if not email or not password:
            return redirect(url_for("opret"))

        if not is_password_strong(password):
            flash(
                "Password must be at least 8 characters long, contain at least a digit, an uppercase letter, a lowercase letter and a special character ",
                "danger",
            )
            return render_template("opret.html")

        # hash the password + salt
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # establish connection do DB
        # %s are placeholders. prevents sql injection
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        result = cur.fetchone()
        if result:
            flash("Email already taken ⛔️", "danger")
            return render_template("opret.html")
        cur.execute(
            "INSERT INTO users(email,password, created_at)VALUES(%s, %s, NOW())",
            (email, hashed_pw),
        )

        mysql.connection.commit()
        cur.close()

        flash("Registration successful 👍", "success")
        return redirect(url_for("home"))

    return render_template("opret.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
