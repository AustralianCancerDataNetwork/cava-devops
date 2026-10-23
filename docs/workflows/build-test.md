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
| `sibling-repos` | string | `''` | Newline-separated private repository names to check out as siblings before `uv sync` |

## Secrets

| Secret | Required | Description |
|---|---|---|
| `token` | only if `sibling-repos` is set | Fine-grained PAT with Contents:read on the sibling repositories |

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

With a private sibling dependency:

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main
    with:
      sibling-repos: |
        ohdsi-prompt-registry
    secrets:
      token: ${{ secrets.CAVA_DEVOPS_TOKEN }}
```

The sibling is checked out with full history at `../ohdsi-prompt-registry`, so
an editable `[tool.uv.sources]` path dependency resolves before `uv sync` and
`hatch-vcs` can determine its version.
