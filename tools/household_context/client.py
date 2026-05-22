from __future__ import annotations

HOUSEHOLD_CONTEXT = {
    "household_name": "Saia-Nitroy household",
    "owners": ["Joe Saia", "Shannon Nitroy-Saia"],
    "deployment_context": "private household Slack",
    "purpose": "manage household operations",
}


class HouseholdContextClient:
    def get_context(self) -> dict[str, object]:
        return dict(HOUSEHOLD_CONTEXT)

    def list_owners(self) -> list[str]:
        return list(HOUSEHOLD_CONTEXT["owners"])

    def summary(self) -> dict[str, object]:
        return {
            "household_name": HOUSEHOLD_CONTEXT["household_name"],
            "owners": list(HOUSEHOLD_CONTEXT["owners"]),
            "deployment_context": HOUSEHOLD_CONTEXT["deployment_context"],
            "purpose": HOUSEHOLD_CONTEXT["purpose"],
        }


def _client() -> HouseholdContextClient:
    return HouseholdContextClient()


def get_context() -> dict[str, object]:
    return _client().get_context()


def list_owners() -> list[str]:
    return _client().list_owners()


def summary() -> dict[str, object]:
    return _client().summary()
