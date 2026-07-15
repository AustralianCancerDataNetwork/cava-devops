# deploy-docs.yml

Reusable workflow that deploys MkDocs to GitHub Pages. Installs the caller's
`dev` optional-dependency group via `uv sync --extra dev`, then runs
`uv run mkdocs gh-deploy --force`. All MkDocs plugins must be declared in the
`dev` extra of the caller's `pyproject.toml`.

## Usage

```yaml
name: Deploy Docs
on:
  push:
    tags: ['v*']
  workflow_dispatch:
permissions:
  contents: write
jobs:
  deploy:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/deploy-docs.yml@main
```

`permissions: contents: write` must be at the workflow level, not the job level,
because permissions cannot be set on a job that calls a reusable workflow.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version |

## Extending

The workflow is all-or-nothing: every step runs as defined. There are no
customisation slots. If a repo needs extra build steps (e.g. code generation
before the docs build), add them as steps in a separate job that runs before the
`deploy` job and produces any generated files as an artifact, or use a
`workflow_dispatch` pre-step in the caller.

For step-level customisation, see [Extending workflows](../guides/extending-workflows.md).
