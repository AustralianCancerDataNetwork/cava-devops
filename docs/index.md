# cava-devops

Centralised CI/CD infrastructure for the [AustralianCancerDataNetwork](https://github.com/AustralianCancerDataNetwork) Python packages. All reusable workflows live here; each package repo contains thin wrapper files that call them.

## What this repo provides

| Component | Location | Purpose |
|---|---|---|
| Reusable workflows | `.github/workflows/` | Label gate, build/test, publish, release drafting |
| Label configuration | `scripts/labels.yml` | Canonical label set with colours and descriptions |
| Label bootstrap script | `scripts/bootstrap-labels.sh` | One-command label setup via `gh` CLI |
| Issue and PR templates | `templates/` | Synced to each package repo |
| Release-drafter config template | `templates/release-drafter.yml` | Canonical changelog config |

## Design principles

- **No commit-back.** Versions are derived from git tags at build time ([`hatch-vcs`](https://github.com/ofek/hatch-vcs)). Nothing writes to `main` outside of reviewed PRs.
- **Label-driven releases.** A PR cannot merge without exactly one bump label. The label determines both the changelog category and the version bump.
- **Centralised, not duplicated.** A change to a reusable workflow here propagates to all callers on their next workflow run. No manual syncing of CI logic across 6 repos.

## Quick links

- [Labels reference](labels.md): colours, descriptions, and bump types
- [Day-to-day PR workflow](guides/pr-workflow.md): from opening an issue to publishing a release
- [Onboard a new repo](guides/setup-new-repo.md): complete setup checklist
- [Workflow reference](workflows/index.md): inputs and usage for every reusable workflow
