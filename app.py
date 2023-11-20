from flask import (
    render_template,
    request,
    redirect,
    flash,
    url_for,
    get_flashed_messages,
    session,
)
from password_validation import is_password_strong
import bcrypt
import bleach
from db import mysql, app


@app.route("/")
def home():
    messages = get_flashed_messages()
    # Hent produkter fra databasen baseret på sektion

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE section='Populær'")
    popular_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE section='Menu'")
    menu_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE section='Drikkevarer'")
    drinks_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE section='Dips'")
    dips_products = cursor.fetchall()

    return render_template(
        "home.html",
        popular_products=popular_products,
        menu_products=menu_products,
        drinks_products=drinks_products,
        dips_products=dips_products,
        messages=messages,
    )


@app.route("/om/")
def om():
    return render_template("om.html")


@app.route("/payment")
def payment():
    print(session["stored_user_id"])
    print("Vi er på  vej til payment siden")
    return render_template("payment.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = bleach.clean(request.form.get("email"))

        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        results = cur.fetchone()

        if results:
            stored_password = results[2]
            if bcrypt.checkpw(
                password.encode("utf-8"), stored_password.encode("utf-8")
            ):
                stored_user_id = results[0]
                session["stored_user_id"] = stored_user_id

                flash(f"Welcome back {results[1]} ", "success")
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
        # sanitizing user input with bleach
        email = bleach.clean(request.form.get("email"))
        password = request.form.get("password")

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

        flash("Du er nu oprettet på siden👍 - Tag et kig på vores menu ", "success")
        return redirect(url_for("home"))

    return render_template("opret.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
