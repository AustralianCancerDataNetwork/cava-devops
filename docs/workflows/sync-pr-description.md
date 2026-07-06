# sync-pr-description.yml

After a PR is merged, rewrites the PR's description field with the body of the squash-merge commit. This makes the merge-time summary (typed in the squash-merge dialog) available to `release-drafter` as `$BODY`.

## Why this exists

`release-drafter` reads `$BODY` from the PR's description field as stored on the PR object. That field is set when the PR is opened and does not automatically update when the PR is merged. The squash-merge dialog's "extended description" box writes into the commit message on `main`, not back into the PR description.

This workflow bridges the gap: it reads the squash commit body via the API and patches the PR description, so `$BODY` in the changelog reflects what was actually written at merge time rather than whatever the PR said when it was opened.

## Usage

Called from `merge.yml`, before `release-drafter.yml`. Must run on `pull_request: types: [closed]` with `if: github.event.pull_request.merged == true`.

```yaml
jobs:
  sync-description:
    if: github.event.pull_request.merged == true
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/sync-pr-description.yml@main
```

## No inputs

This workflow reads everything it needs from the event payload (`merge_commit_sha`, `pull_request.number`).
