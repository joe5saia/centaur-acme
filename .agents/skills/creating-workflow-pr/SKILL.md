---
name: creating-workflow-pr
description: Use when asked to create, modify, schedule, or install a Centaur workflow via GitHub PR in Joe's centaur-acme overlay repo.
---

# Creating Centaur Workflow PRs

Use this skill when Joe asks you to create or change a scheduled/background Centaur workflow.

## Repo and PR Target

Workflow changes belong in Joe's overlay repository:

```text
https://github.com/joe5saia/centaur-acme
```

Open PRs against:

```text
base repo: joe5saia/centaur-acme
base branch: main
```

Do **not** try to edit the mounted workflow overlay inside the running Centaur pod. It is read-only. Do **not** claim the workflow is deployed just because a PR is opened.

## Branch Workflow

1. Clone or update `joe5saia/centaur-acme`.
2. Create a branch from `main` with a descriptive name:

```bash
git checkout main
git pull origin main
git checkout -b workflow/<short-description>
```

3. Add or edit workflow files under:

```text
workflows/
```

4. Run tests when available:

```bash
uv run pytest
```

5. Commit and push:

```bash
git add workflows/ .agents/skills/ AGENTS.md tests/
git commit -m "Add <workflow name> workflow"
git push -u origin workflow/<short-description>
```

6. Open a PR with `gh` or the GitHub API:

```bash
gh pr create \
  --repo joe5saia/centaur-acme \
  --base main \
  --head workflow/<short-description> \
  --title "Add <workflow name> workflow" \
  --body "<summary, schedule, tools used, test plan>"
```

## Workflow File Requirements

Each workflow module should export:

```python
WORKFLOW_NAME = "snake_case_name"

async def handler(inp: dict, ctx):
    ...
```

For scheduled workflows, prefer `SCHEDULE` over bare `CRON`:

```python
SCHEDULE = {
    "schedule_id": "unique_schedule_id",
    "cron": "0 20 * * *",
    "timezone": "America/New_York",
    "catchup_policy": "skip",
}
```

If the workflow sends its own Slack message or DM, add:

```python
"no_delivery": True
```

Otherwise provide a `slack_channel` or `thread_key` so the scheduler has a destination.

## Available Workflow APIs

Inside `handler(inp, ctx)` you can use:

```python
await ctx.call_tool("tool_name", "method_name", args)
await ctx.agent_turn(prompt)
await ctx.post_to_slack(channel, text)
await ctx.sleep("checkpoint_name", timedelta(seconds=...))
```

Use `ctx.agent_turn(...)` for reasoning/summarization. Use `ctx.call_tool(...)` for deterministic tool calls.

## Secrets and Safety

- Never commit secrets or tokens.
- Assume secrets are already provided through Centaur/iron-proxy.
- If a new secret is required, document the required secret name in the PR body.
- For Gmail/Calendar workflows, prefer read-only behavior unless Joe explicitly requests write actions.
- For email workflows, draft replies only unless Joe explicitly grants send permission and OAuth scopes support it.
- For Slack DMs, use Slack user IDs when known.

## PR Body Checklist

Include:

- What the workflow does.
- Schedule and timezone, if any.
- Slack destination, if any.
- Tools used.
- Required secrets/scopes.
- Test plan and whether tests passed.
- Deployment note:

```text
After merge, deploy locally with:
cd /home/saiaj/centaur-local/centaur-acme && git pull origin main
/home/saiaj/centaur-local/rebuild-overlay.sh
```

## Definition of Done

A workflow PR is done when:

- The workflow code is committed on a branch.
- A PR is open against `joe5saia/centaur-acme:main`.
- The PR body includes the checklist above.
- You report the PR URL to Joe.
