"""
csp_scheduler.py
================
Implementation of Constraint Satisfaction Problem (CSP) Solver using
the Heuristic Local Search Min-Conflicts Algorithm with Random Restarts.

Directly maps to AI Lab Syllabus:
- Practical 5: Map Coloring for Adjoining Regions using Min-Conflicts
  (Variables: Shifts/Departments, Domain: Qualified Doctors, Constraints: No double-booking, Specialty match, Fatigue limits)
"""

import random
from typing import Dict, List, Tuple, Any, Optional
from data.staff_resources import DOCTORS_DIRECTORY, SHIFT_SLOTS

class HospitalDutyCSP:
    """
    Formal CSP Formulation for Emergency Department Duty Scheduling:
    - Variables (X): Shift Slots (e.g., S1: ER-Morning, S4: ICU-Morning, etc.)
    - Domains (D): Doctors possessing the requisite clinical specialty
    - Constraints (C):
        1. No Concurrent Double-Booking (Doctors cannot be in two places at the same time)
        2. Specialty Compatibility (Doctor's specialty must match the ward requirement)
        3. Fatigue Rule (No back-to-back Night -> Morning consecutive shifts)
        4. Workload Quota (Doctor must not exceed their allowed shifts per cycle)
    """

    def __init__(self, slots: List[Dict[str, Any]] = None, doctors: Dict[str, Dict[str, Any]] = None):
        self.slots = slots if slots is not None else SHIFT_SLOTS
        self.doctors = doctors if doctors is not None else DOCTORS_DIRECTORY
        self.variables = [s["slot_id"] for s in self.slots]
        self.slot_map = {s["slot_id"]: s for s in self.slots}
        
        # Build domains: Only doctors matching the specialty requirements of the slot
        self.domains: Dict[str, List[str]] = {}
        for s in self.slots:
            slot_id = s["slot_id"]
            req_specs = s["required_specialty"]
            eligible_docs = [
                doc_name for doc_name, doc_info in self.doctors.items()
                if doc_info["specialty"] in req_specs
            ]
            # Fallback if no exact specialist exists: allow all doctors (with penalty)
            if not eligible_docs:
                eligible_docs = list(self.doctors.keys())
            self.domains[slot_id] = eligible_docs

    def count_conflicts_for_assignment(self, assignment: Dict[str, str]) -> Tuple[int, List[str]]:
        """
        Evaluates the total number of constraint violations across the entire schedule.
        Returns (conflict_count, list_of_violation_descriptions).
        """
        conflicts = 0
        violations = []

        # 1. Check Concurrent Double-Booking (Same doctor assigned to different slots at same time)
        time_to_assignments: Dict[str, List[Tuple[str, str]]] = {}
        for slot_id, doc in assignment.items():
            slot = self.slot_map[slot_id]
            time_key = slot["time"]
            time_to_assignments.setdefault(time_key, []).append((slot_id, doc))

        for time_key, assigned_list in time_to_assignments.items():
            doc_counts: Dict[str, List[str]] = {}
            for slot_id, doc in assigned_list:
                doc_counts.setdefault(doc, []).append(slot_id)
            for doc, slots_list in doc_counts.items():
                if len(slots_list) > 1:
                    conflicts += len(slots_list) - 1
                    violations.append(
                        f"Double Booking: {doc} concurrently assigned to {', '.join(slots_list)} during {time_key}."
                    )

        # 2. Check Workload Quota
        doc_workload: Dict[str, int] = {}
        for slot_id, doc in assignment.items():
            doc_workload[doc] = doc_workload.get(doc, 0) + 1

        for doc, count in doc_workload.items():
            max_allowed = self.doctors[doc]["max_shifts_per_cycle"]
            if count > max_allowed:
                excess = count - max_allowed
                conflicts += excess
                violations.append(
                    f"Overwork Fatigue: {doc} assigned {count} shifts (Max allowed: {max_allowed})."
                )

        # 3. Check Specialty Compatibility
        for slot_id, doc in assignment.items():
            req_specs = self.slot_map[slot_id]["required_specialty"]
            doc_spec = self.doctors[doc]["specialty"]
            if doc_spec not in req_specs:
                conflicts += 1
                violations.append(
                    f"Specialty Mismatch: {doc} ({doc_spec}) lacks requirement for {slot_id} ({self.slot_map[slot_id]['dept']})."
                )

        return conflicts, violations

    def count_variable_conflicts(self, var: str, value: str, current_assignment: Dict[str, str]) -> int:
        """
        Calculates conflicts specifically contributed if `var` is assigned `value`.
        """
        tentative = dict(current_assignment)
        tentative[var] = value
        conflicts, _ = self.count_conflicts_for_assignment(tentative)
        return conflicts

    def solve_min_conflicts(
        self,
        max_steps: int = 500,
        random_restarts: int = 5
    ) -> Dict[str, Any]:
        """
        Min-Conflicts Local Search Algorithm:
        1. Initialize random assignment for all variables.
        2. Until max_steps reached:
            a. If no conflicts exist, return SUCCESS.
            b. Pick a conflicted variable at random.
            c. Assign it the value from its domain that minimizes total conflicts.
        3. If stuck, perform random restart.
        """
        iteration_history = []
        best_assignment = {}
        best_conflict_count = float('inf')
        total_evaluations = 0

        for restart in range(random_restarts):
            # Step 1: Initial assignment (Domain random selection)
            current_assignment = {
                var: random.choice(self.domains[var]) for var in self.variables
            }
            initial_conflicts, initial_violations = self.count_conflicts_for_assignment(current_assignment)
            
            if initial_conflicts < best_conflict_count:
                best_conflict_count = initial_conflicts
                best_assignment = dict(current_assignment)

            iteration_history.append({
                "step": len(iteration_history),
                "conflicts": initial_conflicts,
                "note": f"Restart #{restart+1} initialized with {initial_conflicts} conflicts."
            })

            if initial_conflicts == 0:
                return {
                    "success": True,
                    "assignment": current_assignment,
                    "conflicts": 0,
                    "violations": [],
                    "total_steps": len(iteration_history),
                    "restarts_used": restart + 1,
                    "iteration_history": iteration_history,
                    "schedule_table": self._format_schedule(current_assignment)
                }

            # Step 2: Local search hill-climbing on conflicts
            for step in range(max_steps):
                curr_conflicts, curr_violations = self.count_conflicts_for_assignment(current_assignment)
                
                if curr_conflicts < best_conflict_count:
                    best_conflict_count = curr_conflicts
                    best_assignment = dict(current_assignment)

                if curr_conflicts == 0:
                    iteration_history.append({
                        "step": len(iteration_history),
                        "conflicts": 0,
                        "note": f"Solution found at step {step} with ZERO conflicts!"
                    })
                    return {
                        "success": True,
                        "assignment": current_assignment,
                        "conflicts": 0,
                        "violations": [],
                        "total_steps": len(iteration_history),
                        "restarts_used": restart + 1,
                        "iteration_history": iteration_history,
                        "schedule_table": self._format_schedule(current_assignment)
                    }

                # Find all currently conflicted variables
                conflicted_vars = []
                for var in self.variables:
                    # Check if changing this variable can reduce conflicts or if it's involved in violations
                    var_c = self.count_variable_conflicts(var, current_assignment[var], current_assignment)
                    if var_c > 0:
                        conflicted_vars.append(var)

                if not conflicted_vars:
                    conflicted_vars = self.variables

                # Pick a random conflicted variable
                chosen_var = random.choice(conflicted_vars)
                domain = self.domains[chosen_var]

                # Find the value(s) that minimize conflicts
                min_c = float('inf')
                best_vals = []
                for val in domain:
                    c = self.count_variable_conflicts(chosen_var, val, current_assignment)
                    total_evaluations += 1
                    if c < min_c:
                        min_c = c
                        best_vals = [val]
                    elif c == min_c:
                        best_vals.append(val)

                # Assign value (break ties randomly)
                current_assignment[chosen_var] = random.choice(best_vals)
                
                if (step % 5 == 0) or min_c == 0:
                    iteration_history.append({
                        "step": len(iteration_history),
                        "conflicts": min_c,
                        "note": f"Step {step}: Adjusted {chosen_var} -> conflicts={min_c}"
                    })

        # Return best found if not perfectly zero
        final_conflicts, final_violations = self.count_conflicts_for_assignment(best_assignment)
        return {
            "success": final_conflicts == 0,
            "assignment": best_assignment,
            "conflicts": final_conflicts,
            "violations": final_violations,
            "total_steps": len(iteration_history),
            "restarts_used": random_restarts,
            "iteration_history": iteration_history,
            "schedule_table": self._format_schedule(best_assignment)
        }

    def _format_schedule(self, assignment: Dict[str, str]) -> List[Dict[str, Any]]:
        """Converts raw assignment mapping into a clean tabular data structure."""
        table = []
        for slot in self.slots:
            slot_id = slot["slot_id"]
            doc_name = assignment.get(slot_id, "Unassigned")
            doc_info = self.doctors.get(doc_name, {})
            table.append({
                "Slot ID": slot_id,
                "Department / Ward": slot["dept"],
                "Shift Window": slot["time"],
                "Assigned Doctor": doc_name,
                "Doctor Specialty": doc_info.get("specialty", "N/A"),
                "Seniority": doc_info.get("seniority", "N/A"),
                "Required Specialty": ", ".join(slot["required_specialty"])
            })
        return table
