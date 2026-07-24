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

## 4. Dependency ranges on sibling packages (if applicable)

Skip this step if the repo has no dependency on another CAVA package (e.g. `oa-configurator`, which is a base/leaf package with no siblings of its own).

If this repo depends on one or more CAVA sibling packages, prefer a semver range over an exact pin once the sibling has itself migrated to this centralised CI/CD (its releases are label-gated, so MAJOR only happens on a `breaking`-labelled PR):

```toml
dependencies = [
    "oa-configurator>=0.1.2,<1.0.0",  # not =="0.1.2"
]
```

CI installs with plain `uv sync`, which prefers what's already committed in `uv.lock` but will fail loudly if it no longer satisfies `pyproject.toml`, see [Keeping `uv.lock` in sync](#keeping-uvlock-in-sync) below for how that stays consistent with `pyproject.toml`. Enable **Dependabot security updates** in the repo's settings (Advanced Security) for CVE coverage; no `dependabot.yml` file is needed for that.

---

## 5. Keeping `uv.lock` in sync

`ci.yml` installs with plain `uv sync`. It prefers whatever's already committed in `uv.lock` (so a dependency that's still valid never gets bumped just because something newer shipped upstream), but it re-resolves and fails loudly the moment the lock can no longer satisfy `pyproject.toml`. Confirmed directly against `--frozen` (which blindly trusts the lock with no validation at all, silently passing even when the two have diverged) and `--locked`/`--check` (which fails on any staleness at all, not just genuine inconsistency) before settling on plain `uv sync` as the one mode that does both correctly. That makes it important that `uv.lock` actually reflects `pyproject.toml`, without relying on someone remembering to run `uv lock` after every dependency edit.

Install the canonical pre-commit hook:

```bash
mkdir -p .githooks
cp <path-to-cava-devops>/templates/githooks/pre-commit .githooks/pre-commit
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

`git config core.hooksPath` is a one-time, per-clone setting (not committed), so each contributor needs to run it once after cloning.

What it does: when `pyproject.toml` is part of a commit, the hook diffs it to find exactly which dependency line(s) changed, then runs `uv lock --upgrade-package <name>` for just those -- not a blanket `uv lock`. This touches only the package(s) you actually edited (plus whatever *that* package's new version transitively requires), never an unrelated dependency that merely happens to have a newer release available. Confirmed directly: `uv lock --upgrade-package certifi` moved only `certifi`, leaving every other locked package untouched.

This runs locally, before the commit is created. By the time a PR is opened, `uv.lock` is already correct, and CI's `uv sync` install just confirms it.

---

## 6. Delete old files

Remove these files if present in the repo:

| File | What it was |
|---|---|
| `release.yml` | Monolithic release workflow (semantic-release or similar) |
| `lint-pr.yml` | PR title lint check (`amannn/action-semantic-pull-request`) |
| `.releaserc.json` | semantic-release configuration |
| `python-publish.yml` | Previous PyPI publish workflow |
| `tests.yml` | Previous standalone test workflow |

---

## 7. GitHub configuration

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

## 8. First release after cutover

Merge all migration changes via a PR labelled `chore`. `merge.yml` triggers and release-drafter creates a draft. What to do next depends on whether the repo has existing tags.

=== "Existing tags"

    The draft body will be empty (chore is excluded from the changelog) and the suggested version will be the next patch after the last existing tag (e.g. `v1.2.4` if the last tag was `v1.2.3`).

    Leave the draft unpublished. The next real `feature` or `fix` PR will update the same draft with a proper changelog entry. Publish when you are ready to ship that change.

=== "No existing tags"

    The draft will suggest an arbitrary version since there is no base tag to work from.

    Before publishing, confirm the package name is available on PyPI and the trusted publisher entry is in place.

    Go to the Releases page, open the draft, and change the "Tag version" field to the correct initial version (e.g. `v0.1.0`). Confirm the target branch is `main`. Click **Publish release** to create the tag, which triggers `publish.yml` and uploads the first release to PyPI.
