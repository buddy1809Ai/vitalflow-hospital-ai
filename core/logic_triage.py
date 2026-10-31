"""
logic_triage.py
================
Implementation of Propositional Logic, Horn-Clause Forward Chaining Inference,
and First-Order Logic Unification for Emergency Patient Triage & Ward Routing.

Directly maps to AI Lab Syllabus:
- Practical 7: Smart Garden System (Propositional Logic & Inference)
- Practical 8: Assistant Bot using Unification (First-Order Logic - Unification)
"""

from typing import Dict, List, Set, Tuple, Any, Optional

class PropositionalRule:
    """Represents a Definite Horn Clause: Antecedent_1 AND Antecedent_2 ... => Consequent"""
    def __init__(self, antecedents: List[str], consequent: str, rule_name: str, explanation: str):
        self.antecedents = set(antecedents)
        self.consequent = consequent
        self.rule_name = rule_name
        self.explanation = explanation

    def can_fire(self, known_facts: Set[str]) -> bool:
        return self.antecedents.issubset(known_facts)

class ClinicalTriageInferenceEngine:
    """
    Forward-Chaining Inference Engine on Propositional Horn Clauses.
    Deduces emergency acuity (ESI-1 to ESI-5), required intervention,
    and target hospital bay with step-by-step logical proof trace.
    """
    def __init__(self):
        self.rules: List[PropositionalRule] = self._init_knowledge_base()

    def _init_knowledge_base(self) -> List[PropositionalRule]:
        return [
            # Level 1: Resuscitation (Immediate Life Threat)
            PropositionalRule(
                antecedents=["severe_airway_compromise"],
                consequent="immediate_life_threat",
                rule_name="R1_AirwayToThreat",
                explanation="Severe airway compromise prevents oxygenation, causing immediate life threat."
            ),
            PropositionalRule(
                antecedents=["active_massive_hemorrhage"],
                consequent="immediate_life_threat",
                rule_name="R2_BleedToThreat",
                explanation="Massive arterial/venous hemorrhage induces rapid exsanguination and circulatory collapse."
            ),
            PropositionalRule(
                antecedents=["immediate_life_threat"],
                consequent="ESI_LEVEL_1_RESUSCITATION",
                rule_name="R3_ThreatToESI1",
                explanation="Immediate life threat mandates Emergency Severity Index Level 1 (Zero-minute delay)."
            ),
            PropositionalRule(
                antecedents=["ESI_LEVEL_1_RESUSCITATION"],
                consequent="ROUTE_TO_RESUS_BAY_ALPHA",
                rule_name="R4_ESI1ToBay",
                explanation="Level 1 patients are routed directly to Resuscitation Bay Alpha with Crash Team."
            ),

            # Level 2: Emergent (High Risk / Time Sensitive)
            PropositionalRule(
                antecedents=["chest_pain_diaphoresis", "vital_signs_unstable"],
                consequent="acute_coronary_syndrome",
                rule_name="R5_ChestPainToACS",
                explanation="Chest pain with diaphoresis and vital instability indicates acute coronary syndrome (MI)."
            ),
            PropositionalRule(
                antecedents=["acute_coronary_syndrome"],
                consequent="ESI_LEVEL_2_EMERGENT",
                rule_name="R6_ACSToESI2",
                explanation="Acute Coronary Syndrome requires immediate emergency ECG and Cath Lab readiness (Level 2)."
            ),
            PropositionalRule(
                antecedents=["suspected_stroke_symptoms"],
                consequent="emergent_neuro_window",
                rule_name="R7_StrokeToNeuroWindow",
                explanation="Acute focal neurological deficit suggests ischemic stroke within thrombolysis window."
            ),
            PropositionalRule(
                antecedents=["emergent_neuro_window"],
                consequent="ESI_LEVEL_2_EMERGENT",
                rule_name="R8_NeuroToESI2",
                explanation="Time-critical stroke protocol requires emergency CT and neurology consultation (Level 2)."
            ),
            PropositionalRule(
                antecedents=["ESI_LEVEL_2_EMERGENT"],
                consequent="ROUTE_TO_CRITICAL_CARE_BAY",
                rule_name="R9_ESI2ToBay",
                explanation="Level 2 patients assigned to Critical Care Bay with continuous cardiac telemetry."
            ),

            # Level 3: Urgent (Multiple Diagnostic Resources Needed, Stable Vitals)
            PropositionalRule(
                antecedents=["high_fever_lethargy"],
                consequent="systemic_infection_workup",
                rule_name="R10_FeverToInfection",
                explanation="High-grade fever with systemic lethargy requires blood cultures and IV antibiotics."
            ),
            PropositionalRule(
                antecedents=["systemic_infection_workup"],
                consequent="ESI_LEVEL_3_URGENT",
                rule_name="R11_InfectionToESI3",
                explanation="Patient requires 2 or more diagnostic resources (Lab + IV hydration), classified as ESI Level 3."
            ),
            PropositionalRule(
                antecedents=["ESI_LEVEL_3_URGENT"],
                consequent="ROUTE_TO_URGENT_OBSERVATION_BAY",
                rule_name="R12_ESI3ToBay",
                explanation="Level 3 patients routed to Urgent Observation Unit (doctor review within 30 min)."
            ),

            # Level 5: Non-Urgent
            PropositionalRule(
                antecedents=["mild_abrasion"],
                consequent="ESI_LEVEL_5_NON_URGENT",
                rule_name="R13_AbrasionToESI5",
                explanation="Superficial injury with normal baseline requires simple dressing only."
            ),
            PropositionalRule(
                antecedents=["ESI_LEVEL_5_NON_URGENT"],
                consequent="ROUTE_TO_FAST_TRACK_OPD",
                rule_name="R14_ESI5ToBay",
                explanation="Level 5 routed to Fast-Track Outpatient Clinic (no acute ER bed consumed)."
            )
        ]

    def forward_chain(self, initial_facts: List[str]) -> Dict[str, Any]:
        """
        Executes Forward Chaining Inference on propositional knowledge base.
        Returns all derived facts, firing trace, and inferred clinical decision.
        """
        known_facts = set(initial_facts)
        firing_history = []
        rules_fired = set()

        changed = True
        step = 1
        while changed:
            changed = False
            for rule in self.rules:
                if rule.rule_name not in rules_fired and rule.can_fire(known_facts):
                    rules_fired.add(rule.rule_name)
                    known_facts.add(rule.consequent)
                    firing_history.append({
                        "step": step,
                        "rule": rule.rule_name,
                        "antecedents": list(rule.antecedents),
                        "consequent": rule.consequent,
                        "explanation": rule.explanation
                    })
                    step += 1
                    changed = True

        # Extract conclusions
        esi_level = "ESI_LEVEL_4_SEMI_URGENT (Default Safe)"
        for f in known_facts:
            if "ESI_LEVEL_" in f:
                esi_level = f
                break

        assigned_bay = "GENERAL_EXAM_ROOM"
        for f in known_facts:
            if "ROUTE_TO_" in f:
                assigned_bay = f
                break

        return {
            "initial_facts": list(initial_facts),
            "derived_facts": list(known_facts),
            "firing_history": firing_history,
            "final_esi_level": esi_level,
            "assigned_bay": assigned_bay,
            "rules_fired_count": len(rules_fired)
        }


# --- First-Order Logic Unification Component (Practical 8) ---
def is_variable(term: Any) -> bool:
    """A logic term is a variable if it is a string starting with '?' or lowercase x, y, z."""
    return isinstance(term, str) and (term.startswith("?") or term in ["x", "y", "z"])

def unify_terms(x: Any, y: Any, subst: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """
    Standard Unification Algorithm for First-Order Logic expressions:
    Finds Most General Unifier (MGU) theta such that Subst(theta, x) == Subst(theta, y).
    """
    if subst is None:
        return None
    elif x == y:
        return subst
    elif is_variable(x):
        return unify_var(x, y, subst)
    elif is_variable(y):
        return unify_var(y, x, subst)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return None
        curr_subst = subst
        for xi, yi in zip(x, y):
            curr_subst = unify_terms(xi, yi, curr_subst)
            if curr_subst is None:
                return None
        return curr_subst
    else:
        return None

def unify_var(var: str, x: Any, subst: Dict[str, str]) -> Optional[Dict[str, str]]:
    if var in subst:
        return unify_terms(subst[var], x, subst)
    elif is_variable(x) and x in subst:
        return unify_terms(var, subst[x], subst)
    else:
        new_subst = dict(subst)
        new_subst[var] = x
        return new_subst

def match_clinical_duty(patient_predicate: List[str], doctor_predicate: List[str]) -> Dict[str, Any]:
    """
    Demonstrates First-Order Logic Unification for Clinical Care Matching:
    e.g., Target: NeedsDoctor(?patient, "Cardiology", ?shift)
          Candidate: AvailableDoctor("Dr. Meera Iyer", ?specialty, "Morning")
    """
    mgu = unify_terms(patient_predicate, doctor_predicate, {})
    return {
        "predicate_1": patient_predicate,
        "predicate_2": doctor_predicate,
        "unification_success": mgu is not None,
        "most_general_unifier": mgu if mgu is not None else "Unification Failed (No MGU)"
    }
