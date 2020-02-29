import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
import requests
from flask_sessions import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from unicodedata import normalize
from datetime import datetime
import psycopg2
import pprint
import random


app = Flask(__name__)
app.secret_key = '301289'
app.static_folder = 'static'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")
