
from datetime import datetime, timezone
from typing import Any, Dict, List


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_interactions(first_url: str) -> Dict[str, Any]:
    return {
        "clicks": [],
        "scrolls": 0,
        "pages": [first_url],
        "timeline": [],  # extra: records events with timestamps
    }


def record_event(
    interactions: Dict[str, Any],
    event_type: str,
    description: str,
    url: str | None = None,
) -> None:
    interactions.setdefault("timeline", [])
    interactions["timeline"].append(
        {
            "time": utc_now_iso(),
            "event": event_type,
            "description": description,
            "url": url,
        }
    )


def classify_error(exc: Exception, phase: str) -> Dict[str, str]:
    msg = str(exc)
    kind = "unknown_error"
    lower = msg.lower()
    if "timeout" in lower:
        kind = "timeout"
    elif "network" in lower:
        kind = "network_error"
    elif "playwright" in lower or "browser" in lower:
        kind = "js_engine_error"
    elif "invalid" in lower or "url" in lower:
        kind = "input_error"

    return {
        "message": msg,
        "phase": phase,
        "kind": kind,  # extra field beyond spec
    }


def total_text_length(sections: List[Dict[str, Any]]) -> int:
    return sum(len(s.get("content", {}).get("text", "")) for s in sections)
