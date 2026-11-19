# build-test-sqlite-v2.yml

Runs only the SQLite-marked test suite (`pytest -q -m sqlite` by default). SQLite is embedded, so the job needs no service container. Replaces [`build-test-sqlite.yml`](build-test-sqlite.md), which ran the whole default suite.

Pair it with [`build-test-nodb.yml`](build-test-nodb.md), which runs the tests that carry no routing mark, or those tests never run. Add the other dialect workflows for the routing marks the repo uses.

Pass `markers` for a repo whose SQLite tests carry a different mark, for example `sqlitevec` or `faiss` in omop-emb.

!!! tip "Use workflow only where needed"
    A run that collects no tests fails. Do not call this workflow in a repo that has no tests for `markers`.

## Required status check name

```
build-test-sqlite / test
```

The check name is `{calling-job-name} / test`. Keep the calling job name `build-test-sqlite`, so the required check of existing repos does not change.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |
| `markers` | string | `sqlite` | `pytest -m` expression selecting the SQLite tests |

## Usage

```yaml
jobs:
  build-test-nodb:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-nodb.yml@main
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite-v2.yml@main
```

With a different marker:

```yaml
jobs:
  build-test-faiss:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-sqlite-v2.yml@main
    with:
      markers: faiss
```

See [Testing conventions](../guides/testing-conventions.md) for how tests choose their routing marks.
