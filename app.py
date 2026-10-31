"""
app.py
======
VitalFlow AI: Autonomous Hospital Operations & Emergency Logistics Platform
Executive healthcare operations platform powered by classical and heuristic AI.

Core AI Implementations:
1. Heuristic State-Space Graph Search (A* Search vs Greedy Best-First)
2. Model-Based Reflex Agent with Internal Temporal State Vector
3. Constraint Satisfaction Problem (CSP) with Min-Conflicts Local Search
4. Propositional Horn-Clause Forward Chaining Inference
5. Partial Order Planning (POP) with Causal Preconditions
"""

import streamlit as st
import pandas as pd
import numpy as np

# UI & Component Imports
from ui.styles import get_custom_css
from ui.components import (
    render_html,
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

# Core AI & Data Imports
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

# Inject High-Contrast SaaS Styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION (FOCUSED 4 PRODUCT MODULES ONLY)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 22px;">
        <div style="width: 36px; height: 36px; border-radius: 9px; background: #0284c7; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.15rem; box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);">V</div>
        <div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #0f172a; line-height: 1.1;">VitalFlow AI</div>
            <div style="font-size: 0.78rem; color: #475569; font-weight: 600;">Operations Command</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        label="Navigation Menu",
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
    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #0f172a; margin-bottom: 8px;'>TRAFFIC & HAZARDS</div>", unsafe_allow_html=True)
    
    traffic_multiplier = st.select_slider(
        "Congestion Factor",
        options=[1.0, 1.2, 1.5, 2.0, 2.5],
        value=1.2,
        format_func=lambda x: f"{x}x {'(Standard)' if x==1.0 else '(Peak Rush)' if x>=2.0 else '(Moderate)'}"
    )

    simulate_road_closure = st.checkbox("Simulate Wardha Road Closure", value=False)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.76rem; color: #475569; line-height: 1.5;">
        <strong>Spatial Grid:</strong> Nagpur Regional<br>
        <strong>Core Models:</strong> A* Search, Reflex Agent, CSP Solver, Horn Logic, POP
    </div>
    """, unsafe_allow_html=True)

# Render Global Top Executive Bar
render_top_header()


# =============================================================================
# 1. OVERVIEW DASHBOARD
# =============================================================================
if nav_selection == "Overview":
    total_facilities = len(HOSPITAL_NODES)
    total_beds = sum(n.get("icu_beds", 0) for n in HOSPITAL_NODES.values())
    trauma_centers = sum(1 for n in HOSPITAL_NODES.values() if n.get("trauma_ready", False))
    
    render_kpi_cards([
        {"label": "Network Facilities", "value": f"{total_facilities} Centers", "context": "Hospitals & Emergency Outposts"},
        {"label": "Total Monitored Beds", "value": f"{total_beds} Beds", "context": "Across Regional Network"},
        {"label": "Apex Trauma Bays", "value": f"{trauma_centers} Units", "context": "Equipped for Polytrauma Care"},
        {"label": "Dynamic Traffic Index", "value": f"{traffic_multiplier}x", "context": "Active Road Congestion Factor"}
    ])

    st.write("")
    
    col_map, col_info = st.columns([1.8, 1])

    with col_map:
        st.subheader("Nagpur Healthcare Transit Topology")
        st.caption("Interactive spatial map showing emergency facilities, arterial links, and bypass routes.")

        blocked = [("Wardha_Road", "Airport_Metro")] if simulate_road_closure else []
        fig_overview = plot_hospital_network(blocked_edges=blocked)
        st.plotly_chart(fig_overview, use_container_width=True)

    with col_info:
        # NATIVE STREAMLIT WORKFLOW CARD - 100% IMMUNE TO RAW HTML ESCAPING
        st.subheader("Operational Workflow")
        st.caption("How decision support is structured in VitalFlow AI:")
        
        st.markdown("##### 1. Ambulance Route Dispatch")
        st.write("A* Search guarantees minimal transit time to apex centers (AIIMS / GMC Nagpur), avoiding road closures via the Outer Ring Road.")
        
        st.markdown("##### 2. Patient Telemetry Monitoring")
        st.write("Model-Based Reflex Agent tracks continuous physiological trends (Shock Index) to catch early sepsis while suppressing false alarms.")
        
        st.markdown("##### 3. Hospital Staff Scheduling")
        st.write("Constraint Satisfaction Problem (CSP) solved via Min-Conflicts local search to produce 100% conflict-free doctor rosters.")
        
        st.markdown("##### 4. Emergency Triage & Surgical Protocol")
        st.write("Propositional forward chaining classifies acuity (ESI 1-5), and Partial Order Planning schedules parallel multi-team surgical steps.")

    render_academic_disclaimer()


# =============================================================================
# 2. EMERGENCY ROUTE PLANNER (HERO FEATURE)
# =============================================================================
elif nav_selection == "Emergency Route Planner":
    render_syllabus_pill("Practical 4 & 3", "Optimal Path Using A* Search vs Greedy Best-First Search")

    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        st.subheader("Ambulance Dispatch Control")
        st.caption("Select incident location and receiving emergency trauma hospital.")

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
        st.metric(
            label="A* Search (Optimal)",
            value=f"{a_star['total_cost_minutes']} min",
            delta=f"Expanded: {a_star['nodes_expanded']} nodes"
        )
        st.caption("Guaranteed shortest route via f(n) = g(n) + h(n).")

    with col_m2:
        is_suboptimal = greedy["total_cost_minutes"] > a_star["total_cost_minutes"]
        diff_min = round(greedy["total_cost_minutes"] - a_star["total_cost_minutes"], 2)
        st.metric(
            label="Greedy Best-First",
            value=f"{greedy['total_cost_minutes']} min",
            delta=f"+{diff_min} min detour" if is_suboptimal else "Optimal match",
            delta_color="inverse" if is_suboptimal else "normal"
        )
        st.caption("Suboptimal detour taken: f = h ignores accumulated travel cost g.")

    with col_m3:
        st.metric(
            label="Dijkstra Search",
            value=f"{dijkstra['total_cost_minutes']} min",
            delta=f"Expanded: {dijkstra['nodes_expanded']} nodes"
        )
        st.caption("Optimal but uninformed (h = 0), exploring in all directions.")

    st.write("")
    with st.expander("Search Trace & Priority Queue Decisions (A* Node Expansion Log)"):
        df_log = pd.DataFrame(a_star["visited_order"])
        st.dataframe(df_log[["step", "display_name", "g", "h", "f", "explanation"]], use_container_width=True)

    render_academic_disclaimer()


# =============================================================================
# 3. HOSPITAL OPERATIONS COMMAND
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
            st.subheader("Patient Telemetry Stream")
            st.caption("Inspect rolling vital signs and agent response over time.")

            selected_pid = st.selectbox(
                "Monitored Patient Bed",
                options=list(PATIENT_TELEMETRY_STREAM.keys()),
                format_func=lambda k: f"{k}: {PATIENT_TELEMETRY_STREAM[k]['name']} ({PATIENT_TELEMETRY_STREAM[k]['bed']})"
            )

            p_info = PATIENT_TELEMETRY_STREAM[selected_pid]
            timesteps = p_info.get("timesteps", [])
            total_steps = len(timesteps)

            st.markdown(f"**Diagnosis:** {p_info['admit_diagnosis']}")
            st.markdown(f"**Expected Trajectory:** {p_info['expected_progression']}")

            # 100% BULLETPROOF SLIDER: Uses discrete select_slider with safe index mapper
            def format_step_label(val):
                try:
                    v_int = int(val)
                    if 1 <= v_int <= len(timesteps):
                        t_str = timesteps[v_int - 1].get("time", "")
                        return f"Step {v_int} ({t_str})" if t_str else f"Step {v_int}"
                    return f"Step {v_int}"
                except Exception:
                    return f"Step {val}"

            step_options = list(range(1, total_steps + 1))
            time_step = st.select_slider(
                "Inspection Time Window",
                options=step_options,
                value=step_options[-1],
                format_func=format_step_label,
                key=f"ts_slider_{selected_pid}"
            )
            time_step_int = int(time_step)

        # Run both agents safely
        mb_agent = ModelBasedReflexAgent(selected_pid, p_info["name"])
        sr_agent = SimpleReflexAgent()

        agent_log = []
        for i in range(time_step_int):
            ts = timesteps[i]
            t_label = str(ts.get("time", f"T{i+1}"))
            mb_out = mb_agent.update_internal_state(ts, t_label)
            sr_out = sr_agent.evaluate_percept(ts)
            agent_log.append({
                "time": t_label,
                "vitals": ts,
                "mb": mb_out,
                "sr": sr_out
            })

        curr_mb = agent_log[-1]["mb"]
        curr_sr = agent_log[-1]["sr"]
        curr_vitals = agent_log[-1]["vitals"]

        with col_pat_plot:
            fig_vitals = plot_patient_telemetry(timesteps[:time_step_int], p_info["name"])
            st.plotly_chart(fig_vitals, use_container_width=True)

        st.markdown("### Agent Decision Comparison")
        col_ag_mb, col_ag_sr = st.columns(2)

        with col_ag_mb:
            alert_color = "#dc2626" if "LEVEL_3" in curr_mb["alert_level"] else "#d97706" if "LEVEL_2" in curr_mb["alert_level"] else "#16a34a"
            st.markdown(f"#### Model-Based Reflex Agent (Practical 2)")
            st.markdown(f"**Action:** `{curr_mb['action']}`")
            st.markdown(f"**Physiological Trend:** `{curr_mb['trend']}`")
            st.markdown(f"**Shock Index:** `{curr_mb['shock_index']}` (Normal: 0.5 - 0.7)")
            st.markdown(f"**Detected Syndrome:** {curr_mb['suspected_syndrome']}")
            st.info(f"**Agent Rationale:** {curr_mb['rationale']}")

        with col_ag_sr:
            st.markdown(f"#### Simple Reflex Agent (Practical 1)")
            st.markdown(f"**Action:** `{curr_sr['action']}`")
            st.markdown(f"**Current Percept:** HR={curr_vitals['hr']} bpm, BP={curr_vitals['sys_bp']}/{curr_vitals['dia_bp']} mmHg, SpO2={curr_vitals['spo2']}%")
            st.markdown(f"**Memory Model:** None ($S = \\emptyset$)")
            st.warning(f"**Limitation:** {curr_sr['message']}")

    # --- TAB 2: Staff Duty Scheduling (CSP Min-Conflicts) ---
    with ops_tab2:
        render_syllabus_pill("Practical 5", "Map Coloring for Adjoining Regions using Min-Conflicts (CSP)")

        col_csp_l, col_csp_r = st.columns([1, 1.8])

        with col_csp_l:
            st.subheader("Constraint Satisfaction Solver")
            st.caption("Assign specialists to emergency shifts without constraint violations.")

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

    # --- TAB 3: Emergency Triage & Surgical Protocol ---
    with ops_tab3:
        render_syllabus_pill("Practical 7 & 10", "Propositional Logic Inference & Partial Order Planning")

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
            st.metric("Inferred Emergency Acuity", triage_out['final_esi_level'])
            st.markdown(f"**Target Department:** `{triage_out['assigned_bay']}`")
            st.caption(f"Derived via {triage_out['rules_fired_count']} Horn clauses using Modus Ponens forward deduction.")

            if triage_out["firing_history"]:
                st.markdown("##### Fired Inference Rules:")
                for step in triage_out["firing_history"]:
                    st.code(f"Rule [{step['rule']}]: {' ∧ '.join(step['antecedents'])} ⇒ {step['consequent']}")

        st.write("")
        st.markdown("---")

        st.markdown("### 2. Trauma Resuscitation Protocol (Partial Order Planning)")
        st.caption("Rather than rigid linear sequencing, Partial Order Planning coordinates independent clinical tasks in parallel.")

        pop_engine = PartialOrderPlanner()
        pop_plan = pop_engine.generate_plan()

        fig_pop = plot_partial_order_plan(pop_plan["execution_tiers"])
        st.plotly_chart(fig_pop, use_container_width=True)

        with st.expander("View POP Causal Preconditions & Link Dependencies"):
            df_causal = pd.DataFrame(pop_plan["causal_links"])
            st.dataframe(df_causal[["from_action", "condition", "to_action", "from_name", "to_name"]], use_container_width=True)

    render_academic_disclaimer()


# =============================================================================
# 4. AI INSIGHTS & ALGORITHM EXPLANATIONS
# =============================================================================
elif nav_selection == "AI Insights & Algorithms":
    st.subheader("AI Architecture & Mathematical Foundations")
    st.caption("Clear, demonstrable explanations of how each algorithm works with actual execution results.")

    ai_tab1, ai_tab2 = st.tabs(["Algorithm Decision Principles", "Complexity & Optimality Analysis"])

    with ai_tab1:
        st.markdown("""
        ### How the 5 AI Algorithms Work in VitalFlow AI:

        #### 1. A* Search vs Greedy Best-First Search (Ambulance Navigation)
        * **A* Search Formula:** $f(n) = g(n) + h(n)$
          * $g(n)$: Accumulated travel time from incident site to current node.
          * $h(n)$: Admissible Euclidean distance divided by max speed.
          * **Why Selected:** Guarantees mathematically optimal shortest route without getting trapped in traffic bottlenecks.
        * **Greedy Best-First Formula:** $f(n) = h(n)$
          * Ignores accumulated cost $g(n)$, often taking congested detours that appear superficially direct.

        #### 2. Model-Based Reflex Agent (ICU Patient Telemetry)
        * **Agent Formula:** $S_{t+1} = \text{UpdateState}(S_t, A_t, P_{t+1})$
        * **Why Selected:** Unlike a Simple Reflex Agent which evaluates only instantaneous thresholds and triggers false alarms on transient anxiety spikes, the Model-Based Agent maintains rolling vital histories to calculate the **Shock Index** ($\text{HR}/\text{Sys BP}$) and detect progressive multi-organ sepsis.

        #### 3. Constraint Satisfaction Problem & Min-Conflicts (Doctor Duty Roster)
        * **CSP Triplet:** $(X, D, C)$
          * $X$: 10 Hospital Shift Slots
          * $D$: Qualified Medical Specialists
          * $C$: No concurrent double-booking, specialty qualification, and maximum shift quotas.
        * **Why Selected:** Min-Conflicts is a heuristic local search that resolves schedule violations in milliseconds with $O(n)$ space.

        #### 4. Propositional Horn-Clause Forward Chaining (Emergency Clinical Triage)
        * **Clause Structure:** $p_1 \land p_2 \land \dots \land p_k \implies q$
        * **Why Selected:** Uses Modus Ponens to derive explainable acuity levels (ESI 1-5) directly from clinical symptoms with a complete proof trace.

        #### 5. Partial Order Planning (Trauma Surgery Coordination)
        * **Plan Structure:** $\langle \text{Actions}, \text{Ordering Constraints}, \text{Causal Links} \rangle$
        * **Why Selected:** Enables multi-team concurrency: nursing sets IV access while surgical technicians simultaneously sterilize laparotomy instruments in parallel.
        """)

    with ai_tab2:
        st.markdown("### Asymptotic Complexity & Optimality Comparison")
        theory_table = [
            {"Algorithm": "A* Search", "Evaluation Function": "f(n) = g(n) + h(n)", "Time Complexity": "O(b^d)", "Space Complexity": "O(b^d)", "Optimality": "Guaranteed (h is admissible)", "Completeness": "Complete"},
            {"Algorithm": "Greedy Best-First", "Evaluation Function": "f(n) = h(n)", "Time Complexity": "O(b^m)", "Space Complexity": "O(b^m)", "Optimality": "Not Guaranteed (Suboptimal)", "Completeness": "Incomplete without cycle check"},
            {"Algorithm": "Dijkstra (UCS)", "Evaluation Function": "f(n) = g(n)", "Time Complexity": "O(b^(C*/ε))", "Space Complexity": "O(b^(C*/ε))", "Optimality": "Guaranteed", "Completeness": "Complete"},
            {"Algorithm": "Min-Conflicts CSP", "Evaluation Function": "arg min conflicts(var = v)", "Time Complexity": "O(k · n)", "Space Complexity": "O(n)", "Optimality": "Conflict-Free Satisficing", "Completeness": "Incomplete (mitigated by restarts)"},
            {"Algorithm": "Model-Based Reflex Agent", "Evaluation Function": "S_{t+1} = Update(S_t, P_{t+1})", "Time Complexity": "O(1) per cycle", "Space Complexity": "O(k) rolling history", "Optimality": "High Signal-to-Noise Ratio", "Completeness": "Deterministic"},
            {"Algorithm": "Partial Order Planning", "Evaluation Function": "Causal Links & Preconditions", "Time Complexity": "NP-Hard in general", "Space Complexity": "O(|Actions| + |Links|)", "Optimality": "Shortest Parallel Schedule", "Completeness": "Complete"}
        ]
        st.dataframe(pd.DataFrame(theory_table), use_container_width=True)

    render_academic_disclaimer()
