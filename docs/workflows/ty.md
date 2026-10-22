# ty.yml

Installs the full environment with `uv sync --locked --all-extras --dev` and runs `ty check` with the version locked in the caller's `uv.lock`. ty needs the project's dependencies to resolve imports, so unlike [`ruff.yml`](ruff.md) this installs everything. `--locked` fails the job if `uv.lock` is out of date.

Pair with [`ruff.yml`](ruff.md) and the lint-free test workflows ([`build-test-sqlite.yml`](build-test-sqlite.md), [`build-test-postgres-v3.yml`](build-test-postgres-v3.md), [`build-test-duckdb.yml`](build-test-duckdb.md)).

## Required status check name

```
ty / check
```

The check name is `{calling-job-name} / check`.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `ty-src` | string | `src/ tests/` | Space-separated paths passed to `ty check` |

## Usage

```yaml
jobs:
  ty:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ty.yml@main
```

By default both `src/` and `tests/` are checked, so test doubles and fakes stay consistent with the interfaces they replace. For a repo whose package is not under `src/`:

```yaml
jobs:
  ty:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ty.yml@main
    with:
      ty-src: my_package tests
```

## Updating ty

Bump the exact pin in `pyproject.toml`, run `uv lock`, and fix what the new version reports. The workflow picks up the new version from the lockfile.
