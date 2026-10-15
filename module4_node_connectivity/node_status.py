
from datetime import datetime, timezone, timedelta


HEARTBEAT_TIMEOUT_SECONDS = 60


def check_node_status(node_id, last_seen=None):
    if not node_id:
        raise ValueError("node_id is required")

    now = datetime.now(timezone.utc)

    if last_seen is None:
        status = "UNKNOWN"
    else:
        if isinstance(last_seen, str):
            last_seen = datetime.fromisoformat(
                last_seen.replace("Z", "+00:00")
            )

        if last_seen.tzinfo is None:
            raise ValueError(
                "last_seen must include a timezone"
            )

        age = (now - last_seen.astimezone(timezone.utc)).total_seconds()

        if age < 0:
            raise ValueError("last_seen cannot be in the future")

        status = (
            "CONNECTED"
            if age <= HEARTBEAT_TIMEOUT_SECONDS
            else "DISCONNECTED"
        )

    return {
        "nodeId": node_id,
        "status": status,
        "checkedAt": now.isoformat()
    }


if __name__ == "__main__":
    current_time = datetime.now(timezone.utc).isoformat()

    print("No heartbeat:")
    print(check_node_status("NODE-001"))

    print("\nRecent heartbeat:")
    print(check_node_status("NODE-001", current_time))

    print("\nOld heartbeat:")
    old_time = (
        datetime.now(timezone.utc) - timedelta(seconds=120)
    ).isoformat()

    print(check_node_status("NODE-001", old_time))