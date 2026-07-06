# publish.yml

Verifies that the triggering tag is reachable from `origin/main`, builds the wheel and sdist with `uv build`, and uploads them as a workflow artifact named `dist`. It does **not** publish to PyPI directly.

## Why the publish step is not here

PyPI OIDC trusted publishing matches the `job_workflow_ref` claim in the OIDC token against the configured trusted publisher. When `pypa/gh-action-pypi-publish` runs inside a reusable workflow in a different repository (`cava-devops`), the `job_workflow_ref` points to `cava-devops`, not the package repo. This causes an `invalid-publisher` error.

The upload step must therefore live in the calling repo's `publish.yml` as an inline job, after downloading the `dist` artifact produced here.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `python-version` | string | `3.12` | Python version used to build the wheel |

## Usage

```yaml
# .github/workflows/publish.yml in each package repo
name: Publish
on:
  push:
    tags: ['v*']

jobs:
  build:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/publish.yml@main

  publish:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    environment:
      name: pypi
      url: https://pypi.org/p/<package-name>
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
```

!!! success
    Replace `<package-name>` with the PyPI slug.


## Tag verification

The `Verify tag is on main` step fails if the tag was created on a branch that has not been merged. This prevents publishing code that bypassed review.
