# Workflow reference

All workflows are called via `uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/<name>.yml@main`.

| Workflow | Trigger context | Purpose |
|---|---|---|
| [`label-gate.yml`](label-gate.md) | PR open/update | Blocks merge until exactly one bump label is present |
| [`build-test.yml`](build-test.md) | PR open/update | Superseded by `build-test-sqlite.yml`, `ruff.yml` and `ty.yml`. Installs, lints, and runs the test suite |
| [`build-test-postgres.yml`](build-test-postgres.md) | PR open/update | Superseded by `build-test-postgres-v3.yml`. Full test suite with a Postgres service container |
| [`build-test-postgres-v2.yml`](build-test-postgres-v2.md) | PR open/update | Superseded by `build-test-postgres-v3.yml`. `postgresql`-marked suite with a Postgres service container; pair with `build-test.yml` |
| [`build-test-duckdb.yml`](build-test-duckdb.md) | PR open/update | `duckdb`-marked suite, no service container needed; no lint; pair with `build-test-sqlite.yml` |
| [`ruff.yml`](ruff.md) | PR open/update | `ruff check` and `ruff format --check` with the version locked in `uv.lock` |
| [`ty.yml`](ty.md) | PR open/update | `ty check` with the version locked in `uv.lock` |
| [`build-test-sqlite.yml`](build-test-sqlite.md) | PR open/update | Default (SQLite) suite without ruff and ty; replaces `build-test.yml`; pair with `ruff.yml` and `ty.yml` |
| [`build-test-postgres-v3.yml`](build-test-postgres-v3.md) | PR open/update | `build-test-postgres-v2.yml` without ruff and ty; pair with `build-test-sqlite.yml` |
| [`lint-imports.yml`](lint-imports.md) | PR open/update | Checks repository-owned import contracts |
| [`release-drafter.yml`](release-drafter.md) | PR merged | Updates the standing draft release with the merged PR |
| [`publish.yml`](publish.md) | Tag push | Verifies tag is on main, builds wheel and sdist, uploads as artifact |
| [`deploy-docs.yml`](deploy-docs.md) | Tag push / `workflow_dispatch` | Installs `dev` extra and deploys MkDocs to GitHub Pages |
| [`manual-release.yml`](manual-release.md) | `workflow_dispatch` | Emergency: creates a tag and release directly from main |
