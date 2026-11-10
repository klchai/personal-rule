#!/usr/bin/env bash
# Publish the sync script's working tree.
#
# Prefer a pull request. This repository currently rejects pull requests
# created by the Actions GITHUB_TOKEN, so when GitHub returns that specific
# error the same branch is left for review and an issue is opened instead.
# Enabling "Allow GitHub Actions to create and approve pull requests"
# makes the pull-request path succeed and this fallback is skipped.

set -euo pipefail

SUMMARY="${SYNC_SUMMARY:?SYNC_SUMMARY is required}"
BRANCH="${SYNC_BRANCH:-sync/upstream}"
TITLE="${SYNC_TITLE:-同步上游规则更新}"
REPO="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"

: "${GIT_AUTHOR_NAME:?GIT_AUTHOR_NAME is required}"
: "${GIT_AUTHOR_EMAIL:?GIT_AUTHOR_EMAIL is required}"
: "${GIT_COMMITTER_NAME:?GIT_COMMITTER_NAME is required}"
: "${GIT_COMMITTER_EMAIL:?GIT_COMMITTER_EMAIL is required}"

if [[ ! -f "$SUMMARY" ]]; then
  echo "Missing sync summary: $SUMMARY" >&2
  exit 1
fi

settings_url="https://github.com/${REPO}/settings/actions"
compare_url="https://github.com/${REPO}/compare/main...${BRANCH}?expand=1"

step_summary() {
  if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
    printf '%s\n' "$1" >>"$GITHUB_STEP_SUMMARY"
  fi
}

tracking_issue_number() {
  gh issue list \
    --repo "$REPO" \
    --state open \
    --limit 100 \
    --json number,title \
    --jq ".[] | select(.title == \"${TITLE}\") | .number" |
    awk 'NR == 1 { print; exit }'
}

close_tracking_issue() {
  local existing
  existing="$(tracking_issue_number)" || return 0
  if [[ -z "$existing" ]]; then
    return 0
  fi
  gh issue close "$existing" \
    --repo "$REPO" \
    --comment "上游快照已与 main 一致，关闭这条同步提醒。"
  echo "Closed tracking issue #${existing}."
}

push_branch() {
  if git ls-remote --exit-code origin "refs/heads/${BRANCH}" >/dev/null 2>&1; then
    git fetch --no-tags origin \
      "refs/heads/${BRANCH}:refs/remotes/origin/${BRANCH}"
    # Pass the expected remote SHA explicitly. A bare --force-with-lease
    # rejects the push as stale when HEAD is main and a local branch of
    # the same name already exists.
    expected="$(git rev-parse "refs/remotes/origin/${BRANCH}")"
    git push --force-with-lease="refs/heads/${BRANCH}:${expected}" \
      origin "HEAD:refs/heads/${BRANCH}"
  else
    git push origin "HEAD:refs/heads/${BRANCH}"
  fi
}

write_issue_body() {
  local dest="$1"
  {
    cat "$SUMMARY"
    cat <<EOF

分支 \`${BRANCH}\` 已更新，等待审核：${compare_url}

GitHub Actions 在这个仓库不能创建 pull request。在 Settings → Actions → General → Workflow permissions 勾选 Allow GitHub Actions to create and approve pull requests 后，每周同步会直接开 PR：${settings_url}
EOF
  } >"$dest"
}

git add -A
if git diff --cached --quiet; then
  echo "No upstream changes."
  close_tracking_issue || echo "Tracking issue was left unchanged."
  step_summary "上游没有需要提交的变化。"
  exit 0
fi

commit_file="$(mktemp)"
{
  echo "Sync rules with upstream sources"
  echo
  cat "$SUMMARY"
} >"$commit_file"
git commit -F "$commit_file"
push_branch

pr_log="$(mktemp)"
owner="${REPO%%/*}"
open_pr=""
if open_pr="$(gh pr list \
  --repo "$REPO" \
  --head "${owner}:${BRANCH}" \
  --base main \
  --state open \
  --json url \
  --jq '.[0].url // empty' 2>"$pr_log")"; then
  :
else
  open_pr=""
fi
if [[ -n "$open_pr" ]]; then
  gh pr edit "$open_pr" --repo "$REPO" --title "$TITLE" --body-file "$SUMMARY"
  echo "Updated existing pull request: ${open_pr}"
  step_summary "已更新 pull request：${open_pr}"
  exit 0
fi

if gh pr create \
  --repo "$REPO" \
  --base main \
  --head "$BRANCH" \
  --title "$TITLE" \
  --body-file "$SUMMARY" >"$pr_log" 2>&1; then
  echo "Opened pull request: $(cat "$pr_log")"
  step_summary "已打开 pull request：$(cat "$pr_log")"
  exit 0
fi

cat "$pr_log" >&2
if ! grep -q "not permitted to create or approve pull requests" "$pr_log"; then
  echo "Failed to open a pull request." >&2
  exit 1
fi

issue_body="$(mktemp)"
write_issue_body "$issue_body"
existing="$(tracking_issue_number)"
if [[ -n "$existing" ]]; then
  gh issue edit "$existing" --repo "$REPO" --body-file "$issue_body"
  issue_ref="#${existing}"
  echo "Updated tracking issue ${issue_ref}."
else
  issue_url="$(gh issue create --repo "$REPO" --title "$TITLE" --body-file "$issue_body")"
  issue_ref="$issue_url"
  echo "Opened tracking issue: ${issue_ref}"
fi

echo "::warning title=Actions cannot open pull requests::Enable Allow GitHub Actions to create and approve pull requests at ${settings_url}. Review ${compare_url}."
step_summary "$(cat <<EOF
Actions 不能在这个仓库创建 pull request，已改为 issue ${issue_ref}。

审核分支：${compare_url}

启用自动 PR：${settings_url}
EOF
)"
