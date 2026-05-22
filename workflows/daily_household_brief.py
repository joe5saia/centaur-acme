from datetime import timedelta

WORKFLOW_NAME = "daily_household_brief"
CRON = "0 14 * * 1-5"
SLACK_CHANNEL = "centaur-updates"
PROMPT = (
    "Use the Saia-Nitroy household overlay. Prepare a concise private-household "
    "brief for Joe Saia and Shannon Nitroy-Saia. Focus on household tasks, "
    "calendar/email follow-ups, open reminders, and recommended next actions. "
    "Keep the output focused on private household operations."
)


async def handler(inp, ctx):
    result = await ctx.agent_turn(PROMPT)
    await ctx.post_to_slack(SLACK_CHANNEL, result["result_text"])
    await ctx.sleep("cooldown", timedelta(seconds=1))
    return result
