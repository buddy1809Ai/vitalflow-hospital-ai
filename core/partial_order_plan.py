"""
partial_order_plan.py
=====================
Implementation of Partial Order Planning (POP) with Causal Links, Preconditions,
and Topological Linearization for Emergency Surgical & Trauma Resuscitation.

Directly maps to AI Lab Syllabus:
- Practical 10: Kitchen Task Planner for Anaya (Partial Order Planning)
"""

from typing import Dict, List, Set, Tuple, Any

class PlanAction:
    def __init__(self, action_id: str, name: str, duration_min: int, preconditions: List[str], effects: List[str], team: str):
        self.action_id = action_id
        self.name = name
        self.duration_min = duration_min
        self.preconditions = set(preconditions)
        self.effects = set(effects)
        self.team = team

class PartialOrderPlanner:
    """
    Partial Order Planner (POP):
    Instead of rigid single-threaded sequencing, POP maintains:
    - Actions (Steps)
    - Causal Links: Step_A --(achieves effect 'p')--> Step_B
    - Ordering Constraints: Step_A < Step_B
    - Open Preconditions: Conditions required by steps not yet satisfied.
    
    Allows simultaneous execution by different medical teams (e.g., Nursing, Anesthesia, Surgery).
    """
    def __init__(self):
        self.actions: Dict[str, PlanAction] = self._init_trauma_protocol()

    def _init_trauma_protocol(self) -> Dict[str, PlanAction]:
        return {
            "START": PlanAction(
                action_id="START",
                name="Patient Arrival at Trauma Resuscitation Bay",
                duration_min=0,
                preconditions=[],
                effects=["patient_on_stretcher", "trauma_alert_broadcast"],
                team="Triage Nursing"
            ),
            "IV_ACCESS": PlanAction(
                action_id="IV_ACCESS",
                name="Establish Two Large-Bore Peripheral IV Lines",
                duration_min=4,
                preconditions=["patient_on_stretcher"],
                effects=["iv_access_secured"],
                team="Resus Nurse Alpha"
            ),
            "BLOOD_DRAW": PlanAction(
                action_id="BLOOD_DRAW",
                name="Emergency Blood Draw & Cross-Match 4 Units PRBC",
                duration_min=6,
                preconditions=["iv_access_secured"],
                effects=["blood_crossmatched", "type_specific_blood_available"],
                team="Blood Bank Tech"
            ),
            "AIRWAY_INTUBATION": PlanAction(
                action_id="AIRWAY_INTUBATION",
                name="Rapid Sequence Intubation & Mechanical Ventilation",
                duration_min=8,
                preconditions=["iv_access_secured"],
                effects=["airway_protected", "mechanical_ventilation_active"],
                team="Anesthesiologist"
            ),
            "STERILIZE_INSTRUMENTS": PlanAction(
                action_id="STERILIZE_INSTRUMENTS",
                name="Sterilize Laparotomy Trays & Verify Hemostatic Staplers",
                duration_min=10,
                preconditions=["trauma_alert_broadcast"],
                effects=["surgical_instruments_sterile"],
                team="Scrub Nurse"
            ),
            "PATIENT_SURG_PREP": PlanAction(
                action_id="PATIENT_SURG_PREP",
                name="ChloraPrep Skin Antisepsis & Sterile Draping",
                duration_min=5,
                preconditions=["airway_protected"],
                effects=["sterile_surgical_field_ready"],
                team="Surgical Assistant"
            ),
            "EMERGENCY_LAPAROTOMY": PlanAction(
                action_id="EMERGENCY_LAPAROTOMY",
                name="Emergency Exploratory Laparotomy & Splenic Hemostasis",
                duration_min=35,
                preconditions=[
                    "airway_protected",
                    "sterile_surgical_field_ready",
                    "surgical_instruments_sterile",
                    "type_specific_blood_available"
                ],
                effects=["active_hemorrhage_controlled", "surgical_hemostasis_achieved"],
                team="Trauma Surgeon"
            ),
            "FINISH": PlanAction(
                action_id="FINISH",
                name="Transfer to Surgical Intensive Care Unit (SICU)",
                duration_min=0,
                preconditions=["surgical_hemostasis_achieved"],
                effects=["patient_transferred_to_sicu"],
                team="SICU Transport Team"
            )
        }

    def generate_plan(self) -> Dict[str, Any]:
        """
        Synthesizes causal links and ordering constraints to resolve all open preconditions.
        Performs topological sorting to generate parallel execution phases.
        """
        causal_links = []
        ordering_constraints = set()

        # Step 1: Match preconditions to achieving actions
        for act_id, act in self.actions.items():
            if act_id == "START":
                continue
            for pre in act.preconditions:
                # Find an action that produces this effect
                found_producer = None
                for candidate_id, candidate in self.actions.items():
                    if candidate_id != act_id and pre in candidate.effects:
                        found_producer = candidate_id
                        break
                if found_producer:
                    causal_links.append({
                        "from_action": found_producer,
                        "from_name": self.actions[found_producer].name,
                        "condition": pre,
                        "to_action": act_id,
                        "to_name": act.name
                    })
                    ordering_constraints.add((found_producer, act_id))

        # Step 2: Compute in-degree for topological linearization
        all_action_ids = list(self.actions.keys())
        in_degree = {act_id: 0 for act_id in all_action_ids}
        adj_list: Dict[str, List[str]] = {act_id: [] for act_id in all_action_ids}

        for u, v in ordering_constraints:
            adj_list[u].append(v)
            in_degree[v] += 1

        # Kahn's Algorithm for Topological Linearization grouped into parallel execution tiers
        queue = [act_id for act_id in all_action_ids if in_degree[act_id] == 0]
        tiers: List[List[Dict[str, Any]]] = []
        linearized_order = []
        
        while queue:
            current_tier = []
            next_queue = []
            for act_id in queue:
                linearized_order.append(act_id)
                current_tier.append({
                    "action_id": act_id,
                    "name": self.actions[act_id].name,
                    "team": self.actions[act_id].team,
                    "duration_min": self.actions[act_id].duration_min,
                    "preconditions": list(self.actions[act_id].preconditions),
                    "effects": list(self.actions[act_id].effects)
                })
                for nxt in adj_list[act_id]:
                    in_degree[nxt] -= 1
                    if in_degree[nxt] == 0:
                        next_queue.append(nxt)
            tiers.append(current_tier)
            queue = next_queue

        # Critical Path calculation (sum of longest chain of durations)
        total_time_estimate = sum(max(step["duration_min"] for step in tier) for tier in tiers)

        return {
            "plan_type": "Partial Order Plan (Non-Linear Parallel Scheduling)",
            "total_actions": len(self.actions),
            "causal_links": causal_links,
            "ordering_constraints_count": len(ordering_constraints),
            "execution_tiers": tiers,
            "linearized_sequence": linearized_order,
            "estimated_critical_path_minutes": total_time_estimate
        }
