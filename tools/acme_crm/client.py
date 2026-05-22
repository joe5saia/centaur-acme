from __future__ import annotations

SAMPLE_ACCOUNTS = {
    "globex": {
        "name": "Globex",
        "owner": "Avery Chen",
        "plan": "Enterprise",
        "health": "green",
        "open_tickets": 1,
        "notes": "Pilot expanded from support automation to weekly reporting.",
    },
    "initech": {
        "name": "Initech",
        "owner": "Sam Rivera",
        "plan": "Business",
        "health": "yellow",
        "open_tickets": 3,
        "notes": "Waiting on SSO configuration before production launch.",
    },
}


class AcmeCrmClient:
    def list_accounts(self) -> list[dict[str, object]]:
        return list(SAMPLE_ACCOUNTS.values())

    def get_account(self, name: str) -> dict[str, object]:
        key = name.strip().lower()
        if key not in SAMPLE_ACCOUNTS:
            raise KeyError(f"unknown sample account: {name}")
        return SAMPLE_ACCOUNTS[key]

    def health_summary(self) -> dict[str, object]:
        accounts = self.list_accounts()
        return {
            "account_count": len(accounts),
            "open_tickets": sum(int(account["open_tickets"]) for account in accounts),
            "yellow_accounts": [account["name"] for account in accounts if account["health"] == "yellow"],
            "sample_data": True,
        }


def _client() -> AcmeCrmClient:
    return AcmeCrmClient()


# Keep module-level functions for the template tests and local CLI.
def list_accounts() -> list[dict[str, object]]:
    return _client().list_accounts()


def get_account(name: str) -> dict[str, object]:
    return _client().get_account(name)


def health_summary() -> dict[str, object]:
    return _client().health_summary()
