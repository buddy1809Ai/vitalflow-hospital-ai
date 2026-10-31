"""
app.py
======
VITALFLOW AI: Autonomous Hospital Operations & Emergency Logistics Command System
B.Tech Artificial Intelligence & Data Science (AIDS) V-Semester Minor Project

Author: AI & Data Science Engineering Student
Affiliation: YCCE (Autonomous under RTMNU Nagpur)
Technology Stack: Python, Streamlit, Plotly, NumPy, Pandas, Scikit-learn
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from typing import List, Tuple

# Import custom design system & UI components
from ui.styles import get_custom_css
from ui.components import render_hero_banner, render_kpi_row, render_alert_strip, render_syllabus_badge
from ui.visualizers import (
    plot_hospital_network,
    plot_patient_telemetry,
    plot_csp_convergence,
    plot_partial_order_plan
)

# Import Core AI Algorithms
from data.hospital_network import HOSPITAL_NODES, ROAD_EDGES, get_network_graph
from data.patient_cases import PATIENT_TELEMETRY_STREAM, TRIAGE_PRESET_SCENARIOS
from data.staff_resources import DOCTORS_DIRECTORY, SHIFT_SLOTS
from core.search_planner import compare_search_algorithms, a_star_search, greedy_best_first_search, dijkstra_search
from core.reflex_agents import SimpleReflexAgent, ModelBasedReflexAgent
from core.csp_scheduler import HospitalDutyCSP
from core.logic_triage import ClinicalTriageInferenceEngine, match_clinical_duty
from core.partial_order_plan import PartialOrderPlanner

# Page configuration
st.set_page_config(
    page_title="VitalFlow AI - Hospital Operations Command",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom SaaS styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <span style="font-size: 1.8rem;">🩺</span>
        <div>
            <h2 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #0f172a;">VITALFLOW AI</h2>
            <span style="font-size: 0.76rem; color: #64748b; font-weight: 600;">Autonomous Operations Hub</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation Modules")
    selected_module = st.radio(
        label="Select Operational Module",
        options=[
            "🚑 Emergency Ambulance Route Planner",
            "🩺 ICU Patient Telemetry Agent",
            "🧩 Medical Staff & Bed CSP Allocator",
            "⚖️ Clinical Triage & Proof Engine",
            "⏱️ Trauma Protocol Partial Order Planner",
            "📊 Algorithmic Benchmarks & Complexity",
            "🎓 Viva Preparation & Project Guide"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### City Environmental Conditions")
    traffic_condition = st.select_slider(
        "Urban Traffic Congestion Multiplier",
        options=[1.0, 1.2, 1.5, 2.0, 2.5],
        value=1.2,
        format_func=lambda x: f"{x}x {'(Normal)' if x==1.0 else '(Peak Rush)' if x>=2.0 else '(Moderate)'}"
    )

    road_closure_toggle = st.checkbox("Simulate Wardha Road Construction Closure", value=False)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.78rem; color: #64748b; line-height: 1.5;">
        <strong>Project Details:</strong><br>
        B.Tech V-Sem AI & DS Minor Project<br>
        YCCE Nagpur (Dept. of Computer Technology)<br>
        Core: State-Space Search, Reflex Agents, CSP, Horn Logic, POP
    </div>
    """, unsafe_allow_html=True)


# Render Global Top Hero
render_hero_banner()

# Global metrics row
kpi_data = [
    {"title": "Network Nodes", "value": f"{len(HOSPITAL_NODES)} Facilities", "sub": "Nagpur Urban Healthcare Grid"},
    {"title": "Active Traffic Multiplier", "value": f"{traffic_condition}x", "sub": "Dynamic Time Cost Multiplier"},
    {"title": "AI Algorithms Running", "value": "5 Distinct Paradigms", "sub": "Search, Agents, CSP, Logic, POP"},
    {"title": "System Health", "value": "100% Operational", "sub": "Zero-failure fault tolerance"}
]
render_kpi_row(kpi_data)
st.write("")


# ==============================================================================
# MODULE 1: Dynamic Emergency Transit & Ambulance Routing (A* vs Greedy vs Dijkstra)
# ==============================================================================
if selected_module == "🚑 Emergency Ambulance Route Planner":
    render_syllabus_badge(
        practical_num=4,
        practical_title="Optimal Path Using A* Search & Practical 3: Greedy Best-First Search & Practical 9: Forward Route Planning",
        ai_concept="Heuristic State-Space Search (f(n) = g(n) + h(n))"
    )

    col1, col2 = st.columns([1, 2.2])

    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">🚑 Dispatch Parameters</div>
            <div class="section-desc">Select emergency incident origin and destination apex trauma facility.</div>
        </div>
        """, unsafe_allow_html=True)

        start_station = st.selectbox(
            "Incident Location (Origin)",
            options=list(HOSPITAL_NODES.keys()),
            index=list(HOSPITAL_NODES.keys()).index("Sitabuldi")
        )

        goal_station = st.selectbox(
            "Apex Receiving Hospital (Destination)",
            options=list(HOSPITAL_NODES.keys()),
            index=list(HOSPITAL_NODES.keys()).index("AIIMS_Nagpur")
        )

        heuristic_choice = st.radio(
            "Heuristic Function h(n)",
            options=["euclidean", "manhattan"],
            format_func=lambda x: "Euclidean Distance (Straight Line)" if x == "euclidean" else "Manhattan Distance (L1 City Block Grid)"
        )

        blocked_roads = []
        if road_closure_toggle:
            blocked_roads.append(("Wardha_Road", "Airport_Metro"))
            st.warning("⚠️ Road Closure Active: Wardha Road Arterial Link is BLOCKED.")

        run_search_btn = st.button("🚀 Calculate Emergency Routes", use_container_width=True, type="primary")

    # Compute Search
    results_bundle = compare_search_algorithms(
        start=start_station,
        goal=goal_station,
        traffic_multiplier=traffic_condition,
        blocked_edges=blocked_roads,
        heuristic_type=heuristic_choice
    )

    a_star = results_bundle["results"]["A* Search"]
    greedy = results_bundle["results"]["Greedy Best-First"]
    dijkstra = results_bundle["results"]["Dijkstra"]

    with col2:
        fig_map = plot_hospital_network(
            a_star_path=a_star["path"] if a_star["success"] else [],
            greedy_path=greedy["path"] if greedy["success"] else [],
            blocked_edges=blocked_roads
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # Comparative Metric Cards
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #10b981;">
            <div class="metric-title">A* Search (Optimal)</div>
            <div class="metric-value">{a_star['total_cost_minutes']} min</div>
            <div class="metric-sub" style="color: #059669;">
                Expanded: {a_star['nodes_expanded']} nodes | Peak Frontier: {a_star['peak_frontier_size']}
            </div>
            <div style="font-size: 0.78rem; color: #64748b; margin-top: 6px;">
                Guaranteed shortest route via f(n) = g(n) + h(n).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with mcol2:
        is_suboptimal = greedy['total_cost_minutes'] > a_star['total_cost_minutes']
        tag_color = "#f59e0b" if not is_suboptimal else "#ef4444"
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {tag_color};">
            <div class="metric-title">Greedy Best-First Search</div>
            <div class="metric-value">{greedy['total_cost_minutes']} min</div>
            <div class="metric-sub" style="color: {tag_color};">
                Expanded: {greedy['nodes_expanded']} nodes | Peak Frontier: {greedy['peak_frontier_size']}
            </div>
            <div style="font-size: 0.78rem; color: #64748b; margin-top: 6px;">
                {"⚠️ Suboptimal Detour Detected!" if is_suboptimal else "Greedy matches optimal path in this topology."}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with mcol3:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #3b82f6;">
            <div class="metric-title">Dijkstra (Uniform Cost)</div>
            <div class="metric-value">{dijkstra['total_cost_minutes']} min</div>
            <div class="metric-sub" style="color: #2563eb;">
                Expanded: {dijkstra['nodes_expanded']} nodes | Peak Frontier: {dijkstra['peak_frontier_size']}
            </div>
            <div style="font-size: 0.78rem; color: #64748b; margin-top: 6px;">
                Optimal but uninformed (h=0), blind search exploration.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    with st.expander("🔍 Step-by-Step Search Decision Log (A* Node Expansion Order)", expanded=False):
        st.write("Detailed trace showing how $f(n) = g(n) + h(n)$ guided the priority queue:")
        df_trace = pd.DataFrame(a_star["visited_order"])
        st.dataframe(df_trace[["step", "display_name", "g", "h", "f", "explanation"]], use_container_width=True)


# ==============================================================================
# MODULE 2: ICU Patient Telemetry & Deterioration Monitor (Model-Based Reflex Agent)
# ==============================================================================
elif selected_module == "🩺 ICU Patient Telemetry Agent":
    render_syllabus_badge(
        practical_num=2,
        practical_title="Hospital Patient Monitoring Agent (Model-Based Reflex Agent) & Practical 1: Smart Light Agent",
        ai_concept="Intelligent Agent Architecture with Internal Temporal State"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">🩺 Telemetry Stream Selection</div>
            <div class="section-desc">Select patient telemetry stream to simulate real-time vital monitoring.</div>
        </div>
        """, unsafe_allow_html=True)

        patient_choice = st.selectbox(
            "Select Monitored Bed / Patient",
            options=list(PATIENT_TELEMETRY_STREAM.keys()),
            format_func=lambda k: f"{k}: {PATIENT_TELEMETRY_STREAM[k]['name']} ({PATIENT_TELEMETRY_STREAM[k]['bed']})"
        )

        patient_data = PATIENT_TELEMETRY_STREAM[patient_choice]
        st.info(f"**Clinical Context:** {patient_data['admit_diagnosis']}\n\n**Expected Trajectory:** {patient_data['expected_progression']}")

        inspection_step = st.slider(
            "Simulate Time Step Inspection Window",
            min_value=1,
            max_value=len(patient_data["timesteps"]),
            value=len(patient_data["timesteps"]),
            format_func=lambda s: f"Time {patient_data['timesteps'][s-1]['time']} (Interval #{s})"
        )

    # Instantiate Agents
    mb_agent = ModelBasedReflexAgent(patient_id=patient_choice, patient_name=patient_data["name"])
    sr_agent = SimpleReflexAgent()

    # Feed history up to current slider
    history_logs = []
    for i in range(inspection_step):
        current_ts = patient_data["timesteps"][i]
        mb_decision = mb_agent.update_internal_state(current_ts, current_ts["time"])
        sr_decision = sr_agent.evaluate_percept(current_ts)
        history_logs.append({
            "step": i + 1,
            "time": current_ts["time"],
            "vitals": current_ts,
            "mb_agent": mb_decision,
            "sr_agent": sr_decision
        })

    latest_mb = history_logs[-1]["mb_agent"]
    latest_sr = history_logs[-1]["sr_agent"]
    latest_vitals = history_logs[-1]["vitals"]

    with col2:
        sub_timesteps = patient_data["timesteps"][:inspection_step]
        fig_telemetry = plot_patient_telemetry(sub_timesteps, patient_data["name"])
        st.plotly_chart(fig_telemetry, use_container_width=True)

    # Agent Comparison Panel
    st.markdown("### Agent Decision Comparison: Model-Based vs Simple Reflex")
    c_mb, c_sr = st.columns(2)

    with c_mb:
        level_color = "#ef4444" if "LEVEL_3" in latest_mb["alert_level"] else "#f59e0b" if "LEVEL_2" in latest_mb["alert_level"] else "#10b981"
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {level_color};">
            <div class="metric-title">Model-Based Reflex Agent (Practical 2)</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: {level_color}; margin: 8px 0;">
                {latest_mb['action']}
            </div>
            <div style="font-size: 0.85rem; color: #1e293b; line-height: 1.5;">
                <strong>Internal Trend:</strong> {latest_mb['trend']}<br>
                <strong>Shock Index:</strong> {latest_mb['shock_index']} (Normal: 0.5 - 0.7)<br>
                <strong>Syndrome Detected:</strong> {latest_mb['suspected_syndrome']}<br>
                <strong>Agent Rationale:</strong> {latest_mb['rationale']}
            </div>
            <div style="margin-top: 10px; font-size: 0.78rem; color: #64748b;">
                ✅ Maintains state memory across rolling intervals ($S_{{t+1}} = \\text{{Update}}(S_t, P_t)$).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_sr:
        sr_color = "#ef4444" if latest_sr["severity"] == "CRITICAL" else "#f59e0b" if latest_sr["severity"] == "HIGH" else "#10b981"
        st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid {sr_color};">
            <div class="metric-title">Simple Reflex Agent (Practical 1)</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: {sr_color}; margin: 8px 0;">
                {latest_sr['action']}
            </div>
            <div style="font-size: 0.85rem; color: #1e293b; line-height: 1.5;">
                <strong>Current Percept Only:</strong> HR={latest_vitals['hr']}, BP={latest_vitals['sys_bp']}/{latest_vitals['dia_bp']}, SpO2={latest_vitals['spo2']}%<br>
                <strong>Memory Model:</strong> None ($S_t = \\emptyset$)<br>
                <strong>Agent Message:</strong> {latest_sr['message']}<br>
                <strong>Reasoning:</strong> {latest_sr['reasoning']}
            </div>
            <div style="margin-top: 10px; font-size: 0.78rem; color: #64748b;">
                ⚠️ Vulnerable to false alarms during stress spikes and blind to slow deterioration trends.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    with st.expander("📋 Inspection History Log & Internal State Vector", expanded=False):
        table_rows = []
        for l in history_logs:
            table_rows.append({
                "Time": l["time"],
                "Heart Rate": l["vitals"]["hr"],
                "Blood Pressure": f"{l['vitals']['sys_bp']}/{l['vitals']['dia_bp']}",
                "SpO2 (%)": l["vitals"]["spo2"],
                "Shock Index": l["mb_agent"]["shock_index"],
                "Model Agent Action": l["mb_agent"]["action"],
                "Trend": l["mb_agent"]["trend"],
                "Simple Reflex Action": l["sr_agent"]["action"]
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True)


# ==============================================================================
# MODULE 3: Medical Staff & Bed CSP Allocator (Min-Conflicts Algorithm)
# ==============================================================================
elif selected_module == "🧩 Medical Staff & Bed CSP Allocator":
    render_syllabus_badge(
        practical_num=5,
        practical_title="Map Coloring for Adjoining Regions using Min-Conflicts (CSP & Local Search)",
        ai_concept="Constraint Satisfaction Problem (Variables, Domains, Hard Constraints)"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">🧩 CSP Duty Scheduling</div>
            <div class="section-desc">Assign qualified doctors to emergency shifts without constraint violations.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Hard Constraints Applied:**
        1. 🚫 **No Double Booking:** Doctor cannot work two shifts at same time.
        2. 🎓 **Specialty Match:** Doctor's specialty must qualify for the ward.
        3. 🔋 **Fatigue Limit:** Doctor cannot exceed allotted shifts per cycle.
        """)

        max_steps_slider = st.slider("Max Search Iterations per Restart", 50, 500, 200, step=50)
        restarts_slider = st.slider("Random Restarts Count", 1, 10, 5)

        solve_csp_btn = st.button("⚡ Solve Schedule with Min-Conflicts", use_container_width=True, type="primary")

    csp = HospitalDutyCSP()
    csp_res = csp.solve_min_conflicts(max_steps=max_steps_slider, random_restarts=restarts_slider)

    with col2:
        fig_conv = plot_csp_convergence(csp_res["iteration_history"])
        st.plotly_chart(fig_conv, use_container_width=True)

    if csp_res["success"]:
        render_alert_strip(f"✅ Constraint Satisfaction Solved with ZERO Conflicts in {csp_res['total_steps']} steps (Restarts used: {csp_res['restarts_used']}).", "green")
    else:
        render_alert_strip(f"⚠️ Search stopped at local minimum with {csp_res['conflicts']} remaining conflicts. Try increasing restarts.", "red")

    st.markdown("### Optimized Duty Roster Schedule Table")
    df_sched = pd.DataFrame(csp_res["schedule_table"])
    st.dataframe(df_sched, use_container_width=True)

    with st.expander("🔍 Medical Specialists Directory (CSP Variable Domains)"):
        doc_rows = []
        for name, info in DOCTORS_DIRECTORY.items():
            doc_rows.append({
                "Doctor Name": info["name"],
                "Specialty": info["specialty"],
                "Seniority": info["seniority"],
                "Max Shift Quota": info["max_shifts_per_cycle"]
            })
        st.dataframe(pd.DataFrame(doc_rows), use_container_width=True)


# ==============================================================================
# MODULE 4: Clinical Triage & Proof Engine (Propositional Logic & Unification)
# ==============================================================================
elif selected_module == "⚖️ Clinical Triage & Proof Engine":
    render_syllabus_badge(
        practical_num=7,
        practical_title="Smart Garden System (Propositional Logic) & Practical 8: Assistant Bot using Unification (FOL)",
        ai_concept="Definite Horn-Clause Forward Chaining & MGU Unification"
    )

    triage_subtab1, triage_subtab2 = st.tabs(["Prop Logic Forward-Chaining Triage", "First-Order Logic Unification Matcher"])

    with triage_subtab1:
        col1, col2 = st.columns([1, 1.8])

        with col1:
            st.markdown("""
            <div class="section-card">
                <div class="section-header">⚖️ Presenting Symptoms</div>
                <div class="section-desc">Toggle clinical findings to trigger propositional inference rules.</div>
            </div>
            """, unsafe_allow_html=True)

            scenario_preset = st.selectbox(
                "Or Select Clinical Preset Scenario",
                options=["Custom"] + list(TRIAGE_PRESET_SCENARIOS.keys())
            )

            # Checkbox values
            if scenario_preset != "Custom":
                preset = TRIAGE_PRESET_SCENARIOS[scenario_preset]
                c_airway = st.checkbox("Severe Airway Compromise / Stridor", value=preset.get("severe_airway_compromise", False))
                c_bleed = st.checkbox("Active Massive Arterial Hemorrhage", value=preset.get("active_massive_hemorrhage", False))
                c_chest = st.checkbox("Chest Pain with Diaphoresis (Suspected STEMI)", value=preset.get("chest_pain_diaphoresis", False))
                c_stroke = st.checkbox("Acute Focal Deficit (Suspected Stroke)", value=preset.get("suspected_stroke_symptoms", False))
                c_unstable = st.checkbox("Physiological Vitals Unstable (Hypotension/Tachycardia)", value=preset.get("vital_signs_unstable", False))
                c_fever = st.checkbox("High-Grade Fever with Lethargy", value=preset.get("high_fever_lethargy", False))
                c_mild = st.checkbox("Isolated Minor Superficial Abrasion", value=preset.get("mild_abrasion", False))
            else:
                c_airway = st.checkbox("Severe Airway Compromise / Stridor", value=False)
                c_bleed = st.checkbox("Active Massive Arterial Hemorrhage", value=False)
                c_chest = st.checkbox("Chest Pain with Diaphoresis (Suspected STEMI)", value=True)
                c_stroke = st.checkbox("Acute Focal Deficit (Suspected Stroke)", value=False)
                c_unstable = st.checkbox("Physiological Vitals Unstable (Hypotension/Tachycardia)", value=True)
                c_fever = st.checkbox("High-Grade Fever with Lethargy", value=False)
                c_mild = st.checkbox("Isolated Minor Superficial Abrasion", value=False)

            active_facts = []
            if c_airway: active_facts.append("severe_airway_compromise")
            if c_bleed: active_facts.append("active_massive_hemorrhage")
            if c_chest: active_facts.append("chest_pain_diaphoresis")
            if c_stroke: active_facts.append("suspected_stroke_symptoms")
            if c_unstable: active_facts.append("vital_signs_unstable")
            if c_fever: active_facts.append("high_fever_lethargy")
            if c_mild: active_facts.append("mild_abrasion")

        # Run forward chaining
        engine = ClinicalTriageInferenceEngine()
        triage_res = engine.forward_chain(active_facts)

        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 4px solid #3b82f6; margin-bottom: 16px;">
                <div class="metric-title">Automated Triage Inference Result</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 6px 0;">
                    {triage_res['final_esi_level']}
                </div>
                <div style="font-size: 0.95rem; color: #2563eb; font-weight: 600;">
                    Target Department: {triage_res['assigned_bay']}
                </div>
                <div style="font-size: 0.82rem; color: #64748b; margin-top: 6px;">
                    Deduction reached via {triage_res['rules_fired_count']} Horn clauses in propositional knowledge base.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Logical Proof Trace (Deduction Chain)")
            if triage_res["firing_history"]:
                for step in triage_res["firing_history"]:
                    st.markdown(f"""
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                        <strong style="color: #2563eb;">Step {step['step']}: Rule [{step['rule']}] Fired</strong><br>
                        <code style="font-size: 0.82rem; color: #0f172a;">{' ∧ '.join(step['antecedents'])} ⇒ {step['consequent']}</code><br>
                        <span style="font-size: 0.8rem; color: #64748b;"><em>{step['explanation']}</em></span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No inference rules triggered. Patient categorized under default safe observation tier.")

    with triage_subtab2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">🤖 First-Order Logic Unification (Practical 8)</div>
            <div class="section-desc">
                Matches patient clinical resource needs with attending physician qualifications using Unification.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_p, col_d = st.columns(2)
        with col_p:
            pred_patient_str = st.text_input("Patient Need Predicate", value="NeedsSpecialist(P-101, Cardiology, ?shift)")
        with col_d:
            pred_doctor_str = st.text_input("Doctor Availability Predicate", value="NeedsSpecialist(?patient, ?spec, Morning)")

        # Parse terms
        p_terms = [t.strip() for t in pred_patient_str.replace("(", ",").replace(")", "").split(",")]
        d_terms = [t.strip() for t in pred_doctor_str.replace("(", ",").replace(")", "").split(",")]

        unif_res = match_clinical_duty(p_terms, d_terms)

        st.markdown("#### Unification Results")
        if unif_res["unification_success"]:
            st.success(f"✅ Unification Succeeded! Most General Unifier (MGU θ):")
            st.json(unif_res["most_general_unifier"])
        else:
            st.error("❌ Unification Failed: Terms cannot be unified into an MGU.")


# ==============================================================================
# MODULE 5: Trauma Protocol Partial Order Planner (POP)
# ==============================================================================
elif selected_module == "⏱️ Trauma Protocol Partial Order Planner":
    render_syllabus_badge(
        practical_num=10,
        practical_title="Kitchen Task Planner for Anaya (Partial Order Planning)",
        ai_concept="Non-Linear Planning with Causal Links and Open Preconditions"
    )

    col1, col2 = st.columns([1, 2.2])

    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">⏱️ Trauma Surgery Protocol</div>
            <div class="section-desc">Synthesize non-linear parallel task schedule respecting causal constraints.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Why Partial Order Planning?**
        - Unlike rigid linear planning ($A_1 \\to A_2 \\to A_3$), POP allows independent tasks (like Sterilization and IV access) to execute **in parallel** by multiple medical sub-teams.
        - Resolves open preconditions via **causal links**: $A_i \\xrightarrow{p} A_j$.
        """)

        pop_planner = PartialOrderPlanner()
        pop_res = pop_planner.generate_plan()

        st.markdown(f"""
        <div class="metric-card" style="margin-top: 14px;">
            <div class="metric-title">Critical Path Duration</div>
            <div class="metric-value">{pop_res['estimated_critical_path_minutes']} min</div>
            <div class="metric-sub">Across {len(pop_res['execution_tiers'])} Parallel Stages</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig_pop = plot_partial_order_plan(pop_res["execution_tiers"])
        st.plotly_chart(fig_pop, use_container_width=True)

    st.markdown("### Causal Link Dependency Structure")
    df_causal = pd.DataFrame(pop_res["causal_links"])
    st.dataframe(df_causal[["from_action", "condition", "to_action", "from_name", "to_name"]], use_container_width=True)


# ==============================================================================
# MODULE 6: Algorithmic Benchmarks & Complexity Visualizer
# ==============================================================================
elif selected_module == "📊 Algorithmic Benchmarks & Complexity":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">📊 Theoretical & Experimental Algorithmic Analysis</div>
        <div class="section-desc">
            Direct syllabus comparison of Time & Space Complexity, Optimality Guarantees, and Performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    comp_data = [
        {
            "Algorithm": "A* Search",
            "Syllabus Lab": "Practical 4",
            "Evaluation Function": "f(n) = g(n) + h(n)",
            "Time Complexity": "O(b^d)",
            "Space Complexity": "O(b^d) [Keeps all in memory]",
            "Optimality Guarantee": "Optimal (if h is admissible)",
            "Completeness": "Complete"
        },
        {
            "Algorithm": "Greedy Best-First",
            "Syllabus Lab": "Practical 3",
            "Evaluation Function": "f(n) = h(n)",
            "Time Complexity": "O(b^m)",
            "Space Complexity": "O(b^m)",
            "Optimality Guarantee": "Not Optimal (can take detours)",
            "Completeness": "Incomplete (can loop without visited set)"
        },
        {
            "Algorithm": "Dijkstra (UCS)",
            "Syllabus Lab": "Classical Baseline",
            "Evaluation Function": "f(n) = g(n)",
            "Time Complexity": "O(b^(C*/ε))",
            "Space Complexity": "O(b^(C*/ε))",
            "Optimality Guarantee": "Optimal",
            "Completeness": "Complete"
        },
        {
            "Algorithm": "Min-Conflicts Local Search",
            "Syllabus Lab": "Practical 5 (CSP)",
            "Evaluation Function": "arg min conflicts(var = v)",
            "Time Complexity": "O(k * n)",
            "Space Complexity": "O(n) [Extremely lightweight]",
            "Optimality Guarantee": "Satisficing (Conflict-Free)",
            "Completeness": "Incomplete (mitigated by restarts)"
        },
        {
            "Algorithm": "Model-Based Reflex Agent",
            "Syllabus Lab": "Practical 2",
            "Evaluation Function": "S_{t+1} = Update(S_t, P_t)",
            "Time Complexity": "O(1) per percept cycle",
            "Space Complexity": "O(k) rolling history window",
            "Optimality Guarantee": "High Signal-to-Noise Ratio",
            "Completeness": "Deterministic"
        },
        {
            "Algorithm": "Partial Order Planning",
            "Syllabus Lab": "Practical 10",
            "Evaluation Function": "Causal Links & Ordering",
            "Time Complexity": "NP-Hard in general",
            "Space Complexity": "O(|A| + |Constraints|)",
            "Optimality Guarantee": "Shortest Parallel Schedule",
            "Completeness": "Complete"
        }
    ]

    st.dataframe(pd.DataFrame(comp_data), use_container_width=True)

    st.write("")
    st.markdown("### Interactive Pathfinding Stress-Test Across All City Nodes")
    if st.button("Run Comprehensive All-Pairs Benchmark (Sitabuldi to All Hospitals)"):
        benchmark_rows = []
        graph = get_network_graph(traffic_multiplier=traffic_condition)
        for dest in HOSPITAL_NODES:
            if dest == "Sitabuldi":
                continue
            a_res = a_star_search("Sitabuldi", dest, graph)
            g_res = greedy_best_first_search("Sitabuldi", dest, graph)
            d_res = dijkstra_search("Sitabuldi", dest, graph)
            benchmark_rows.append({
                "Destination Node": HOSPITAL_NODES[dest]["name"],
                "A* Time (min)": a_res["total_cost_minutes"],
                "A* Nodes Expanded": a_res["nodes_expanded"],
                "Greedy Time (min)": g_res["total_cost_minutes"],
                "Greedy Nodes Expanded": g_res["nodes_expanded"],
                "Dijkstra Time (min)": d_res["total_cost_minutes"],
                "Dijkstra Nodes Expanded": d_res["nodes_expanded"],
                "Greedy Suboptimal?": "YES (Suboptimal)" if g_res["total_cost_minutes"] > a_res["total_cost_minutes"] else "Matches A*"
            })
        st.dataframe(pd.DataFrame(benchmark_rows), use_container_width=True)


# ==============================================================================
# MODULE 7: Viva Preparation & Project Guide
# ==============================================================================
elif selected_module == "🎓 Viva Preparation & Project Guide":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">🎓 Comprehensive Viva Preparation & Academic Defense Guide</div>
        <div class="section-desc">
            Everything you need to master your 5th-Semester B.Tech AI & Data Science project viva.
        </div>
    </div>
    """, unsafe_allow_html=True)

    guide_tab1, guide_tab2, guide_tab3 = st.tabs(["Project Architecture", "Syllabus Mapping", "Top 25 Viva Questions & Answers"])

    with guide_tab1:
        st.markdown("""
        ### Project Summary: VitalFlow AI
        **VitalFlow AI** is an intelligent hospital operations and emergency logistics command system that synthesizes classical, heuristic, constraint satisfaction, and logical reasoning algorithms to solve life-critical urban healthcare challenges.

        #### System Architecture Flow:
        1. **Emergency Call & Dispatch**: Emergency ambulance dispatch selects optimal routes across Nagpur using **A* Search** ($f(n)=g(n)+h(n)$) compared against **Greedy Best-First Search** (Practicals 3, 4, 9).
        2. **ICU Telemetry Monitoring**: Streaming patient vital signs are processed by a **Model-Based Reflex Agent** that maintains temporal state history to detect progressive deterioration patterns (Sepsis, Cushing's Triad) while suppressing false alarm noise (Practicals 1, 2).
        3. **Hospital Staff & Bed Allocation**: Doctor shift schedules and emergency ward assignments are formulated as a **Constraint Satisfaction Problem (CSP)** and resolved with zero conflicts using the **Min-Conflicts Local Search Algorithm** (Practical 5).
        4. **Emergency Triage Inference**: Presenting emergency symptoms trigger a **Propositional Horn-Clause Forward Chaining Engine** that classifies acuity (ESI 1-5) and routes patients to the appropriate resuscitation bay (Practical 7). Attending doctor qualifications are matched using **First-Order Logic Unification** (Practical 8).
        5. **Surgical Protocol Coordination**: Emergency trauma surgeries are scheduled non-linearly using **Partial Order Planning (POP)** with causal links, enabling simultaneous parallel team execution (Practical 10).
        """)

    with guide_tab2:
        st.markdown("""
        ### Exact Mapping to Lab Syllabus (23ADS1502):
        | Practical # | Syllabus Experiment Title | AI Concept | Implementation in VitalFlow AI |
        |---|---|---|---|
        | **P1** | Smart Light Agent | Simple Reflex Agent | Baseline patient monitor evaluating current vital thresholds without memory |
        | **P2** | Hospital Patient Monitoring Agent | Model-Based Reflex Agent | Telemetry agent tracking multi-interval trend vectors & Shock Index |
        | **P3** | Shortest Path Using Greedy Best-First | Heuristic Search ($f=h$) | Heuristic routing showing how greedy choices lead to suboptimal detours |
        | **P4** | Optimal Path Using A* Search | $f(n) = g(n) + h(n)$ | Ambulance route optimization guaranteeing minimal travel time |
        | **P5** | Map Coloring using Min-Conflicts | CSP & Local Search | Emergency medical staff & ICU ward duty roster conflict minimization |
        | **P7** | Smart Garden System | Propositional Logic | Clinical Triage Knowledge Base with Horn-Clause Forward Chaining |
        | **P8** | Assistant Bot using Unification | FOL Unification | Attending doctor capability matching with clinical patient needs |
        | **P9** | Nagpur Metro Route Planner | State-Space Search | Nagpur urban healthcare transit network topological graph |
        | **P10**| Kitchen Task Planner for Anaya | Partial Order Planning | Emergency Trauma Laparotomy multi-team parallel protocol |
        """)

    with guide_tab3:
        st.markdown("### Top Viva Questions with Simple, Student-Friendly Answers")
        
        viva_qa = [
            ("Q1: What is the main objective of VitalFlow AI?",
             "VitalFlow AI is an autonomous hospital operations command system. It combines classical and heuristic AI algorithms to optimize emergency ambulance routing, ICU patient vitals monitoring, doctor shift scheduling, emergency triage, and surgical workflows."),
            
            ("Q2: Why did you choose A* Search over Dijkstra and Greedy Best-First Search for ambulance dispatch?",
             "A* combines the actual cost traveled so far g(n) with an admissible heuristic estimate to the goal h(n). Dijkstra is optimal but uninformed (h=0), expanding nodes blindly in all directions. Greedy Best-First considers only h(n), making it fast but prone to suboptimal detours. A* guarantees the mathematically optimal shortest route with minimal node expansions."),
            
            ("Q3: What makes a heuristic admissible in A* Search?",
             "A heuristic h(n) is admissible if it never overestimates the true cost to reach the goal (i.e., h(n) <= h*(n)). In our ambulance routing, we used straight-line Euclidean distance divided by the maximum possible theoretical road speed, ensuring our time estimate is always less than or equal to actual road travel time."),
            
            ("Q4: How does a Model-Based Reflex Agent differ from a Simple Reflex Agent in patient monitoring?",
             "A Simple Reflex Agent acts only on current percepts with no memory (S = ∅). It causes false alarms during temporary stress spikes and misses gradual deterioration. A Model-Based Reflex Agent maintains an internal state representation across time, tracking physiological trends, Shock Index, and rate-of-change to detect true medical crises like sepsis."),
            
            ("Q5: What is Shock Index and why does the agent compute it?",
             "Shock Index is defined as Heart Rate divided by Systolic Blood Pressure (Normal: 0.5 to 0.7). An elevated Shock Index (> 0.9) reveals occult hemorrhagic or septic shock even before standard blood pressure thresholds drop catastrophically."),
            
            ("Q6: How is hospital duty scheduling formulated as a Constraint Satisfaction Problem (CSP)?",
             "A CSP is defined by a triplet (X, D, C). In our system: Variables X are the shift slots (e.g. ICU Morning, ER Night). Domains D are the eligible doctors. Constraints C include no double-booking at the same time, specialty eligibility, and maximum shift quotas per cycle."),
            
            ("Q7: How does the Min-Conflicts algorithm work?",
             "Min-Conflicts is a heuristic local search algorithm. It starts with an initial (possibly conflicted) assignment. In each iteration, it selects a conflicted variable and reassigns it the value from its domain that results in the minimum number of total constraint violations. If trapped in local minima, it performs a random restart."),
            
            ("Q8: What is Forward Chaining in Propositional Logic?",
             "Forward Chaining is a data-driven reasoning strategy. It starts with known asserted facts in the knowledge base and fires Definite Horn Clauses whose antecedents are satisfied, deriving new facts until a goal conclusion (such as ESI Acuity Level 1 or 2) is proven."),
            
            ("Q9: What is the Unification algorithm in First-Order Logic?",
             "Unification is an algorithmic process that finds a substitution mapping (Most General Unifier or MGU θ) for variables in two predicate logic expressions such that Subst(θ, p1) == Subst(θ, p2). We use it to match patient clinical demands with available physician attributes."),
            
            ("Q10: What is Partial Order Planning (POP) and why is it better than Linear Planning for trauma resuscitation?",
             "Linear planning forces all actions into a single strict sequence. Partial Order Planning produces a plan with ordering constraints and causal links, specifying order only when necessary. This allows multiple hospital teams (such as nurses starting IV lines and scrub technicians sterilizing instruments) to execute tasks concurrently in parallel stages.")
        ]

        for q, a in viva_qa:
            with st.expander(f"**{q}**"):
                st.write(a)
