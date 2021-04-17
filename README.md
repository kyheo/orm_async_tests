# ORM Async Tests

A couple of tests checking how SQLAlchemy async works.

## How to use it

We use docker compose for the DB and just in case we add other services in the 
future, like FastAPI which I would love to see it working along with 
SQLAlchemy.

`docker compose up` will start the DB and create the default user, password 
and database.

Then you, after installing Poetry on the system 
(info [here](https://python-poetry.org)), run `poetry install`.

Then you can choose:

- Run any script defined in `pyproject.toml`:
```shell
$ poetry run test1
```

- Run any script from within inside a shell:
```shell
$ poetry shell
$ test1
```

## Tools and libraries
We use the following tools:
- docker: With compose, used to create the environment in which everything 
  runs.
- poetry: To manage the project, requirements and venv.
- nox: As a Python replacement of tox, automation tool.
- alembic: To handle DB migrations. 
  [Aync support](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html?highlight=async)
  
And the following libraries and Python packages:
- SQLAlchemy: As the ORM.
- asyncpg: To connect to Postgresql.

## Nox

Below you can see a list of commands that could help you run usual commands. 
Each session can receive parameters, for that after the command use `--` as a
separator between nox parameters and the session ones.

- `nox`: Runs the default sessions. 
- `nox -l`: Lists the sessions that can be executed.
- `nox -s <session>`: Executes `<session>`.


## Alembic and DB migrations
Alembic handles the DB migrations. You can see the docs in 
[here](https://alembic.sqlalchemy.org/en/latest/). It has support for branches
and other more complex stuff that are not used in here because of the 
simplicity of the tests done. For instance, branches could be used as a way
to split migrations from different packages or applications inside the code.

### Init
Init requires a template that works in an async way, this is already done
because Alembic is only initialized once, but for future reference:

```shell
$ alembic init -t async src/alembic
```

### Create a new revision

The following commands creates a new revision. `--autogenerate` looks for
changes in the models and includes them in the migration file.

```shell
$ alembic revision --autogenerate -m 'Some message'
```

### See the migration history
```shell
$ alembic history
```

### Apply a migration
Apply all migrations
```shell
$ alembic upgrade head
```

To apply up to a specific migration replace `head` with th revision hash.

### Rollback migrations
Rollback the last migration
```shell
$ alembic downgrade -1
```

To rollback to a specific migration replace `-1` with the hash of the 
revision you want.
