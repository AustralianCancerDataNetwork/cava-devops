# Contributing

## Development setup

```bash
uv sync --all-extras --dev
uv run pytest -q
uv run ruff check .
```

## Opening a pull request

1. Apply **exactly one** bump label before merging:

   | Label | When to use |
   |---|---|
   | `major` / `breaking` | Public API change, backward-incompatible |
   | `minor` / `feature` | New functionality, backward-compatible |
   | `patch` / `fix` | Bug fix |
   | `chore` / `dependencies` | Housekeeping, dependency updates |
   | `skip-changelog` | Typo fix, docs-only — not worth a changelog entry |

2. When merging (squash), write a clear extended description in the merge dialog. That text — not the PR's opening description — becomes the changelog entry for this change.

## Versioning and releases

Versions are derived from git tags; there is no version string in any source file. Releases are triggered by a maintainer publishing the standing draft release on the repository's Releases page. There is no automated commit-back to `main`.
