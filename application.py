import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
import requests
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from unicodedata import normalize
from datetime import datetime
import psycopg2
import pprint
import random
import json
import sys
import logging


app = Flask(__name__)
app.secret_key = '301289'

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


@app.route("/journals")
def journals():
    return render_template("pages.html")


@app.route("/poetry")
def poetry():
    get_poems_query = "Select name,text,written_at from content where type=:type"
    poems = db.execute(get_poems_query, {"type":"poem"}).fetchall()

    titles=[]
    only_poems = []
    dates = []

    for title in poems:
        titles.append(title[0])

    for poem in poems:
        only_poems.append((poem[1]))

    for date in poems:
        dates.append(date[2])

    all_poems = clean_poems(only_poems)

    return render_template("pages.html", data=merge(titles, all_poems))

@app.route("/prose")
def prose():
    return render_template("pages.html")


@app.route("/articles")
def articles():
    return render_template("pages.html")


@app.route("/photography")
def photography():
    return render_template("pages.html")


@app.route("/aphorisms")
def aphorisms():
    return render_template("pages.html")


@app.route("/old-poems")
def oldpoems():
    return render_template("pages.html")

def merge(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

def clean_poems(poems):
    new_list = []
    for item in poems:
        new_list.append(item['content'])
    return new_list
