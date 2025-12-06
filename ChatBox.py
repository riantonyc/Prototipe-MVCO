# main.py
import os
import json
from google import genai
from dotenv import load_dotenv

# Load environment (.env)
load_dotenv()

# Client otomatis membaca GEMINI_API_KEY
client = genai.Client()


# Fungsi membaca semua file JSON dalam folder SaveJson/
def load_multiple_json(folder_path="SaveJson"):
    combined_data = {}

    # Pastikan folder ada
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' tidak ditemukan!")
        return combined_data

    # Membaca semua file json
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    combined_data[file] = json.load(f)
            except Exception as e:
                print(f"Gagal membaca {file}: {e}")

    return combined_data


# ------------------------------------------------------------
# Fungsi untuk bertanya ke Gemini
# ------------------------------------------------------------
def ask_gemini(question, context_json):
    prompt = f"""
Kamu adalah AI yang memahami data berikut (berasal dari banyak file JSON):

{json.dumps(context_json, indent=2)}

Jawablah pertanyaan berikut berdasarkan data di atas:

Pertanyaan:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text


# ------------------------------------------------------------
# Chatbox CLI
# ------------------------------------------------------------
def chatbox():
    print("=== Chatbox AI – Pembaca Banyak JSON (Folder: SaveJson/) ===")

    context_json = load_multiple_json("SaveJson")

    if not context_json:
        print("❌ Tidak ada file JSON ditemukan dalam folder SaveJson/")
        return

    print(f"✔ {len(context_json)} file JSON berhasil dimuat!")
    print("Ketik 'exit' untuk keluar.\n")

    while True:
        question = input("Anda: ")

        if question.lower() in ["exit", "quit", "keluar"]:
            print("Keluar dari chatbox...")
            break

        answer = ask_gemini(question, context_json)
        print(f"\nAI: {answer}\n")



# Main Program
if __name__ == "__main__":
    chatbox()
