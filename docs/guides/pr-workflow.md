# Day-to-day PR workflow

From opening an issue to publishing a release.

---

## 1. Open an issue (optional)

Three issue templates are available:

| Template | Use when | Issue Type |
|---|---|---|
| Bug Report | Reproducible bug with clear expected vs actual behaviour | `Bug` (set automatically) |
| Feature Request | New functionality or enhancement proposal | `Feature` (set automatically) |
| Something is not working | Unexpected behaviour where root cause is unclear | (none set) |

The issue Type is set automatically by the Bug Report and Feature Request templates.

!!! info "Issue Type vs PR label"
    These are separate. The issue Type categorises the issue for the project board. The PR label (step 3) is what drives the changelog and version bump. **It must still be applied manually on the PR** (see below).
---

## 2. Open a pull request

Branch off `main` using the PR branch name guide below, make your changes, publish branch and start the PR.

| Type | PR Title | PR branch name |
|---|---|---|
| **With linked issue** | `Fix memory leakage` | `42-fix-memory-leakage` |
| **Without an issue** | `Add support for custom node weights` | `add-support-custom-node-weights`

!!! info
    Do not include the issue number in the PR title. The changelog template already appends the PR number automatically (`(#15)` style). The issue reference belongs in the extended description at merge time (step 5) as `Fixes #42`, which closes the issue and appears in `$BODY`. Putting both in the title would produce two different numbers in one line.

    The title is written for someone reading the changelog months later, not for the diff reviewer. Keep it concise and factual.

### Opening description

This is **only** for reviewers. It does not appear in the changelog. Use it to explain context, trade-offs, or anything a reviewer needs to know.

### Linking issues

Add `Fixes #42` or `Closes #42` in the description or in the merge-time extended description (step 5). GitHub auto-closes the linked issue when the PR merges.

!!! success "Style Guide"
    If the issues are enumerate (e.g. `- Fixes #42`), the title of the issue is being displayed instead of just the number.

### What ends up in the changelog

| **What your write** | **Changelog field** | **When** |
|---|---|---|
| PR title | `$TITLE$`: The heading line for this entry | When the PR is opened; confirmed at merge |
| Squash-merge extended description | `$BODY$`: The indented detail under the title | Written at merge time (step 5) |

---

## 3. Apply exactly one bump label

See the full [label reference](../labels.md) for colours, bump types, and version resolution rules.

| Label | Use when | Version bump |
|---|---|---|
| <span style="background:#B60205;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">breaking</span> | Removes or alters existing behaviour in a way that breaks callers | MAJOR `x+1.y.z` |
| <span style="background:#0E8A16;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">feature</span> | New functionality that is backwards-compatible | MINOR `x.y+1.z` |
| <span style="background:#0075CA;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">fix</span> | Bug fix | PATCH `x.y.z+1` |
| <span style="background:#6F42C1;color:#fff;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">dependencies</span> | Dependency version bump | PATCH `x.y.z+1` |
| <span style="background:#FEF2C0;color:#333;padding:2px 10px;border-radius:12px;font-size:.85em;font-weight:600">chore</span> | CI changes, refactoring, test additions, or any work that does not affect the public API. Bypasses the gate; excluded from changelog; no version bump. | none |

The `label-gate / check` status check blocks merge until exactly one label is present. It re-runs automatically when you add or remove a label, so you can fix a missing label without pushing new commits.

---

## 4. Review and approval

Normal PR review. Branch protection on `main` requires (usually) at least one approval. This process may be different amongst repositories.

---

## 5. Squash-merge with a real description

When merging, GitHub shows a dialog with two fields: a title (pre-filled from the PR title) and an extended description.

!!! important "Before clicking Merge"
    1. Confirm the title is accurate. Edit it if anything changed during review.
    2. Clear the extended description box (or leave it blank if the repo uses "Pull request title only" as its default squash message).
    3. Write a fresh summary in your own words describing what changed and why.
    4. Include `Fixes #42` or `Closes #42` if this PR resolves a tracked issue.

This text is synced back to the PR description after merge and becomes the `$BODY` in the release notes.

### Example

<table>
<thead>
<tr><th>Merge dialog input</th><th>Release draft (raw markdown)</th></tr>
</thead>
<tbody>
<tr>
<td>
<strong>Title</strong><br>
<code>Fix graph traversal null pointer</code>
<br><br>
<strong>Extended description</strong><br>
<pre><code>Graph.traverse() raised a NullPointerException when
called on an empty graph. Added an early return for
that case; the existing behaviour is unchanged.

Fixes #42</code></pre>
</td>
<td>
<pre><code>### Fixes

- **Fix graph traversal null pointer** (#15) by @nico-loesch
  Graph.traverse() raised a NullPointerException
  when called on an empty graph. Added an early
  return for that case; the existing behaviour
  is unchanged.

  Fixes #42</code></pre>
</td>
</tr>
<tr>
<td>
<strong>Extended description with list items</strong><br>
<pre><code>Added an early return for empty graphs.

- Existing behaviour unchanged
- No API changes

Fixes #42</code></pre>
</td>
<td>
<pre><code>- **Fix graph traversal null pointer** (#15) by @nico-loesch
  Added an early return for empty graphs.

  - Existing behaviour unchanged
  - No API changes

  Fixes #42</code></pre>
</td>
</tr>
</tbody>
</table>

---

## 6. Automatic draft update

After merge, two workflow jobs run in sequence with no action needed:

1. [`sync-pr-description`](../workflows/sync-pr-description.md) reads the squash commit body and writes it back to the PR description field.
2. [`release-drafter`](../workflows/release-drafter.md) appends this PR's entry to the standing draft release and recomputes the suggested next version from the highest-priority bump label seen across all included PRs.

Repeat steps 2-6 for each PR. The draft accumulates entries until a release is published.

---

## 7. Publish the release

When ready to ship, go to the **Releases page**, open the draft, review or edit the body if needed, and click **Publish release**.

Publishing creates a git tag on current `main` HEAD. The tag push triggers `publish.yml`, which builds the wheel and uploads to PyPI. The version in the wheel is derived from the tag by `hatch-vcs`; no file in the repository is modified.

---

## 8. Verify

Check the Actions tab for the `Publish` workflow run. Confirm the upload succeeded and the new version appears on PyPI.
