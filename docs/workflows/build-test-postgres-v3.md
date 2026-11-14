# build-test-postgres-v3.yml

[`build-test-postgres-v2.yml`](build-test-postgres-v2.md) without the ruff and ty steps. Runs only the `postgresql`-marked test suite against a live Postgres service container. Linting and type checking run as their own jobs through [`ruff.yml`](ruff.md) and [`ty.yml`](ty.md).

**Always pair this with [`build-test-sqlite.yml`](build-test-sqlite.md)** in a separate job, or the dialect-agnostic default suite never runs.

The `ruff` and `ty-src` inputs no longer exist. A caller that still passes them fails, which is intended: move them to the `ruff` and `ty` jobs.

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

## Usage

```yaml
jobs:
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite.yml@main
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
