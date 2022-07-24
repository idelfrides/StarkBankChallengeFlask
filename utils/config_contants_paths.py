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

TOTAL_ROUNDS = 1    # FOR REAL 8 | FOR TESTING USE 3

SLEEP_MINUTES = 15   # FOR REAL 180 minutes (3h=180 min) | FOR TESTING USE 15


# ------------------------------- PATHS ------------------------------------


RANDOM_PERSON_FILE_PATH = '/'.join([os.path.dirname(os.path.abspath(__file__)), 'stage/FILES_DIR/RANDOM_PERSON.text'])
