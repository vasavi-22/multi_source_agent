import json
from pathlib import Path

def trigger_alerts(decision_result):
    events = decision_result.get("events", [])
    severity = decision_result.get("severity")

    if not events:
        return {
            "status": "no_action",
            "message": "No alerts triggered."
        }

    print("\n=== ALERT EVENTS ===")
    print(f"Severity: {severity}")
    print(f"Total Events: {len(events)}")

    for event in events:
        print(f"- [{event['domain'].upper()}] {event['entity']} -> {event['reason']}")

    # Save to file (simulate persistence layer)
    output_path = Path("alert_log.json")
    with open(output_path, "a") as f:
        json.dump(decision_result, f, indent=2)

    return {
        "status": "action_executed",
        "stored_at": str(output_path),
        "events_processed": len(events)
    }