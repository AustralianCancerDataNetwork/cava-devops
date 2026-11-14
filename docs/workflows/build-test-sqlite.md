# build-test-sqlite.yml

Checks out the repo, installs dependencies with `uv sync`, then runs the default `pytest -q` suite, which needs no database service and runs against SQLite. Replaces [`build-test.yml`](build-test.md). Linting and type checking run as their own jobs through [`ruff.yml`](ruff.md) and [`ty.yml`](ty.md).

The `ruff` and `ty-src` inputs no longer exist. A caller that still passes them fails, which is intended: move them to the `ruff` and `ty` jobs.

For the dialect-specific suites, pair it with [`build-test-postgres-v3.yml`](build-test-postgres-v3.md) or [`build-test-duckdb.yml`](build-test-duckdb.md).

## Required status check name

```
build-test-sqlite / test
```

The check name is `{calling-job-name} / test`. Name the calling job `build-test-sqlite` to get the name above.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |

## Usage

```yaml
jobs:
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite.yml@main
  ruff:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ruff.yml@main
  ty:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ty.yml@main
```

With a custom Python version and inline setup commands:

```yaml
jobs:
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite.yml@main
    with:
      python-version: '3.13'
      setup-commands: |
        uv run my-tool configure my_package \
          --test-host localhost \
          --test-port 5432
```
