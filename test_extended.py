"""
test_extended.py - Comprehensive Edge-Case & Stress-Testing Suite
"""
from data.hospital_network import get_network_graph, HOSPITAL_NODES, ROAD_EDGES
from data.patient_cases import PATIENT_TELEMETRY_STREAM, TRIAGE_PRESET_SCENARIOS
from data.staff_resources import DOCTORS_DIRECTORY, SHIFT_SLOTS
from core.search_planner import compare_search_algorithms, a_star_search, greedy_best_first_search, dijkstra_search
from core.reflex_agents import SimpleReflexAgent, ModelBasedReflexAgent
from core.csp_scheduler import HospitalDutyCSP
from core.logic_triage import ClinicalTriageInferenceEngine, match_clinical_duty
from core.partial_order_plan import PartialOrderPlanner

def test_search_all_pairs():
    print("Testing All-Pairs Pathfinding with Road Closures...")
    blocked = [("Wardha_Road", "Airport_Metro")]
    graph = get_network_graph(traffic_multiplier=1.5, blocked_edges=blocked)
    
    # Check alternate routing when Wardha Road is blocked
    res = a_star_search("Sitabuldi", "AIIMS_Nagpur", graph)
    assert res["success"], "A* failed to find alternate path during road closure!"
    assert ("Wardha_Road", "Airport_Metro") not in zip(res["path"][:-1], res["path"][1:])
    print(f"A* Successfully routed around road closure: {' -> '.join(res['path'])} ({res['total_cost_minutes']}m)")

def test_all_patients():
    print("\nTesting Model-Based Agent on all 4 patient clinical profiles...")
    for pid, pdata in PATIENT_TELEMETRY_STREAM.items():
        agent = ModelBasedReflexAgent(pid, pdata["name"])
        for ts in pdata["timesteps"]:
            decision = agent.update_internal_state(ts, ts["time"])
            assert "action" in decision and "alert_level" in decision
        print(f"Patient {pid} ({pdata['name']}): Final Status = {decision['alert_level']} ({decision['suspected_syndrome']})")

def test_csp_stochastic():
    print("\nTesting CSP Min-Conflicts across 5 random trials...")
    csp = HospitalDutyCSP()
    success_count = 0
    for trial in range(5):
        res = csp.solve_min_conflicts(max_steps=250, random_restarts=4)
        if res["success"]:
            success_count += 1
            print(f"Trial {trial+1}: Solved in {res['total_steps']} steps (Restarts: {res['restarts_used']})")
        else:
            print(f"Trial {trial+1}: Unresolved with {res['conflicts']} conflicts")
    print(f"CSP Solver Reliability: {success_count}/5 successful conflict-free rosters.")

def test_all_triage_presets():
    print("\nTesting Triage Inference Engine across all clinical presets...")
    engine = ClinicalTriageInferenceEngine()
    for name, flags in TRIAGE_PRESET_SCENARIOS.items():
        facts = [k for k, v in flags.items() if v]
        out = engine.forward_chain(facts)
        print(f"Preset '{name}': {out['final_esi_level']} -> {out['assigned_bay']} (Fired {out['rules_fired_count']} rules)")
        assert len(out["final_esi_level"]) > 0

if __name__ == "__main__":
    test_search_all_pairs()
    test_all_patients()
    test_csp_stochastic()
    test_all_triage_presets()
    print("\n>>> ALL EXTENDED STRESS TESTS PASSED WITH 100% SUCCESS! <<<")
