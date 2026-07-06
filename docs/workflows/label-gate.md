# label-gate.yml

Checks that a PR carries exactly one bump label before it can merge. This is the mechanism that replaces conventional-commit title parsing.

## Behaviour

- If the PR has zero bump labels: fails with a message listing the required labels.
- If the PR has two or more bump labels: fails asking the contributor to keep only one.
- If the PR has exactly one bump label: passes.
- If the PR has the <span style="background:#FEF2C0;color:#333;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">chore</span> label: passes unconditionally (changelog entry is skipped).

The check re-runs whenever a label is added or removed (`labeled`, `unlabeled` events), so a contributor can fix a missing label without pushing new commits.

## Required status check name

```
label-gate / check
```

Add this to the branch protection ruleset for `main`.

## Inputs

| Input | Type | Default | Description |
|---|---|---|---|
| `bump-labels` | string | <span style="background:#B60205;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">breaking</span>,<span style="background:#0E8A16;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">feature</span>,<span style="background:#0075CA;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">fix</span>,<span style="background:#6F42C1;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">dependencies</span> | Comma-separated list of labels that count as bump labels |
| `skip-labels` | string | <span style="background:#FEF2C0;color:#333;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">chore</span> | Comma-separated list of labels that bypass the gate |


## Usage

```yaml
jobs:
  label-gate:
    uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/label-gate.yml@main
```
