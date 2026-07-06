# Labels

Every package repo uses the same five labels. Apply them with `scripts/bootstrap-labels.sh`.

```bash
scripts/bootstrap-labels.sh AustralianCancerDataNetwork/<repo-name>
```

## Label reference

| Label | Colour | Description | Version bump |
|---|---|---|---|
| <span style="background:#B60205;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">breaking</span> | `#B60205` | Incompatible API change | **MAJOR** `x+1.y.z` |
| <span style="background:#0E8A16;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">feature</span> | `#0E8A16` | New backwards-compatible functionality | **MINOR** `x.y+1.z` |
| <span style="background:#0075CA;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">fix</span> | `#0075CA` | Bug fix, backwards-compatible | **PATCH** `x.y.z+1` |
| <span style="background:#6F42C1;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">dependencies</span> | `#6F42C1` | Dependency update | **PATCH** `x.y.z+1` |
| <span style="background:#FEF2C0;color:#333;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">chore</span> | `#FEF2C0` | Maintenance, refactoring, or housekeeping. Excluded from changelog; no version bump. | none |

## Rules

- Every PR that targets `main` must carry **exactly one** label before it can merge. The label gate (`label-gate.yml`) enforces this as a required status check.
- `breaking`, `feature`, `fix`, and `dependencies` are bump labels: they must be the sole label on a PR and they produce a changelog entry.
- `chore` bypasses the gate entirely. The PR merges without a version bump and does not appear in the release draft. Use it for CI changes, refactoring, test additions, or any work that does not affect the public-facing package.
- If a single PR closes issues of mixed types apply the highest-priority label. E.g. a bug fix and a small feature should get the <span style="background:#0E8A16;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">feature</span> label.

## Version resolution

When multiple PRs accumulate in a draft release, the resolved version bump is the highest priority across all included labels:

<span style="background:#B60205;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">breaking</span> > <span style="background:#0E8A16;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">feature</span> > <span style="background:#0075CA;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">fix</span>  = <span style="background:#6F42C1;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">dependencies</span> 
