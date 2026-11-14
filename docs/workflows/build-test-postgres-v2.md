# build-test-postgres-v2.yml

!!! warning "Superseded"
    Use [`build-test-postgres-v3.yml`](build-test-postgres-v3.md), which is identical without the ruff and ty steps. Pair it with [`build-test-sqlite.yml`](build-test-sqlite.md), [`ruff.yml`](ruff.md) and [`ty.yml`](ty.md). This workflow keeps working unchanged for existing callers.

Includes a Postgres service container and runs **only** the `postgresql`-marked test suite (`pytest -q -m postgresql`). Supports both plain Postgres and pgvector via the `postgres-image` input.

**Always pair this with [`build-test.yml`](build-test.md)** in a separate job. A repo's own `addopts` typically excludes `db_dialect`-marked tests from a plain `pytest -q` run by default — this workflow is what actually exercises those excluded tests. It deliberately does not also run the plain suite itself: that's `build-test.yml`'s job. One job per dialect axis, matching oa-configurator's per-dialect marker design.

A repo with no `postgresql`-marked tests does not fail on this: pytest's exit code 5 ("no tests collected") is treated as a pass for this step. Any other nonzero exit still fails the job.

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
| `ty-src` | string | `src/` | Path passed to `ty check` for type checking |

## Usage

The snippets below show this workflow's own job. Every usage also needs a paired `build-test.yml` job for the default suite.

Standard Postgres:

```yaml
jobs:
  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres-v2.yml@main
    with:
      postgres-db: my_test_db
```

With pgvector:

```yaml
jobs:
  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres-v2.yml@main
    with:
      postgres-image: pgvector/pgvector:pg16
      postgres-user: postgres
      postgres-password: postgres
      postgres-db: postgres
```

## Pre-test setup commands

Use `setup-commands` to write config or run setup after the container is up but before tests run:

```yaml
jobs:
  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres-v2.yml@main
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

## Pairing with build-test.yml

Use distinct job names so both status checks are visible:

```yaml
jobs:
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main

  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres-v2.yml@main
    with:
      postgres-db: test_db
```

The required status check names become `build-test-sqlite / test` and `build-test-postgres / test`.
