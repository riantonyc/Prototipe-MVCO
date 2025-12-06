import os
import joblib
import pandas as pd
import numpy as np
import json
from datetime import datetime


# ============================================================
# Konfigurasi Model
# ============================================================

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


# ============================================================
# Kategori Nilai Kategorikal
# ============================================================

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


# ============================================================
# Fungsi Utilitas
# ============================================================

def load_model(path):
    """Memuat model dari file .pkl"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File model tidak ditemukan: {path}")

    model_data = joblib.load(path)
    if isinstance(model_data, dict) and "model" in model_data:
        return model_data["model"], model_data.get("feature_order")
    return model_data, None


def normalize_input(value, feature_name=None):
    """Menormalkan input agar sesuai format model"""
    if value in [None, "", "None", "none", "NaN", "nan", np.nan]:
        return 0.0

    # Normalisasi kategorikal
    if feature_name in CATEGORICAL_MAP:
        value_str = str(value).strip().lower()
        valid_values = [v.lower() for v in CATEGORICAL_MAP[feature_name]]
        if value_str in valid_values:
            idx = valid_values.index(value_str)
            return CATEGORICAL_MAP[feature_name][idx]
        return value_str.capitalize()

    # Normalisasi numerik
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def predict_with_model(model, input_values, feature_names):
    """Prediksi berdasarkan model dan input"""
    X_input = pd.DataFrame([input_values], columns=feature_names)
    X_input = X_input.replace([None, np.nan, "nan", "NaN"], 0)

    try:
        prediction = model.predict(X_input)
        prob = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_input)
            if proba.shape[1] > 1:
                prob = {str(cls): float(p) for cls, p in zip(model.classes_, proba[0])}
            else:
                prob = {"Positive": float(proba[0][0])}
        return prediction[0], prob
    except Exception as e:
        return f"Error: {e}", None


def save_prediction_to_json(model_name, features, inputs, prediction, probabilities=None, filename="SaveJson/prediction_log.json"):
    """Menyimpan hasil prediksi ke JSON"""
    os.makedirs("SaveJson", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def convert(val):
        if isinstance(val, (np.integer, np.floating)):
            return float(val)
        if isinstance(val, (np.ndarray, list, tuple)):
            return [convert(v) for v in val]
        if isinstance(val, dict):
            return {k: convert(v) for k, v in val.items()}
        return val

    data_entry = {
        "Timestamp": timestamp,
        "Model": str(model_name),
        "Prediction": convert(prediction),
        "Probabilities": convert(probabilities) if probabilities else None,
        "Inputs": {str(feat): convert(val) for feat, val in zip(features, inputs)}
    }

    existing = []
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing = json.load(f)
                if not isinstance(existing, list):
                    existing = [existing]
        except json.JSONDecodeError:
            existing = []

    existing.append(data_entry)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)


def get_test_inputs():
    """Data dummy untuk uji otomatis"""
    return {
        "weather": {'Temperature_C': 30.5, 'Humidity_Percent': 78, 'Rainfall_mm': 5.2, 'Wind_Speed_mps': 3.4,
                    'Wind_Direction_deg': 120, 'Visibility_km': 8.5, 'Pressure_hPa': 1010, 'Sea_State_Level': 2,
                    'Wave_Height_m': 1.2, 'Tide_Level_m': 0.6, 'Storm_Warning': 0, 'Weather_Condition': "Clear"},
        "road": {'Surface_Type': "Asphalt", 'Surface_Condition': "Wet", 'Pothole_Density': 0.3, 'Slope_Angle_Degrees': 5,
                 'Traffic_Density': 0.7, 'Flood_Level_m': 0.1, 'Access_Status': "Open", 'Dust_Level_PPM': 45,
                 'Ground_Vibration_mm_s': 2.1, 'Road_Temperature_C': 35, 'Rainfall_mm': 4.5, 'Soil_Moisture_%': 35,
                 'Maintenance_Activity': "None", 'Accident_Count': 1},
    }
