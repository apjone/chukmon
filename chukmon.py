#!/usr/bin/env python3

#####################################################
# Companies House UK Monitor
# Tony Jones
# https://github.com/apjone/chukmon
#####################################################

# Let's import what we need
import sys, os, flask
sys.path.append("app")
from dotenv import load_dotenv
from time import sleep
from chukmon_version import *
from chukmon_database import *
from chukmon_companieshouse import *
from chukmon_flask import *
from chukmon_cron import *
import threading

# Load Enviroment file
load_dotenv()

DB_FILE = os.getenv('DB_FILE')
APP_PORT = os.getenv('APP_PORT')
APP_HOST = os.getenv('APP_HOST')
POLL_TIME = int(os.getenv('POLL_TIME'))

# Let's run some checks on the DB
chuk_ver()
chuk_initdb(DB_FILE)
chuk_checkdb(DB_FILE)
print()
print("\033[4mPreflight DB checks passed, Lets go\033[0m")

threading.Thread(target=lambda: every(POLL_TIME, chukmon_chinfo)).start()

if __name__ == '__main__':
    app.run(debug=False, host=APP_HOST, port=APP_PORT)
