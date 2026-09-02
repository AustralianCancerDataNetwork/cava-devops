# build-test-postgres.yml

Identical to [`build-test.yml`](build-test.md) but includes a Postgres service container. Use this for repos whose test suite requires a running database. Supports both plain Postgres and pgvector via the `postgres-image` input.

## Required status check name

```
build-test / test
```

As with `build-test.yml`, the prefix is the calling job name.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `ruff` | boolean | `true` | Whether to run `ruff check .` |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |
| `postgres-image` | string | `postgres:16` | Docker image for the Postgres service |
| `postgres-db` | string | `test` | Database name to create |
| `postgres-user` | string | `test` | Postgres user |
| `postgres-password` | string | `test` | Postgres password |

## Usage

Standard Postgres:

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres.yml@main
    with:
      postgres-db: my_test_db
```

With pgvector:

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres.yml@main
    with:
      postgres-image: pgvector/pgvector:pg16
      postgres-user: postgres
      postgres-password: postgres
      postgres-db: postgres
```

## Pre-test setup commands

Use `setup-commands` to write config or run any setup that must happen after the container is up but before tests run. Pass commands inline as a YAML block scalar:

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres.yml@main
    with:
      postgres-db: test_db
      setup-commands: |
        uv run omop-config configure my_package \
          --test-dialect postgresql+psycopg \
          --test-host localhost \
          --test-port 5432 \
          --test-user test \
          --test-password test \
          --test-database-name test_db
```

The commands run after `uv sync` and before lint and tests.

## Repos with two test suites

If a repo runs both SQLite and Postgres test suites, use both workflows with distinct job names:

```yaml
jobs:
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main

  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres.yml@main
    with:
      postgres-db: test_db
```

The required status check names become `build-test-sqlite / test` and `build-test-postgres / test`. Add both to the branch protection ruleset.
