from tools.household_context.client import get_context, list_owners, summary


def test_context_names_household():
    assert get_context()["household_name"] == "Saia-Nitroy household"


def test_owners_are_configured():
    assert list_owners() == ["Joe Saia", "Shannon Nitroy-Saia"]


def test_summary_describes_private_slack_deployment():
    assert summary()["deployment_context"] == "private household Slack"
