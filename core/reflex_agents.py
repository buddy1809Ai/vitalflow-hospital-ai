"""
reflex_agents.py
================
Implementation of Intelligent Agent Architectures for Clinical Telemetry Monitoring:
1. Simple Reflex Agent: Condition-Action rules based strictly on immediate percept.
2. Model-Based Reflex Agent: Maintains internal state, tracks temporal vital trends,
   detects multi-organ deterioration patterns, and eliminates false alarms.

Directly maps to AI Lab Syllabus:
- Practical 1: Smart Light Agent (Simple Reflex Agent)
- Practical 2: Hospital Patient Monitoring Agent (Model-Based Reflex Agent)
"""

from typing import Dict, List, Any, Optional
import numpy as np

class SimpleReflexAgent:
    """
    Simple Reflex Agent:
    Decides actions solely on the basis of the current percept (no memory of past states).
    Rules:
    - If HR > 120 or Sys_BP < 90 or SpO2 < 90: Alert Emergency Doctor!
    - Else: Maintain Routine Monitoring.
    """
    def __init__(self, agent_name: str = "SimpleReflexMonitor"):
        self.agent_name = agent_name

    def evaluate_percept(self, vitals: Dict[str, float]) -> Dict[str, Any]:
        hr = vitals.get("hr", 75)
        sys_bp = vitals.get("sys_bp", 120)
        spo2 = vitals.get("spo2", 98)
        temp = vitals.get("temp", 37.0)

        # Immediate threshold condition-action evaluation
        if hr > 130 or sys_bp < 85 or spo2 < 88:
            action = "CRITICAL_CODE_BLUE"
            message = "EMERGENCY: Immediate threshold breached! Dispatch Code Blue team!"
            severity = "CRITICAL"
        elif hr > 105 or sys_bp < 95 or spo2 < 92 or temp > 38.5:
            action = "ALERT_DOCTOR"
            message = "WARNING: Vital parameter outside normal boundary. Doctor alerted."
            severity = "HIGH"
        elif hr > 100 or sys_bp > 140 or spo2 < 94:
            action = "NOTIFY_NURSE"
            message = "CAUTION: Minor vital deviation observed. Nursing check requested."
            severity = "MODERATE"
        else:
            action = "CONTINUE_MONITORING"
            message = "NORMAL: Current vitals within standard acceptable baseline."
            severity = "NORMAL"

        return {
            "agent_type": "Simple Reflex Agent",
            "action": action,
            "severity": severity,
            "message": message,
            "has_memory": False,
            "reasoning": f"Evaluated current reading alone: HR={hr}, BP={sys_bp}, SpO2={spo2}%."
        }


class ModelBasedReflexAgent:
    """
    Model-Based Reflex Agent:
    Maintains an internal model of the world and a history of patient state transitions.
    Formula: State_{t+1} = Update_State(State_t, Action_t, Percept_{t+1}, Model)
    
    Capabilities:
    - Tracks rolling history of vitals across intervals.
    - Computes Shock Index (HR / Systolic BP), normal range 0.5 - 0.7.
    - Computes rate-of-change (slopes) for SpO2 and Blood Pressure.
    - Filters out single-spike transient anomalies (anxiety/motion artifacts).
    - Detects progressive Sepsis and Cushing's Triad (bradycardia + hypertension + bradypnea).
    """
    def __init__(self, patient_id: str, patient_name: str):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.history: List[Dict[str, Any]] = []
        self.internal_state: Dict[str, Any] = {
            "condition_trend": "STABLE",
            "consecutive_abnormal_intervals": 0,
            "shock_index": 0.65,
            "spo2_delta_last_step": 0.0,
            "active_alert_level": "LEVEL_0_GREEN",
            "suspected_syndrome": "None"
        }

    def reset_state(self):
        """Clears patient history and resets the agent's internal world model."""
        self.history.clear()
        self.internal_state = {
            "condition_trend": "STABLE",
            "consecutive_abnormal_intervals": 0,
            "shock_index": 0.65,
            "spo2_delta_last_step": 0.0,
            "active_alert_level": "LEVEL_0_GREEN",
            "suspected_syndrome": "None"
        }

    def update_internal_state(self, vitals: Dict[str, float], time_stamp: str) -> Dict[str, Any]:
        """
        Processes new percept, updates historical buffer, and recalculates internal model metrics.
        """
        hr = vitals.get("hr", 75.0)
        sys_bp = vitals.get("sys_bp", 120.0)
        dia_bp = vitals.get("dia_bp", 80.0)
        spo2 = vitals.get("spo2", 98.0)
        rr = vitals.get("rr", 16.0)
        temp = vitals.get("temp", 37.0)

        # 1. Compute physiological markers
        shock_index = round(hr / max(sys_bp, 1.0), 2)  # Normal: 0.5 - 0.7; > 0.9 = Occult Shock
        
        # 2. Compute deltas from previous inspection interval
        spo2_delta = 0.0
        hr_delta = 0.0
        sys_bp_delta = 0.0
        
        if self.history:
            prev_vitals = self.history[-1]["vitals"]
            spo2_delta = round(spo2 - prev_vitals["spo2"], 1)
            hr_delta = round(hr - prev_vitals["hr"], 1)
            sys_bp_delta = round(sys_bp - prev_vitals["sys_bp"], 1)

        # Record into history buffer
        record = {
            "step": len(self.history) + 1,
            "time": time_stamp,
            "vitals": vitals,
            "shock_index": shock_index,
            "spo2_delta": spo2_delta,
            "hr_delta": hr_delta,
            "sys_bp_delta": sys_bp_delta
        }
        self.history.append(record)

        # 3. Model-Based Pattern Recognition
        suspected_syndrome = "None"
        trend = "STABLE"
        
        # Pattern A: Progressive Septic Shock (Tachycardia + Hypotension + Hyperthermia + Elevated Shock Index)
        if shock_index >= 1.0 and temp >= 38.3:
            suspected_syndrome = "Severe Septic Shock Cascade"
            trend = "CRITICAL_DETERIORATION"
        # Pattern B: Cushing's Reflex / Raised ICP (Severe Bradycardia + Severe Hypertension + Bradypnea)
        elif hr < 55 and sys_bp > 165 and rr < 12:
            suspected_syndrome = "Cushing's Triad (Elevated Intracranial Pressure / Brain Herniation Risk)"
            trend = "ACUTE_NEURO_CRISIS"
        # Pattern C: Hypoxic Respiratory Failure (Steady SpO2 drop + Tachypnea)
        elif spo2 < 88 and rr >= 28:
            suspected_syndrome = "Hypoxic Respiratory Decompensation"
            trend = "RESPIRATORY_FAILURE"
        # Pattern D: Mild Progressive Drift
        elif (shock_index > 0.85 or spo2 < 93 or temp > 38.0) and len(self.history) >= 2:
            suspected_syndrome = "Borderline Hemodynamic Instability"
            trend = "DOWNWARD_DRIFT"
        # Pattern E: Transient Spike followed by Normalization (Handling Artifacts / Anxiety)
        elif len(self.history) >= 3 and abs(hr_delta) > 20 and 70 <= hr <= 90:
            suspected_syndrome = "Transient Stress Artifact (Resolved)"
            trend = "NORMALIZING"

        # Update consecutive abnormal counter
        if trend in ["CRITICAL_DETERIORATION", "ACUTE_NEURO_CRISIS", "RESPIRATORY_FAILURE"]:
            self.internal_state["consecutive_abnormal_intervals"] += 1
        elif trend == "DOWNWARD_DRIFT":
            self.internal_state["consecutive_abnormal_intervals"] += 1
        else:
            self.internal_state["consecutive_abnormal_intervals"] = max(0, self.internal_state["consecutive_abnormal_intervals"] - 1)

        # 4. Action Selection using Internal State + Rules
        if trend in ["CRITICAL_DETERIORATION", "ACUTE_NEURO_CRISIS", "RESPIRATORY_FAILURE"]:
            action = "DISPATCH_CRASH_CART_CODE_BLUE"
            alert_level = "LEVEL_3_RED"
            rationale = (f"CRITICAL: Agent internal state detected {suspected_syndrome}. "
                         f"Shock Index={shock_index} (Ref: 0.5-0.7). Immediate senior intervention mandated.")
        elif trend == "DOWNWARD_DRIFT" or self.internal_state["consecutive_abnormal_intervals"] >= 2:
            action = "URGENT_RESIDENT_PHYSICIAN_EVALUATION"
            alert_level = "LEVEL_2_ORANGE"
            rationale = (f"HIGH: Agent detected progressive downward drift across consecutive cycles. "
                         f"Sustained abnormal delta observed (SpO2={spo2}%, Shock Index={shock_index}).")
        elif trend == "NORMALIZING" or (hr > 100 and len(self.history) >= 2 and self.history[-2]["vitals"]["hr"] < 85):
            action = "MAINTAIN_NURSING_VIGILANCE"
            alert_level = "LEVEL_1_YELLOW"
            rationale = ("MODERATE: Transient spike detected. Memory model indicates prior baseline was normal. "
                         "Suppressing full Code Blue alarm to prevent alarm fatigue.")
        else:
            action = "ROUTINE_TELEMETRY_MONITORING"
            alert_level = "LEVEL_0_GREEN"
            rationale = "NORMAL: Patient physiological parameters stable within safe equilibrium envelope."

        self.internal_state.update({
            "condition_trend": trend,
            "shock_index": shock_index,
            "spo2_delta_last_step": spo2_delta,
            "active_alert_level": alert_level,
            "suspected_syndrome": suspected_syndrome
        })

        return {
            "agent_type": "Model-Based Reflex Agent",
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "time": time_stamp,
            "action": action,
            "alert_level": alert_level,
            "suspected_syndrome": suspected_syndrome,
            "trend": trend,
            "shock_index": shock_index,
            "rationale": rationale,
            "has_memory": True,
            "history_depth": len(self.history),
            "internal_state_snapshot": dict(self.internal_state)
        }
