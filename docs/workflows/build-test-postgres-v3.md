# build-test-postgres-v3.yml

[`build-test-postgres-v2.yml`](build-test-postgres-v2.md) without the ruff and ty steps. Runs only the `postgresql`-marked test suite against a live Postgres service container. Linting and type checking run as their own jobs through [`ruff.yml`](ruff.md) and [`ty.yml`](ty.md).

**Always pair this with [`build-test-nodb.yml`](build-test-nodb.md)** in a separate job, or the tests without a routing mark never run.

!!! tip "Use workflow only where needed"
    A run that collects no tests fails. Do not call this workflow in a repo that has no tests for `markers`.


## Required status check name

```
build-test-postgres / test
```

The check name is `{calling-job-name} / test`.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |
| `postgres-image` | string | `postgres:16` | Docker image for the Postgres service |
| `postgres-db` | string | `test` | Database name to create |
| `postgres-user` | string | `test` | Postgres user |
| `postgres-password` | string | `test` | Postgres password |
| `markers` | string | `postgresql` | `pytest -m` expression selecting the Postgres tests, e.g. `pgvector` |

## Usage

```yaml
jobs:
  build-test-nodb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-nodb.yml@main
  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres-v3.yml@main
    with:
      postgres-db: my_package_test
  ruff:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ruff.yml@main
  ty:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ty.yml@main
```

For repos that need pgvector, pass `postgres-image: pgvector/pgvector:pg16`.

See [Testing conventions](../guides/testing-conventions.md) for how tests choose their routing marks.
