from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
# Import a function to convert BLOB data into image data
from io import BytesIO

# Import our recommendation giving function from a separate file
from recommendation import find_closest

# Import some CS50 helpers
from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///musicals.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show the homepage of the website"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # db.execute will always get back a list
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get the username and password inputted by the user
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Check for possible erros
        # Ensure username was submitted
        if not username:
            return apology("must provide username")
        # Ensure password was submitted
        if not password:
            return apology("must provide password")
        if not confirmation:
            return apology("must provide password again")
        # Ensure match
        if confirmation != password:
            return apology("Password does not match")
        # Generate a hash of the password for security purpose
        h = generate_password_hash(password)
        # Use try!
        # Insert the new user into users table
        try:
            # Add it in
            new = db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, h)
        except:
            return apology("Username already exists")
        # Remember which user has logged in
        # How should I find the id of that? -->store the new execution insert as new user
        # troublesome, do not inqury database again rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # db.execute returned the index of only the last inserted line
        session["user_id"] = new
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

# Set up lists for the language, theme, and setting options
LANGUAGE = [x["language"] for x in db.execute("SELECT DISTINCT language FROM musicals")]
THEME= [x["theme"] for x in db.execute("SELECT DISTINCT theme FROM theme")]
SETTING= [x["setting"] for x in db.execute("SELECT DISTINCT setting FROM musicals")]

@app.route("/explore", methods=["GET", "POST"])
def explore():
    """Renders the explore page and manages searches"""
    # this crazy whatever thing, must have a way to do it
    if (request.method == "POST"):
        # Get the user submitted information
        search = request.form.get("search")
        language = request.form.get("language")
        theme = request.form.get("theme")
        setting = request.form.get("setting")

        # Set up the query that we need to make to the database
        query = "SELECT name, description, vphoto FROM musicals"
        clauses = []
        values = []

        # If the user actually inputted values for these fields, we need to add them to the query
        if search:
            clauses.append("description LIKE ?")
            values.append(f"%{search}%")
        if language:
            clauses.append("language = ?")
            values.append(language)
        if theme:
            clauses.append("id IN (SELECT musical_id FROM match WHERE theme_id IN (SELECT id FROM theme WHERE theme = ?))")
            values.append(theme)
        if setting:
            clauses.append("setting = ?")
            values.append(setting)
        # Checks if there are any additional clauses to add, if there are then add the clauses to the query
        if clauses:
            query = query + " WHERE " + " AND ".join(clauses)
        # Get the search results
        results = db.execute(query, *values)

        # If there are no results we need to print the sorry message and display all the musicals
        if len(results) == 0:
            results = db.execute("SELECT name, description, vphoto FROM musicals")
            search_success = False
        # If the search was successful we don't need the sorry message
        else:
            search_success = True
        # Render the correct page
        return render_template("explore.html", language=LANGUAGE, theme = THEME, setting = SETTING, results=results, search_success=search_success)
    else:
        # If you reach here via get you must not have entered any searches, so we display all the musicals by default
        results = db.execute("SELECT name, description,vphoto FROM musicals")
        return render_template("explore.html", language=LANGUAGE, theme = THEME, setting = SETTING, results=results)

@app.route("/musical_info/<musical_name>", methods=["GET", "POST"])
def musical_info(musical_name):
    # We need to get information about this musical from the database, but if it's an invalid name we want to return an error
    try:
        musical = db.execute("SELECT id, name, description, setting, language FROM musicals WHERE name = ?", musical_name)[0]
    except(IndexError):
        return apology("not a musical in database")
    # We also need to grab the themes if it's a valid musical
    themes = db.execute("SELECT theme FROM theme WHERE id IN (SELECT theme_id FROM match WHERE musical_id = ?)", musical["id"])

    # Render the page with the musical's info
    return render_template("musical_info.html", musical=musical, themes=themes)

# Source: https://stackoverflow.com/questions/63340686/render-blob-from-sqlite-server-in-html-with-flask-python
@app.route('/images/<photo_type>/<musical_name>')
def get_photo(photo_type, musical_name):
    """Allows us to display the photos in our database"""
    # Check if the photo_type inputted is valid
    if (photo_type not in ["hphoto", "vphoto"]):
        return apology("no photo of that type in database")

    # If it's a valid photo type, to grab the correct photo for that musical - catch exception if it doesn't exist and return an apology
    try:
        photo = db.execute(f"SELECT {photo_type} FROM musicals WHERE name = ?", musical_name)[0][photo_type]
    except(IndexError):
        return apology("not a musical in database")

    # Convert the SQL blob to a format that html can display
    bytes_io = BytesIO(photo)

    # Send the image data
    return send_file(bytes_io, mimetype='image/jpeg')


@app.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
     if request.method == "POST":
        # If the submit survey button is pressed, we need to run the code to process the survey inputs
        if request.form["survey_page_action"] == "submit_survey":
            # Do some setup to get user information
            question_info = db.execute("SELECT type from survey")
            user_data={}

            # Try to add the user submitted data in the survey to the list of user data, rejecting non-numerical values and bad keys
            for question in question_info:
                try:
                    user_data[question["type"]] = int(request.form[question['type']])
                except (ValueError, KeyError):
                    return apology("Invalid form - try again!")

            # Check if all of the user data is in the correct range
            if not all(1 <= data <= 5 for data in user_data.values()):
                return apology("Invalid form - try again!")

            # Calculate the recommendation using the algorithm
            musical_info = db.execute("SELECT id, romance, humour, fiction_history, action, mystery FROM musicals")

            # Use our *special* algorithm to find the musical that matches most closely with the user's answers!
            recommended_id = find_closest(user_data, musical_info)

            # Get the info for the musical we recommend
            musical = db.execute("SELECT id, name, description, setting, language FROM musicals WHERE id = ?", recommended_id)[0]

            # Get the themes for the musical we recommended
            themes = db.execute("SELECT theme FROM theme WHERE id IN (SELECT theme_id FROM match WHERE musical_id = ?)", musical["id"])

            # Update the user's data so that we know they completed the survey and which musical we recommended
            db.execute("UPDATE users SET survey_completed = 1, recommended_musical_id = ? WHERE id = ?", recommended_id, session["user_id"])

            # Render the survey completed page!
            return render_template("survey_completed.html", musical=musical, themes=themes)

        # If the retake survey button is clicked, we need to clean out the user's data and render the survey page again
        elif request.form["survey_page_action"] == "retake_survey":
            # Reset the user's data
            db.execute("UPDATE users SET survey_completed = 0, recommended_musical_id = NULL WHERE id = ?", session["user_id"])
            # Send the user back to the survey page
            return redirect("/survey")

        # Otherwise, someone messed with the values of the buttons, so we don't like them
        else:
            return apology("Invalid button value")

     else:
        # If we get here via get, check if the user has submitted the survey before - if they have, just show their recommended musical
        if (db.execute("SELECT survey_completed FROM users WHERE id = ?", session["user_id"])[0]["survey_completed"] == 1):
            # Get the musical we recommended before
            musical = db.execute("SELECT id, name, description, setting, language FROM musicals WHERE id = (SELECT recommended_musical_id FROM users WHERE id = ?)", session["user_id"])[0]
            # Get the themes for the musical we recommended
            themes = db.execute("SELECT theme FROM theme WHERE id IN (SELECT theme_id FROM match WHERE musical_id = ?)", musical["id"])

            # Render the completed survey page
            return render_template("survey_completed.html", musical=musical, themes=themes)
        # Otherwise, return the default survey page
        else:
            questions = db.execute("SELECT question, answer1, answer2, answer3, answer4, answer5, type FROM survey")
            return render_template("survey.html", questions=questions)

