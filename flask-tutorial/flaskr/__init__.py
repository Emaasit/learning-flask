# This init file tells Python that the flaskr directory should be treated as a package
# This init file will also contain the Application Factory.
# Instead of creating a Flask instance globally, you will create it inside a function.
# This function is known as the application factory.
# Any configuration, registration, and other setup the application needs will happen inside
# the function, then the application will be returned.

import os
from flask import Flask
from flask_pymongo import PyMongo


# Create the application factory function called "create_app"
def create_app(test_config=None):
    """
    This function is known as the application factory.
    Any configuration, registration, and other setup the application needs will happen inside
    the function, then the application will be returned

    :param test_config:
    :return:
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
    mongo = PyMongo(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        # Load the install config it it exists
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the instance config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # Python functions that will run the SQL commands in schema.sql
    from . import db
    db.init_app(app=app)

    # Import and register the auth blueprint from the factory
    from . import auth
    app.register_blueprint(auth.bp)

    # Import and register the blog blueprint from the factory
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app

