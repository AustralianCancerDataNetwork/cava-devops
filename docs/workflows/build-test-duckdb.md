# build-test-duckdb.yml

Needs no service container (DuckDB is embedded) and runs **only** the DuckDB-marked test suite (`pytest -q -m "duckdb"` by default). Pass `markers` for a repo whose DuckDB-specific tests carry a different marker name (e.g. `duckdbvss`).

**Always pair this with [`build-test-nodb.yml`](build-test-nodb.md)** in a separate job, which runs the tests that carry no routing mark. This workflow runs only the tests selected by `markers`. One job per routing mark.

It does not lint or type check. Run [`ruff.yml`](ruff.md) and [`ty.yml`](ty.md) as their own jobs. The old `ruff` and `ty-src` inputs no longer exist, so a caller that still passes them fails.

!!! tip "Use workflow only where needed"
    A run that collects no tests fails. Do not call this workflow in a repo that has no tests for `markers`.

## Required status check name

```
build-test-duckdb / test
```

The check name is `{calling-job-name} / test`.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |
| `markers` | string | `duckdb` | `pytest -m` marker expression selecting the DuckDB-only tests |

## Usage

The snippet below shows this workflow's own job. Every usage also needs a paired `build-test-nodb.yml` job.

```yaml
jobs:
  build-test-duckdb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-duckdb.yml@main
```

With a different marker name:

```yaml
jobs:
  build-test-duckdb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-duckdb.yml@main
    with:
      markers: duckdbvss
```

## Pairing with build-test-nodb.yml

Use distinct job names so each status check is visible:

```yaml
jobs:
  build-test-nodb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-nodb.yml@main

  build-test-duckdb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-duckdb.yml@main

  ruff:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ruff.yml@main

  ty:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ty.yml@main
```

The required status check names become `build-test-nodb / test` and `build-test-duckdb / test`.

See [Testing conventions](../guides/testing-conventions.md) for how tests choose their routing marks.
