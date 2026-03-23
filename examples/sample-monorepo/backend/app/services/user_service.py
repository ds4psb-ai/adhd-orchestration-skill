"""User service — intentional stub to demonstrate ADHD gap detection."""


def get_user(user_id: int) -> dict:
    """Fetch user by ID."""
    return {"id": user_id, "name": "demo"}


def update_user(user_id: int, data: dict) -> dict:
    raise NotImplementedError("Stub: update_user not yet implemented")


def delete_user(user_id: int) -> bool:
    raise NotImplementedError("Stub: delete_user not yet implemented")
