<h1>Prototipe-MVCO</h1>
<p> Model utama menggunakan algoritma Random Forest Classification untuk memprediksi kondisi operasional, mendeteksi potensi risiko,
      serta memberikan status keputusan yang akan diproses oleh AI Recommender. Hasil prediksi tersebut kemudian diperkaya dengan logika
      rekomendasi berbasis aturan, parameter operasional, serta reasoning LLM untuk menghasilkan output yang lebih akurat dan dapat diambil
      sebagai operational insights. </p>
<p>Proyek ini mencakup:</p>
    <ul>
      <li>Pipeline preprocessing, termasuk normalisasi data, encoding, dan pembersihan dataset.</li>
      <li>Training model Random Forest, evaluasi performa, serta penyimpanan model (format <code>.pkl</code>).</li>
      <li>CLI Demo, yang memungkinkan pengguna menjalankan prediksi, menampilkan rekomendasi, dan menguji skenario operasional.</li>
      <li>Sistem Rekomendasi AI, yang menggabungkan hasil prediksi model ML dengan prompt-based reasoning dari Gemini.</li>
      <li>ChatBox AI, yang berfungsi sebagai asisten operasional untuk menjawab pertanyaan, menjelaskan alasan prediksi, dan memberikan keputusan berbasis kebijakan nilai rantai produksi (value chain optimization).</li>
    </ul>



 <!-- ===================== FOLDER UTAMA ======================= -->
  <h2>📁 1. Folder Utama</h2>
<pre style="background:#f6f8fa; padding:16px; border-radius:6px; font-size:14px; overflow-x:auto;">

PROJECTAPPLICATION/
├── __pycache__/
│
├── data/
│
├── Dataset_Raw_Data/
│   ├── heavy_equipment_dataset.csv
│   ├── logistics_dataset.csv
│   ├── production_dataset.csv
│   ├── road_condition_dataset.csv
│   ├── vessel_schedule_dataset.csv
│   ├── weather_dataset.csv
│
├── models/
│   ├── model_equipment.pkl
│   ├── model_logistics.pkl
│   ├── model_production.pkl
│   ├── model_road.pkl
│   ├── model_vessel.pkl
│   ├── model_weather.pkl
│
├── myenv/
│
├── notebook/
│   └── Main_Model.ipynb
│
├── SaveJson/
│   ├── prediction_log.json
│   ├── recommendation_output.json
│   └── reviews.json
│
├── .env
├── .gitignore
│
├── ai_recommender.py
├── app_cli.py
├── app.py
├── ChatBox.py
├── email_generator.py
├── main_entry.py
├── prediction_utils.py
├── processor.py
├── requirements.txt
├── review_manager.py
├── status_manager.py
└── storage.py

</pre>

  <p><strong>data/</strong><br>
  Berisi data operasional mentah atau data input lain yang dipakai aplikasi (misalkan parameter harian, data produksi, dan lainnya).</p>

  <p><strong>Dataset/</strong><br>
  Berisi dataset untuk training model machine learning, termasuk data preprocessing dan label yang digunakan oleh Random Forest.</p>

  <p><strong>models/</strong><br>
  Folder penyimpanan model ML yang sudah dilatih (format <code>.pkl</code>).</p>

  <p><strong>notebook/</strong><br>
  Berisi Jupyter Notebook untuk eksplorasi data, preprocessing, training, dan evaluasi sebelum digunakan ke aplikasi utama.</p>

  <p><strong>SaveJson/</strong><br>
  Tempat penyimpanan output prediksi dan rekomendasi, misalnya:
  <ul>
    <li>hasil prediksi ML,</li>
    <li>hasil reasoning rekomendasi AI,</li>
    <li>riwayat operasi sistem.</li>
  </ul>
  </p>

  <p><strong>myenv/</strong><br>
  Virtual environment Python untuk isolasi lingkungan eksekusi.</p>

  <hr>

  <!-- ===================== FILE PYTHON ======================= -->
  <h2>📌 2. File-File Python Utama</h2>

  <p><strong>app.py</strong><br>
  Entry point aplikasi berbasis API yang mengelola:
  <ul>
    <li>service prediksi,</li>
    <li>service rekomendasi,</li>
    <li>integrasi backend → frontend.</li>
  </ul>
  </p>

  <p><strong>app_cli.py</strong><br>
  Antarmuka CLI untuk menjalankan fitur aplikasi secara manual:
  <ul>
    <li>prediksi,</li>
    <li>rekomendasi,</li>
    <li>lihat log,</li>
    <li>testing pipeline.</li>
  </ul>
  </p>

  <p><strong>main_entry.py</strong><br>
  Orchestrator utama yang menjalankan pipeline:
  <ul>
    <li>load model,</li>
    <li>load data,</li>
    <li>prediksi → rekomendasi.</li>
  </ul>
  </p>

  <p><strong>ai_recommender.py</strong><br>
  Mesin rekomendasi AI yang menggabungkan:
  <ul>
    <li>prediksi dari ML,</li>
    <li>aturan operasional,</li>
    <li>reasoning LLM (Gemini).</li>
  </ul>
  </p>

  <p><strong>prediction_utils.py</strong><br>
  Modul pendukung prediksi:
  <ul>
    <li>load model,</li>
    <li>preprocess input,</li>
    <li>menjalankan model ML,</li>
    <li>memformat output prediksi.</li>
  </ul>
  </p>

  <p><strong>processor.py</strong><br>
  Modul preprocessing data:
  <ul>
    <li>cleaning,</li>
    <li>encoding,</li>
    <li>scaling,</li>
    <li>transformasi lainnya.</li>
  </ul>
  </p>

  <p><strong>storage.py</strong><br>
  Modul penyimpanan:
  <ul>
    <li>simpan hasil prediksi ke JSON,</li>
    <li>simpan rekomendasi,</li>
    <li>kelola log sistem.</li>
  </ul>
  </p>

  <p><strong>status_manager.py</strong><br>
  Mengatur status eksekusi:
  <ul>
    <li>status job,</li>
    <li>status prediksi terakhir,</li>
    <li>status rekomendasi terakhir.</li>
  </ul>
  </p>

  <p><strong>review_manager.py</strong><br>
  Mengatur proses review hasil rekomendasi:
  <ul>
    <li>validasi keputusan,</li>
    <li>pengecekan manual,</li>
    <li>finalisasi keputusan.</li>
  </ul>
  </p>

  <p><strong>email_generator.py</strong><br>
  Pembuat email otomatis berdasarkan hasil prediksi & rekomendasi.</p>

  <p><strong>ChatBox.py</strong><br>
  Chatbot berbasis Gemini API:
  <ul>
    <li>menjawab pertanyaan operasional,</li>
    <li>menjelaskan alasan prediksi,</li>
    <li>memberikan rekomendasi berbasis teks.</li>
  </ul>
  </p>

  <hr>

  <!-- ===================== CARA KERJA SISTEM ======================= -->
  <h2>📌 3. Cara Kerja Sistem (Ringkas)</h2>

<li><strong>Pengguna memberikan input</strong><br>
      Melalui CLI, API, atau ChatBox.</li>

<li><strong>Data masuk ke Processor → preprocessing</strong><br>
      <em>processor.py</em> membersihkan dan menyiapkan data untuk model ML.</li>

<li><strong>Model ML (Random Forest) melakukan prediksi</strong><br>
      Diproses oleh <em>prediction_utils.py</em>.</li>

<li><strong>Hasil prediksi dikirim ke AI Recommender</strong><br>
      <em>ai_recommender.py</em> memproses:
      <ul>
        <li>hasil ML,</li>
        <li>aturan operasional,</li>
        <li>reasoning LLM (Gemini).</li>
      </ul>
    </li>

<li><strong>Hasil disimpan ke SaveJson</strong><br>
      Melalui <em>storage.py</em>.</li>

<li><strong>Hasil ditinjau / ditampilkan</strong><br>
      <ul>
        <li>CLI → <em>app_cli.py</em></li>
        <li>API → <em>app.py</em></li>
        <li>Chatbot → <em>ChatBox.py</em></li>
        <li>Manual review → <em>review_manager.py</em></li>
      </ul>
    </li>

<li><strong>Notifikasi otomatis</strong><br>
      <em>email_generator.py</em> menghasilkan email keputusan.</li>
  

  <hr>
