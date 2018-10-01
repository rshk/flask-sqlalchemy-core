Flask / SQLAlchemy Core
#######################

Provides integration for using SQLAlchemy Core in a Flask application.

Most importantly, it provides a mechanism for sharing the same
connection across nested functions (in the same thread /
greenlet).

This allows for cleaner nested transactions, and also reduces test run
time by wrapping each test function run in a transaction which will be
rolled back at the end, removing the need to fully recreate the whole
database schema over and over.


Usage
=====

Set up
------

.. code-block:: python

    import os
    from flask_sqlalchemy_core import FlaskSQLAlchemy

    DATABASE_URL = os.environ['DATABASE_URL']

    db = FlaskSQLAlchemy(DATABASE_URL)


Running queries
---------------

.. code-block:: python

    from sqlalchemy import select

    # Create your query here
    query = select(...)

    with db.connect() as conn:
        result = conn.execute(query)
        # Do something with the result...



Define tables
-------------

Just do as you normally would (create a Metadata
instance, use it to define your schema).


Creating schema
---------------

.. code-block:: python

    metadata.create_all(db.get_engine())


Test fixtures
-------------

For use with pytest, place those in a ``conftest.py`` file in your
tests directory.

**Note:** you might want to change your ``DATABASE_URL`` environment
variable during testing, to avoid overriding your current development
database.

.. code-block:: python

    import pytest

    @pytest.fixture
    def db(db_schema):
        with db.transaction(autocommit=False, rollback=True):
            # By wrapping execution in a transaction that automatically
            # gets rolled back, we can avoid having to recreate the whole
            # schema for every test function run.
            yield

    @pytest.fixture(scope='session')
    def db_schema():
        engine = db.get_engine()

        # Clean up, in case tables were left around from a previous run.
        # This can happen if the test process was abruptly killed.
        metadata.drop_all(engine)

        metadata.create_all(engine)

        yield

        metadata.drop_all(engine)


Testing
=======

Before running the test suite, you'll need to start a SQL database and
set the DATABASE_URL environment variable.

For convenience, you can use the ``bin/run-test-database`` script,
which will automatically run a PostgreSQL instance via Docker.

The script will print a suitable value for ``DATABASE_URL`` as well.

Oncer you're done, simply kill it via Ctrl-C.


To install test dependencies::

    pip install -r test_requirements.txt

To run the test suite::

    pytest -vvv ./tests
