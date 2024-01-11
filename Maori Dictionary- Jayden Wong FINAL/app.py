##################################################
# Imports
##################################################

# Coding used to import Flask, Sqlite and bcrypt into the coding
from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt

##################################################
# Variables
##################################################

# Makes it so that db_file can be used as a variable for "Maori_Dictionary.db"
db_file = "Maori_Dictionary.db"

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ksdnai91e1jwqjjwj093u3rjeq02"

##################################################
# Database connection
##################################################

# Creates connection to the database file, Maori_dictionary.db
def create_connection(db_file):
    # create a connection to the sqlite db
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None

##################################################
# Website page code
##################################################


#Homepage Coding
@app.route('/', methods=['GET', 'POST'])
def render_homepage():
    ##### Coding for adding a new topic into the database #####
    if request.method == "POST" and is_logged_in():
        add_topic = request.form['topic_name'].title() #Renames variable from the "add word" form to a tidier one.
        if len(add_topic) < 3: #If length of topic trying to be added is less than 3 characters, error will display
            return redirect("/?error=Topic+Name+must+be+at+least+3+letters+long.")
        else:
            con = create_connection(db_file) # connect to the database

            query = "INSERT INTO Categories (id, topic) VALUES(NULL, ?)" #Will insert the new topic into a new variable
            cur = con.cursor()  # You need this line next
            try:
                cur.execute(query, (add_topic,))  # this line actually executes the query
            except sqlite3.IntegrityError: # Error shows if the database already has a name that is the same.
                return redirect('/?error=Topic+already+exists.')

            con.commit()
            con.close()
            return redirect('/?message=Topic+added!.')


    return render_template('home.html', topics=topic_list(), logged_in=is_logged_in())


##### Webpage for categories #####
@app.route('/<catID>', methods=["GET", "POST"])
def render_dictionary(catID):

    ##### display title #####
    con = create_connection(db_file) # connects page to db_file (Maori_Dictionary.db).

    query = "SELECT id, topic FROM Categories WHERE id=?" #Selects the topic from the Categories table

    cur = con.cursor()
    cur.execute(query, (catID,))
    topic_title = cur.fetchall()
    con.close()

    ##### code to add new words into category #####
    if request.method == "POST" and is_logged_in() and 'add_word' in request.form:

        # changes the form code into a cleaner variable. Also makes words lowercase.
        add_english = request.form['english'].lower()
        add_maori = request.form['maori'].lower()
        add_description = request.form['description']
        add_level = request.form['level']

        # Connects to the database
        con = create_connection(db_file)
        # SELECT the things you want from your table(s). Makes it so that words from the selected category is chosen
        query = "SELECT english, maori FROM Dictionary WHERE english=?"

        cur = con.cursor()
        cur.execute(query, (add_english,)) #executes query. "?" variable is "add_english" variable.
        add_word = cur.fetchall()
        con.close()
        try: #Code to check if words already exist in dictionary.
            maori = add_word[0][0]
            english = add_word[0][1]
        except IndexError: # If words don't exist, word will be added to dictionary.
            # Code to check lengths of variables. error will show if word or description not long enough
            if len(add_english) < 1:
                return redirect("/?error=English+name+must+be+at+least+1+letter+long.")
            elif len(add_maori) < 2:
                return redirect("/?error=Maori+name+must+be+at+least+2+letters+long.")
            elif len(add_description) < 10:
                return redirect("/?error=Description+must+be+at+least+10+letters+long.")
            else:
                con = create_connection(db_file)# connect to the database

                #inserts data into dictionary.
                query = "INSERT INTO Dictionary (id, english, maori, description, level, date, author, image, catID) " \
                        "VALUES(NULL, ?, ?, ?, ?, date(), ?, 'noimage.png', ?)"

                cur = con.cursor()  # You need this line next
                try:
                    # this line actually executes the query. Adds these values to "?" variables.
                    cur.execute(query, (add_english, add_maori, add_description, add_level, session['firstname'], catID))
                except: # if any other errors appear, this code will appear
                    return redirect('/?error=Unknown+error')
                con.commit()
                con.close()
        else: # if the word already exists in the database, this appears.
            return redirect("/?error=Word+already+exists!")

    ##### code for editing topics #####
    if request.method == "POST" and is_logged_in() and 'edit_topic' in request.form:
        edit_topic = request.form['topic_edit'].title()

        # Edited topic must be at least 3 characters long.
        if len(edit_topic) < 3:
            return redirect('signup?error=Category+must+be+at+least+3+characters!')
        # Connects to the database
        con = create_connection(db_file)

        # Selects what variable in the database that you want to update.
        query = "UPDATE Categories SET topic=? WHERE id=?"

        cur = con.cursor()
        try:
            cur.execute(query, (edit_topic, catID,)) # executes the query. puts variables in "?"
        except sqlite3.IntegrityError: # if topic already exists, this error appears.
            return redirect('/?error=Topic+already+exists!')

        con.commit()
        con.close()
        return redirect('/?message=Topic+edited!')

    ##### Code for deleting topic #####
    if request.method == "POST" and is_logged_in() and 'delete_topic' in request.form:

        # creates connection
        con = create_connection(db_file)

        # deletes the specific category that you are on. "?" variable is catID.
        query = "DELETE FROM Categories WHERE id=?"
        cur = con.cursor()
        cur.execute(query, (catID,)) # execute query

        # deletes words in topic deleted by using catID.
        query = "DELETE FROM Dictionary WHERE catID=?"
        cur = con.cursor()
        cur.execute(query, (catID,)) # "?" variable is catID.

        con.commit()
        con.close() # close connection

        return redirect('/?message=Topic+deleted!') #redirects back to homepage.

    # Connects to the database
    con = create_connection(db_file)
    # SELECT the things you want from your table(s). Makes it so that words from the selected category is chosen
    query = "SELECT id, english, maori, catID, description, level, date, author, image FROM Dictionary WHERE catID=?"

    cur = con.cursor()  # You need this line next
    cur.execute(query, (catID,))  # this line actually executes the query
    word_list = cur.fetchall()  # puts the results into a list usable in python
    con.close()


    return render_template('dictionary_categories.html', words=word_list, topics=topic_list(), title=topic_title, logged_in=is_logged_in())


@app.route('/login', methods=["GET", "POST"])
def render_login_page():
    if is_logged_in():
        return redirect('/')
    if request.method == "POST":
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        query = """SELECT id, fname, password FROM User WHERE email = ?"""
        con = create_connection(db_file)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()

        try:
            userid = user_data[0][0]
            firstname = user_data[0][1]
            db_password = user_data[0][2]
        except IndexError:
            return redirect("/login?error=Email+invalid or password incorrect")

        if not bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['userid'] = userid
        session['firstname'] = firstname
        print(session)
        return redirect('/?message=Logged+in!')

    return render_template('login.html', topics=topic_list(), logged_in=is_logged_in())


@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():

    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').strip().title()
        lname = request.form.get('lname').strip().lower()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # When signing up, if repeat password not the same, it gives error
        if password != password2:
            return redirect('signup?error=Passwords+dont+match!')

        # If password is less than 8 characters, it gives error
        if len(password) < 8:
            return redirect('signup?error=Password+must+be+at+least+8+characters!')

        # Hashes password, meaning that the password will be scrambled in the table. Makes website more secure.
        hashed_password = bcrypt.generate_password_hash(password)
        con = create_connection(db_file)

        query = "INSERT INTO User (id, fname, lname, email, password) " \
                "VALUES(NULL,?,?,?,?)"

        cur = con.cursor()
        try:
            cur.execute(query, (fname, lname, email, hashed_password))
        except sqlite3.IntegrityError:
            return redirect('/signup?error=Email+is+already+being+used!')

        con.commit()
        con.close()
        return redirect('/login')


    return render_template('signup.html', topics=topic_list(), logged_in=is_logged_in())


@app.route('/<catID>/<id>', methods=['GET', 'POST'])
def render_word_info(catID, id):

    ##### Code to show word information #####
    # connects to database
    con = create_connection(db_file)

    # SELECT the things you want from your table(s). Makes it so that words from the selected category is chosen
    query = "SELECT id, english, maori, catID, description, level, date, author, image FROM Dictionary WHERE id=?"

    cur = con.cursor()  # You need this line next
    cur.execute(query, (id,))  # this line actually executes the query
    word_info = cur.fetchall()  # puts the results into a list usable in python
    con.close()

    ##### code to edit words #####
    if request.method == "POST" and is_logged_in() and 'edit_word_button' in request.form:
        edit_english = request.form['edit_english'].lower()
        edit_maori = request.form['edit_maori'].lower()
        edit_description = request.form['edit_description']
        edit_level = request.form['edit_level']

        # Connects to the database
        con = create_connection(db_file)
        # SELECT the things you want from your table(s). Makes it so that words from the selected category is chosen
        query = "SELECT english, maori FROM Dictionary WHERE english=?"

        cur = con.cursor()
        cur.execute(query, (edit_english,))  # executes query. "?" variable is "add_english" variable.
        add_word = cur.fetchall()
        con.close()
        if len(edit_english) < 1:
            return redirect("/?error=English+name+must+be+at+least+1+letter+long.")
        elif len(edit_maori) < 2:
            return redirect("/?error=Maori+name+must+be+at+least+2+letters+long.")
        elif len(edit_description) < 10:
            return redirect("/?error=Description+must+be+at+least+10+letters+long.")
        else:
            con = create_connection(db_file)  # connect to the database

            # inserts data into dictionary.
            query = "UPDATE Dictionary SET english=?, maori=?, description=?, level=? WHERE id=? "

            cur = con.cursor()  # You need this line next
            cur.execute(query, (edit_english, edit_maori, edit_description, edit_level, id))

            con.commit()
            con.close()
            return redirect('/?message=Word+Edited!')


    ##### Code for deleting word #####
    if request.method == "POST" and is_logged_in() and 'delete_word' in request.form:

        # creates connection
        con = create_connection(db_file)

        # deletes word that user is currently on
        query = "DELETE FROM Dictionary WHERE id=?"
        cur = con.cursor()
        cur.execute(query, (id,)) # "?" variable is catID.

        con.commit()
        con.close() # close connection

        return redirect('/?message=Word+deleted!') #redirects back to homepage.

    return render_template('word_info.html', info=word_info, topics=topic_list(), logged_in=is_logged_in())


@app.route('/search')
def render_search_function():
    ##### Code for search function #####
    # Connects to the database
    con = create_connection(db_file)
    # SELECT the things you want from your table(s). Makes it so that words from the selected category is chosen
    query = "SELECT id, english, maori, catID, description, level, date, author, image FROM Dictionary"

    cur = con.cursor()  # You need this line next
    cur.execute(query)  # this line actually executes the query
    word_list = cur.fetchall()  # puts the results into a list usable in python
    con.close()

    return render_template('search_function.html', words=word_list, topics=topic_list(),logged_in=is_logged_in())


# Function for logging out of website
@app.route('/logout')
def logout():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/?message=See+you+next+time!')


##################################################
# Other Functions
##################################################

# Function for logging into a website
def is_logged_in():
    if session.get("email") is None:
        return False
    else:
        return True
        
        
#Function to show topics on navigation
def topic_list():
    ##### code to show navigation categories #####
    # connects page to db_file (Maori_Dictionary.db)
    con = create_connection(db_file)
    # used to display the categories on the side for navigation.
    query = "SELECT id, topic FROM Categories"

    cur = con.cursor()
    cur.execute(query)
    topic_list = cur.fetchall()
    con.close()

    return topic_list


app.run(host='0.0.0.0')
