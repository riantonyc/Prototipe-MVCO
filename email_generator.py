# membuat email summary (local fallback)
# email_generator.py
from ai_recommender import generate_email_summary_with_gemini
from storage import save_json

def create_email_summary(recommendation_record):
    """
    Coba gunakan Gemini untuk membuat email, jika gagal gunakan fallback local.
    """
    result = generate_email_summary_with_gemini(recommendation_record)
    if isinstance(result, dict) and "error" not in result:
        return result
    # fallback
    subject = f"Summary Plan - {recommendation_record.get('model')} - {recommendation_record.get('timestamp')}"
    # build body concise
    primary = recommendation_record.get("recommendations", {}).get("primary", [])
    primary_actions = "\n".join([f"- {a.get('action')}" if isinstance(a, dict) else f"- {a}" for a in primary])
    body = f"""
Ringkasan Rencana untuk model {recommendation_record.get('model')}:

Primary Recommendations:
{primary_actions}

Status: {recommendation_record.get('status')}

Silakan cek sistem untuk detail dan berikan persetujuan.
"""
    return {"subject": subject, "body": body}
