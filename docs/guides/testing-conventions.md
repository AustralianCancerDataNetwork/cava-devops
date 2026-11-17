# Testing conventions

How tests select their database and their CI job, across every repo. The recommended workflows are 

- [`build-test-nodb.yml`](../workflows/build-test-nodb.md), 
- [`build-test-sqlite-v2.yml`](../workflows/build-test-sqlite-v2.md), 
- [`build-test-duckdb.yml`](../workflows/build-test-duckdb.md) and 
- [`build-test-postgres-v3.yml`](../workflows/build-test-postgres-v3.md).


## Rules

- A routing mark names the infrastructure a test needs and decides which CI job runs it. In most repos the routing marks are the dialects: `sqlite`, `duckdb` and `postgresql`. Other routing marks can be used but require adapting the `ci.yml` of the repository, for example `omop-emb`'s `sqlitevec`, `pgvector`, `duckdbvss` and `faiss`.
- A test without a routing mark needs no database. It runs in the `build-test-nodb` job.
- A test with a routing mark needs real infrastructure and counts as an integration test. A test without one needs none and counts as a unit test. Neither term is a pytest mark.
- A test carries the routing mark of every job it should run in, and must pass in each. A test that depends on one backend carries one mark. A test meant for several dialects is parametrized with `DIALECT_PARAMS`, which marks each param.
- Adding a routing mark requires adding its CI job. Otherwise those tests never run.
- Every test gets its database from an `isolated_test_database` fixture. No test opens its own engine or connection.
- Every fixture that calls `isolated_test_database` passes `request`. A test that lacks the routing mark fails at fixture setup, before any DDL runs.
- Use the `Dialect` enum, never string literals.
- Use `pytestmark` when every test in a module needs the marks, and a decorator for a single test.
- Set `--strict-markers` in `addopts`, so a misspelled mark is an error.
---

## Marking tests

A module that needs one dialect:

```python
import pytest

pytestmark = pytest.mark.postgresql


def test_loads_into_postgres(pg_db): ...
```

A single test:

```python
@pytest.mark.sqlite
def test_loads_into_sqlite(sqlite_db): ...
```

A test body that must pass on every dialect:

```python
from oa_configurator.testing import DIALECT_PARAMS


@pytest.fixture(params=DIALECT_PARAMS)
def dialect_session(request):
    return request.getfixturevalue(SESSION_FIXTURE_BY_DIALECT[request.param])


def test_runs_on_every_dialect(dialect_session): ...
```

!!! tip
    A test that needs no database carries no mark.

---

## Writing a fixture

```python
from oa_configurator import Dialect
from oa_configurator.testing import isolated_test_database


@pytest.fixture
def sqlite_db(request):
    with isolated_test_database(
        MyConfig, "test_cdm_db_sqlite", dialect=Dialect.SQLITE, request=request
    ) as db:
        yield db
```

A repo whose jobs route on another mark names it, e.g. preconfigured test elements from `oa-configurator`:

```python
with isolated_test_database(
    MyConfig, "test_emb_db_pg", request=request, routing_mark="pgvector"
) as db:
    yield db
```

### Session-scoped databases

`isolated_test_database(..., request=request)` can only check the marks of the test that is running when its fixture is function-scoped. A fixture with a wider scope, for example one that loads a vocabulary once per session, gets the session as `request.node`, so it cannot know which test will use it.

Open the database in the wide fixture without `request`, and put a function-scoped fixture on top that checks the marks of each test:

```python
from oa_configurator import Dialect
from oa_configurator.testing import isolated_test_database, require_routing_mark


@pytest.fixture(scope="session")
def engine(tmp_path_factory):
    # Missing `request`
    with isolated_test_database(MyConfig, "test_cdm_db_sqlite", dialect=Dialect.SQLITE) as db:
        load_vocabulary(db.connection.engine)
        yield db.connection.engine


@pytest.fixture
def session(request, engine):
    # Added routing with `request`
    require_routing_mark(request, "test_cdm_db_sqlite", Dialect.SQLITE)
    with so.Session(engine) as session:
        yield session
```

Every test that uses `session` must now carry `sqlite`, or it fails at setup:

```python
@pytest.mark.sqlite
def test_reads_a_concept(session): ...
```

!!! tip
    Tests should use the function-scoped fixture, never `engine` directly. A test that uses `engine` directly skips the check.

---

## CI jobs

One job per routing mark, plus the nodb job. Keep the job ids, so the required check names stay `build-test-nodb / test`, `build-test-sqlite / test`, `build-test-duckdb / test` and `build-test-postgres / test`.

```yaml
jobs:
  build-test-nodb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-nodb.yml@main
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite-v2.yml@main
  build-test-duckdb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-duckdb.yml@main
  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres-v3.yml@main
```

A job that collects no tests fails, so a repo only calls the workflows for marks it has tests for.

A repo with other routing marks passes them to the jobs:

```yaml
jobs:
  build-test-nodb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-nodb.yml@main
    with:
      exclude-markers: sqlitevec or pgvector or duckdbvss or faiss
  build-test-faiss:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite-v2.yml@main
    with:
      markers: faiss
```

---

## Banning inline engines

Ruff's `TID251` bans the calls that open a database outside the fixtures:

```toml
[tool.ruff.lint]
extend-select = ["TID251"]

[tool.ruff.lint.flake8-tidy-imports.banned-api]
"sqlalchemy.create_engine".msg = "Get a database from an isolated_test_database fixture."
"sqlalchemy.engine.create_engine".msg = "Get a database from an isolated_test_database fixture."
"sqlite3.connect".msg = "Get a database from an isolated_test_database fixture."
"duckdb.connect".msg = "Get a database from an isolated_test_database fixture."

[tool.ruff.lint.per-file-ignores]
"src/**" = ["TID251"]
"tests/conftest.py" = ["TID251"]
```

!!! warning
    It does not catch methods such as `resolved.create_engine()`. A test that opens an engine on purpose, such as a test of an engine guard, says why on the line:

    ```python
    admin = sa.create_engine(url)  # noqa: TID251 - admin connection to create the target database
    ```

---

## Mixing dialects in one process

!!! warning "Dialects share ORM metadata"
    SQLAlchemy's `create_all()` on a dialect that supports `ALTER` (PostgreSQL, DuckDB) defers circular foreign keys and records that on the constraint objects of the shared `MetaData`. A later `create_all()` on SQLite then leaves those foreign keys out, without an error.

    Symptom: foreign keys are missing in SQLite after PostgreSQL or DuckDB tables were created in the same process.

### What is handled

oa-configurator's pytest plugin wraps `MetaData.create_all()` and `MetaData.drop_all()` and restores the constraints afterwards. A plain `pytest` can therefore run the tests of every dialect in one process. The plugin loads automatically when oa-configurator is installed.

### What is not handled

- Code that creates tables outside a test, such as an application bootstrap that touches several dialects in one process. Wrap the call in `oa_configurator.preserve_create_rules(metadata)`:

    ```python
    from oa_configurator import preserve_create_rules

    with preserve_create_rules(Base.metadata):
        Base.metadata.create_all(engine)
    ```

- A repo or script that runs without the plugin.
- A SQLAlchemy release that changes the private attribute the fix restores. It was tested with SQLAlchemy 2.0.50, and a test in oa-configurator fails when the behaviour changes.

### In CI

Run each dialect in its own job, with one routing mark per job. Do not combine dialect marks in one `markers` expression such as `sqlite or postgresql`. Each job then only needs the infrastructure of its own dialect, and no process creates tables for more than one dialect.
