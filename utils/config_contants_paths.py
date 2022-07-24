#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


# ----------------------------- CONSTANTS -------------------------------------

PERSON_QUANTITY = 100

DEFAULT_PERSON_NAME = 'Stark Bank Person'

TOTAL_TRIES = 3

MIN_LIMIT = 8

MAX_LIMIT = 12

WEBHOOK_WAIT_TIME = 3

DAYS_OF_DUE_DATE = 3

FILE_OPERATION = {
    'read': 'r',
    'write': 'w',
    'add new': 'a',
    'write binary file': 'wb'
}

# ------------------------------ NGROK --------------------------------------

# remove thsi line at the end

# NGROK_API_KEY = '<NGROK_API_KEY>'

NGROK_API_KEY = '2CJOZXfRZdJOZABSJo6g9wXcF9o_6BKYhps9j62ggdLUJHSPV'


# ---------------------- MAKE YOUR CHANGES ----------------------------------

# NOTE: make some changes to these two constants to see app working

TOTAL_ROUNDS = 2    # FOR REAL 8 | FOR TESTING USE 3

SLEEP_MINUTES = 15   # FOR REAL 180 minutes (3h=180 min) | FOR TESTING USE 15


# ------------------------------- PATHS ------------------------------------


RANDOM_PERSON_FILE_PATH = '/'.join([os.path.dirname(os.path.abspath(__file__)), 'stage/FILES_DIR/RANDOM_PERSON.text'])



APP_INFO = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index - Stark Bank App</title>

</head>
<body>
    <h1>HELLO WORLD!!!</h1>
    <h4>
        My name is <string>Idelfrid Jorge</string>, I am a Python Developer.
    </h4>

    <h2>About this app</h2>

    <p> This project is the challenge to avaluate my skill as DEV  to  become part of Stark Bank company.  The challenge consist in : 1.  Issues 8 to 12 Invoices every 3 hours to random people for 24 hours (our Sandbox emulation environment will make sure some of those are automatically paid); 2. Receives the webhook callback of the Invoice credit and sends the received amount (minus eventual fees) to the following account using a Transfer .</p>
</body>
</html>
"""
