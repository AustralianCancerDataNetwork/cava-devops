# Workflow reference

All workflows are called via `uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/<name>.yml@main`.

| Workflow | Trigger context | Purpose |
|---|---|---|
| [`label-gate.yml`](label-gate.md) | PR open/update | Blocks merge until exactly one bump label is present |
| [`build-test.yml`](build-test.md) | PR open/update | Installs, lints, and runs the test suite |
| [`build-test-postgres.yml`](build-test-postgres.md) | PR open/update | Same as `build-test`, with a Postgres service container |
| [`sync-pr-description.yml`](sync-pr-description.md) | PR merged | Rewrites the PR description from the squash-merge commit body |
| [`release-drafter.yml`](release-drafter.md) | PR merged | Updates the standing draft release with the merged PR |
| [`publish.yml`](publish.md) | Tag push | Verifies tag is on main, builds wheel and sdist, uploads as artifact |
| [`manual-release.yml`](manual-release.md) | `workflow_dispatch` | Emergency: creates a tag and release directly from main |
