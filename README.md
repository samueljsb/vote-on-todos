# vote-on-todos

This is an application to keep todo lists and vote on items to prioritise them.

## usage

This project uses Python 3.12.

You can run this project in a virtual environment using `nox`:

```shell
nox -s runserver
```

This will create a virtual environment, a database file, and start the web
server. You can then create an account and start creating todo lists via the
website.

If you don't have or don't want to install `nox`, you can run the project with:

```shell
python3.12 -mvenv venv
. venv/bin/activate
python -m pip install -rrequirements/prod.txt
python -m manage migrate
python -mm anage runserver
```

## why is it over-engineered?

Because I'm using it as practice for architectural patterns that are useful for
larger/enterprise software (see also
https://github.com/samueljsb/toy-event-sourced-settings).
