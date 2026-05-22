# Saia-Nitroy Household Centaur Overlay

This repository contains the local Centaur overlay for the private Saia-Nitroy household deployment.

The deployment is active in the household's private Slack. The household owners are Joe Saia and Shannon Nitroy-Saia, and this Centaur instance is used to help manage their household.

## Overlay contents

```text
.
├── .agents/skills/household-management/  # sandbox skill loaded with the overlay
├── services/sandbox/SYSTEM_PROMPT.md     # household-specific agent guidance
├── tools/                                # API-discovered tools
├── workflows/                            # durable workflows
├── tests/
└── Dockerfile                            # copies the overlay to /overlay
```

## Guidance

- Treat household information as private.
- Keep responses concise and action-oriented for private household Slack.
- Use available tools and workflows only when they are relevant to household operations.
- Keep user-facing prompts, workflow output, and skills focused on the Saia-Nitroy household.

## Build the overlay image

```bash
docker build -t ghcr.io/<org>/<overlay-repo>:local .
```

The image copies this repository to `/overlay`. Centaur's Helm chart mounts that path at `/app/overlay/org` in the API and `/home/agent/overlay/org` in sandbox pods.

## Verify in a running deployment

From the API pod:

```bash
echo "$TOOL_DIRS"
echo "$WORKFLOW_DIRS"
ls -la /app/overlay/org
```

From a sandbox:

```bash
echo "$CENTAUR_OVERLAY_DIR"
ls "$CENTAUR_OVERLAY_DIR"
ls "$CENTAUR_OVERLAY_DIR/.agents/skills"
```

## Local checks

```bash
uv run pytest
```
