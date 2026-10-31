"""
patient_cases.py
================
Clinical Telemetry & Emergency Triage Datasets for VitalFlow AI.
Supplies continuous time-series vitals for Model-Based Reflex Agents and
clinical symptom cases for Propositional Logic Triage Inference.
"""

from typing import Dict, List, Any

# Time-series telemetry streams for hospital ICU/HDU patients across 6 inspection intervals
PATIENT_TELEMETRY_STREAM: Dict[str, Dict[str, Any]] = {
    "P-101": {
        "name": "Rajesh Sharma (Age 54)",
        "bed": "ICU-Bed 04",
        "admit_diagnosis": "Post-Cholecystectomy / Suspected Sepsis",
        "timesteps": [
            {"time": "08:00", "hr": 84, "sys_bp": 122, "dia_bp": 78, "spo2": 98, "rr": 16, "temp": 37.1},
            {"time": "08:15", "hr": 92, "sys_bp": 114, "dia_bp": 72, "spo2": 97, "rr": 19, "temp": 37.6},
            {"time": "08:30", "hr": 108, "sys_bp": 105, "dia_bp": 68, "spo2": 95, "rr": 23, "temp": 38.3},
            {"time": "08:45", "hr": 122, "sys_bp": 94, "dia_bp": 60, "spo2": 93, "rr": 27, "temp": 38.9},
            {"time": "09:00", "hr": 134, "sys_bp": 82, "dia_bp": 52, "spo2": 90, "rr": 31, "temp": 39.4},
            {"time": "09:15", "hr": 142, "sys_bp": 74, "dia_bp": 48, "spo2": 87, "rr": 34, "temp": 39.8}
        ],
        "expected_progression": "Septic Shock Cascade (Rapid Multiorgan Deterioration)"
    },
    "P-102": {
        "name": "Sunita Patil (Age 68)",
        "bed": "HDU-Bed 09",
        "admit_diagnosis": "Acute Exacerbation of COPD",
        "timesteps": [
            {"time": "08:00", "hr": 88, "sys_bp": 136, "dia_bp": 84, "spo2": 94, "rr": 20, "temp": 36.8},
            {"time": "08:15", "hr": 95, "sys_bp": 142, "dia_bp": 88, "spo2": 91, "rr": 24, "temp": 36.9},
            {"time": "08:30", "hr": 106, "sys_bp": 148, "dia_bp": 92, "spo2": 87, "rr": 28, "temp": 37.0},
            {"time": "08:45", "hr": 118, "sys_bp": 156, "dia_bp": 98, "spo2": 83, "rr": 33, "temp": 37.1},
            {"time": "09:00", "hr": 128, "sys_bp": 164, "dia_bp": 102, "spo2": 79, "rr": 38, "temp": 37.2},
            {"time": "09:15", "hr": 138, "sys_bp": 172, "dia_bp": 108, "spo2": 74, "rr": 42, "temp": 37.3}
        ],
        "expected_progression": "Hypoxic Respiratory Arrest Risk"
    },
    "P-103": {
        "name": "Anil Deshmukh (Age 42)",
        "bed": "General Ward 12",
        "admit_diagnosis": "Mild Viral Pyrexia & Anxiety",
        "timesteps": [
            {"time": "08:00", "hr": 76, "sys_bp": 118, "dia_bp": 76, "spo2": 99, "rr": 15, "temp": 36.9},
            {"time": "08:15", "hr": 112, "sys_bp": 138, "dia_bp": 86, "spo2": 98, "rr": 18, "temp": 37.0},  # Transient anxiety spike
            {"time": "08:30", "hr": 84, "sys_bp": 124, "dia_bp": 80, "spo2": 98, "rr": 16, "temp": 36.9},   # Normalizes
            {"time": "08:45", "hr": 78, "sys_bp": 120, "dia_bp": 78, "spo2": 99, "rr": 15, "temp": 36.8},
            {"time": "09:00", "hr": 74, "sys_bp": 118, "dia_bp": 76, "spo2": 99, "rr": 14, "temp": 36.8},
            {"time": "09:15", "hr": 75, "sys_bp": 119, "dia_bp": 77, "spo2": 99, "rr": 15, "temp": 36.7}
        ],
        "expected_progression": "Transient Benign Fluctuation (No Code Blue Needed)"
    },
    "P-104": {
        "name": "Kavita Rao (Age 29)",
        "bed": "Trauma-Bay 02",
        "admit_diagnosis": "Closed Head Injury / Road Accident",
        "timesteps": [
            {"time": "08:00", "hr": 72, "sys_bp": 124, "dia_bp": 80, "spo2": 98, "rr": 16, "temp": 36.7},
            {"time": "08:15", "hr": 68, "sys_bp": 134, "dia_bp": 82, "spo2": 98, "rr": 15, "temp": 36.7},
            {"time": "08:30", "hr": 60, "sys_bp": 152, "dia_bp": 88, "spo2": 97, "rr": 13, "temp": 36.6},
            {"time": "08:45", "hr": 52, "sys_bp": 174, "dia_bp": 94, "spo2": 96, "rr": 11, "temp": 36.5},  # Cushing's Triad begins
            {"time": "09:00", "hr": 46, "sys_bp": 192, "dia_bp": 100, "spo2": 94, "rr": 9, "temp": 36.5},
            {"time": "09:15", "hr": 42, "sys_bp": 210, "dia_bp": 106, "spo2": 91, "rr": 8, "temp": 36.4}
        ],
        "expected_progression": "Severe Increased ICP (Cushing's Reflex: Severe Bradycardia + Hypertension)"
    }
}

# Clinical emergency symptom scenarios for Propositional Logic & Horn Clause Inference
TRIAGE_PRESET_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "Major Highway Polytrauma": {
        "severe_airway_compromise": True,
        "active_massive_hemorrhage": True,
        "altered_mental_status": True,
        "chest_pain_diaphoresis": False,
        "high_fever_lethargy": False,
        "mild_abrasion": False,
        "vital_signs_unstable": True,
        "suspected_stroke_symptoms": False
    },
    "Acute ST-Elevation Myocardial Infarction (STEMI)": {
        "severe_airway_compromise": False,
        "active_massive_hemorrhage": False,
        "altered_mental_status": False,
        "chest_pain_diaphoresis": True,
        "high_fever_lethargy": False,
        "mild_abrasion": False,
        "vital_signs_unstable": True,
        "suspected_stroke_symptoms": False
    },
    "Acute Ischemic Stroke (Golden Hour Window)": {
        "severe_airway_compromise": False,
        "active_massive_hemorrhage": False,
        "altered_mental_status": True,
        "chest_pain_diaphoresis": False,
        "high_fever_lethargy": False,
        "mild_abrasion": False,
        "vital_signs_unstable": False,
        "suspected_stroke_symptoms": True
    },
    "Pediatric High-Grade Febrile Infection": {
        "severe_airway_compromise": False,
        "active_massive_hemorrhage": False,
        "altered_mental_status": False,
        "chest_pain_diaphoresis": False,
        "high_fever_lethargy": True,
        "mild_abrasion": False,
        "vital_signs_unstable": False,
        "suspected_stroke_symptoms": False
    },
    "Outpatient Minor Sprain / Superficial Laceration": {
        "severe_airway_compromise": False,
        "active_massive_hemorrhage": False,
        "altered_mental_status": False,
        "chest_pain_diaphoresis": False,
        "high_fever_lethargy": False,
        "mild_abrasion": True,
        "vital_signs_unstable": False,
        "suspected_stroke_symptoms": False
    }
}
