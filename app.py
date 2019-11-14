from flask import Flask, request, redirect, url_for, session, render_template
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
    return render_template("home.html", name=name)

#this page is the form
@app.route('/form', methods=["GET","POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    else:
        # in this part i am extracting the values from the form
        var_name = request.form["username"]
        var_location = request.form["location"]
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
        return render_template("about.html")

@app.route('/logout')
def logout():
    session.pop("username")
    return "<h1>Successfully logged out!</h1>"



if __name__ == "__main__":
    app.run()