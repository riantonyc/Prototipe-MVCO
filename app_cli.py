import os
import joblib
import pandas as pd
import numpy as np
import json
from datetime import datetime


models_config = [
    {
        "name": "weather",
        "file": "models/model_weather.pkl",
        "features": [
            'Temperature_C', 'Humidity_Percent', 'Rainfall_mm', 'Wind_Speed_mps',
            'Wind_Direction_deg', 'Visibility_km', 'Pressure_hPa', 'Sea_State_Level',
            'Wave_Height_m', 'Tide_Level_m', 'Storm_Warning', 'Weather_Condition'
        ]
    },
    {
        "name": "road",
        "file": "models/model_road.pkl",
        "features": [
            'Surface_Type', 'Surface_Condition', 'Pothole_Density', 'Slope_Angle_Degrees',
            'Traffic_Density', 'Flood_Level_m', 'Access_Status', 'Dust_Level_PPM',
            'Ground_Vibration_mm_s', 'Road_Temperature_C', 'Rainfall_mm', 'Soil_Moisture_%',
            'Maintenance_Activity', 'Accident_Count'
        ]
    },
    {
        "name": "equipment",
        "file": "models/model_equipment.pkl",
        "features": [
            'Machine_Type', 'Engine_Temperature_C', 'Oil_Pressure_Bar', 'Fuel_Level_Percent',
            'Engine_RPM', 'Vibration_Level_g', 'Hydraulic_Pressure_Bar', 'Working_Hours',
            'Maintenance_Status', 'Fault_Code', 'Operational_Mode', 'Ambient_Temperature_C',
            'Gear_Position', 'Fuel_Consumption_L_h', 'Torque_Nm', 'Engine_Load_Percent'
        ]
    },
    {
        "name": "vessel",
        "file": "models/model_vessel.pkl",
        "features": [
            'Delay_Minutes', 'Cargo_Type', 'Load_Weight_Tons', 'Port_Condition',
            'Weather_Impact_Score', 'Sea_Condition_Code', 'Crew_Availability_Percent',
            'Vessel_Status', 'Fuel_Consumption_Tons', 'Engine_RPM', 'Distance_Traveled_km',
            'Average_Speed_knots', 'Departure_Hour', 'Departure_Weekday', 'Departure_Month',
            'Planned_Duration_hours'
        ]
    },
    {
        "name": "logistics",
        "file": "models/model_logistics.pkl",
        "features": [
            'Date', 'Route_Code', 'Origin_Location', 'Destination_Location', 'Cargo_Type',
            'Cargo_Weight_Tons', 'Transport_Mode', 'Distance_km', 'Travel_Time_hr',
            'Actual_Travel_Time_hr', 'Fuel_Used_Liters', 'Fuel_Cost_USD', 'Delivery_Status',
            'Delay_Cause', 'CO2_Emission_kg'
        ]
    },
    {
        "name": "production",
        "file": "models/model_production.pkl",
        "features": [
            'Record_Timestamp', 'Production_ID', 'Date', 'Machine_ID', 'Shift', 'Operator_ID',
            'Material_Type', 'Working_Hours', 'Production_Tons', 'Fuel_Consumed_Liters',
            'Downtime_Minutes', 'Weather_Condition', 'Road_Condition_Status',
            'Equipment_Efficiency_Percent', 'Fuel_Efficiency_Tons_per_Liter',
            'Incident_Report', 'Maintenance_Required', 'CO2_Emission_kg',
            'Production_Cost_USD', 'Revenue_USD'
        ]
    },
]


CATEGORICAL_MAP = {
    "Weather_Condition": ["Clear", "Rainy", "Storm"],
    "Surface_Type": ["Asphalt", "Dirt", "Gravel"],
    "Surface_Condition": ["Dry", "Wet", "Slippery"],
    "Access_Status": ["Open", "Closed", "Restricted"],
    "Machine_Type": ["Excavator", "Dump Truck", "Bulldozer"],
    "Maintenance_Status": ["OK", "Service Required", "Fault"],
    "Operational_Mode": ["Idle", "Active", "Travel"],
    "Port_Condition": ["Normal", "Busy", "Closed"],
    "Sea_Condition_Code": ["Calm", "Moderate", "Rough"],
    "Transport_Mode": ["Truck", "Train", "Vessel"],
    "Delivery_Status": ["Completed", "Delayed", "In Transit"],
    "Delay_Cause": ["Weather", "Traffic", "Mechanical"],
    "Shift": ["Morning", "Afternoon", "Night"],
    "Road_Condition_Status": ["Good", "Moderate", "Bad"],
    "Material_Type": ["Coal", "Nickel", "Iron Ore"],
}


def load_model(path):
    """
    Memuat file model dari direktori "models".
    Jika model disimpan sebagai dictionary (berisi model dan urutan fitur),
    maka fungsi akan mengembalikan tuple (model, feature_order).
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File model tidak ditemukan: {path}")

    model_data = joblib.load(path)
    if isinstance(model_data, dict) and "model" in model_data:
        return model_data["model"], model_data.get("feature_order")
    return model_data, None


def normalize_input(value, feature_name=None):
    """
    Membersihkan dan menormalkan setiap input dari pengguna atau data uji.
    - Mengubah nilai kosong/None/nan menjadi 0.
    - Mengubah nilai kategorikal sesuai peta CATEGORICAL_MAP.
    - Mengonversi nilai numerik ke float.
    """
    if value in [None, "", "None", "none", "NaN", "nan", np.nan]:
        return 0.0

    if feature_name in CATEGORICAL_MAP:
        value_str = str(value).strip()
        std_list = [v.lower() for v in CATEGORICAL_MAP[feature_name]]
        if value_str.lower() in std_list:
            idx = std_list.index(value_str.lower())
            return CATEGORICAL_MAP[feature_name][idx]
        return value_str.capitalize()

    try:
        return float(value)
    except Exception:
        return 0.0


def predict_with_model(model, input_values, feature_names):
    """
    Melakukan prediksi berdasarkan model dan input yang diberikan.
    Jika model memiliki method predict_proba(), maka probabilitas hasil juga dikembalikan.
    """
    X_input = pd.DataFrame([input_values], columns=feature_names)

    num_cols, cat_cols = [], []
    try:
        preproc = model.named_steps.get("preprocessor", None)
        if preproc is not None:
            for name, transformer, cols in preproc.transformers_:
                if name == "num":
                    num_cols.extend(cols)
                elif name == "cat":
                    cat_cols.extend(cols)
    except Exception:
        pass

    for col in X_input.columns:
        val = X_input.at[0, col]
        if val in [None, "", "None", "nan", np.nan]:
            X_input.at[0, col] = 0.0 if col in num_cols else "Unknown"
            continue
        if col in num_cols:
            X_input[col] = pd.to_numeric(X_input[col], errors="coerce").fillna(0.0)
        else:
            X_input[col] = str(val).capitalize()

    X_input = X_input.replace([None, np.nan, "nan", "NaN"], 0)

    try:
        prediction = model.predict(X_input)
        prob = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_input)
            # Jika klasifikasi multi-class → tampilkan probabilitas tiap kelas
            if proba.shape[1] > 1:
                prob = {str(cls): float(p) for cls, p in zip(model.classes_, proba[0])}
            else:
                # Untuk binary classifier dengan 1 output (class positif)
                prob = {"Positive": float(proba[0][0])}
        return prediction[0], prob
    except Exception as e:
        return f"Error: {e}", None



def save_prediction_to_json(model_name, features, inputs, prediction, probabilities=None, filename="SaveJson/prediction_log.json"):
    """
    Menyimpan hasil prediksi ke JSON:
    - prediction_log.json (riwayat)
    - latest_prediction.json (hasil terakhir)
    Sekarang juga menyertakan probabilitas prediksi jika tersedia.
    """
    os.makedirs("SaveJson", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def convert_to_native(val):
        if isinstance(val, (np.int64, np.int32)):
            return int(val)
        elif isinstance(val, (np.float64, np.float32)):
            return float(val)
        elif isinstance(val, (np.bool_)):
            return bool(val)
        elif isinstance(val, (np.ndarray, list, tuple)):
            return [convert_to_native(v) for v in val]
        elif isinstance(val, dict):
            return {k: convert_to_native(v) for k, v in val.items()}
        return val

    data_entry = {
        "Timestamp": timestamp,
        "Model": str(model_name),
        "Prediction": convert_to_native(prediction),
        "Probabilities": convert_to_native(probabilities) if probabilities else None,
        "Inputs": {str(feat): convert_to_native(val) for feat, val in zip(features, inputs)}
    }

    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            if not isinstance(existing_data, list):
                existing_data = [existing_data]
        except json.JSONDecodeError:
            existing_data = []
    else:
        existing_data = []

    existing_data.append(data_entry)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"JSON → {filename}")


def get_test_inputs():
    """
    Menghasilkan data uji (dummy) untuk setiap model.
    Data ini digunakan untuk menguji sistem prediksi secara otomatis
    tanpa input manual.
    """
    return {
        "weather": {
            'Temperature_C': 30.5, 'Humidity_Percent': 78, 'Rainfall_mm': 5.2, 'Wind_Speed_mps': 3.4,
            'Wind_Direction_deg': 120, 'Visibility_km': 8.5, 'Pressure_hPa': 1010, 'Sea_State_Level': 2,
            'Wave_Height_m': 1.2, 'Tide_Level_m': 0.6, 'Storm_Warning': 0, 'Weather_Condition': "Clear"
        },
        "road": {
            'Surface_Type': "Asphalt", 'Surface_Condition': "Wet", 'Pothole_Density': 0.3, 'Slope_Angle_Degrees': 5,
            'Traffic_Density': 0.7, 'Flood_Level_m': 0.1, 'Access_Status': "Open", 'Dust_Level_PPM': 45,
            'Ground_Vibration_mm_s': 2.1, 'Road_Temperature_C': 35, 'Rainfall_mm': 4.5, 'Soil_Moisture_%': 35,
            'Maintenance_Activity': "None", 'Accident_Count': 1
        },
        "equipment": {
            'Machine_Type': "Excavator", 'Engine_Temperature_C': 82, 'Oil_Pressure_Bar': 4.2, 'Fuel_Level_Percent': 65,
            'Engine_RPM': 1800, 'Vibration_Level_g': 0.8, 'Hydraulic_Pressure_Bar': 210, 'Working_Hours': 6.5,
            'Maintenance_Status': "OK", 'Fault_Code': 0, 'Operational_Mode': "Active", 'Ambient_Temperature_C': 32,
            'Gear_Position': "3", 'Fuel_Consumption_L_h': 12.5, 'Torque_Nm': 450, 'Engine_Load_Percent': 78
        },
        "vessel": {
            'Delay_Minutes': 15, 'Cargo_Type': "Coal", 'Load_Weight_Tons': 1200, 'Port_Condition': "Normal",
            'Weather_Impact_Score': 0.6, 'Sea_Condition_Code': "Moderate", 'Crew_Availability_Percent': 95,
            'Vessel_Status': "Departed", 'Fuel_Consumption_Tons': 20.5, 'Engine_RPM': 1600, 'Distance_Traveled_km': 320,
            'Average_Speed_knots': 14, 'Departure_Hour': 8, 'Departure_Weekday': 3, 'Departure_Month': 11,
            'Planned_Duration_hours': 10
        },
        "logistics": {
            'Date': "2025-11-11", 'Route_Code': "R123", 'Origin_Location': "Pontianak", 'Destination_Location': "Balikpapan",
            'Cargo_Type': "Fuel", 'Cargo_Weight_Tons': 35, 'Transport_Mode': "Truck", 'Distance_km': 470,
            'Travel_Time_hr': 9.5, 'Actual_Travel_Time_hr': 10.2, 'Fuel_Used_Liters': 220, 'Fuel_Cost_USD': 180,
            'Delivery_Status': "Completed", 'Delay_Cause': "Traffic", 'CO2_Emission_kg': 75
        },
        "production": {
            'Record_Timestamp': "2025-11-11 10:00:00", 'Production_ID': "PRD_091", 'Date': "2025-11-11",
            'Machine_ID': "MCH_07", 'Shift': "Morning", 'Operator_ID': "OP_12", 'Material_Type': "Iron Ore",
            'Working_Hours': 8, 'Production_Tons': 420, 'Fuel_Consumed_Liters': 140, 'Downtime_Minutes': 25,
            'Weather_Condition': "Sunny", 'Road_Condition_Status': "Good", 'Equipment_Efficiency_Percent': 88,
            'Fuel_Efficiency_Tons_per_Liter': 3.0, 'Incident_Report': 0, 'Maintenance_Required': 0,
            'CO2_Emission_kg': 65, 'Production_Cost_USD': 21000, 'Revenue_USD': 28000
        }
    }

# ini bisa di hapus model test dan manual input sesuaikan dengan keperluan web
def test_all_models():
    """
    Menguji semua model secara otomatis menggunakan data dummy dari get_test_inputs().
    Untuk setiap model:
    - Memuat model dan fitur
    - Menormalkan input
    - Melakukan prediksi
    - Menyimpan hasil ke file JSON
    """
    test_data = get_test_inputs()
    results = {}

    print("\n=== ⚡ TEST OTOMATIS SEMUA MODEL ===\n")

    for cfg in models_config:
        name = cfg["name"]
        model, feat_order = load_model(cfg["file"])
        features = feat_order or cfg["features"]

        data = test_data[name]
        input_values = [normalize_input(data[f], f) for f in features]
        prediction, prob = predict_with_model(model, input_values, features)
        save_prediction_to_json(name, features, input_values, prediction, prob)



        results[name] = prediction
        print(f"{name.upper()} → Hasil Prediksi: {prediction}")

    print("\nRINGKASAN HASIL TEST:")
    for k, v in results.items():
        print(f" - {k}: {v}")


def manual_input_for_model():
    """
    Meminta pengguna memilih model dan memasukkan nilai fitur satu per satu.
    Hasil prediksi akan disimpan ke JSON dan ditampilkan di layar.
    """
    print("\n=== MODE INPUT MANUAL ===\n")
    print("Daftar model yang tersedia:")
    for i, cfg in enumerate(models_config):
        print(f"{i + 1}. {cfg['name']}")
    choice = input("\nPilih nomor model yang ingin diuji: ")
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(models_config):
            print("Nomor model tidak valid.")
            return
    except ValueError:
        print("Input tidak valid.")
        return

    cfg = models_config[idx]
    model, feat_order = load_model(cfg["file"])
    features = feat_order or cfg["features"]

    print(f"\nMasukkan nilai untuk model: {cfg['name'].upper()}")
    user_inputs = {}
    for feat in features:
        val = input(f"  {feat}: ")
        user_inputs[feat] = normalize_input(val, feat)

    input_values = [user_inputs[f] for f in features]
    prediction = predict_with_model(model, input_values, features)
    print(f"\nHasil Prediksi untuk {cfg['name'].upper()}: {prediction}\n")

    save_prediction_to_json(cfg["name"], features, input_values, prediction)


def main():
    """
    Fungsi utama yang menjalankan aplikasi prediksi.
    Pengguna dapat memilih:
    - Mode 1: input manual (belum diaktifkan)
    - Mode 2: test otomatis dengan data dummy
    """
    print("=== SISTEM PREDIKSI MULTI DATASET (CLI) ===")
    mode = input("Ketik '1' untuk input manual, atau '2' untuk test otomatis: ")

    if mode.strip() == "2":
        test_all_models()
    else:
        print("\n Mode input manual aktif...\n")
        test_all_models()


if __name__ == "__main__":
    main()
