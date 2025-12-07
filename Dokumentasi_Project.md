

<body>
<h1>📘 Dokumentasi Struktur & Cara Menjalankan Project</h1>

<!-- ===================== SECTION 1 ===================== -->
<h2>📁 1. Folder Wajib Ada</h2>

<p>Pastikan folder-folder berikut tersedia sesuai struktur project Anda:</p>

<pre>
project/
│
├── data/          → data operasional harian
├── Dataset/       → dataset training model ML
├── models/        → model ML yang sudah dilatih (.pkl)
├── notebook/      → jupyter notebook training & experiment
├── SaveJson/      → hasil prediksi & rekomendasi (output)
├── myenv/         → environment python (opsional)
</pre>

<h3>Penjelasan Singkat:</h3>

<p><strong>data/</strong> → file input untuk prediksi saat runtime.</p>
<p><strong>Dataset/</strong> → file training & preprocessing.</p>
<p><strong>models/</strong> → harus berisi file <code>.pkl</code> (model Random Forest).</p>
<p><strong>SaveJson/</strong> → otomatis terisi hasil prediksi & rekomendasi.</p>
<p><strong>myenv/</strong> → tempat virtual environment Python (boleh dibuat baru).</p>

<hr>

<!-- ===================== SECTION 2 ===================== -->
<h2>📄 2. File Utama yang Harus Ada</h2>

<p>Pastikan file berikut ada dan tidak rusak/hilang:</p>

<table>
  <tr>
    <th>File</th>
    <th>Fungsi Singkat</th>
  </tr>
  <tr><td>app.py</td><td>API untuk frontend / backend</td></tr>
  <tr><td>app_cli.py</td><td>CLI demo prediksi & rekomendasi</td></tr>
  <tr><td>main_entry.py</td><td>Runner utama (bootstrap project)</td></tr>
  <tr><td>ai_recommender.py</td><td>Engine rekomendasi</td></tr>
  <tr><td>prediction_utils.py</td><td>Fungsi prediksi model</td></tr>
  <tr><td>processor.py</td><td>Preprocessing data</td></tr>
  <tr><td>storage.py</td><td>Penyimpanan output JSON</td></tr>
  <tr><td>status_manager.py</td><td>Status proses</td></tr>
  <tr><td>review_manager.py</td><td>Review hasil rekomendasi</td></tr>
  <tr><td>email_generator.py</td><td>Pengiriman notifikasi email</td></tr>
  <tr><td>ChatBox.py</td><td>Chatbot Gemini API</td></tr>
  <tr><td>.env</td><td>API KEY Gemini, konfigurasi lain</td></tr>
  <tr><td>requirements.txt</td><td>Daftar library Python</td></tr>
</table>

<p><strong>📌 Penting:</strong><br>
File <code>.pkl</code> model ML harus berada di folder <code>models/</code> agar <code>prediction_utils.py</code> dapat memuat model.</p>

<hr>

<!-- ===================== SECTION 3 ===================== -->
<h2>⚙️ 3. Hal yang Harus Disiapkan Sebelum Menjalankan Project</h2>

<h3>1️⃣ Install Virtual Environment</h3>

<pre>python -m venv myenv</pre>

<h3>2️⃣ Aktifkan Environment</h3>

<p><strong>Windows:</strong></p>
<pre>myenv\Scripts\activate</pre>

<p><strong>Linux/macOS:</strong></p>
<pre>source myenv/bin/activate</pre>

<h3>3️⃣ Install dependencies</h3>
<pre>pip install -r requirements.txt</pre>

<h3>4️⃣ Siapkan file .env</h3>

<p>Isi minimal:</p>

<pre>
GEMINI_API_KEY=YOUR_KEY
MODEL_PATH=models/model.pkl
</pre>

<p><strong>Tanpa file .env ini, ChatBox & prediksi tidak akan berjalan.</strong></p>

<hr>

<!-- ===================== SECTION 4 ===================== -->
<h2>▶️ 4. Cara Menjalankan Project</h2>

<h3>A. Menjalankan CLI Demo</h3>
<pre>python app_cli.py</pre>

<p>Anda bisa:</p>
<ul>
  <li>Menjalankan prediksi</li>
  <li>Melihat rekomendasi</li>
  <li>Testing pipeline</li>
</ul>

<h3>B. Menjalankan Sistem Utama</h3>
<pre>python main_entry.py</pre>

<p>Ini akan:</p>
<ul>
  <li>Memuat model</li>
  <li>Memproses input</li>
  <li>Menjalankan prediksi → rekomendasi</li>
</ul>

<h3>C. Menjalankan API Backend</h3>

<pre>python app.py</pre>

<p><strong>Jika menggunakan FastAPI:</strong></p>
<pre>uvicorn app:app --reload</pre>

<h3>D. Menjalankan ChatBot Operasional</h3>

<pre>python ChatBox.py</pre>

<p>Fungsi:</p>
<ul>
  <li>Reasoning AI menggunakan Gemini</li>
  <li>Menjelaskan keputusan operasional</li>
  <li>Menjawab pertanyaan user</li>
</ul>

<hr>

<!-- ===================== SUMMARY ===================== -->
<h2>⭐ RINGKASAN SUPER SINGKAT</h2>

<p><strong>Folder wajib:</strong></p>
<ul>
  <li>data/</li>
  <li>Dataset/</li>
  <li>models/</li>
  <li>SaveJson/</li>
  <li>notebook/</li>
</ul>

<p><strong>File wajib:</strong></p>
<ul>
  <li>app.py</li>
  <li>app_cli.py</li>
  <li>main_entry.py</li>
  <li>ai_recommender.py</li>
  <li>prediction_utils.py</li>
  <li>.env</li>
  <li>model .pkl di folder models/</li>
</ul>

<p><strong>Sebelum menjalankan:</strong></p>
<pre>
pip install -r requirements.txt
Buat file .env dengan API key Gemini.
Pastikan model .pkl sudah ada.
</pre>

<p><strong>Perintah utama:</strong></p>
<ul>
  <li>CLI → <code>python app_cli.py</code></li>
  <li>Engine → <code>python main_entry.py</code></li>
  <li>API → <code>python app.py</code></li>
  <li>Chatbot → <code>python ChatBox.py</code></li>
</ul>

</body>
