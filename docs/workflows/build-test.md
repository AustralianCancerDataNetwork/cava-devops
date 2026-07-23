# build-test.yml

Checks out the repo, installs dependencies with `uv sync`, optionally runs `ruff`, then runs `pytest`. For repos that require a Postgres or pgvector service, use [`build-test-postgres.yml`](build-test-postgres.md) instead.

## Required status check name

```
build-test / test
```

The check name is `{calling-job-name} / test`. If you name the calling job differently, the check name changes accordingly.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `ruff` | boolean | `true` | Whether to run `ruff check .` |
| `setup-commands` | string | `''` | Shell commands to run before tests (YAML block scalar, no script file needed) |
| `ty-src` | string | `src/` | Path passed to `ty check` for type checking |
| `resolution` | string | `highest` | uv resolution strategy: `highest`, `lowest`, or `lowest-direct` |

## Usage

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main
```

With a custom Python version and inline setup commands:

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main
    with:
      python-version: '3.13'
      setup-commands: |
        uv run my-tool configure my_package \
          --test-host localhost \
          --test-port 5432
```

## Minimum-version testing

Add a second job with `resolution: lowest-direct` to verify that the floor of
every declared dependency range is actually sufficient, not just the latest
version normally resolved in CI:

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main

  build-test-lowest-direct:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main
    with:
      resolution: lowest-direct
```
