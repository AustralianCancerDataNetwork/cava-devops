# build-test-duckdb.yml

Needs no service container (DuckDB is embedded) and runs **only** the DuckDB-marked test suite (`pytest -q -m "duckdb"` by default). Pass `markers` for a repo whose DuckDB-specific tests carry a different marker name (e.g. `duckdbvss`).

**Always pair this with [`build-test-sqlite.yml`](build-test-sqlite.md)** in a separate job. A repo's own `addopts` typically excludes `db_dialect`-marked tests from a plain `pytest -q` run by default; this workflow is what actually exercises those excluded tests. It deliberately does not also run the plain suite itself: that's `build-test-sqlite.yml`'s job. One job per dialect axis, matching oa-configurator's per-dialect marker design (and [`build-test-postgres-v3.yml`](build-test-postgres-v3.md)'s).

It does not lint or type check. Run [`ruff.yml`](ruff.md) and [`ty.yml`](ty.md) as their own jobs. The old `ruff` and `ty-src` inputs no longer exist, so a caller that still passes them fails.

A repo with no tests matching `markers` does not fail on this: pytest's exit code 5 ("no tests collected") is treated as a pass for this step. Any other nonzero exit still fails the job.

## Required status check name

```
build-test / test
```

The prefix is the calling job name.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |
| `markers` | string | `duckdb` | `pytest -m` marker expression selecting the DuckDB-only tests |

## Usage

The snippet below shows this workflow's own job. Every usage also needs a paired `build-test-sqlite.yml` job for the default suite.

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

## Pairing with build-test-sqlite.yml

Use distinct job names so both status checks are visible:

```yaml
jobs:
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite.yml@main

  build-test-duckdb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-duckdb.yml@main

  ruff:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ruff.yml@main

  ty:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/ty.yml@main
```

The required status check names become `build-test-sqlite / test` and `build-test-duckdb / test`.
