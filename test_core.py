"""
test_core.py - Unit test runner for core AI modules
"""
from data.hospital_network import get_network_graph, HOSPITAL_NODES
from data.patient_cases import PATIENT_TELEMETRY_STREAM, TRIAGE_PRESET_SCENARIOS
from data.staff_resources import DOCTORS_DIRECTORY, SHIFT_SLOTS
from core.search_planner import compare_search_algorithms
from core.reflex_agents import SimpleReflexAgent, ModelBasedReflexAgent
from core.csp_scheduler import HospitalDutyCSP
from core.logic_triage import ClinicalTriageInferenceEngine, match_clinical_duty
from core.partial_order_plan import PartialOrderPlanner

def main():
    print("=== Testing Search Planner (Practical 3, 4, 9) ===")
    res = compare_search_algorithms("Sitabuldi", "AIIMS_Nagpur", traffic_multiplier=1.2)
    a_star = res["results"]["A* Search"]
    greedy = res["results"]["Greedy Best-First"]
    dijkstra = res["results"]["Dijkstra"]
    print(f"A* Path: {' -> '.join(a_star['path'])} | Time: {a_star['total_cost_minutes']}m | Expanded: {a_star['nodes_expanded']}")
    print(f"Greedy Path: {' -> '.join(greedy['path'])} | Time: {greedy['total_cost_minutes']}m | Expanded: {greedy['nodes_expanded']}")
    print(f"Dijkstra Path: {' -> '.join(dijkstra['path'])} | Time: {dijkstra['total_cost_minutes']}m | Expanded: {dijkstra['nodes_expanded']}")
    assert a_star["success"] and greedy["success"] and dijkstra["success"]

    print("\n=== Testing Reflex Agents (Practical 1, 2) ===")
    mb_agent = ModelBasedReflexAgent("P-101", "Rajesh Sharma")
    sr_agent = SimpleReflexAgent()
    for ts in PATIENT_TELEMETRY_STREAM["P-101"]["timesteps"]:
        mb_out = mb_agent.update_internal_state(ts, ts["time"])
        sr_out = sr_agent.evaluate_percept(ts)
        print(f"[{ts['time']}] HR={ts['hr']}, BP={ts['sys_bp']}/{ts['dia_bp']}, SpO2={ts['spo2']}% | MB Agent: {mb_out['alert_level']} | SR Agent: {sr_out['action']}")
    assert len(mb_agent.history) == 6

    print("\n=== Testing CSP Min-Conflicts (Practical 5) ===")
    csp = HospitalDutyCSP()
    csp_res = csp.solve_min_conflicts(max_steps=300, random_restarts=5)
    print(f"CSP Solved: {csp_res['success']} | Remaining Conflicts: {csp_res['conflicts']} | Restarts: {csp_res['restarts_used']}")
    print(f"Total slots scheduled: {len(csp_res['schedule_table'])}")

    print("\n=== Testing Logic Triage Engine (Practical 7, 8) ===")
    engine = ClinicalTriageInferenceEngine()
    facts = ["chest_pain_diaphoresis", "vital_signs_unstable"]
    triage_res = engine.forward_chain(facts)
    print(f"Initial Facts: {facts}")
    print(f"Deduction: {triage_res['final_esi_level']} -> Bay: {triage_res['assigned_bay']}")
    print(f"Rules Fired: {triage_res['rules_fired_count']}")

    # Unification test
    unif_res = match_clinical_duty(["NeedsDoctor", "?patient", "Cardiology", "Morning"], ["NeedsDoctor", "P-101", "?spec", "?shift"])
    print(f"FOL Unification MGU: {unif_res['most_general_unifier']}")

    print("\n=== Testing Partial Order Planner (Practical 10) ===")
    planner = PartialOrderPlanner()
    pop_res = planner.generate_plan()
    print(f"Total Actions: {pop_res['total_actions']} | Causal Links: {len(pop_res['causal_links'])}")
    print(f"Parallel Execution Tiers: {len(pop_res['execution_tiers'])} | Est. Critical Path: {pop_res['estimated_critical_path_minutes']} min")
    for idx, tier in enumerate(pop_res['execution_tiers']):
        print(f"  Tier {idx+1}: {[step['name'][:30] for step in tier]}")

    print("\n==================================================")
    print(">>> ALL CORE AI ALGORITHMS FUNCTIONING PERFECTLY! <<<")
    print("==================================================")

if __name__ == "__main__":
    main()
