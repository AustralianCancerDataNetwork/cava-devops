# manual-release.yml

Emergency escape hatch. Creates a git tag and GitHub release directly from `main` via `workflow_dispatch`, bypassing the normal draft-publish flow.

## When to use

- The normal publish path is broken (e.g. `publish.yml` is failing and you need to ship a hotfix).
- You need to backfill a tag for a version that was never properly tagged.

Do **not** use this for routine releases. The standard flow is: merge PRs with labels, publish the draft release from the Releases page.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `version` | string | yes | Version in `X.Y.Z` format (no `v` prefix) |
| `title` | string | no | Release title (defaults to `vX.Y.Z`) |
| `body` | string | no | Release body text |

## Usage

Trigger from the Actions tab in the package repo (not in cava-devops). The workflow runs against `main` HEAD.

```yaml
# .github/workflows/manual-release.yml in each package repo
jobs:
  release:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/manual-release.yml@main
    secrets: inherit
```
