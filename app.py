"""
app.py
======
VitalFlow AI: Autonomous Hospital Operations & Emergency Logistics Platform
A clean, focused multi-agent decision support and state-space optimization system.

Core AI Algorithms Implemented:
1. Informed State-Space Graph Search (A* Search vs Greedy Best-First)
2. Model-Based Reflex Agent with Internal Temporal State Vector
3. Constraint Satisfaction Problem (CSP) with Min-Conflicts Local Search
4. Propositional Horn-Clause Forward Chaining Inference
5. Partial Order Planning (POP) with Causal Preconditions
"""

import streamlit as st
import pandas as pd
import numpy as np

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
from core.search_planner import compare_search_algorithms
from core.reflex_agents import SimpleReflexAgent, ModelBasedReflexAgent
from core.csp_scheduler import HospitalDutyCSP
from core.logic_triage import ClinicalTriageInferenceEngine
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
# SIDEBAR NAVIGATION (3 CLEAN SECTIONS ONLY)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="width: 34px; height: 34px; border-radius: 8px; background: #0284c7; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.05rem;">V</div>
        <div>
            <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a; line-height: 1.1;">VitalFlow AI</div>
            <div style="font-size: 0.75rem; color: #64748b;">Operations Command</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        label="Navigation",
        options=[
            "Overview",
            "Emergency Route Planner",
            "Hospital Operations"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: #475569; margin-bottom: 8px;'>TRAFFIC & ROADS</div>", unsafe_allow_html=True)
    
    traffic_multiplier = st.select_slider(
        "Traffic Multiplier",
        options=[1.0, 1.2, 1.5, 2.0, 2.5],
        value=1.2,
        format_func=lambda x: f"{x}x {'(Standard)' if x==1.0 else '(Peak Rush)' if x>=2.0 else '(Moderate)'}"
    )

    simulate_road_closure = st.checkbox("Simulate Wardha Road Closure", value=False)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #94a3b8; line-height: 1.5;">
        <strong>Network:</strong> Nagpur Urban Grid<br>
        <strong>Active Modules:</strong> A* Route, ICU Reflex Agent, CSP Shift Solver, Triage Horn Logic, POP Surgery
    </div>
    """, unsafe_allow_html=True)

# Top Executive Bar
render_top_header()


# =============================================================================
# 1. OVERVIEW
# =============================================================================
if nav_selection == "Overview":
    total_facilities = len(HOSPITAL_NODES)
    total_beds = sum(n["icu_beds"] for n in HOSPITAL_NODES.values())
    trauma_centers = sum(1 for n in HOSPITAL_NODES.values() if n["trauma_ready"])
    
    render_kpi_cards([
        {"label": "Connected Facilities", "value": f"{total_facilities} Centers", "context": "Hospitals & Emergency Junctions"},
        {"label": "Network ICU Beds", "value": f"{total_beds} Beds", "context": "Monitored Bed Capacity"},
        {"label": "Trauma Resus Centers", "value": f"{trauma_centers} Units", "context": "Critical Receiving Facilities"},
        {"label": "Current Traffic Index", "value": f"{traffic_multiplier}x", "context": "Dynamic Transit Time Factor"}
    ])

    st.write("")
    
    col_map, col_info = st.columns([1.8, 1])

    with col_map:
        st.markdown("""
        <div class="content-card">
            <div class="content-header">Nagpur Healthcare Transit Topology</div>
            <div class="content-sub">Interactive spatial map showing emergency hospitals, corridors, and arterial links.</div>
        </div>
        """, unsafe_allow_html=True)

        blocked = [("Wardha_Road", "Airport_Metro")] if simulate_road_closure else []
        fig_overview = plot_hospital_network(blocked_edges=blocked)
        st.plotly_chart(fig_overview, use_container_width=True)

    with col_info:
        st.markdown("""
        <div class="content-card">
            <div class="content-header">Operational Workflow</div>
            <div class="content-sub">How decision support is structured in VitalFlow AI:</div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.88rem;">1. Ambulance Route Dispatch</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">A* Search guarantees minimal transit time to apex hospitals (AIIMS / GMC Nagpur), avoiding road closures via the Outer Ring Road.</span>
            </div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.88rem;">2. Patient Telemetry Monitoring</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">Model-Based Reflex Agent tracks continuous physiological trends (Shock Index) to catch early sepsis while suppressing false alarms.</span>
            </div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.88rem;">3. Hospital Staff Scheduling</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">Constraint Satisfaction Problem (CSP) solved via Min-Conflicts local search to produce 100% conflict-free doctor rosters.</span>
            </div>
            
            <div>
                <strong style="color: #0f172a; font-size: 0.88rem;">4. Emergency Triage & Surgical Protocol</strong><br>
                <span style="color: #64748b; font-size: 0.82rem;">Propositional forward chaining classifies acuity (ESI 1-5), and Partial Order Planning schedules parallel multi-team surgical steps.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_academic_disclaimer()


# =============================================================================
# 2. EMERGENCY ROUTE PLANNER
# =============================================================================
elif nav_selection == "Emergency Route Planner":
    render_syllabus_pill("Practical 4 & 3", "Optimal Path Using A* Search vs Greedy Best-First Search")

    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        st.markdown("""
        <div class="content-card">
            <div class="content-header">Ambulance Dispatch</div>
            <div class="content-sub">Select emergency incident origin and target receiving hospital.</div>
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
            render_banner("⚠️ Wardha Road link is blocked. Rerouting via Outer Ring Road.", "warning")

        calc_btn = st.button("Calculate Optimal Routes", type="primary", use_container_width=True)

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

    # Comparison KPI Cards
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
                Guaranteed shortest route via f(n) = g(n) + h(n).
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
        df_log = pd.DataFrame(a_star["visited_order"])
        st.dataframe(df_log[["step", "display_name", "g", "h", "f", "explanation"]], use_container_width=True)

    render_academic_disclaimer()


# =============================================================================
# 3. HOSPITAL OPERATIONS (PATIENT TELEMETRY + STAFF CSP + SURGERY WORKFLOW)
# =============================================================================
elif nav_selection == "Hospital Operations":
    ops_tab1, ops_tab2, ops_tab3 = st.tabs([
        "ICU Patient Monitoring",
        "Staff Duty Scheduling (CSP)",
        "Emergency Triage & Surgical Protocol"
    ])

    # --- TAB 1: ICU Telemetry Monitoring (Model-Based Agent) ---
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

    # --- TAB 2: Staff Duty Scheduling (CSP Min-Conflicts) ---
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

    # --- TAB 3: Emergency Triage & Surgical Protocol (Horn Logic + POP) ---
    with ops_tab3:
        render_syllabus_pill("Practical 7 & 10", "Propositional Logic Inference & Partial Order Planning")

        # Top half: Propositional Logic Triage
        st.markdown("### 1. Emergency Clinical Triage (Horn-Clause Forward Chaining)")
        
        col_t1, col_t2 = st.columns([1, 1.8])

        with col_t1:
            scenario_sel = st.selectbox(
                "Clinical Presentation Preset",
                options=["Custom Evaluation"] + list(TRIAGE_PRESET_SCENARIOS.keys())
            )

            if scenario_sel != "Custom Evaluation":
                sc_data = TRIAGE_PRESET_SCENARIOS[scenario_sel]
                sym_airway = st.checkbox("Severe Airway Compromise", value=sc_data.get("severe_airway_compromise", False))
                sym_bleed = st.checkbox("Active Massive Hemorrhage", value=sc_data.get("active_massive_hemorrhage", False))
                sym_chest = st.checkbox("Chest Pain with Diaphoresis (STEMI)", value=sc_data.get("chest_pain_diaphoresis", False))
                sym_stroke = st.checkbox("Acute Focal Deficit (Stroke Window)", value=sc_data.get("suspected_stroke_symptoms", False))
                sym_unstable = st.checkbox("Physiological Vitals Unstable", value=sc_data.get("vital_signs_unstable", False))
            else:
                sym_airway = st.checkbox("Severe Airway Compromise", value=False)
                sym_bleed = st.checkbox("Active Massive Hemorrhage", value=False)
                sym_chest = st.checkbox("Chest Pain with Diaphoresis (STEMI)", value=True)
                sym_stroke = st.checkbox("Acute Focal Deficit (Stroke Window)", value=False)
                sym_unstable = st.checkbox("Physiological Vitals Unstable", value=True)

            facts = []
            if sym_airway: facts.append("severe_airway_compromise")
            if sym_bleed: facts.append("active_massive_hemorrhage")
            if sym_chest: facts.append("chest_pain_diaphoresis")
            if sym_stroke: facts.append("suspected_stroke_symptoms")
            if sym_unstable: facts.append("vital_signs_unstable")

        engine = ClinicalTriageInferenceEngine()
        triage_out = engine.forward_chain(facts)

        with col_t2:
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 3px solid #0284c7; margin-bottom: 12px;">
                <div class="kpi-label">Inferred Emergency Acuity</div>
                <div style="font-size: 1.35rem; font-weight: 700; color: #0f172a; margin: 4px 0;">
                    {triage_out['final_esi_level']}
                </div>
                <div style="font-size: 0.86rem; color: #0284c7; font-weight: 600;">
                    Target Department: {triage_out['assigned_bay']}
                </div>
                <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">
                    Derived via {triage_out['rules_fired_count']} Horn clauses using Modus Ponens forward deduction.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if triage_out["firing_history"]:
                for step in triage_out["firing_history"]:
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 12px; margin-bottom: 6px; font-size: 0.8rem;">
                        <strong style="color: #0284c7;">Rule [{step['rule']}]:</strong> <code>{' ∧ '.join(step['antecedents'])} ⇒ {step['consequent']}</code>
                    </div>
                    """, unsafe_allow_html=True)

        st.write("")
        st.markdown("---")

        # Bottom half: Partial Order Planning for Trauma Surgery
        st.markdown("### 2. Trauma Resuscitation Protocol (Partial Order Planning)")
        st.markdown("Rather than rigid linear sequencing, Partial Order Planning coordinates independent clinical tasks in parallel.")

        pop_engine = PartialOrderPlanner()
        pop_plan = pop_engine.generate_plan()

        fig_pop = plot_partial_order_plan(pop_plan["execution_tiers"])
        st.plotly_chart(fig_pop, use_container_width=True)

        with st.expander("View POP Causal Preconditions & Link Dependencies"):
            df_causal = pd.DataFrame(pop_plan["causal_links"])
            st.dataframe(df_causal[["from_action", "condition", "to_action", "from_name", "to_name"]], use_container_width=True)

    render_academic_disclaimer()
