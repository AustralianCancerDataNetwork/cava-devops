# build-test-nodb.yml

Runs every test that carries none of the routing marks (`pytest -q -m "not (sqlite or duckdb or postgresql)"` by default). An unmarked test needs no database, so the job needs no service container.

Pair it with the dialect workflows for the routing marks the repo uses: [`build-test-sqlite-v2.yml`](build-test-sqlite-v2.md), [`build-test-duckdb.yml`](build-test-duckdb.md) and [`build-test-postgres-v3.yml`](build-test-postgres-v3.md). A repo whose routing marks are not the dialect names (for example omop-emb's backend marks) passes them in `exclude-markers`.

!!! tip "Use workflow only where needed"
    A run that collects no tests fails. Do not call this workflow in a repo that has no tests for `markers`.

## Required status check name

```
build-test-nodb / test
```

The check name is `{calling-job-name} / test`. Name the calling job `build-test-nodb` to get the name above.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |
| `exclude-markers` | string | `sqlite or duckdb or postgresql` | `pytest -m` expression naming the routing marks to exclude |

## Usage

```yaml
jobs:
  build-test-nodb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-nodb.yml@main
```

With custom routing marks:

```yaml
jobs:
  build-test-nodb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-nodb.yml@main
    with:
      exclude-markers: sqlitevec or pgvector or duckdbvss or faiss
```

See [Testing conventions](../guides/testing-conventions.md) for how tests choose their routing marks.
