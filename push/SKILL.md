---
name: push
description: Commit all current code changes and push them to the GitHub main branch. Manual invocation only.
disable-model-invocation: true
---

# Push

Commit every pending change in the current git repository and push it to `main` on GitHub.

## Steps

1. **Check the repository state.** Run `git status` and `git diff` (staged and unstaged) to see what changed. If there is nothing to commit and nothing unpushed, say so and stop.

2. **Confirm the branch.** Run `git branch --show-current`. If it is not `main`, stop and tell the user which branch they are on rather than switching or merging.

3. **Screen for things that should not be committed.** Before staging, look for secrets or junk among the changed and untracked files: `.env` files, credentials, private keys, tokens, large build outputs (`dist/`, `node_modules/`), OS files (`.DS_Store`). If any appear, leave them out and tell the user what was skipped.

4. **Stage the changes.** Stage all remaining modified, deleted and untracked files (`git add -A`, minus anything excluded in step 3).

5. **Write the commit message.** Read the staged diff and write a concise, imperative subject line (under ~70 characters) that says what changed, matching the style of recent commits (`git log --oneline -10`). Add a short body only when the change needs explaining. End the message with any attribution lines the session requires.

6. **Commit.** Pass the message with a heredoc so formatting survives. If a pre-commit hook fails, fix the issue and make a new commit; never use `--no-verify` or `--amend`.

7. **Push.** Run `git push origin main`. If the push is rejected because the remote is ahead, run `git pull --rebase origin main` and push again. If the rebase hits conflicts, stop and report them; never force-push.

8. **Report.** Give the commit hash, the subject line, the files included, and confirm the push succeeded.
