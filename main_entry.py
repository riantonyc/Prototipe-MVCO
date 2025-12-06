# main.py
import uuid
import json
from storage import load_json, save_json
from processor import prepare_recommendation_payload
from ai_recommender import generate_recommendations_with_gemini, revise_recommendations_with_gemini
from review_manager import add_review, list_pending_for_role
from email_generator import create_email_summary

INPUT_PATH = "SaveJson/prediction_log.json"       # input asli
RECS_PATH = "SaveJson/recommendation_output.json" # output rekomendasi


def load_input():
    return load_json(INPUT_PATH, [])

def save_recommendations(recs):
    save_json(RECS_PATH, recs)

def generate_all_recommendations():
    records = load_input()
    results = []
    for rec in records:
        rec_id = str(uuid.uuid4())
        model_name, prediction, probabilities, sorted_labels, inputs = prepare_recommendation_payload(rec)
        ai_out = generate_recommendations_with_gemini(model_name, prediction, probabilities, sorted_labels, inputs)
        new_rec = {
            "id": rec_id,
            "timestamp": rec.get("Timestamp"),
            "model": model_name,
            "prediction": prediction,
            "probabilities": probabilities,
            "sorted_labels": sorted_labels,
            "inputs": inputs,
            "recommendations": ai_out,
            "status": "pending_review_mine_planner",
            "assigned_reviewers": ["mine_planner", "shipping_planner"],
            "version": 1,
            "review_history": []
        }
        results.append(new_rec)
    save_recommendations(results)
    print(f"Generated {len(results)} recommendation records → saved to {RECS_PATH}")

def list_recommendations(filter_status=None):
    recs = load_json(RECS_PATH, [])
    for r in recs:
        if filter_status and r.get("status") != filter_status:
            continue
        print("ID:", r.get("id"))
        print("Model:", r.get("model"))
        print("Prediction:", r.get("prediction"))
        print("Status:", r.get("status"))
        print("Confidence (top):", max(r.get("probabilities", {}).values()) if r.get("probabilities") else None)
        print("-"*40)

def interactive_review():
    rec_id = input("Masukkan Recommendation ID: ").strip()
    role = input("Role reviewer (mine_planner/shipping_planner): ").strip()
    name = input("Nama reviewer: ").strip()
    action = input("Action (approve/reject/request_changes): ").strip()
    comments = input("Komentar: ").strip()
    review = add_review(rec_id, role, name, action, comments)
    print("Review recorded:", review)

def request_revision_by_ai():
    rec_id = input("Masukkan Recommendation ID yang perlu direvisi: ").strip()
    comments = input("Masukkan instruksi / komentar dari reviewer (alasan revisi): ").strip()
    recs = load_json(RECS_PATH, [])
    target = None
    for r in recs:
        if r.get("id") == rec_id:
            target = r
            break
    if not target:
        print("Recommendation ID tidak ditemukan.")
        return
    # panggil Gemini revise
    original_payload = target.get("recommendations", {})
    revised = revise_recommendations_with_gemini(original_payload, comments)
    # update record
    target["recommendations"] = revised
    target["status"] = "pending_review_mine_planner"  # kembali ke mine planner
    target["version"] = target.get("version", 1) + 1
    save_json(RECS_PATH, recs)
    print("Revisi selesai, record diupdate dan dikembalikan ke mine_planner.")

def generate_email():
    rec_id = input("Masukkan Recommendation ID untuk generate email: ").strip()
    recs = load_json(RECS_PATH, [])
    for r in recs:
        if r.get("id") == rec_id:
            email = create_email_summary(r)
            print("Subject:", email.get("subject"))
            print("Body:\n", email.get("body"))
            return
    print("ID tidak ditemukan.")

def list_pending_for(role):
    items = list_pending_for_role(role)
    if not items:
        print("Tidak ada pending untuk role", role)
        return
    for r in items:
        print("ID:", r.get("id"), "| Model:", r.get("model"), "| Timestamp:", r.get("timestamp"))

def main_menu():
    while True:
        print("\n=== Agentic AI CLI ===")
        print("1. Generate semua rekomendasi dari data/input.json")
        print("2. List semua rekomendasi")
        print("3. List rekomendasi by status")
        print("4. Review (manual) - add review")
        print("5. List pending untuk role")
        print("6. Request AI revision (dengan komentar reviewer)")
        print("7. Generate email summary untuk sebuah recommendation")
        print("0. Exit")
        c = input("Pilih: ").strip()
        if c == "1":
            generate_all_recommendations()
        elif c == "2":
            list_recommendations()
        elif c == "3":
            st = input("Masukkan status filter (e.g. pending_review_mine_planner): ")
            list_recommendations(filter_status=st)
        elif c == "4":
            interactive_review()
        elif c == "5":
            role = input("Masukkan role (mine_planner/shipping_planner): ")
            list_pending_for(role)
        elif c == "6":
            request_revision_by_ai()
        elif c == "7":
            generate_email()
        elif c == "0":
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main_menu()
