# Workflow reference

All workflows are called via `uses: AustralianCancerDataNetwork/cava-devops/.github/workflows/<name>.yml@main`.

Status `✅ Current` marks the workflows to use. `⛔ Superseded` workflows keep working unchanged for existing callers, but new repos should use the workflow in the "Use instead" column.

| Status | Workflow | Use instead | Trigger context | Purpose |
|---|---|---|---|---|
| ✅ Current | [`label-gate.yml`](label-gate.md) | | PR open/update | Blocks merge until exactly one bump label is present |
| ✅ Current | [`ruff.yml`](ruff.md) | | PR open/update | `ruff check` and `ruff format --check` with the version locked in `uv.lock` |
| ✅ Current | [`ty.yml`](ty.md) | | PR open/update | `ty check` with the version locked in `uv.lock` |
| ✅ Current | [`build-test-nodb.yml`](build-test-nodb.md) | | PR open/update | Tests without a routing mark, no database needed; pair with the dialect workflows |
| ✅ Current | [`build-test-sqlite-v2.yml`](build-test-sqlite-v2.md) | | PR open/update | `sqlite`-marked suite (or `markers`), no service container needed; pair with `build-test-nodb.yml` |
| ✅ Current | [`build-test-duckdb.yml`](build-test-duckdb.md) | | PR open/update | `duckdb`-marked suite (or `markers`), no service container needed; pair with `build-test-nodb.yml` |
| ✅ Current | [`build-test-postgres-v3.yml`](build-test-postgres-v3.md) | | PR open/update | `postgresql`-marked suite (or `markers`) with a Postgres service container; pair with `build-test-nodb.yml` |
| ✅ Current | [`lint-imports.yml`](lint-imports.md) | | PR open/update | Checks repository-owned import contracts |
| ✅ Current | [`release-drafter.yml`](release-drafter.md) | | PR merged | Updates the standing draft release with the merged PR |
| ✅ Current | [`publish.yml`](publish.md) | | Tag push | Verifies tag is on main, builds wheel and sdist, uploads as artifact |
| ✅ Current | [`deploy-docs.yml`](deploy-docs.md) | | Tag push / `workflow_dispatch` | Installs `dev` extra and deploys MkDocs to GitHub Pages |
| ✅ Current | [`manual-release.yml`](manual-release.md) | | `workflow_dispatch` | Emergency: creates a tag and release directly from main |
| ⛔ Superseded | [`build-test-sqlite.yml`](build-test-sqlite.md) | `build-test-sqlite-v2.yml` and `build-test-nodb.yml` | PR open/update | Default suite without ruff and ty |
| ⛔ Superseded | [`build-test-postgres-v2.yml`](build-test-postgres-v2.md) | `build-test-postgres-v3.yml` | PR open/update | `postgresql`-marked suite with a Postgres service container, with ruff and ty; pair with `build-test.yml` |
| ⛔ Superseded | [`build-test-postgres.yml`](build-test-postgres.md) | `build-test-postgres-v3.yml` and `build-test-nodb.yml` | PR open/update | Full test suite with a Postgres service container |
| ⛔ Superseded | [`build-test.yml`](build-test.md) | `build-test-nodb.yml`, the dialect workflows, `ruff.yml` and `ty.yml` | PR open/update | Installs, lints, and runs the test suite |
