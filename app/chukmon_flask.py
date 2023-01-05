#!/usr/bin/env python3
import os, sqlite3
from flask import Flask, render_template, request, jsonify
from chukmon_companieshouse import chukmon_chinfo
from dotenv import load_dotenv

load_dotenv()
DB_FILE = os.getenv('DB_FILE')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/goodcompanies')
def goodcompanies():
    return render_template('goodcompanies.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/allcompanies')
def getall():
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("select companyname, company_number, company_status, company_type, incorporation_date, registered_office_address, \"<p><i class='fa fa-times fa-2x' aria-hidden='true' onclick=ignore('\" || company_number || \"')></i></p>\" from companieshouse where company_number not in ( select company_number from goodcompanies) order by incorporation_date desc")    
    return jsonify(data=results.fetchall())

@app.route('/api/goodcompanies')
def getgood():
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("select c.companyname, g.company_number, c.registered_office_address, \"<p><i class='fa fa-times fa-2x' aria-hidden='true' onclick=remove('\" || g.company_number || \"')></i></p>\" from goodcompanies g join companieshouse c on g.company_number = c.company_number order by g.company_number desc")    
    return jsonify(data=results.fetchall())

@app.route('/api/terms')
def getterms():
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("select term, \"<p><i class='fa fa-times fa-2x' aria-hidden='true' onclick=removeterm('\" || id || \"')></i></p>\" from searchcompanies")
    return jsonify(data=results.fetchall())

@app.route('/api/ignore/<string:company_number>')
def ignore(company_number: int):
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("insert or replace into goodcompanies values('" + company_number +"');")
    connection.commit()
    return "OK"

@app.route('/api/remove/<string:company_number>')
def remove(company_number: str):
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("delete from goodcompanies where company_number = '" + company_number + "';")
    connection.commit()
    return "OK"

@app.route('/api/removeterm/<string:term>')
def removeterm(term: str):
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("delete from searchcompanies where id = '" + term + "';")
    connection.commit()
    return "OK"

@app.route('/api/refresh')
def refresh():
    chukmon_chinfo()
    return "OK"

@app.route('/api/lastrefresh')
def lastrefresh():
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("select value from config where option = 'last_refresh';").fetchone()
    return str(results[0])

@app.route('/api/add/<string:term>')
def addterm(term: str):
    try:
        connection = sqlite3.connect(DB_FILE)
    except Exception as e:
        print("Error:" + str(e))
        exit(1)
    c = connection.cursor()
    results = c.execute("insert or replace into searchcompanies(term) values('" + term +"');")
    connection.commit()
    return "OK"