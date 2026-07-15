# Extending workflows

## All-or-nothing vs step-level

GitHub reusable workflows (`on: workflow_call`) are all-or-nothing: when a repo
calls `uses: cava-devops/.../build-test.yml@main`, the entire job runs as
defined in cava-devops. There is no way to add, remove, or modify individual
steps from the caller side.

**Composite actions** are the step-level equivalent. A composite action is a
directory with an `action.yml` that defines a sequence of steps. A workflow can
`uses:` a composite action inside a step, which lets callers mix reusable steps
with their own. The trade-off: composite actions cannot host service containers
(Postgres, Redis), so they cannot replace `build-test-postgres.yml`.

## Baked-in slots

Where repos need to inject behaviour into a fixed workflow, cava-devops provides
`inputs` that act as customisation slots. The caller passes values; the
workflow interpolates them at defined points.

### `setup-commands` (build-test-postgres.yml)

The most common slot. Accepts a YAML block scalar of shell commands run after
`uv sync` and before lint and tests. Use it to write config files, seed data,
or do any setup that requires the Postgres container to already be up.

```yaml
jobs:
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres.yml@main
    with:
      postgres-db: my_db
      setup-commands: |
        uv run my-tool configure my_package \
          --test-host localhost \
          --test-port 5432 \
          --test-user test \
          --test-password test \
          --test-database-name my_db
```

Commands run in the same runner environment as the rest of the workflow, so
`uv run` uses the already-installed virtualenv.

## When to add a new slot

Add an input when a single point in a fixed workflow needs to vary per-repo and
the variation can be expressed as a string (a command, a flag, a version). Do
not add inputs to cover every possible difference; the default should work for
most repos.

If a repo's requirements diverge enough that a slot does not fit, copy the
relevant workflow into the repo and maintain it locally. That is the correct
escape hatch, not an ever-growing input list.

## Why publish stays inline

`deploy-docs.yml` and `publish.yml` show the two sides of this boundary:

- **`deploy-docs.yml`** is fully centralisable because the OIDC token's
  `job_workflow_ref` claim is not relevant to GitHub Pages.
- **`publish.yml`** (the PyPI upload step) must stay inline in each repo because
  PyPI's trusted publisher checks `job_workflow_ref`. When a step runs inside a
  reusable workflow, `job_workflow_ref` points to the reusable workflow's path
  in cava-devops, not the calling repo. PyPI's trusted publisher entry is
  registered against the calling repo's `publish.yml`, so moving the upload
  step to cava-devops would make the OIDC claim mismatch and reject the token.
