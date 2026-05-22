# Centaur ACME overlay workflow authoring

This repository is the local Centaur overlay used for Joe's Centaur deployment.

## Workflow PR process

When asked to create or change a Centaur workflow:

1. Create a new branch from `main` with a descriptive name, for example `workflow/daily-email-digest`.
2. Add or edit workflow files under `workflows/`.
3. A workflow file must export:
   - `WORKFLOW_NAME: str`
   - `handler(inp, ctx)` async function
   - optionally `SCHEDULE` or `CRON` for scheduler registration.
4. Prefer `SCHEDULE` for scheduled workflows. Include `schedule_id`, `cron`, `timezone`, and `catchup_policy`.
5. If a workflow sends its own Slack message/DM, set `SCHEDULE["no_delivery"] = True`.
6. Use existing Centaur tools through `ctx.call_tool(...)` and agent turns through `ctx.agent_turn(...)`.
7. Do not commit secrets. Credentials are provided by Centaur Kubernetes secrets / iron-proxy.
8. Run lightweight tests if present: `uv run pytest`.
9. Commit changes and push to `joe5saia/centaur-acme`.
10. Open a pull request against `joe5saia/centaur-acme:main` for review.

Do not attempt to write directly into the mounted overlay inside a running Centaur pod; it is read-only. Deployment happens after the PR is reviewed/merged and the operator runs `/home/saiaj/centaur-local/rebuild-overlay.sh` from the host.
