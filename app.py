"""
app.py
======
VitalFlow AI: Autonomous Hospital Operations & Emergency Logistics Platform
A clean, professional multi-agent decision support and state-space optimization system.

Architecture & Algorithms:
- Module 1: Heuristic State-Space Graph Search (A* Search vs Greedy Best-First)
- Module 2: Model-Based Reflex Agent with Internal Temporal State Vector
- Module 3: Constraint Satisfaction Problem (CSP) with Min-Conflicts Local Search
- Module 4: Propositional Horn-Clause Forward Chaining & FOL Unification
- Module 5: Partial Order Planning (POP) with Causal Preconditions
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Tuple

# UI / Styling imports
from ui.styles import get_custom_css
from ui.components import (
    render_top_header,
    render_kpi_cards,
    render_banner,
    render_syllabus_pill,
    render_academic_disclaimer
)
from ui.visualizers import (
    plot_hospital_network,
    plot_patient_telemetry,
    plot_csp_convergence,
    plot_partial_order_plan
)

# Core AI & Data imports
from data.hospital_network import HOSPITAL_NODES, ROAD_EDGES, get_network_graph
from data.patient_cases import PATIENT_TELEMETRY_STREAM, TRIAGE_PRESET_SCENARIOS
from data.staff_resources import DOCTORS_DIRECTORY, SHIFT_SLOTS
from core.search_planner import compare_search_algorithms, a_star_search, greedy_best_first_search, dijkstra_search
from core.reflex_agents import SimpleReflexAgent, ModelBasedReflexAgent
from core.csp_scheduler import HospitalDutyCSP
from core.logic_triage import ClinicalTriageInferenceEngine, match_clinical_duty
from core.partial_order_plan import PartialOrderPlanner

# Page Setup
st.set_page_config(
    page_title="VitalFlow AI — Hospital Operations Platform",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject SaaS Styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="width: 32px; height: 32px; border-radius: 8px; background: #0284c7; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem;">V</div>
        <div>
            <div style="font-weight: 700; font-size: 1.05rem; color: #0f172a; line-height: 1.1;">VitalFlow AI</div>
            <div style="font-size: 0.75rem; color: #64748b;">Operations Command</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        label="Main Navigation",
        options=[
            "Overview",
            "Emergency Route Planner",
            "Hospital Operations",
            "AI Insights & Algorithms"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: #475569; margin-bottom: 8px;'>ENVIRONMENT SETTINGS</div>", unsafe_allow_html=True)
    
    traffic_multiplier = st.select_slider(
        "Urban Traffic Congestion",
        options=[1.0, 1.2, 1.5, 2.0, 2.5],
        value=1.2,
        format_func=lambda x: f"{x}x {'(Standard)' if x==1.0 else '(Peak Rush)' if x>=2.0 else '(Moderate)'}"
    )

    simulate_road_closure = st.checkbox("Simulate Wardha Road Closure", value=False)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #94a3b8; line-height: 1.4;">
        <strong>System Status:</strong> Active Simulation<br>
        <strong>Region:</strong> Nagpur Healthcare Grid<br>
        <strong>Algorithms:</strong> A*, CSP, Reflex Agents, Horn Logic, POP
    </div>
    """, unsafe_allow_html=True)

# Top Executive Bar
render_top_header()


# =============================================================================
# SECTION 1: OVERVIEW / DASHBOARD
# =============================================================================
if nav_selection == "Overview":
    # Real metrics derived from data structures
    total_facilities = len(HOSPITAL_NODES)
    total_beds = sum(n["icu_beds"] for n in HOSPITAL_NODES.values())
    trauma_centers = sum(1 for n in HOSPITAL_NODES.values() if n["trauma_ready"])
    
    render_kpi_cards([
        {"label": "Network Facilities", "value": f"{total_facilities} Centers", "context": "Hospitals & Transit Outposts"},
        {"label": "Total ICU Beds", "value": f"{total_beds} Beds", "context": "Across Regional Network"},
        {"label": "Apex Trauma Bays", "value": f"{trauma_centers} Units", "context": "Critical Resuscitation Centers"},
        {"label": "Traffic Index", "value": f"{traffic_multiplier}x", "context": "Dynamic Congestion Factor"}
    ])

    st.write("")
    
    col_map, col_info = st.columns([1.8, 1])

    with col_map:
        st.markdown("""
        <div class="content-card">
            <div class="content-header">Nagpur Healthcare Transit Topology</div>
            <div class="content-sub">Interactive spatial map showing urban emergency facilities and transit corridors.</div>
        </div>
        """, unsafe_allow_html=True)

        blocked = [("Wardha_Road", "Airport_Metro")] if simulate_road_closure else []
        fig_overview = plot_hospital_network(blocked_edges=blocked)
        st.plotly_chart(fig_overview, use_container_width=True)

    with col_info:
        st.markdown("""
        <div class="content-card">
            <div class="content-header">System Architecture Summary</div>
            <div class="content-sub">Core decision-support capabilities active in this instance:</div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.88rem;">1. Ambulance Route Optimization</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">Informed A* search benchmarked against Greedy Best-First to guarantee minimal transit times during the emergency Golden Hour.</span>
            </div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.88rem;">2. ICU Patient Telemetry</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">Model-Based Reflex Agent tracking rolling physiological trends (Shock Index, SpO2) to detect sepsis and suppress false alarms.</span>
            </div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.88rem;">3. Hospital Staff Scheduling (CSP)</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">Min-Conflicts local search resolving doctor duty rosters without concurrent double-booking or fatigue violations.</span>
            </div>
            
            <div>
                <strong style="color: #0f172a; font-size: 0.88rem;">4. Clinical Triage & Surgical Planning</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">Propositional Horn-clause forward chaining for emergency triage paired with Partial Order Planning for parallel surgical workflows.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_academic_disclaimer()


# =============================================================================
# SECTION 2: EMERGENCY ROUTE PLANNER
# =============================================================================
elif nav_selection == "Emergency Route Planner":
    render_syllabus_pill("Practical 4 & 3", "Optimal Path Using A* Search vs Greedy Best-First Search")

    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        st.markdown("""
        <div class="content-card">
            <div class="content-header">Ambulance Dispatch Control</div>
            <div class="content-sub">Configure incident origin and destination receiving center.</div>
        </div>
        """, unsafe_allow_html=True)

        start_node = st.selectbox(
            "Incident Location (Origin)",
            options=list(HOSPITAL_NODES.keys()),
            index=list(HOSPITAL_NODES.keys()).index("Sitabuldi")
        )

        goal_node = st.selectbox(
            "Destination Hospital",
            options=list(HOSPITAL_NODES.keys()),
            index=list(HOSPITAL_NODES.keys()).index("AIIMS_Nagpur")
        )

        heuristic_mode = st.radio(
            "Heuristic Evaluation Mode h(n)",
            options=["euclidean", "manhattan"],
            format_func=lambda x: "Euclidean (Straight-Line Distance)" if x == "euclidean" else "Manhattan (Grid Distance)"
        )

        blocked_segments = []
        if simulate_road_closure:
            blocked_segments.append(("Wardha_Road", "Airport_Metro"))
            render_banner("⚠️ Wardha Road Arterial Link is blocked due to active construction.", "warning")

        calc_btn = st.button("Calculate Optimal Routes", type="primary", use_container_width=True)

    # Compute Search
    search_results = compare_search_algorithms(
        start=start_node,
        goal=goal_node,
        traffic_multiplier=traffic_multiplier,
        blocked_edges=blocked_segments,
        heuristic_type=heuristic_mode
    )

    a_star = search_results["results"]["A* Search"]
    greedy = search_results["results"]["Greedy Best-First"]
    dijkstra = search_results["results"]["Dijkstra"]

    with col_viz:
        fig_route = plot_hospital_network(
            a_star_path=a_star["path"] if a_star["success"] else [],
            greedy_path=greedy["path"] if greedy["success"] else [],
            blocked_edges=blocked_segments
        )
        st.plotly_chart(fig_route, use_container_width=True)

    # Comparison Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid #059669;">
            <div class="kpi-label">A* Search (Optimal)</div>
            <div class="kpi-value">{a_star['total_cost_minutes']} min</div>
            <div class="kpi-context">
                Nodes Expanded: <strong>{a_star['nodes_expanded']}</strong> | Frontier: <strong>{a_star['peak_frontier_size']}</strong>
            </div>
            <div style="font-size: 0.78rem; color: #059669; margin-top: 8px;">
                Guaranteed optimal route via f(n) = g(n) + h(n).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        is_suboptimal = greedy["total_cost_minutes"] > a_star["total_cost_minutes"]
        border_c = "#ef4444" if is_suboptimal else "#f59e0b"
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid {border_c};">
            <div class="kpi-label">Greedy Best-First</div>
            <div class="kpi-value">{greedy['total_cost_minutes']} min</div>
            <div class="kpi-context">
                Nodes Expanded: <strong>{greedy['nodes_expanded']}</strong> | Frontier: <strong>{greedy['peak_frontier_size']}</strong>
            </div>
            <div style="font-size: 0.78rem; color: {'#dc2626' if is_suboptimal else '#d97706'}; margin-top: 8px;">
                {'Suboptimal detour taken due to f = h ignoring cost g.' if is_suboptimal else 'Matches optimal route in this corridor.'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid #0284c7;">
            <div class="kpi-label">Dijkstra Search</div>
            <div class="kpi-value">{dijkstra['total_cost_minutes']} min</div>
            <div class="kpi-context">
                Nodes Expanded: <strong>{dijkstra['nodes_expanded']}</strong> | Frontier: <strong>{dijkstra['peak_frontier_size']}</strong>
            </div>
            <div style="font-size: 0.78rem; color: #0284c7; margin-top: 8px;">
                Optimal but uninformed (h = 0), blind exploration.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    with st.expander("Search Trace & Priority Queue Decisions (A* Node Expansion Log)"):
        st.markdown("Detailed step-by-step breakdown of how $f(n) = g(n) + h(n)$ prioritized nodes:")
        df_log = pd.DataFrame(a_star["visited_order"])
        st.dataframe(df_log[["step", "display_name", "g", "h", "f", "explanation"]], use_container_width=True)

    render_academic_disclaimer()


# =============================================================================
# SECTION 3: HOSPITAL OPERATIONS COMMAND (PATIENT + STAFF + TRIAGE)
# =============================================================================
elif nav_selection == "Hospital Operations":
    ops_tab1, ops_tab2, ops_tab3 = st.tabs([
        "ICU Telemetry Monitoring",
        "Staff Duty Scheduling (CSP)",
        "Emergency Triage Inference"
    ])

    # --- SUB-TAB 1: ICU Telemetry Monitoring ---
    with ops_tab1:
        render_syllabus_pill("Practical 2 & 1", "Hospital Patient Monitoring Agent (Model-Based vs Simple Reflex)")

        col_pat_ctrl, col_pat_plot = st.columns([1, 2])

        with col_pat_ctrl:
            st.markdown("""
            <div class="content-card">
                <div class="content-header">Patient Telemetry Stream</div>
                <div class="content-sub">Inspect rolling vital signs and agent response over time.</div>
            </div>
            """, unsafe_allow_html=True)

            selected_pid = st.selectbox(
                "Monitored Patient Bed",
                options=list(PATIENT_TELEMETRY_STREAM.keys()),
                format_func=lambda k: f"{k}: {PATIENT_TELEMETRY_STREAM[k]['name']} ({PATIENT_TELEMETRY_STREAM[k]['bed']})"
            )

            p_info = PATIENT_TELEMETRY_STREAM[selected_pid]
            st.markdown(f"**Diagnosis:** {p_info['admit_diagnosis']}")
            st.markdown(f"**Expected Trajectory:** {p_info['expected_progression']}")

            time_step = st.slider(
                "Inspection Time Window",
                min_value=1,
                max_value=len(p_info["timesteps"]),
                value=len(p_info["timesteps"]),
                format_func=lambda s: f"Step {s} ({p_info['timesteps'][s-1]['time']})"
            )

        mb_agent = ModelBasedReflexAgent(selected_pid, p_info["name"])
        sr_agent = SimpleReflexAgent()

        agent_log = []
        for i in range(time_step):
            ts = p_info["timesteps"][i]
            mb_out = mb_agent.update_internal_state(ts, ts["time"])
            sr_out = sr_agent.evaluate_percept(ts)
            agent_log.append({
                "time": ts["time"],
                "vitals": ts,
                "mb": mb_out,
                "sr": sr_out
            })

        curr_mb = agent_log[-1]["mb"]
        curr_sr = agent_log[-1]["sr"]
        curr_vitals = agent_log[-1]["vitals"]

        with col_pat_plot:
            fig_vitals = plot_patient_telemetry(p_info["timesteps"][:time_step], p_info["name"])
            st.plotly_chart(fig_vitals, use_container_width=True)

        st.markdown("### Agent Decision Comparison")
        col_ag_mb, col_ag_sr = st.columns(2)

        with col_ag_mb:
            alert_color = "#dc2626" if "LEVEL_3" in curr_mb["alert_level"] else "#d97706" if "LEVEL_2" in curr_mb["alert_level"] else "#16a34a"
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 3px solid {alert_color};">
                <div class="kpi-label">Model-Based Reflex Agent (With Temporal Memory)</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: {alert_color}; margin: 6px 0;">
                    {curr_mb['action']}
                </div>
                <div style="font-size: 0.84rem; line-height: 1.5; color: #334155;">
                    <strong>Physiological Trend:</strong> {curr_mb['trend']}<br>
                    <strong>Calculated Shock Index:</strong> {curr_mb['shock_index']} (Normal: 0.5 - 0.7)<br>
                    <strong>Pattern Detected:</strong> {curr_mb['suspected_syndrome']}<br>
                    <strong>Clinical Rationale:</strong> {curr_mb['rationale']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_ag_sr:
            sr_c = "#dc2626" if curr_sr["severity"] == "CRITICAL" else "#d97706" if curr_sr["severity"] == "HIGH" else "#16a34a"
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 3px solid {sr_c};">
                <div class="kpi-label">Simple Reflex Agent (Immediate Percept Only)</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: {sr_c}; margin: 6px 0;">
                    {curr_sr['action']}
                </div>
                <div style="font-size: 0.84rem; line-height: 1.5; color: #334155;">
                    <strong>Observation:</strong> HR={curr_vitals['hr']}, BP={curr_vitals['sys_bp']}/{curr_vitals['dia_bp']}, SpO2={curr_vitals['spo2']}%<br>
                    <strong>Memory State:</strong> None (S = ∅)<br>
                    <strong>Evaluation:</strong> {curr_sr['message']}<br>
                    <strong>Limitation:</strong> Susceptible to false alarms on transient spikes; delayed detection of gradual septic collapse.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- SUB-TAB 2: Staff Duty Scheduling (CSP) ---
    with ops_tab2:
        render_syllabus_pill("Practical 5", "Map Coloring for Adjoining Regions using Min-Conflicts (CSP)")

        col_csp_l, col_csp_r = st.columns([1, 1.8])

        with col_csp_l:
            st.markdown("""
            <div class="content-card">
                <div class="content-header">Constraint Satisfaction Solver</div>
                <div class="content-sub">Assign specialists to emergency shifts without constraint violations.</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            **Hard Constraints:**
            * **No Double Booking:** A doctor cannot work two shifts simultaneously.
            * **Specialty Match:** Clinical specialty must match the department requirements.
            * **Fatigue Limit:** Doctors cannot exceed their allotted shift quotas per cycle.
            """)

            max_steps = st.slider("Max Iterations per Restart", 50, 400, 200, step=50)
            restarts = st.slider("Random Restarts", 1, 8, 4)

            solve_csp = st.button("Solve Roster with Min-Conflicts", type="primary", use_container_width=True)

        duty_csp = HospitalDutyCSP()
        csp_output = duty_csp.solve_min_conflicts(max_steps=max_steps, random_restarts=restarts)

        with col_csp_r:
            fig_csp = plot_csp_convergence(csp_output["iteration_history"])
            st.plotly_chart(fig_csp, use_container_width=True)

        if csp_output["success"]:
            render_banner(f"Constraint Satisfaction Solved: ZERO conflicts across all {len(csp_output['schedule_table'])} shift slots in {csp_output['total_steps']} steps.", "success")
        else:
            render_banner(f"Local minimum reached with {csp_output['conflicts']} remaining conflicts. Try increasing random restarts.", "warning")

        st.markdown("### Optimized Duty Roster Schedule")
        df_schedule = pd.DataFrame(csp_output["schedule_table"])
        st.dataframe(df_schedule, use_container_width=True)

    # --- SUB-TAB 3: Clinical Triage Inference ---
    with ops_tab3:
        render_syllabus_pill("Practical 7 & 8", "Smart Garden Propositional Logic & Assistant Bot FOL Unification")

        triage_sub1, triage_sub2 = st.tabs(["Propositional Forward Chaining", "First-Order Logic Unification"])

        with triage_sub1:
            col_t1, col_t2 = st.columns([1, 1.8])

            with col_t1:
                st.markdown("""
                <div class="content-card">
                    <div class="content-header">Clinical Presentation</div>
                    <div class="content-sub">Toggle symptoms to trigger propositional Horn-clause rules.</div>
                </div>
                """, unsafe_allow_html=True)

                scenario_sel = st.selectbox(
                    "Clinical Preset Scenarios",
                    options=["Custom Evaluation"] + list(TRIAGE_PRESET_SCENARIOS.keys())
                )

                if scenario_sel != "Custom Evaluation":
                    sc_data = TRIAGE_PRESET_SCENARIOS[scenario_sel]
                    sym_airway = st.checkbox("Severe Airway Compromise", value=sc_data.get("severe_airway_compromise", False))
                    sym_bleed = st.checkbox("Active Massive Hemorrhage", value=sc_data.get("active_massive_hemorrhage", False))
                    sym_chest = st.checkbox("Chest Pain with Diaphoresis (STEMI)", value=sc_data.get("chest_pain_diaphoresis", False))
                    sym_stroke = st.checkbox("Acute Focal Deficit (Stroke Window)", value=sc_data.get("suspected_stroke_symptoms", False))
                    sym_unstable = st.checkbox("Physiological Vitals Unstable", value=sc_data.get("vital_signs_unstable", False))
                    sym_fever = st.checkbox("High-Grade Fever with Lethargy", value=sc_data.get("high_fever_lethargy", False))
                    sym_mild = st.checkbox("Superficial Laceration / Sprain", value=sc_data.get("mild_abrasion", False))
                else:
                    sym_airway = st.checkbox("Severe Airway Compromise", value=False)
                    sym_bleed = st.checkbox("Active Massive Hemorrhage", value=False)
                    sym_chest = st.checkbox("Chest Pain with Diaphoresis (STEMI)", value=True)
                    sym_stroke = st.checkbox("Acute Focal Deficit (Stroke Window)", value=False)
                    sym_unstable = st.checkbox("Physiological Vitals Unstable", value=True)
                    sym_fever = st.checkbox("High-Grade Fever with Lethargy", value=False)
                    sym_mild = st.checkbox("Superficial Laceration / Sprain", value=False)

                facts = []
                if sym_airway: facts.append("severe_airway_compromise")
                if sym_bleed: facts.append("active_massive_hemorrhage")
                if sym_chest: facts.append("chest_pain_diaphoresis")
                if sym_stroke: facts.append("suspected_stroke_symptoms")
                if sym_unstable: facts.append("vital_signs_unstable")
                if sym_fever: facts.append("high_fever_lethargy")
                if sym_mild: facts.append("mild_abrasion")

            engine = ClinicalTriageInferenceEngine()
            triage_out = engine.forward_chain(facts)

            with col_t2:
                st.markdown(f"""
                <div class="kpi-card" style="border-top: 3px solid #0284c7; margin-bottom: 16px;">
                    <div class="kpi-label">Inferred Emergency Acuity</div>
                    <div style="font-size: 1.4rem; font-weight: 700; color: #0f172a; margin: 6px 0;">
                        {triage_out['final_esi_level']}
                    </div>
                    <div style="font-size: 0.88rem; color: #0284c7; font-weight: 600;">
                        Target Bay: {triage_out['assigned_bay']}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 6px;">
                        Derived via {triage_out['rules_fired_count']} Horn clauses using Modus Ponens forward deduction.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### Logical Proof Trace")
                if triage_out["firing_history"]:
                    for step in triage_out["firing_history"]:
                        st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                            <strong style="color: #0284c7; font-size: 0.85rem;">Step {step['step']}: Rule [{step['rule']}] Fired</strong><br>
                            <code style="font-size: 0.8rem; color: #0f172a;">{' ∧ '.join(step['antecedents'])} ⇒ {step['consequent']}</code><br>
                            <span style="font-size: 0.78rem; color: #64748b;">{step['explanation']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No acute rules satisfied. Patient categorized under routine observation.")

        with triage_sub2:
            st.markdown("""
            <div class="content-card">
                <div class="content-header">First-Order Logic Unification Matcher</div>
                <div class="content-sub">Matches patient specialty requirements with available attending physicians.</div>
            </div>
            """, unsafe_allow_html=True)

            col_up, col_ud = st.columns(2)
            with col_up:
                p_pred = st.text_input("Patient Demand Predicate", value="NeedsSpecialist(P-101, Cardiology, ?shift)")
            with col_ud:
                d_pred = st.text_input("Physician Availability Predicate", value="NeedsSpecialist(?patient, ?spec, Morning)")

            p_tokens = [t.strip() for t in p_pred.replace("(", ",").replace(")", "").split(",")]
            d_tokens = [t.strip() for t in d_pred.replace("(", ",").replace(")", "").split(",")]

            unif = match_clinical_duty(p_tokens, d_tokens)
            if unif["unification_success"]:
                render_banner("Unification Successful: Most General Unifier (MGU θ) found.", "success")
                st.json(unif["most_general_unifier"])
            else:
                render_banner("Unification Failed: No valid substitution exists.", "danger")

    render_academic_disclaimer()


# =============================================================================
# SECTION 4: AI INSIGHTS & ALGORITHM LAB
# =============================================================================
elif nav_selection == "AI Insights & Algorithms":
    st.markdown("""
    <div class="content-card">
        <div class="content-header">AI Architecture & Algorithm Foundations</div>
        <div class="content-sub">In-depth mathematical formulation and theoretical analysis of all implemented AI concepts.</div>
    </div>
    """, unsafe_allow_html=True)

    tab_pop, tab_comp, tab_allpairs = st.tabs([
        "Partial Order Planning (Trauma Surgery)",
        "Theoretical Complexity Comparison",
        "Network-Wide Pathfinding Stress Test"
    ])

    with tab_pop:
        render_syllabus_pill("Practical 10", "Kitchen Task Planner for Anaya (Partial Order Planning)")

        col_pop_txt, col_pop_chart = st.columns([1, 2])

        with col_pop_txt:
            st.markdown("""
            <div class="content-card">
                <div class="content-header">Trauma Surgery Protocol</div>
                <div class="content-sub">Non-linear parallel task sequencing using causal links.</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            **Why Partial Order Planning?**
            * **Linear Planning Flaw:** Forces all actions into a rigid line ($A_1 \\to A_2 \\to A_3$), creating bottlenecks.
            * **POP Parallelism:** Actions are ordered only when causal dependencies require it. For example, Nursing establishes IV access while Scrub Techs sterilize instruments **concurrently**.
            """)

            pop_engine = PartialOrderPlanner()
            pop_plan = pop_engine.generate_plan()

            st.markdown(f"""
            <div class="kpi-card" style="margin-top: 14px;">
                <div class="kpi-label">Estimated Critical Path</div>
                <div class="kpi-value">{pop_plan['estimated_critical_path_minutes']} min</div>
                <div class="kpi-context">Structured across {len(pop_plan['execution_tiers'])} Parallel Stages</div>
            </div>
            """, unsafe_allow_html=True)

        with col_pop_chart:
            fig_pop = plot_partial_order_plan(pop_plan["execution_tiers"])
            st.plotly_chart(fig_pop, use_container_width=True)

        st.markdown("### Causal Link Dependencies")
        df_causal = pd.DataFrame(pop_plan["causal_links"])
        st.dataframe(df_causal[["from_action", "condition", "to_action", "from_name", "to_name"]], use_container_width=True)

    with tab_comp:
        st.markdown("### Complexity & Theoretical Analysis")
        theory_table = [
            {"Algorithm": "A* Search", "Evaluation Function": "f(n) = g(n) + h(n)", "Time Complexity": "O(b^d)", "Space Complexity": "O(b^d)", "Optimality": "Guaranteed (h is admissible)", "Completeness": "Complete"},
            {"Algorithm": "Greedy Best-First", "Evaluation Function": "f(n) = h(n)", "Time Complexity": "O(b^m)", "Space Complexity": "O(b^m)", "Optimality": "Not Guaranteed (Suboptimal)", "Completeness": "Incomplete without cycle check"},
            {"Algorithm": "Dijkstra (UCS)", "Evaluation Function": "f(n) = g(n)", "Time Complexity": "O(b^(C*/ε))", "Space Complexity": "O(b^(C*/ε))", "Optimality": "Guaranteed", "Completeness": "Complete"},
            {"Algorithm": "Min-Conflicts Local Search", "Evaluation Function": "arg min conflicts(var = v)", "Time Complexity": "O(k · n)", "Space Complexity": "O(n)", "Optimality": "Conflict-Free Satisficing", "Completeness": "Incomplete (mitigated by restarts)"},
            {"Algorithm": "Model-Based Reflex Agent", "Evaluation Function": "S_{t+1} = Update(S_t, P_{t+1})", "Time Complexity": "O(1) per percept", "Space Complexity": "O(k) rolling history", "Optimality": "High Signal-to-Noise Ratio", "Completeness": "Deterministic"},
            {"Algorithm": "Partial Order Planning", "Evaluation Function": "Causal Links & Ordering", "Time Complexity": "NP-Hard in general", "Space Complexity": "O(|Actions| + |Links|)", "Optimality": "Shortest Parallel Schedule", "Completeness": "Complete"}
        ]
        st.dataframe(pd.DataFrame(theory_table), use_container_width=True)

    with tab_allpairs:
        st.markdown("### All-Pairs Pathfinding Benchmark (Sitabuldi to All Facilities)")
        st.markdown("Run live comparisons across the entire network graph to evaluate A* versus Greedy Best-First.")
        
        if st.button("Run Full Network Benchmark"):
            graph = get_network_graph(traffic_multiplier=traffic_multiplier)
            bench_data = []
            for dest in HOSPITAL_NODES:
                if dest == "Sitabuldi":
                    continue
                a_res = a_star_search("Sitabuldi", dest, graph)
                g_res = greedy_best_first_search("Sitabuldi", dest, graph)
                d_res = dijkstra_search("Sitabuldi", dest, graph)
                bench_data.append({
                    "Destination": HOSPITAL_NODES[dest]["name"],
                    "A* Time (min)": a_res["total_cost_minutes"],
                    "A* Nodes": a_res["nodes_expanded"],
                    "Greedy Time (min)": g_res["total_cost_minutes"],
                    "Greedy Nodes": g_res["nodes_expanded"],
                    "Dijkstra Time (min)": d_res["total_cost_minutes"],
                    "Greedy Suboptimal?": "Suboptimal Detour" if g_res["total_cost_minutes"] > a_res["total_cost_minutes"] else "Matches A*"
                })
            st.dataframe(pd.DataFrame(bench_data), use_container_width=True)

    render_academic_disclaimer()
