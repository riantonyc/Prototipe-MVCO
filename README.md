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
