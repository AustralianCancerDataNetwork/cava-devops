# Setup a new repo

Complete checklist for migrating a package repo to the cava-devops CI/CD system.

---

## 1. pyproject.toml

Switch to `hatch-vcs` for dynamic versioning. Remove the static `version = "X.Y.Z"` line.

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"
raw-options = { tag_regex = '^v?(?P<version>[0-9]+\.[0-9]+\.[0-9]+)$' }

[project]
dynamic = ["version"]
# remove: version = "X.Y.Z"

[tool.uv]
cache-keys = [{ file = "pyproject.toml" }, { git = { commit = true, tags = true } }]
```

The `v?` in `tag_regex` accepts both `v1.2.3` and bare `1.2.3` tags, preserving compatibility with repos that have existing bare tags.

!!! note "uv_build backend"
    If the repo currently uses `uv_build` as its build backend, change both `requires` and `build-backend` to the hatchling values above.

---

## 2. Add workflow files

### ci.yml

For repos **without** a Postgres service:

```yaml
name: CI
on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened, labeled, unlabeled]
jobs:
  label-gate:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/label-gate.yml@main
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main
```

For repos **with** a Postgres service:

```yaml
jobs:
  label-gate:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/label-gate.yml@main
  build-test:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres.yml@main
    with:
      postgres-db: <db-name>         # repo-specific
      # postgres-image: pgvector/pgvector:pg16   # pgvector repos only
```

For repos with **two test suites** (e.g. SQLite + Postgres):

```yaml
jobs:
  label-gate:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/label-gate.yml@main
  build-test-sqlite:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test.yml@main
  build-test-postgres:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/build-test-postgres.yml@main
    with:
      postgres-db: test_db
```

### merge.yml

```yaml
name: Release Update
on:
  pull_request:
    types: [closed]
    branches: [main]
jobs:
  draft:
    if: github.event.pull_request.merged == true
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/release-drafter.yml@main
    secrets: inherit
```

### publish.yml

```yaml
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
        with: { name: dist, path: dist/ }
      - uses: pypa/gh-action-pypi-publish@release/v1
```
!!! success
    Replace `<package-name>` with the PyPI slug.

### docs.yml

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

All MkDocs plugins must be declared in the `dev` extra of `pyproject.toml`.
The reusable workflow installs them via `uv sync --extra dev` and deploys with
`uv run mkdocs gh-deploy --force`. See [deploy-docs.yml](../workflows/deploy-docs.md)
for details.

---

## 3. Add release-drafter config

Copy `templates/release-drafter.yml` from this repo to `.github/release-drafter.yml` in the package repo.

---

## 4. Delete old files

Remove these files if present in the repo:

| File | What it was |
|---|---|
| `release.yml` | Monolithic release workflow (semantic-release or similar) |
| `lint-pr.yml` | PR title lint check (`amannn/action-semantic-pull-request`) |
| `.releaserc.json` | semantic-release configuration |
| `python-publish.yml` | Previous PyPI publish workflow |
| `tests.yml` | Previous standalone test workflow |

---

## 5. GitHub configuration

### Merge settings

In Settings > General > Pull Requests:

Setting | Value
---|---
Allow merge commits | disabled
Allow squash merging | enabled
Default commit message | **Pull request title**
Allow rebase merging | disabled

"Pull request title" sets the squash commit message to the PR title only, which is all the changelog reads. The other options pre-fill with commit messages or the PR description and produce noisy commit messages.

### Branch protection ruleset on main

Setting | Value
---|---
Target | `main`
Require pull request | 1 approval
Required status checks | See below
Require linear history | enabled
Block force pushes | enabled
Allow bypass | Repository admin (for initial setup only)

**Required status checks by CI variant:**

| ci.yml variant | Required status checks |
|---|---|
| Standard (`build-test.yml`) | `label-gate / check`, `build-test / test` |
| Postgres (`build-test-postgres.yml`) | `label-gate / check`, `build-test / test` |
| Two suites (sqlite + postgres) | `label-gate / check`, `build-test-sqlite / test`, `build-test-postgres / test` |

The check name prefix is the calling job name in `ci.yml`.

### GitHub environment

Create an environment named `pypi` in the repo settings (Settings > Environments). No protection rules are required unless you want manual approval before every release.

### PyPI trusted publisher

Add a pending trusted publisher on [pypi.org](https://pypi.org/manage/account/publishing/):

| Field | Value |
|---|---|
| Owner | `AustralianCancerDataNetwork` |
| Repository name | exact GitHub repo name (e.g. `my-repo`) |
| Workflow filename | `publish.yml` |
| Environment name | `pypi` |

If the repo already has a trusted publisher from an old workflow (e.g. `python-publish.yml`), add a new one for `publish.yml` rather than editing the existing entry. The old entry becomes inert when the old workflow is deleted.

### Labels

```bash
# From the cava-devops repo root:
scripts/bootstrap-labels.sh AustralianCancerDataNetwork/<repo-name>
```

This creates five labels: `breaking`, `feature`, `fix`, `dependencies` (bump labels) and `chore` (excluded from changelog, no version bump).

---

## 6. First release after cutover

Merge all migration changes via a PR labelled `chore`. `merge.yml` triggers and release-drafter creates a draft. What to do next depends on whether the repo has existing tags.

=== "Existing tags"

    The draft body will be empty (chore is excluded from the changelog) and the suggested version will be the next patch after the last existing tag (e.g. `v1.2.4` if the last tag was `v1.2.3`).

    Leave the draft unpublished. The next real `feature` or `fix` PR will update the same draft with a proper changelog entry. Publish when you are ready to ship that change.

=== "No existing tags"

    The draft will suggest an arbitrary version since there is no base tag to work from.

    Before publishing, confirm the package name is available on PyPI and the trusted publisher entry is in place.

    Go to the Releases page, open the draft, and change the "Tag version" field to the correct initial version (e.g. `v0.1.0`). Confirm the target branch is `main`. Click **Publish release** to create the tag, which triggers `publish.yml` and uploads the first release to PyPI.
