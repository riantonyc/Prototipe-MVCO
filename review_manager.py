# menyimpan review dan mengupdate status

# review_manager.py
import uuid
from datetime import datetime
from storage import load_json, save_json
from status_manager import update_status_for_recommendation

REVIEWS_PATH = "SaveJson/reviews.json"
RECS_PATH = "SaveJson/recommendation_output.json"


def load_reviews():
    return load_json(REVIEWS_PATH, [])

def save_review(review):
    reviews = load_reviews()
    reviews.append(review)
    save_json(REVIEWS_PATH, reviews)

def add_review(recommendation_id: str, role: str, reviewer_name: str, action: str, comments: str):
    review_record = {
        "id": str(uuid.uuid4()),
        "recommendation_id": recommendation_id,
        "role": role,
        "reviewer_name": reviewer_name,
        "action": action,
        "comments": comments,
        "timestamp": datetime.utcnow().isoformat()
    }
    save_review(review_record)

    # update recommendation status based on action
    update_status_for_recommendation(recommendation_id, role, action, comments)

    return review_record

def list_pending_for_role(role: str):
    recs = load_json(RECS_PATH, [])
    res = []
    for r in recs:
        assigned = r.get("assigned_reviewers", [])
        status = r.get("status", "")
        # show if status pending for this role
        if role == "mine_planner" and status == "pending_review_mine_planner":
            res.append(r)
        if role == "shipping_planner" and status == "pending_review_shipping_planner":
            res.append(r)
    return res
