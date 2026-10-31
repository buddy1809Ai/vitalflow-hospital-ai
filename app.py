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
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    render_html("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 22px;">
        <div style="width: 36px; height: 36px; border-radius: 9px; background: #0284c7; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.15rem; box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);">V</div>
        <div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #0f172a; line-height: 1.1;">VitalFlow AI</div>
            <div style="font-size: 0.78rem; color: #475569; font-weight: 600;">Operations Command</div>
        </div>
    </div>
    """)

    nav_selection = st.radio(
        label="Navigation Menu",
        options=[
            "Overview",
            "Emergency Route Planner",
            "Hospital Operations",
            "AI Insights & Algorithms",
            "Viva Preparation"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #0f172a; margin-bottom: 8px;'>TRAFFIC & ENVIRONMENTAL HAZARDS</div>", unsafe_allow_html=True)
    
    traffic_multiplier = st.select_slider(
        "Congestion Multiplier",
        options=[1.0, 1.2, 1.5, 2.0, 2.5],
        value=1.2,
        format_func=lambda x: f"{x}x {'(Standard)' if x==1.0 else '(Peak Rush)' if x>=2.0 else '(Moderate)'}"
    )

    simulate_road_closure = st.checkbox("Simulate Wardha Road Closure", value=False)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.76rem; color: #475569; line-height: 1.5;">
        <strong>Network:</strong> Nagpur Urban Grid<br>
        <strong>Status:</strong> Active Simulation<br>
        <strong>Syllabus:</strong> 23ADS1502 Core AI
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
        render_html("""
        <div class="content-card">
            <div class="content-header">Nagpur Healthcare Transit Topology</div>
            <div class="content-sub">Interactive spatial map showing emergency facilities, arterial links, and bypass routes.</div>
        </div>
        """)

        blocked = [("Wardha_Road", "Airport_Metro")] if simulate_road_closure else []
        fig_overview = plot_hospital_network(blocked_edges=blocked)
        st.plotly_chart(fig_overview, use_container_width=True)

    with col_info:
        render_html("""
        <div class="content-card">
            <div class="content-header">Operational Workflow</div>
            <div class="content-sub">How decision support is structured in VitalFlow AI:</div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.9rem;">1. Ambulance Route Optimization</strong><br>
                <span style="color: #475569; font-size: 0.83rem;">A* Search guarantees minimal transit time to apex centers (AIIMS / GMC Nagpur), avoiding road closures via the Outer Ring Road.</span>
            </div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.9rem;">2. Patient Telemetry Monitoring</strong><br>
                <span style="color: #475569; font-size: 0.83rem;">Model-Based Reflex Agent tracks continuous physiological trends (Shock Index) to catch early sepsis while suppressing false alarms.</span>
            </div>
            
            <div style="margin-bottom: 14px;">
                <strong style="color: #0f172a; font-size: 0.9rem;">3. Hospital Staff Scheduling</strong><br>
                <span style="color: #475569; font-size: 0.83rem;">Constraint Satisfaction Problem (CSP) solved via Min-Conflicts local search to produce 100% conflict-free doctor rosters.</span>
            </div>
            
            <div>
                <strong style="color: #0f172a; font-size: 0.9rem;">4. Emergency Triage & Surgical Protocol</strong><br>
                <span style="color: #475569; font-size: 0.83rem;">Propositional forward chaining classifies acuity (ESI 1-5), and Partial Order Planning schedules parallel multi-team surgical steps.</span>
            </div>
        </div>
        """)

    render_academic_disclaimer()


# =============================================================================
# 2. EMERGENCY ROUTE PLANNER (HERO FEATURE)
# =============================================================================
elif nav_selection == "Emergency Route Planner":
    render_syllabus_pill("Practical 4 & 3", "Optimal Path Using A* Search vs Greedy Best-First Search")

    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        render_html("""
        <div class="content-card">
            <div class="content-header">Ambulance Dispatch Control</div>
            <div class="content-sub">Select incident location and receiving emergency trauma hospital.</div>
        </div>
        """)

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
        render_html(f"""
        <div class="kpi-card" style="border-top: 3px solid #059669;">
            <div class="kpi-label">A* Search (Optimal)</div>
            <div class="kpi-value">{a_star['total_cost_minutes']} min</div>
            <div class="kpi-context">
                Nodes Expanded: <strong>{a_star['nodes_expanded']}</strong> | Frontier: <strong>{a_star['peak_frontier_size']}</strong>
            </div>
            <div style="font-size: 0.8rem; color: #059669; margin-top: 8px; font-weight: 600;">
                Guaranteed shortest route via f(n) = g(n) + h(n).
            </div>
        </div>
        """)

    with col_m2:
        is_suboptimal = greedy["total_cost_minutes"] > a_star["total_cost_minutes"]
        border_c = "#ef4444" if is_suboptimal else "#f59e0b"
        tag_color = "#dc2626" if is_suboptimal else "#d97706"
        detour_msg = "Suboptimal detour taken due to f = h ignoring cost g." if is_suboptimal else "Matches optimal route in this corridor."
        render_html(f"""
        <div class="kpi-card" style="border-top: 3px solid {border_c};">
            <div class="kpi-label">Greedy Best-First</div>
            <div class="kpi-value">{greedy['total_cost_minutes']} min</div>
            <div class="kpi-context">
                Nodes Expanded: <strong>{greedy['nodes_expanded']}</strong> | Frontier: <strong>{greedy['peak_frontier_size']}</strong>
            </div>
            <div style="font-size: 0.8rem; color: {tag_color}; margin-top: 8px; font-weight: 600;">
                {detour_msg}
            </div>
        </div>
        """)

    with col_m3:
        render_html(f"""
        <div class="kpi-card" style="border-top: 3px solid #0284c7;">
            <div class="kpi-label">Dijkstra Search</div>
            <div class="kpi-value">{dijkstra['total_cost_minutes']} min</div>
            <div class="kpi-context">
                Nodes Expanded: <strong>{dijkstra['nodes_expanded']}</strong> | Frontier: <strong>{dijkstra['peak_frontier_size']}</strong>
            </div>
            <div style="font-size: 0.8rem; color: #0284c7; margin-top: 8px; font-weight: 600;">
                Optimal but uninformed (h = 0), blind exploration.
            </div>
        </div>
        """)

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
            render_html("""
            <div class="content-card">
                <div class="content-header">Patient Telemetry Stream</div>
                <div class="content-sub">Inspect rolling vital signs and agent response over time.</div>
            </div>
            """)

            selected_pid = st.selectbox(
                "Monitored Patient Bed",
                options=list(PATIENT_TELEMETRY_STREAM.keys()),
                format_func=lambda k: f"{k}: {PATIENT_TELEMETRY_STREAM[k]['name']} ({PATIENT_TELEMETRY_STREAM[k]['bed']})"
            )

            p_info = PATIENT_TELEMETRY_STREAM[selected_pid]
            st.markdown(f"**Diagnosis:** {p_info['admit_diagnosis']}")
            st.markdown(f"**Expected Trajectory:** {p_info['expected_progression']}")

            # TYPE-SAFE SLIDER IMPLEMENTATION (Eliminates float indexing TypeError)
            total_steps = len(p_info["timesteps"])
            time_step = st.slider(
                "Inspection Time Window",
                min_value=1,
                max_value=total_steps,
                value=total_steps,
                step=1,
                format_func=lambda s: f"Step {int(s)} ({p_info['timesteps'][int(s)-1]['time']})"
            )
            time_step_int = max(1, min(int(time_step), total_steps))

        mb_agent = ModelBasedReflexAgent(selected_pid, p_info["name"])
        sr_agent = SimpleReflexAgent()

        agent_log = []
        for i in range(time_step_int):
            ts = p_info["timesteps"][i]
            mb_out = mb_agent.update_internal_state(ts, str(ts.get("time", f"T{i+1}")))
            sr_out = sr_agent.evaluate_percept(ts)
            agent_log.append({
                "time": ts.get("time", f"T{i+1}"),
                "vitals": ts,
                "mb": mb_out,
                "sr": sr_out
            })

        curr_mb = agent_log[-1]["mb"]
        curr_sr = agent_log[-1]["sr"]
        curr_vitals = agent_log[-1]["vitals"]

        with col_pat_plot:
            fig_vitals = plot_patient_telemetry(p_info["timesteps"][:time_step_int], p_info["name"])
            st.plotly_chart(fig_vitals, use_container_width=True)

        st.markdown("### Agent Decision Comparison")
        col_ag_mb, col_ag_sr = st.columns(2)

        with col_ag_mb:
            alert_color = "#dc2626" if "LEVEL_3" in curr_mb["alert_level"] else "#d97706" if "LEVEL_2" in curr_mb["alert_level"] else "#16a34a"
            render_html(f"""
            <div class="kpi-card" style="border-top: 3px solid {alert_color};">
                <div class="kpi-label">Model-Based Reflex Agent (With Temporal Memory)</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: {alert_color}; margin: 6px 0;">
                    {curr_mb['action']}
                </div>
                <div style="font-size: 0.85rem; line-height: 1.5; color: #334155;">
                    <strong>Physiological Trend:</strong> {curr_mb['trend']}<br>
                    <strong>Calculated Shock Index:</strong> {curr_mb['shock_index']} (Normal: 0.5 - 0.7)<br>
                    <strong>Pattern Detected:</strong> {curr_mb['suspected_syndrome']}<br>
                    <strong>Clinical Rationale:</strong> {curr_mb['rationale']}
                </div>
            </div>
            """)

        with col_ag_sr:
            sr_c = "#dc2626" if curr_sr["severity"] == "CRITICAL" else "#d97706" if curr_sr["severity"] == "HIGH" else "#16a34a"
            render_html(f"""
            <div class="kpi-card" style="border-top: 3px solid {sr_c};">
                <div class="kpi-label">Simple Reflex Agent (Immediate Percept Only)</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: {sr_c}; margin: 6px 0;">
                    {curr_sr['action']}
                </div>
                <div style="font-size: 0.85rem; line-height: 1.5; color: #334155;">
                    <strong>Observation:</strong> HR={curr_vitals['hr']}, BP={curr_vitals['sys_bp']}/{curr_vitals['dia_bp']}, SpO2={curr_vitals['spo2']}%<br>
                    <strong>Memory State:</strong> None (S = ∅)<br>
                    <strong>Evaluation:</strong> {curr_sr['message']}<br>
                    <strong>Limitation:</strong> Susceptible to false alarms on transient spikes; delayed detection of gradual septic collapse.
                </div>
            </div>
            """)

    # --- TAB 2: Staff Duty Scheduling (CSP Min-Conflicts) ---
    with ops_tab2:
        render_syllabus_pill("Practical 5", "Map Coloring for Adjoining Regions using Min-Conflicts (CSP)")

        col_csp_l, col_csp_r = st.columns([1, 1.8])

        with col_csp_l:
            render_html("""
            <div class="content-card">
                <div class="content-header">Constraint Satisfaction Solver</div>
                <div class="content-sub">Assign specialists to emergency shifts without constraint violations.</div>
            </div>
            """)

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
            render_html(f"""
            <div class="kpi-card" style="border-top: 3px solid #0284c7; margin-bottom: 12px;">
                <div class="kpi-label">Inferred Emergency Acuity</div>
                <div style="font-size: 1.35rem; font-weight: 700; color: #0f172a; margin: 4px 0;">
                    {triage_out['final_esi_level']}
                </div>
                <div style="font-size: 0.88rem; color: #0284c7; font-weight: 600;">
                    Target Department: {triage_out['assigned_bay']}
                </div>
                <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">
                    Derived via {triage_out['rules_fired_count']} Horn clauses using Modus Ponens forward deduction.
                </div>
            </div>
            """)

            if triage_out["firing_history"]:
                for step in triage_out["firing_history"]:
                    render_html(f"""
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 12px; margin-bottom: 6px; font-size: 0.82rem;">
                        <strong style="color: #0284c7;">Rule [{step['rule']}]:</strong> <code>{' ∧ '.join(step['antecedents'])} ⇒ {step['consequent']}</code>
                    </div>
                    """)

        st.write("")
        st.markdown("---")

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


# =============================================================================
# 4. AI INSIGHTS & ALGORITHM EXPLANATIONS
# =============================================================================
elif nav_selection == "AI Insights & Algorithms":
    render_html("""
    <div class="content-card">
        <div class="content-header">AI Architecture & Mathematical Foundations</div>
        <div class="content-sub">Clear, demonstrable explanations of how each algorithm works with actual execution results.</div>
    </div>
    """)

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


# =============================================================================
# 5. VIVA PREPARATION & ACADEMIC DEFENSE
# =============================================================================
elif nav_selection == "Viva Preparation":
    render_html("""
    <div class="content-card">
        <div class="content-header">Viva Voce Preparation & Academic Defense Guide</div>
        <div class="content-sub">Comprehensive reference material, syllabus mapping, and 30 core exam questions with clear, simple answers.</div>
    </div>
    """)

    viva_tab1, viva_tab2, viva_tab3 = st.tabs([
        "Project Architecture & Rationale",
        "Syllabus Practical Mapping",
        "Top 30 Viva Questions & Model Answers"
    ])

    with viva_tab1:
        st.markdown("""
        ### Project Summary: VitalFlow AI
        **VitalFlow AI** is an autonomous hospital operations and emergency logistics command platform that unifies classical search, intelligent agents, constraint satisfaction, formal logic, and partial order planning to solve critical urban healthcare challenges.

        #### Problem Statement:
        In emergency medicine, the first 60 minutes after severe trauma are known as the **Golden Hour**. Traffic congestion delays ambulances, ICU monitors trigger frequent false alarms causing alarm fatigue, doctor shift scheduling suffers from burnout and double-booking, and linear surgical workflows cause preventable delays.

        #### Proposed Solution:
        1. **Ambulance Dispatch Optimization:** Uses **A\* Search** ($f = g + h$) with an admissible Euclidean time heuristic to guarantee minimal transit times across Nagpur, rerouting around roadblocks.
        2. **Intelligent ICU Telemetry:** Implements a **Model-Based Reflex Agent** that tracks rolling physiological vectors (Shock Index, SpO2 drift) to detect sepsis and Cushing's Triad while filtering out benign anxiety spikes.
        3. **Doctor Shift Scheduling:** Formulates duty rosters as a **Constraint Satisfaction Problem (CSP)** solved via **Min-Conflicts Local Search** to guarantee zero double-booking and specialty compliance.
        4. **Clinical Triage:** Applies **Propositional Horn-Clause Forward Chaining** for explainable Emergency Severity Index (ESI) deduction, paired with **First-Order Logic Unification** for doctor-patient matching.
        5. **Surgical Protocol Coordination:** Uses **Partial Order Planning (POP)** to execute independent surgical preparation tasks in parallel.
        """)

    with viva_tab2:
        st.markdown("### Practical Syllabus Mapping (Course Code: 23ADS1502)")
        mapping_rows = [
            {"Practical": "Practical 1", "Title": "Smart Light Agent", "Concept": "Simple Reflex Agent", "VitalFlow Implementation": "Threshold-based telemetry agent evaluating instantaneous percepts without memory."},
            {"Practical": "Practical 2", "Title": "Hospital Patient Monitoring Agent", "Concept": "Model-Based Reflex Agent", "VitalFlow Implementation": "Telemetry agent maintaining internal state history to track physiological deterioration and Shock Index."},
            {"Practical": "Practical 3", "Title": "Shortest Path Using Greedy Best-First", "Concept": "Heuristic Search (f = h)", "VitalFlow Implementation": "Demonstrating that ignoring path cost g leads to congested, suboptimal ambulance detours."},
            {"Practical": "Practical 4", "Title": "Optimal Path Using A* Search", "Concept": "Informed Search (f = g + h)", "VitalFlow Implementation": "Ambulance navigation guaranteeing shortest travel time via an admissible Euclidean heuristic."},
            {"Practical": "Practical 5", "Title": "Map Coloring using Min-Conflicts", "Concept": "CSP & Local Search", "VitalFlow Implementation": "Hospital duty scheduling resolving shift conflicts (Variables: Shifts, Domains: Doctors, Constraints: No double-booking)."},
            {"Practical": "Practical 7", "Title": "Smart Garden System", "Concept": "Propositional Logic", "VitalFlow Implementation": "Emergency Triage Knowledge Base inferring ESI acuity levels using Horn-clause forward chaining."},
            {"Practical": "Practical 8", "Title": "Assistant Bot using Unification", "Concept": "FOL Unification", "VitalFlow Implementation": "Matching patient clinical needs with attending doctor specialties using Most General Unifier (MGU)."},
            {"Practical": "Practical 9", "Title": "Nagpur Metro Route Planner", "Concept": "State-Space Forward Search", "VitalFlow Implementation": "Topological graph of Nagpur healthcare facilities and transit corridors."},
            {"Practical": "Practical 10", "Title": "Kitchen Task Planner", "Concept": "Partial Order Planning", "VitalFlow Implementation": "Multi-team emergency trauma laparotomy protocol scheduled non-linearly with causal links."}
        ]
        st.dataframe(pd.DataFrame(mapping_rows), use_container_width=True)

    with viva_tab3:
        st.markdown("### Top 30 High-Yield Viva Questions & Student-Friendly Answers")
        
        qa_list = [
            ("Q1: What is the primary objective of VitalFlow AI?",
             "VitalFlow AI is an autonomous hospital operations command platform. It applies classical and heuristic AI algorithms to optimize ambulance routing, ICU patient vitals monitoring, doctor shift scheduling, clinical triage, and emergency surgical workflows."),
            
            ("Q2: Why did you choose A* Search over Dijkstra and Greedy Best-First Search for ambulance routing?",
             "A* combines the actual travel time from the origin g(n) with an admissible heuristic estimate to the destination h(n). Dijkstra is optimal but uninformed (h=0), searching blindly in all directions. Greedy Best-First considers only h(n), making it fast but susceptible to suboptimal detours. A* guarantees the mathematically optimal shortest route with minimal node expansions."),
            
            ("Q3: What makes a heuristic admissible in A* Search?",
             "A heuristic h(n) is admissible if it never overestimates the true cost to reach the goal (h(n) <= h*(n)). In our project, travel time is the cost. We divide the straight-line Euclidean distance by the maximum theoretical road speed (60 km/h). Because an ambulance cannot travel faster than 60 km/h or on a path shorter than a straight line, our heuristic time estimate is guaranteed to be <= actual travel time, ensuring A* returns the optimal route."),
            
            ("Q4: How does a Model-Based Reflex Agent differ from a Simple Reflex Agent in patient monitoring?",
             "A Simple Reflex Agent acts only on current percepts with no memory (S = ∅). It triggers false alarms during temporary stress spikes and misses gradual deterioration. A Model-Based Reflex Agent maintains an internal state representation across time (S_{t+1} = Update(S_t, A_t, P_{t+1})), tracking physiological trends, Shock Index, and rate-of-change to detect true medical crises like sepsis."),
            
            ("Q5: What is Shock Index and why does the agent compute it?",
             "Shock Index is defined as Heart Rate divided by Systolic Blood Pressure (Normal: 0.5 to 0.7). An elevated Shock Index (> 0.9) reveals occult hemorrhagic or septic shock even before standard blood pressure thresholds drop catastrophically."),
            
            ("Q6: How is hospital duty scheduling formulated as a Constraint Satisfaction Problem (CSP)?",
             "A CSP is defined by a triplet (X, D, C). In our system: Variables X are the shift slots (e.g., ICU Morning, ER Night). Domains D are the eligible doctors. Constraints C include no double-booking at the same time, specialty eligibility, and maximum shift quotas per cycle."),
            
            ("Q7: How does the Min-Conflicts algorithm work?",
             "Min-Conflicts is a heuristic local search algorithm. It starts with an initial (possibly conflicted) assignment. In each iteration, it selects a conflicted variable and reassigns it the value from its domain that results in the minimum number of total constraint violations. If trapped in local minima, it performs a random restart."),
            
            ("Q8: What is Forward Chaining in Propositional Logic?",
             "Forward Chaining is a data-driven reasoning strategy. It starts with known asserted facts in the knowledge base and fires Definite Horn Clauses whose antecedents are satisfied, deriving new facts until a goal conclusion (such as ESI Acuity Level 1 or 2) is proven."),
            
            ("Q9: What is the Unification algorithm in First-Order Logic?",
             "Unification is an algorithmic process that finds a substitution mapping (Most General Unifier or MGU θ) for variables in two predicate logic expressions such that Subst(θ, p1) == Subst(θ, p2). We use it to match patient clinical demands with available physician attributes."),
            
            ("Q10: What is Partial Order Planning (POP) and why is it better than Linear Planning for trauma resuscitation?",
             "Linear planning forces all actions into a single strict sequence. Partial Order Planning produces a plan with ordering constraints and causal links, specifying order only when necessary. This allows multiple hospital teams (such as nurses starting IV lines and scrub technicians sterilizing instruments) to execute tasks concurrently in parallel stages."),
            
            ("Q11: What is a Definite Horn Clause?",
             "A Definite Horn Clause is a logical clause with exactly one positive literal, written in implication form as p1 ∧ p2 ∧ ... ∧ pk ⇒ q. Horn clauses allow forward chaining to run in linear time with respect to the knowledge base size."),
             
            ("Q12: What is the branching factor in your search graph?",
             "In our Nagpur healthcare graph, the average branching factor is approximately 3. This low branching factor allows A* to find the optimal path in fewer than 15 node expansions."),
             
            ("Q13: How does your system handle dynamic road closures?",
             "When a road closure occurs (such as construction on Wardha Road), the graph adjacency matrix dynamically removes the blocked edge. A* automatically recalculates and navigates around the obstruction via alternative corridors like the Outer Ring Road."),
             
            ("Q14: What is the time complexity of A* Search?",
             "In the worst case, time complexity is O(b^d), where b is the branching factor and d is the depth of the optimal solution. Because A* stores all open and closed nodes in memory, space complexity is also O(b^d)."),
             
            ("Q15: Why did Greedy Best-First Search take a longer path than A* in your benchmark?",
             "Greedy Best-First Search uses f(n) = h(n) and ignores path cost g(n). It expanded nodes that physically appeared closest to the destination, which led it into congested central roads with severe slowdowns, totaling 27.88 minutes compared to 25.23 minutes for A*."),
             
            ("Q16: What is Cushing's Triad and how does your agent detect it?",
             "Cushing's Triad is a physiological response to dangerously elevated intracranial pressure. It consists of severe bradycardia (low HR), severe systolic hypertension (high BP), and irregular/slow bradypneic respiration. Our agent monitors all three parameters simultaneously and flags an acute neuro-crisis."),
             
            ("Q17: What are hard constraints versus soft constraints?",
             "Hard constraints are mandatory conditions that cannot be violated under any circumstances (e.g., a doctor cannot be in two rooms at once). Soft constraints are preferences (e.g., distributing night shifts equally)."),
             
            ("Q18: What is a Causal Link in Partial Order Planning?",
             "A causal link is written as A_i --(p)--> A_j. It asserts that action A_i achieves the precondition condition p that is required by action A_j. Causal links ensure that no interfering action deletes p before A_j executes."),
             
            ("Q19: What is the Emergency Severity Index (ESI)?",
             "ESI is a five-level emergency department triage algorithm: Level 1 is Resuscitation (immediate life threat), Level 2 is Emergent (high risk, time-sensitive), Level 3 is Urgent (needs multiple diagnostic resources), Level 4 is Semi-Urgent, and Level 5 is Non-Urgent."),
             
            ("Q20: Why did you build the application in Streamlit?",
             "Streamlit is an enterprise-grade Python framework that allows seamless integration with scientific computing libraries (NumPy, Pandas, Plotly) without requiring decoupled REST APIs or JavaScript middleware, keeping the code clean, reproducible, and deployable on Streamlit Community Cloud."),
             
            ("Q21: What are the main limitations of the current system?",
             "Currently, road traffic conditions and patient telemetry are simulated based on realistic clinical profiles rather than live hardware IoT pulse oximeters or live Google Maps Traffic API polling."),
             
            ("Q22: How can this project be extended in the future?",
             "Future enhancements include connecting live wearable IoT sensors via MQTT, integrating OpenStreetMap live traffic feeds, and adding Reinforcement Learning for dynamic ambulance dispatch repositioning."),
             
            ("Q23: How does your project satisfy Course Outcome CO2?",
             "CO2 requires students to 'Apply various search algorithms for goal-based problem solving and planning.' Our project implements A* Search, Greedy Best-First Search, Dijkstra, and Partial Order Planning with quantitative benchmark metrics."),
             
            ("Q24: What is the Most General Unifier (MGU)?",
             "In First-Order Logic, the MGU is the most general substitution mapping of variables that makes two predicate logic expressions syntactically identical without unnecessary restrictions."),
             
            ("Q25: Why didn't you build a basic chatbot or Tic-Tac-Toe?",
             "We deliberately selected an integrated healthcare operations command system that unifies five distinct classical and heuristic AI paradigms from our practical syllabus to solve an impactful real-world problem rather than an isolated game toy.")
        ]

        for q, a in qa_list:
            with st.expander(f"**{q}**"):
                st.write(a)

    render_academic_disclaimer()
