"""
staff_resources.py
==================
Hospital Staffing, Department, and Shift Metadata for Constraint Satisfaction (CSP).
Used by the Min-Conflicts Algorithm to resolve multi-department medical duty scheduling.
"""

from typing import Dict, List, Any

# Medical Staff Directory
DOCTORS_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "Dr. Kulkarni": {
        "id": "DOC-01",
        "name": "Dr. Ramesh Kulkarni",
        "specialty": "Trauma & General Surgery",
        "seniority": "Senior Consultant",
        "max_shifts_per_cycle": 2
    },
    "Dr. Ananya Sen": {
        "id": "DOC-02",
        "name": "Dr. Ananya Sen",
        "specialty": "Critical Care / Intensivist",
        "seniority": "Senior Consultant",
        "max_shifts_per_cycle": 2
    },
    "Dr. Farhan Khan": {
        "id": "DOC-03",
        "name": "Dr. Farhan Khan",
        "specialty": "Emergency Medicine",
        "seniority": "Attending Physician",
        "max_shifts_per_cycle": 3
    },
    "Dr. Meera Iyer": {
        "id": "DOC-04",
        "name": "Dr. Meera Iyer",
        "specialty": "Interventional Cardiology",
        "seniority": "Senior Consultant",
        "max_shifts_per_cycle": 2
    },
    "Dr. Vikram Joshi": {
        "id": "DOC-05",
        "name": "Dr. Vikram Joshi",
        "specialty": "Neuro-Trauma",
        "seniority": "Consultant",
        "max_shifts_per_cycle": 2
    },
    "Dr. Tanvi Deshpande": {
        "id": "DOC-06",
        "name": "Dr. Tanvi Deshpande",
        "specialty": "Emergency Medicine",
        "seniority": "Attending Physician",
        "max_shifts_per_cycle": 3
    },
    "Dr. Rohan Verma": {
        "id": "DOC-07",
        "name": "Dr. Rohan Verma",
        "specialty": "Internal Medicine",
        "seniority": "Junior Resident",
        "max_shifts_per_cycle": 2
    },
    "Dr. Sneha Pillai": {
        "id": "DOC-08",
        "name": "Dr. Sneha Pillai",
        "specialty": "Pediatrics / Neonatology",
        "seniority": "Consultant",
        "max_shifts_per_cycle": 2
    }
}

# Shift Slots to be scheduled (Variables in CSP)
# Each variable is a (Ward, Shift_Time) tuple
SHIFT_SLOTS: List[Dict[str, Any]] = [
    {"slot_id": "S1", "dept": "Emergency ER", "time": "Morning (08:00 - 16:00)", "required_specialty": ["Emergency Medicine", "Trauma & General Surgery"]},
    {"slot_id": "S2", "dept": "Emergency ER", "time": "Evening (16:00 - 00:00)", "required_specialty": ["Emergency Medicine", "Internal Medicine"]},
    {"slot_id": "S3", "dept": "Emergency ER", "time": "Night (00:00 - 08:00)", "required_specialty": ["Emergency Medicine", "Critical Care / Intensivist"]},
    {"slot_id": "S4", "dept": "ICU Apex", "time": "Morning (08:00 - 16:00)", "required_specialty": ["Critical Care / Intensivist", "Interventional Cardiology"]},
    {"slot_id": "S5", "dept": "ICU Apex", "time": "Evening (16:00 - 00:00)", "required_specialty": ["Critical Care / Intensivist"]},
    {"slot_id": "S6", "dept": "ICU Apex", "time": "Night (00:00 - 08:00)", "required_specialty": ["Critical Care / Intensivist", "Emergency Medicine"]},
    {"slot_id": "S7", "dept": "Trauma OT", "time": "Morning (08:00 - 16:00)", "required_specialty": ["Trauma & General Surgery", "Neuro-Trauma"]},
    {"slot_id": "S8", "dept": "Trauma OT", "time": "Evening (16:00 - 00:00)", "required_specialty": ["Trauma & General Surgery", "Neuro-Trauma"]},
    {"slot_id": "S9", "dept": "Cath Lab Cardiology", "time": "Morning (08:00 - 16:00)", "required_specialty": ["Interventional Cardiology"]},
    {"slot_id": "S10", "dept": "Pediatric ICU", "time": "Morning (08:00 - 16:00)", "required_specialty": ["Pediatrics / Neonatology", "Critical Care / Intensivist"]}
]
