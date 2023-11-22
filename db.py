from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure the database connection
# app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
# app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
# app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
# app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["MYSQL_HOST"] = "justorderdb.mysql.database.azure.com"
app.config["MYSQL_USER"] = "justorder"
app.config["MYSQL_PASSWORD"] = "Payment="
app.config["MYSQL_DB"] = "flaskapp"
app.config["SECRET_KEY"] = "!22wQw--ø*^r"


# Create the MySQL object
mysql = MySQL(app)
