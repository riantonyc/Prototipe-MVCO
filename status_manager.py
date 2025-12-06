#alur status & update when review occurs
# status_manager.py
from storage import load_json, save_json
from datetime import datetime

# status_manager.py
RECS_PATH = "SaveJson/recommendation_output.json"



def _load_recs():
    return load_json(RECS_PATH, [])

def _save_recs(data):
    save_json(RECS_PATH, data)

def update_status_for_recommendation(rec_id: str, role: str, action: str, comments: str = None):
    """
    Update status based on which role reviews and action taken.
    role: 'mine_planner' or 'shipping_planner'
    action: 'approve' | 'reject' | 'request_changes'
    """
    recs = _load_recs()
    changed = False
    for r in recs:
        if r.get("id") == rec_id:
            # default fields
            history = r.setdefault("review_history", [])
            history.append({
                "role": role,
                "action": action,
                "comments": comments,
                "timestamp": datetime.utcnow().isoformat()
            })
            # state transitions
            if role == "mine_planner":
                if action == "approve":
                    r["status"] = "pending_review_shipping_planner"
                else:
                    # reject or request_changes
                    r["status"] = "awaiting_revision_ai"
            elif role == "shipping_planner":
                if action == "approve":
                    r["status"] = "final_approved"
                else:
                    r["status"] = "awaiting_revision_ai"
            changed = True
            # bump version
            r["version"] = r.get("version", 1) + 1
            r["last_updated"] = datetime.utcnow().isoformat()
            break
    if changed:
        _save_recs(recs)
