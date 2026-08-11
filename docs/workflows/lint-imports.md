# lint-imports.yml

Installs the calling repository's development dependencies and checks its import
contracts. The contract configuration remains in the package repository because package
boundaries are part of that repository's architecture.

## Required status check name

```text
lint-imports / lint-imports
```

The first segment is the calling job name. A differently named calling job changes that
segment.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |
| `config-path` | string | `.importlinter` | Path to the calling repository's import-linter configuration |

## Usage

The calling repository must include `import-linter` in an installed dependency group or
extra.

```yaml
jobs:
  lint-imports:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/lint-imports.yml@main
```
