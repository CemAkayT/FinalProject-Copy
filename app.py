from flask import (
    render_template,
    request,
    redirect,
    flash,
    url_for,
    get_flashed_messages,
    session,
)

import os, stripe, bleach, json, time
from password_validation import is_password_strong
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from db import mysql, app
from models import User

from flask_login import LoginManager, login_user, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(app) #initialize with Flask app
login_manager.login_view = "login"  # Set the login view to your login route
login_manager.login_message = "Login for at se menuen"

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")


mail = Mail(app)
bcrypt = Bcrypt(app)

stripe_keys = {
    "secret_key": os.getenv("STRIPE_SECRET_KEY"), # med SK kan serveren udføre handlinger på min konto såsom starte en transaktion 
    "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY"), #PK fortæller Stripe at forestpørgler der kommer fra frontenden er associeret med min konto
}

stripe.api_key = stripe_keys["secret_key"]


# Implement a user_loader function to retrieve a user based on user_id
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# @app.routes decorators are used to associate a view functions with URL endpoints. 
# Whenever the browser makes a request to an URL, it will invoke the underlyging function.
@app.route("/")
def forside():
    return render_template("forside.html")


@app.route("/home")
@login_required
def home():
    messages = get_flashed_messages()
    # Hent produkter fra databasen baseret på sektion

    # Server side rendering . Thymeleaf er også server side rendering
    # SSR is when a user requests a webpage and the server genereates a complete HTML page ?
    cursor = mysql.connection.cursor() #create cursor object to establish connection to the database and use it to execute SQL queries
    cursor.execute("SELECT * FROM products WHERE section='Populær' ORDER BY Title ASC")
    popular_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE section='Menu' ORDER BY Title ASC")
    menu_products = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM products WHERE section='Drikkevarer' ORDER BY Title ASC"
    )
    drinks_products = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE section='Dips' ORDER BY Title ASC")
    dips_products = cursor.fetchall() # fetch the result 

    # this is serverside rendering, data is sent also to the template
    return render_template(
        "home.html",
        popular_products=popular_products,
        menu_products=menu_products,
        drinks_products=drinks_products,
        dips_products=dips_products,
        messages=messages,
    )


@app.route("/aabningstider/")
def aabningstider():
    return render_template("aabningstider.html")


@app.route("/checkout") #when someone is redirected og goes to this endpoint, the funtion is invoked
@login_required
def checkout():
    return render_template("checkout.html", key=stripe_keys["publishable_key"]) # I pass the Stripe publishable key as a variable named 'key' to the template


@app.route("/charge", methods=["POST"])  # HTTP verbum
@login_required
def charge():
    customer_id = session.get("stored_user_id") # her anmoder jeg brugerens session ID som blev gemt i linje 318
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers WHERE customer_id = %s", [customer_id])
    results = cur.fetchone() # jeg forespørger brugerens PK i databasen

    paid_amount = request.form.get("amountdue") #requst.from object retrieves data from checkout hidden field
    amount = paid_amount

    
    orderJSON = request.form.get("orders") # kommer fra linje 43 i updateTotalPrice.js fra skjult input felt pakket ind i JSON streng
    print("Det her er et array af JSON objekt/er", orderJSON)

    parsedJSON = json.loads(orderJSON) # parser orderJSON til Python objekter med  Pythons indbyggede JSON modul 'json'
    print(f"Dette er den parsede JSON i form af en liste af Python-dictionary/ies: {parsedJSON}")
    try:
        customer = stripe.Customer.create( #creating a customer object inside try block
            email=results[5], source=request.form["stripeToken"] #Token er random string der har en reference til kortdetaljerne og indeholder ingen sensitiv data. 
        )
        charge = stripe.Charge.create( #charging the customer with 'stripe.Charge.create' method
            customer=customer.id,
            amount=amount,
            currency="dkk",
            
        )

        # print(charge) viser hvad man kan bruge i koden fra charge
        # parsedCharge = json.loads(charge). Charge er allerede Python dictionary
        print(f'Det er charge id {charge["id"]}')
        print(f"Det er alt hvad charge indeholder{charge}")
        paymentID = charge["id"] #python dictionary

        for order in parsedJSON:
            query = "INSERT INTO `flaskapp`.`orders` (`order_name`, `quantity`, `price`, `bought_at` ,`customer_id`, `payment_id`) VALUES (%s, %s, %s, DATE_ADD(NOW(), INTERVAL 1 HOUR) ,%s, %s)"
            cur.execute(
                query,
                (order["title"], order["qnty"], order["price"], customer_id, paymentID),
            )
            mysql.connection.commit()

        # Get the current time in seconds since the epoch
        current_time = time.time()

        # Calculate the time 30 minutes from now (30 minutes * 60 seconds per minute)
        # 90 instead of 30 because on Azure time is one hour less
        delivery_time = current_time + 90 * 60

        # Convert the delivery_time back to a human-readable format (e.g., HH:MM)
        delivery_time_formatted = time.strftime("%H:%M", time.localtime(delivery_time))

        mailstr = (
            f"<html><head>"
            + ' <script src="https://kit.fontawesome.com/558b5cad1d.js" crossorigin="anonymous"></script>'
            + ' <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"/>'
            + "<style>"
            + "body {"
            + "  display: flex;"
            + "  flex-direction: column;"
            + "  align-items: center;"
            + "  padding-top: 10px;"
            + "  margin: 0;"
            + "}"
            + "h2 {"
            + "  color: #ff8000"
            + "  font-style: italic;"
            + "}"
            + "p {"
            + "  font-size: 16px;"
            + "  font-weight: 500;"
            + "}"
            + "table {"
            + "  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);"
            + "  border-collapse: collapse;"
            + "  width: 300px;"
            + "}"
            + "table, th, td {"
            + "  border: 1px solid black;"
            + "  text-align: left;"
            + "  font-weight: 400;"
            + "}"
            + "th, td {"
            + "  padding: 8px;"
            + "  background-color:#ff8000;"
            + "}"
            + "</style>"
            + "</head><body>"
            + '<h2>JUST ORDER<i class="fa-solid fa-house fa-2x" style="margin: 10px"></i></h2>'
            + f"<p> Hej {results[1]},</p>"
            + "<p>Du har købt:</p>"
            + "<table>"
            + "<tr><th>Produkt</th><th>Antal</th><th>Pris</th></tr>"
        )

        total = 0
        totalvarer = 0
        for order in parsedJSON: #itererer 'order' objektet
            mailstr = (
                mailstr
                + f"<tr><td>{order['title']}</td><td>{order['qnty']} stk.</td><td>{order['price']},00 kr.</td></tr>"
            )
            total += order["price"]
            totalvarer += int(order["qnty"])

        mailstr = (
            mailstr
            + "<tr><td><strong>Total</strong></td>"
            + f"<td><strong>{totalvarer} stk.</strong></td>"
            + f"<td><strong>{total},00 kr.</strong></td>"
            + "</tr>"
            + "</table>"
            + f"<p>Afhentning kl: <strong>{delivery_time_formatted}</strong></p>"
            + f"<p>Ordrenummer: {paymentID}</p>"
            + "<p>Har du glemt noget?</p>"
            + ' <a class="btn btn-lg contact-button" style="color:black; background-color: #ff8800; border-radius: 50px; outline: none;"  href="https://justorder.azurewebsites.net/aabningstider/" role="button">Kontakt os</a>'
            + "</body></html>"
        )

    
        customer_email = charge["billing_details"]["name"]
      
        subject = "Ordrebekræftelse:"
        
        sender = os.getenv("MAIL_USERNAME")
        recipients = [customer_email, sender]

        msg = Message(subject=subject, sender=sender, recipients=recipients)
        msg.html = mailstr
        mail.send(msg)

        # Pass the amount to the template
        return render_template("charge.html", charge=charge, amount=amount)
    except stripe.error.StripeError as e:
        # Handle Stripe errors and return an error message to the user
        return f"Stripe fejl: {str(e)}"


@app.route("/opret", methods=["GET", "POST"])
def opret():
    if "stored_user_id" in session:
        print("Vi har allerede session id")
        return redirect(url_for("home"))

    if request.method == "POST":
        # sanitizing user input with bleach to protect against vulnerabilities like Cross Site Scripting(XSS)
        name = bleach.clean(request.form.get("name"))
        surname = bleach.clean(request.form.get("surname"))
        town = bleach.clean(request.form.get("town"))
        zip = bleach.clean(request.form.get("zip"))
        email = bleach.clean(request.form.get("email"))
        password = bleach.clean(request.form.get("password"))

        # performing validationg to make sure the fields are not empty
        if not email or not password:
            return redirect(url_for("opret"))
        # additional validation to check for password strength
        elif not is_password_strong(password):
            flash(
                "Adgangskode skal være på mindst 8 tegn, indeholde mindst et ciffer, et stort bogstav, et lille bogstav og et specialtegn",
                "danger",
            )
            return render_template("opret.html")

        # The user's password is hashed using the flask_bcrypt. It automatically handles salting 
        else:
            hashed_pw = bcrypt.generate_password_hash(password)

            # establish connection do DB and
            # %s are placeholders. prevents sql injection
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM customers WHERE email = %s", [email])
            result = cur.fetchone()  # check if provided email already exists
            if result:
                flash("Email er desværre allerede taget 😩", "warning")
                return render_template("opret.html")
            else:
                cur.execute(
                    "INSERT INTO customers(first_name, sur_name, town, zip_code, email, password, created_at) VALUES (%s, %s,%s,%s,%s,%s, DATE_ADD(NOW(), INTERVAL 1 HOUR))",
                    (name, surname, town, zip, email, hashed_pw),
                )

                mysql.connection.commit()
                cur.execute(
                    "SELECT * FROM customers WHERE email = %s", [email]
                )  # Fetch the newly registered user's data
                new_user = cur.fetchone()
                cur.close()
                session["stored_user_id"] = new_user[0]

                print(
                    f"user id {new_user[0]} has been created with email: {new_user[5]}"
                )
                flash(
                    f"Hej {new_user[1]}. Tak fordi du oprettede dig som bruger👍 - Du kan nu logge ind og se vores menu"
                )

                return redirect(url_for("home"))
    return render_template("opret.html")


# route handles both 'GET' and 'POST' requests
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST": # user tries to login becase it's a post request
        email = bleach.clean(request.form.get("email"))
        password = request.form.get("password")

        cur = mysql.connection.cursor() #cursor is like an iterator, pointer
        cur.execute("SELECT * FROM customers WHERE email = %s", [email])
        results = cur.fetchone()

        if results:
            stored_password = results[6]
            if bcrypt.check_password_hash(stored_password, password): #compares stored pw with pw from input field. Returns true if they match else false
                stored_user_id = results[0]
                session["stored_user_id"] = stored_user_id # Flask gemmer 'stored_user_id' sessionvariablen internt i et session objekt. 
                user = User(stored_user_id)
                login_user(user)

                print(f"UserMixin {user.id} has logged in")
                flash(f"Godt at se dig igen {results[1]} ❤️ ", "success")
                return redirect(url_for("home"))
            else:
                flash("Login fejlede. Venligst tjek din login detaljer.", "danger")
                return render_template("login.html")
        else:
            flash("Der findes ikke bruger med denne mail", "warning")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    # Vi sletter den gemte sessionvariabel fra session objektet
    user_id = session.pop("stored_user_id", None)

    if user_id is not None: # vi logger brugeren ud med Flasks login bibliotek
        print(f"user_id {user_id} has been logged out")
        logout_user()
        flash(f"Tak for nu. Vi ses igen snart 🙏 ", "success")

    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
