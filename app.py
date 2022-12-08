from flask import Flask, flash, redirect, render_template, request
from utils import *
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from werkzeug.utils import secure_filename
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = "THISISCS50FINALPROJECT"
app.config["UPLOADS_FOLDER"] = UPLOADS_FORLDER
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
DATA_DIRECTORIES=[]
Session(app)

# create database for users login details  
db = sqlite3.connect('users.db', check_same_thread=False)
cursor = db.cursor()
print("Database created and Successfully Connected to SQLite")
# create table to store data
cursor.execute(
	"CREATE TABLE IF NOT EXISTS users(ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, username text,hash text)")


@app.after_request
def after_request(response):
	"""Ensure responses aren't cached"""
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response


@app.route("/")
def home():
	"""home page"""
	return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	"""register new user in database"""
	if request.method == "GET":
		return render_template("register.html")
	# work with the POST method and get the data from the form
	else:
		username = request.form.get("username")
		password = request.form.get("password")
		confirmation = request.form.get("confirmation")
		# require a username
		if not username:
			return "You forgot to provide the username !"
		# require a password
		if not password:
			return "You forgot to provide the password! "
		# require to retype the password
		if not confirmation:
			return "You forgot to retype your password!"
		# require for match
		if password != confirmation:
			return "Passwords are not matching!"

		# hash the user's password (we can use password or confirmation as both are the same)
		hash_pass = generate_password_hash(password)

		# ensure username is unique
		rows = cursor.execute(
			"SELECT * FROM users WHERE username = :username", (username,))
		if len(rows.fetchall()) >= 1:
			return "User already exists"
		# register new users in users table database
		# if users does not exist
		sql_insert_with_param = "INSERT INTO users(username,hash) VALUES (?,?);"
		inserted_data = (username, hash_pass)
		try:
			new_user = cursor.execute(
				sql_insert_with_param, inserted_data).fetchall()
			db.commit()
			flash(f"Welcome {username}, you have now registered")
		except sqlite3.Error as error:
			print("Failed to insert data into sqlite table", error)
		session['id'] = new_user
		create_folder(username)
		# redirect to the users account page once registered
		return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
	"""log user in"""
	session.clear()
	username = request.form.get("username")
	if request.method == "POST":
		if not request.form.get("username"):
			return "Username Invalid"
		elif not request.form.get("password"):
			return "must provide password"
		user_account = cursor.execute(
			"SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
		if len(user_account) != 1 or not check_password_hash(user_account[0][2], request.form.get("password"),):
			return "Invalid username or password"
		session["id"] = user_account[0][0]
		flash(f"{username}! You are now logged in !")
		return redirect("/")
	else:
		return render_template("login.html")


@app.route("/logout")
def logout():
	"""logout user out"""
	session.clear()
	flash("You have now logged out!")
	return redirect('/')


@app.route("/upload", methods=["GET", "POST"])
def upload():
	"""Upload documents"""
	username = request.form.get("username")
	if request.method == "GET":
		return render_template('upload.html')
	if not "file" in request.files:
		flash("No file part in request")
		return redirect(request.url)
	files = request.files.getlist("file")
	for file in files:
		if file.filename == '':
			flash("No file uploaded")
			return redirect(request.url)
		if file_valid(file.filename):
			filename = secure_filename(file.filename)
			for directory in os.listdir(UPLOADS_FORLDER):
				DATA_DIRECTORIES.append(directory)
				file.save(os.path.join(
					UPLOADS_FORLDER, username, filename))  # type: ignore
		else:
			flash("Invalid file type")
			return redirect(request.url)
	return "File was uploaded succesfully"
	
# @app.route("/account",methods=["GET","POST"])
# def account_details():
# 	"""Get account details displayed"""
# 	if request.method == "GET":
# 		df = pd.read_csv(" ")
# 		df["Customer Creation Timestamp"] = df["Customer Creation Timestamp"].astype("datetime64")
# 		new_df = df[["First Name", "Last Name","Country Of Registration","Membership Status","Customer Creation Timestamp"]].copy()
# 		return render_template("account.html",tables=[new_df.to_html(classes="data",header=True)])

# @app.route("billing",methods=["GET","POST"])
# def billing_details():
# 	"""Get Billing Details"""
# 	if request.method =="GET":
# 		df = pd.read_csv(" ")
# 		df.plot()
# 		# plt.show()
# 		return render_template("billings.html",tables=[plt.show()])



if __name__ == "__main__":
	app.run(debug=True)


 


