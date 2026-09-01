# build-test-postgres.yml

Includes a Postgres service container and runs **only** the `postgresql`-marked test suite (`pytest -q -m postgresql`). Supports both plain Postgres and pgvector via the `postgres-image` input.

**Always pair this with [`build-test.yml`](build-test.md)** in a separate job. A repo's own `addopts` typically excludes `db_dialect`-marked tests from a plain `pytest -q` run by default (so a Postgres-dependent test can't corrupt shared ORM metadata when it happens to share a process with a SQLite one) — this workflow is what actually exercises those excluded tests. It deliberately does not also run the plain suite itself: that's `build-test.yml`'s job, needs no database, and running it a second time here would just duplicate work `build-test.yml` already does. One job per dialect axis, matching oa-configurator's own `db_dialect`/per-dialect marker design — see [Pairing with build-test.yml](#pairing-with-build-testyml) below.

A repo with no `postgresql`-marked tests at all (not yet migrated, or using this workflow for an unrelated reason) doesn't fail on this: pytest's exit code 5 ("no tests collected") is treated as a pass for this specific step. Any other nonzero exit (a real test failure, a collection error) still fails the job as normal.

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

The snippets below show only this workflow's own job, to keep the input syntax readable — every real usage still needs a paired `build-test-sqlite` job alongside it (see [Pairing with build-test.yml](#pairing-with-build-testyml)).

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

## Pairing with build-test.yml

Every repo using this workflow needs `build-test.yml` alongside it as a separate job — not an optional pattern for repos that happen to have "two test suites," but the required shape, since this workflow no longer runs the default suite itself. Use distinct job names:

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
