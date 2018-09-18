import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    g is a special object that is unique for each request. It is used to store data that
    might be accessed by multiple functions during the request. The connection is stored
    and reused instead of creating a new connection if get_db is called a second time in the same request.

    :return: a database connection, which is used to execute the commands read from the file
    """
    if "db" not in g:
        # Establish a connection to the file pointed at by the DATABASE configuration key
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    close_db checks if a connection was created by checking if g.db was set.
    If the connection exists, it is closed.
    :param e:
    :return:
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Add the Python functions that will run these SQL commands.
    open_resource() opens a file relative to the flaskr package, which is useful
    since you won’t necessarily know where that location is when deploying the application later.
    :return:
    """
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# click.command() defines a command line command called init-db that calls the
# init_db function and shows a success message to the user
@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Clear the existing data and create new tables
    :return:
    """
    init_db()
    click.echo(message="Initialized the database")


# Import and call this function from the factory
def init_app(app):
    """
    The close_db and init_db_command functions need to be registered with the application instance,
    otherwise they won’t be used by the application. However, since you’re using a factory function,
    that instance isn’t available when writing the functions. Instead, write a function that takes
    an application and does the registration.

    :param app:
    :return:
    """
    app.teardown_appcontext(close_db)  # call close_db when cleaning up after returning the response
    app.cli.add_command(init_db_command)