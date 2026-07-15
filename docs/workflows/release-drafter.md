# release-drafter.yml

Maintains a single standing draft release. Each time a PR is merged, it appends a changelog entry and recomputes the suggested next version from the highest-priority bump label across all included PRs.

## How it works

- Reads the PR's label to determine changelog category and version bump type.
- Reads the PR title, number, and author.
- If no draft release exists, creates one targeting `main`.
- If a draft already exists, updates it in place.
- The draft is never published automatically. A maintainer publishes it manually from the Releases page, which creates the git tag and triggers `publish.yml`.

## Configuration

Each repo must have a `.github/release-drafter.yml` file. Copy from `templates/release-drafter.yml` in this repo.

The `commitish: main` field is required. Without it, release-drafter may attempt to target a PR merge ref when creating the first draft after a release, which GitHub rejects.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `config-name` | string | `release-drafter.yml` | Config filename relative to `.github/` in the calling repo |

## Usage

Called from `merge.yml`:

```yaml
jobs:
  draft:
    if: github.event.pull_request.merged == true
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/release-drafter.yml@main
    secrets: inherit
```

`secrets: inherit` is required so the workflow receives `GITHUB_TOKEN` from the caller.
