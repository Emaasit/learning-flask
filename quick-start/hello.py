from flask import Flask, url_for, request, render_template

app = Flask(__name__)


# Use the route decorator to define the URL that will trigger the function
@app.route("/")
def index():
    return "This is the index page"


@app.route("/hello")
def hello_world():
    return "Hello, World!"


@app.route("/home/") # Usage of trailing slash
def home_page():
    return "Adding {} plus {} returns {}".format(2, 2, 4)


# Using variable names as URL end points
@app.route("/user/<username>")
def show_user_profile(username):
    # Show the user profile for that user
    return "User %s" %username


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # Show post with the given id
    return "Post with id %d" %post_id


@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    # Show the subpath after /path/
    return "Subpath is %s" %subpath


# URL building
with app.test_request_context():
    print(url_for("home_page"))


# HTTP methods and
# Accessing Request Data
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        return "do_the_login()"
    else:
        return "show_the_login_form()"


# Rendering templates
@app.route("/company/")
@app.route("/company/<name>")
def company(name=None):
    return render_template("index.html", name=name)



