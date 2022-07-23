#!/usr/bin/env python3
"""
Main Code
"""


from flask import Flask


__app__ = Flask(__name__)

__app__.config.from_object('flask_config')
