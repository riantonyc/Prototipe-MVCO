# panggil Gemini untuk generate rekomendasi / revise / summary

# ai_recommender.py
import json
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

def _call_gemini(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    Panggil Gemini dan kembalikan text response.
    """
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return json.dumps({"error": f"Failed to call Gemini: {str(e)}"})

def build_prompt_for_recommendation(model_name, prediction, probabilities, sorted_labels, inputs):
    prompt = f"""
Kamu adalah AI Planner Assistant (agent) yang memahami operasi lapangan (weather, road, equipment, vessel, logistics, production).
Buat TEPAT 3 daftar rekomendasi (primary / alternative / mitigation) berdasarkan probabilitas model.

Model: {model_name}
Prediksi: {prediction}
Probabilitas (label:score): {json.dumps(probabilities)}
Urutan label (tinggi -> rendah): {sorted_labels}
Input snapshot: {json.dumps(inputs)}

Output harus valid JSON dalam format:
{{
  "primary": [{{"action":"...","justification":"...","expected_impact":"..."}}],
  "alternative": [...],
  "mitigation": [...]
}}

Berikan 3-6 action pada setiap list bila relevan. Jawaban harus hanya JSON.
"""
    return prompt

def generate_recommendations_with_gemini(model_name, prediction, probabilities, sorted_labels, inputs):
    prompt = build_prompt_for_recommendation(model_name, prediction, probabilities, sorted_labels, inputs)
    raw = _call_gemini(prompt)
    # coba parse JSON
    try:
        parsed = json.loads(raw)
        return parsed
    except Exception:
        # fallback: bungkus raw text ke field raw jika tidak bisa parse
        return {"error": "Gemini tidak mengembalikan JSON valid", "raw": raw}

def build_prompt_for_revision(original_payload, reviewer_comments):
    prompt = f"""
Seseorang (planner) menolak rekomendasi sebelumnya dengan komentar: {reviewer_comments}

Berikut payload rekomendasi sebelumnya:
{json.dumps(original_payload, indent=2)}

Revisi rekomendasi dengan memperhatikan komentar reviewer. Kembalikan JSON baru dengan struktur:
{{ "primary": [...], "alternative": [...], "mitigation": [...] }}

Jelaskan singkat justification tiap action (2-3 kalimat).
"""
    return prompt

def revise_recommendations_with_gemini(original_payload, reviewer_comments):
    prompt = build_prompt_for_revision(original_payload, reviewer_comments)
    raw = _call_gemini(prompt)
    try:
        return json.loads(raw)
    except Exception:
        return {"error": "Gemini tidak mengembalikan JSON valid pada revisi", "raw": raw}

def build_prompt_for_email_summary(recommendation_record):
    """
    Buat prompt untuk membuat email summary yang ringkas berdasarkan record final.
    """
    prompt = f"""
Buatkan email ringkasan profesional (bahasa Indonesia) untuk customer dan internal team
berdasarkan rekomendasi final berikut (sisipkan justification singkat).

Rekomendasi Record:
{json.dumps(recommendation_record, indent=2, ensure_ascii=False)}

Email harus memiliki:
- Subject singkat
- Body (ringkasan kondisi, tindakan utama, jadwal/impact)
- Tanda tangan singkat

Kembalikan output sebagai JSON:
{{ "subject":"...", "body":"..." }}
"""
    return prompt

def generate_email_summary_with_gemini(recommendation_record):
    prompt = build_prompt_for_email_summary(recommendation_record)
    raw = _call_gemini(prompt)
    try:
        return json.loads(raw)
    except Exception:
        return {"error": "Gemini tidak mengembalikan JSON valid untuk email", "raw": raw}
