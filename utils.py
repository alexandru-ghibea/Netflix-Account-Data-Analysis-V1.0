import os
import sqlite3
from functools import wraps
from flask import redirect, render_template, request, session
import requests
import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd


ALLOWED_EXTENSION = ['csv']
UPLOADS_FORLDER = os.getcwd() + "/Data"


def file_valid(file):
	'''Check file'''
	return "." in file and \
		file.rsplit('.', 1)[1] in ALLOWED_EXTENSION


def create_folder(username):  # aici era username ()
	'''create user folder'''
	parent_dir = UPLOADS_FORLDER
	path_folder = os.path.join(parent_dir, username)
	os.mkdir(path_folder)
	# print("Directory '%s' created" % directory)
	# print(type(path_folder))
	return path_folder


def login_required(f):
	"""
	Decorate routes to require login.

	https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
	"""
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get("user_id") is None:
			return redirect("/login")
		return f(*args, **kwargs)
	return decorated_function


 
