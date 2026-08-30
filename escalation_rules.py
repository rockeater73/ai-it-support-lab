def determine_escalation(analysis):
    category = analysis["category"]
    priority = analysis["priority"]

    if category == "Security":
        return {
            "escalate": True,
            "assigned_tier": "Security Team",
            "reason": "Security-related incidents require specialized review."
        }

    if priority == "Critical":
        return {
            "escalate": True,
            "assigned_tier": "Tier 2",
            "reason": "Critical incidents require immediate escalation."
        }

    return {
        "escalate": False,
        "assigned_tier": "Tier 1",
        "reason": "Ticket can begin with standard Tier 1 troubleshooting."
    }