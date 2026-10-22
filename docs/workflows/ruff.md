# ruff.yml

Runs `ruff check .` and `ruff format --check .` with the exact ruff version locked in the caller's `uv.lock`. It reads the version with `uv export` and runs it through `uvx`, so it does not install the project or its dependencies. ruff must be in the repo's `dev` extra, otherwise the job fails with a message saying so.

Pair with [`ty.yml`](ty.md) and the lint-free test workflows ([`build-test-sqlite.yml`](build-test-sqlite.md), [`build-test-postgres-v3.yml`](build-test-postgres-v3.md), [`build-test-duckdb.yml`](build-test-duckdb.md)).

## Required status check name

```
ruff / check
```

The check name is `{calling-job-name} / check`.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |

## Usage

```yaml
jobs:
  ruff:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ruff.yml@main
```

## Updating ruff

Bump the exact pin in `pyproject.toml`, run `uv lock`, and fix what the new version reports. The workflow picks up the new version from the lockfile.
