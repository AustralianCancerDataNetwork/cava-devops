# Workflow reference

All workflows are called via `uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/<name>.yml@main`.

| Workflow | Trigger context | Purpose |
|---|---|---|
| [`label-gate.yml`](label-gate.md) | PR open/update | Blocks merge until exactly one bump label is present |
| [`build-test.yml`](build-test.md) | PR open/update | Installs, lints, and runs the test suite |
| [`build-test-postgres.yml`](build-test-postgres.md) | PR open/update | Full test suite with a Postgres service container |
| [`build-test-postgres-v2.yml`](build-test-postgres-v2.md) | PR open/update | `postgresql`-marked suite with a Postgres service container; pair with `build-test.yml` |
| [`build-test-duckdb.yml`](build-test-duckdb.md) | PR open/update | `duckdb`-marked suite, no service container needed; pair with `build-test.yml` |
| [`lint-imports.yml`](lint-imports.md) | PR open/update | Checks repository-owned import contracts |
| [`release-drafter.yml`](release-drafter.md) | PR merged | Updates the standing draft release with the merged PR |
| [`publish.yml`](publish.md) | Tag push | Verifies tag is on main, builds wheel and sdist, uploads as artifact |
| [`deploy-docs.yml`](deploy-docs.md) | Tag push / `workflow_dispatch` | Installs `dev` extra and deploys MkDocs to GitHub Pages |
| [`manual-release.yml`](manual-release.md) | `workflow_dispatch` | Emergency: creates a tag and release directly from main |
