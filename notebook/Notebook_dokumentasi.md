<div style="font-family: -apple-system, 'Segoe UI', Roboto, Arial; color:#111; line-height:1.6;">

  <h1>📘 Dokumentasi Notebook — Model Training & Visualisasi</h1>
  <p><strong>Notebook:</strong> <code>Main_Model.ipynb</code></p>
  <p>Dokumen ini menyajikan penjelasan komprehensif mengenai alur kerja, algoritma, pipeline pemodelan, serta komponen visualisasi yang digunakan dalam notebook <code>Main_Model.ipynb</code>. Tujuan utama dokumentasi adalah memberikan gambaran teknis dan metodologis terkait proses pembangunan model ML untuk memudahkan reproduksi, validasi, dan deployment.</p>

  <hr>

  <h2>1. 🎯 Tujuan Notebook</h2>
  <ul>
    <li>Muat dan eksplorasi dataset.</li>
    <li>Preprocessing dan transformasi fitur.</li>
    <li>Membangun ML pipeline yang terstruktur dan dapat direplikasi.</li>
    <li>Melatih model klasifikasi menggunakan <em>Random Forest</em>.</li>
    <li>Mengukur performa model dengan metrik standar.</li>
    <li>Menyediakan visualisasi eksploratif & diagnostik (distribusi kelas, learning curve).</li>
    <li>Menyimpan model terlatih menggunakan <code>joblib</code> untuk deployment.</li>
  </ul>

  <hr>

  <h2>2. 📦 Library yang Digunakan</h2>
  <table style="border-collapse:collapse;width:100%;max-width:900px;">
    <thead>
      <tr style="background:#f0f0f0">
        <th style="border:1px solid #ddd;padding:8px;text-align:left">Library</th>
        <th style="border:1px solid #ddd;padding:8px;text-align:left">Fungsi Utama</th>
      </tr>
    </thead>
    <tbody>
      <tr><td style="border:1px solid #ddd;padding:8px">pandas</td><td style="border:1px solid #ddd;padding:8px">Pemuatan dataset & manipulasi data tabular</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">numpy</td><td style="border:1px solid #ddd;padding:8px">Operasi numerik & komputasi vektor</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">matplotlib.pyplot</td><td style="border:1px solid #ddd;padding:8px">Visualisasi dasar & plotting</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">seaborn</td><td style="border:1px solid #ddd;padding:8px">Visualisasi statistik</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">sklearn.preprocessing</td><td style="border:1px solid #ddd;padding:8px">Encoding kategori & scaling fitur numerik</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">sklearn.model_selection</td><td style="border:1px solid #ddd;padding:8px">Train/test split, learning curve, validasi</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">sklearn.pipeline</td><td style="border:1px solid #ddd;padding:8px">Menyusun pipeline preprocessing + model</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">sklearn.ensemble</td><td style="border:1px solid #ddd;padding:8px">RandomForestClassifier</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">sklearn.metrics</td><td style="border:1px solid #ddd;padding:8px">Metrik evaluasi (accuracy, classification_report)</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">joblib</td><td style="border:1px solid #ddd;padding:8px">Serialisasi & penyimpanan model</td></tr>
      <tr><td style="border:1px solid #ddd;padding:8px">os</td><td style="border:1px solid #ddd;padding:8px">Manajemen direktori model</td></tr>
    </tbody>
  </table>

  <hr>

  <h2>3. ⚙️ Algoritma Machine Learning yang Digunakan</h2>
  <h3>Random Forest Classifier (Ensemble - Bagging)</h3>
  <p><strong>Alasan pemilihan:</strong> menangani fitur numerik & kategorikal, tahan terhadap noise/outlier, mengurangi overfitting via bootstrap aggregation, mudah interpretasi melalui feature importance.</p>

  <h4>Cara kerja singkat</h4>
  <ol>
    <li>Bootstrap sampling membentuk subset data.</li>
    <li>Untuk setiap subset dibangun satu decision tree.</li>
    <li>Prediksi akhir melalui majority voting antar pohon.</li>
  </ol>

  <hr>

  <h2>4. 🔄 Pipeline Preprocessing & Training</h2>
  <p>Pipeline menggabungkan preprocessing dan model sehingga terjamin reproducibility dan konsistensi antara training & inference.</p>

  <h3>✨ Step 1 — Preprocessing</h3>
  <ul>
    <li><code>StandardScaler</code> untuk fitur numerik</li>
    <li><code>OneHotEncoder</code> untuk fitur kategorikal</li>
    <li><code>ColumnTransformer</code> untuk menerapkan transformasi berbeda per tipe variabel</li>
  </ul>

  <h3>✨ Step 2 — Train-Test Split</h3>
  <p><code>train_test_split(X, y, test_size=0.2)</code> (80% train / 20% test).</p>

  <h3>✨ Step 3 — Model Training</h3>
  <p>Gunakan <code>pipeline.fit(X_train, y_train)</code> — preprocessing otomatis diterapkan di dalam pipeline.</p>

  <h3>✨ Step 4 — Evaluasi Model</h3>
  <ul>
    <li><code>accuracy_score</code></li>
    <li><code>classification_report</code> (precision, recall, f1-score, support)</li>
    <li><em>Catatan:</em> belum termasuk confusion matrix, ROC-AUC, precision-recall curve — direkomendasikan untuk analisis lanjutan, khususnya pada dataset imbalance.</li>
  </ul>

  <h3>✨ Step 5 — Model Saving</h3>
  <p>Simpan pipeline utuh agar tidak perlu preprocessing ulang:</p>
  <pre style="background:#f6f8fa;padding:10px;border-radius:6px;">joblib.dump(pipeline, "models/model.pkl")</pre>

  <hr>

  <h2>5. 📊 Fungsi Visualisasi</h2>

  <h3>🟦 plot_class_distribution(df, column)</h3>
  <p><strong>Tujuan:</strong> tampilkan distribusi kelas untuk mendeteksi imbalance.</p>
  <p><strong>Output:</strong> countplot, jumlah sampel per kelas, rotasi label, palet warna konsisten.</p>

  <h3>🟧 check_overfitting_pipeline(model_pipeline, X_train, X_test, y_train, y_test)</h3>
  <p><strong>Tujuan:</strong> menilai overfitting / underfitting / generalization via perbandingan akurasi train vs test dan learning curve.</p>

  <table style="border-collapse:collapse;margin-top:8px;">
    <thead><tr style="background:#f0f0f0"><th style="border:1px solid #ddd;padding:6px">Kondisi</th><th style="border:1px solid #ddd;padding:6px">Indikasi</th><th style="border:1px solid #ddd;padding:6px">Implikasi</th></tr></thead>
    <tbody>
      <tr><td style="border:1px solid #ddd;padding:6px">Train ↑, Test ↓</td><td style="border:1px solid #ddd;padding:6px">Overfitting</td><td style="border:1px solid #ddd;padding:6px">Model terlalu sesuai noise</td></tr>
      <tr><td style="border:1px solid #ddd;padding:6px">Train ↓, Test ↓</td><td style="border:1px solid #ddd;padding:6px">Underfitting</td><td style="border:1px solid #ddd;padding:6px">Model kurang kompleks</td></tr>
      <tr><td style="border:1px solid #ddd;padding:6px">Train ≈ Test (keduanya tinggi)</td><td style="border:1px solid #ddd;padding:6px">Good Fit</td><td style="border:1px solid #ddd;padding:6px">Generalization baik</td></tr>
    </tbody>
  </table>

  <hr>

  <h2>6. 🧪 Evaluasi Model</h2>
  <table style="border-collapse:collapse;">
    <thead><tr style="background:#f0f0f0"><th style="border:1px solid #ddd;padding:6px">Metrik</th><th style="border:1px solid #ddd;padding:6px">Status</th></tr></thead>
    <tbody>
      <tr><td style="border:1px solid #ddd;padding:6px">accuracy_score</td><td style="border:1px solid #ddd;padding:6px">✔ digunakan</td></tr>
      <tr><td style="border:1px solid #ddd;padding:6px">classification_report</td><td style="border:1px solid #ddd;padding:6px">✔ digunakan</td
    </tbody>
  </table>


  <hr>

  <h2>7. 💾 Model Saving & Deployment</h2>
  <p>Simpan pipeline preprocessing + model secara utuh untuk deployment:</p>
  <pre style="background:#f6f8fa;padding:10px;border-radius:6px;">joblib.dump(pipeline, "models/nama_model.pkl")</pre>
  <p>Keunggulan: konsistensi preprocessing, langsung pakai di API (FastAPI / Flask), cocok untuk MLOps workflow.</p>

  <hr>

  <h2>8. 📝 Ringkasan Arsitektur Notebook</h2>
  <pre style="background:#f6f8fa;padding:12px;border-radius:6px;white-space:pre-wrap;">
┌──────────────────────────────────┐
│       Load Dataset (pandas)      │
└──────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│       Preprocessing Pipeline     │
│  - Scaling (StandardScaler)      │
│  - Encoding (OneHotEncoder)      │
└──────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│       Train/Test Split           │
└──────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│       Model Training             │
│     (RandomForestClassifier)     │
└──────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│         Evaluation               │
│  - Accuracy                      │
│  - Classification Report         │
│  - Learning Curve (Visual)       │
└──────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│     Save Model (.pkl / joblib)   │
└──────────────────────────────────┘
  </pre>
</div>
