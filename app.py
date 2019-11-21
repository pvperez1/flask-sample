from flask import Flask, request, redirect, url_for, session, render_template
import sqlite3
app = Flask(__name__)

# Configuration for app starts here
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "thisisasecretkey!"
# Configuration ends here

@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

@app.route('/home', defaults={"name":"Person"})
@app.route('/home/<name>')
def home(name):
    session["username"] = name #in this part, i am setting the value of the session["username"]
    my_subjects = ["LIS 51", "LIS 160", "LIS 161"]
    books = [{"title":"Harry Potter","author":"J.K. Rowling"}
        ,{"title":"Book1","author":"author2"}
        ,{"title":"Book3","author":"author3"}]
    person = {"name":"Paul","email":"pvperez1@gmail.com"}

    ### This is where I extract from DB

    return render_template("home.html", home_name = name, user_flag = 2, home_subjects = my_subjects, books = books, person=person)

#this page is the form
@app.route('/form', methods=["GET","POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    else:
        # in this part i am extracting the values from the form
        var_name = request.form["username"]
        var_location = request.form["location"]

        ####
        ####This is where i save the variable to database
        conn = sqlite3.connect('flask.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name,location) VALUES (?,?)', (var_name,var_location))
        conn.commit()
        cur.close()
        ####


        if var_name == '':
            return redirect(url_for('unsuccessful'))
        else:
            return redirect(url_for('home', name=var_name, location=var_location))

@app.route('/unsuccessful')
def unsuccessful():
    return "<h1>Username not found</h1>"


@app.route('/about')
def about():
    if session.get("username") is None:
        return redirect(url_for("form"))
    else:
        name = session["username"]
        return render_template("about.html", about_name = name)

@app.route('/logout')
def logout():
    session.pop("username")
    return "<h1>Successfully logged out!</h1>"


@app.route('/showall')
def showall():
    # Read all contents of user table
    conn = sqlite3.connect('flask.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    results = cur.fetchall()
    cur.close()
    #end of db transaction

    return render_template('showall.html', results=results)


if __name__ == "__main__":
    app.run()