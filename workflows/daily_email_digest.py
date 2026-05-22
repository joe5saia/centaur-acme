"""Workflow: daily personal email digest.

Reviews Gmail messages received today and DMs a summary + suggested replies.
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any

WORKFLOW_NAME = "daily_email_digest"

SCHEDULE = {
    "schedule_id": "daily_email_digest_8pm_ny",
    "cron": "0 20 * * *",
    "timezone": "America/New_York",
    "catchup_policy": "skip",
    # The workflow sends its own Slack DM. Avoid requiring a schedule delivery
    # channel/thread, which is intended for agent-turn delivery streams.
    "no_delivery": True,
}

SLACK_DM_USER = "U0A1U5A7NLV"

PROMPT_TEMPLATE = """
You are preparing Joe's daily personal email digest.

Today is {date_label} in America/New_York. Use the gsuite Gmail tools to review
emails received today only. Focus on messages that are either:
1. personal/direct emails to Joe, or
2. notifications that Joe received a message on another platform (LinkedIn,
   Twitter/X, GitHub, Notion, Linear, Slack email notifications, calendar/contact
   forms, marketplace/app message notifications, etc.).

Search broadly enough to find relevant same-day messages. Use gmail_search and
gmail_get as needed. Ignore marketing newsletters, promotions, automated security
noise, bulk updates, receipts, and low-signal automated mail unless they clearly
represent a person trying to reach Joe.

Output Slack-ready markdown with:
- *Daily email review — {date_label}*
- *Relevant emails* — bullet list with sender, subject, received time if available,
  why it matters, and whether action is needed.
- *Summary* — concise synthesis of important themes/messages.
- *Draft replies* — for emails Joe has not replied to and should reply to, include a
  short suggested response. Keep drafts brief, natural, and ready to copy/paste.

If there are no relevant emails, say so briefly. Do not send any emails or modify
Gmail. Draft only.
""".strip()


def _today_label() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")


async def handler(inp: dict[str, Any], ctx) -> dict[str, Any]:
    date_label = _today_label()
    prompt = PROMPT_TEMPLATE.format(date_label=date_label)
    result = await ctx.agent_turn(prompt)
    text = str(result.get("result_text") or "").strip()
    if not text:
        text = f"*Daily email review — {date_label}*\nNo result was produced."

    await ctx.call_tool(
        "slack",
        "send_message",
        {
            "channel": SLACK_DM_USER,
            "text": text,
            "no_attribution": True,
            "unfurl_links": False,
            "unfurl_media": False,
        },
    )
    result["slack_dm_user"] = SLACK_DM_USER
    result["date_label"] = date_label
    return result
