# VITALFLOW AI 🩺
### Autonomous Hospital Operations & Emergency Logistics Command System
*A Multi-Agent Decision Support & State-Space Optimization Engine for Urban Healthcare Operations*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Syllabus Alignment](https://img.shields.io/badge/Syllabus-23ADS1502%20(V%20Sem)-indigo.svg)](#syllabus-alignment)

---

## 🌟 Executive Summary
**VitalFlow AI** is an intelligent, multi-agent hospital operations command platform engineered for the **5th-Semester B.Tech Artificial Intelligence & Data Science (AIDS)** curriculum at **Yeshwantrao Chavan College of Engineering (YCCE), Nagpur**.

Rather than implementing trivial toys (like Tic-Tac-Toe or simple rule chatbots), VitalFlow AI unifies foundational AI algorithms—including **Informed State-Space Search (A\*, Greedy Best-First, Dijkstra)**, **Model-Based Reflex Agents**, **Constraint Satisfaction Problems (CSP with Min-Conflicts)**, **Propositional Horn-Clause Forward Chaining**, **First-Order Logic (FOL) Unification**, and **Partial Order Planning (POP)**—into a mission-critical operations command system designed to save lives during the emergency **Golden Hour**.

---

## 🚀 Key Modules & AI Implementations

| # | System Module | AI Concept & Algorithm | Practical Syllabus Reference | Real-World Medical Application |
|---|---|---|---|---|
| **1** | **Ambulance Route Optimizer** | **A\* Search** ($f(n)=g(n)+h(n)$) vs **Greedy Best-First** vs **Dijkstra** | Practical 3, 4 & 9 | Minimizes emergency ambulance transit times across Nagpur with traffic congestion and road closures. |
| **2** | **ICU Telemetry Monitor** | **Model-Based Reflex Agent** ($S_{t+1} = \text{Update}(S_t, P_{t+1})$) | Practical 1 & 2 | Continuous vital trend monitoring; computes Shock Index; detects Sepsis & Cushing's Triad; suppresses false alarms. |
| **3** | **Medical Staff & Bed CSP** | **Min-Conflicts Local Search Algorithm** with Random Restarts | Practical 5 | Resolves emergency shift scheduling without double-booking, overwork burnout, or specialty mismatches. |
| **4** | **Clinical Triage Engine** | **Propositional Horn-Clause Forward Chaining** & **FOL Unification** | Practical 7 & 8 | Infers emergency acuity (ESI Level 1-5), assigns resuscitation bays, and matches attending physicians with unifiers. |
| **5** | **Trauma Surgery Planner** | **Partial Order Planning (POP)** with Causal Links | Practical 10 | Synthesizes parallel multi-team schedules for trauma surgery, compressing critical-path preoperative delays. |
| **6** | **Algorithmic Benchmarking** | Time & Space Complexity ($O(b^d)$), Admissibility & Optimality | Core Theory | Interactive side-by-side performance comparison across heuristic metrics and varying scale. |
| **7** | **Viva Companion** | Architecture Flow & Top 30 Academic Viva Defense Q&A | Course Evaluation | In-app, interactive oral examination prep guide. |

---

## 📐 System Architecture

```
                                [ EMERGENCY 108 DISPATCH ]
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    MODULE 1: AMBULANCE ROUTE OPTIMIZER       │
                      │    - Graph: Nagpur Healthcare Spatial Grid   │
                      │    - Alg: A* Search vs Greedy Best-First     │
                      │    - Heuristic: Admissible Euclidean Time    │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    MODULE 4: CLINICAL TRIAGE ENGINE          │
                      │    - Knowledge Base: Horn Clause Implication │
                      │    - Inference: Data-Driven Forward Chaining │
                      │    - Matching: FOL Most General Unifier (MGU)│
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    MODULE 3: CSP MEDICAL STAFF SCHEDULER     │
                      │    - Variables: Ward Shifts {S1 ... S10}     │
                      │    - Constraints: No Double-Booking, Quotas  │
                      │    - Solver: Heuristic Min-Conflicts Search  │
                      └──────────────────────┬───────────────────────┘
                                             │
                      ┌──────────────────────┴──────────────────────┐
                      ▼                                             ▼
        ┌────────────────────────────┐               ┌────────────────────────────┐
        │  MODULE 2: ICU TELEMETRY   │               │ MODULE 5: TRAUMA SURGERY   │
        │  - Model-Based Reflex Agent│               │ - Partial Order Planning   │
        │  - Rolling Internal State  │               │ - Causal Links & Threat Fix│
        │  - Sepsis & Shock Detection│               │ - Parallel Resuscitation   │
        └────────────────────────────┘               └────────────────────────────┘
```

---

## 🛠️ Technology Stack
* **Programming Language:** Python 3.10 / 3.11
* **Web Application UI:** Streamlit (Custom SaaS CSS Theme, Responsive Columns, Status Banners)
* **Interactive Visualizations:** Plotly Graph Objects & Plotly Express
* **Data Processing & Matrices:** Pandas, NumPy
* **Scientific & Network Graphs:** NetworkX, SciPy, Scikit-learn
* **Testing:** Custom Test Suite (`test_core.py`)
* **Deployment Target:** Streamlit Community Cloud

---

## 💻 Local Installation & Setup

### Prerequisites
* Python 3.10, 3.11, or 3.12 installed on your machine.
* Git installed (for version control).

### Step 1: Clone or Open the Repository
```bash
git clone https://github.com/your-username/VitalFlow-AI.git
cd VitalFlow-AI
```

### Step 2: Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Unit Test Suite
Verify that all algorithms and heuristic modules execute flawlessly:
```bash
python test_core.py
```
*Expected Output:*
```
=== Testing Search Planner (Practical 3, 4, 9) ===
A* Path: Sitabuldi -> Ramdaspeth -> Chhatrapati_Sq -> Wardha_Road -> Airport_Metro -> New_Khapri -> MIHAN -> AIIMS_Nagpur | Time: 25.23m | Expanded: 13
Greedy Path: Sitabuldi -> Dhantoli -> GMC_Nagpur -> Wardha_Road -> Airport_Metro -> New_Khapri -> MIHAN -> AIIMS_Nagpur | Time: 27.88m | Expanded: 8
...
>>> ALL CORE AI ALGORITHMS FUNCTIONING PERFECTLY! <<<
```

### Step 5: Launch the Streamlit Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## ☁️ Streamlit Community Cloud Deployment Guide

VitalFlow AI is 100% prepared for **Streamlit Community Cloud** deployment with zero configuration files needed:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit of VitalFlow AI Minor Project"
   git branch -M main
   git remote add origin https://github.com/<your-github-username>/vitalflow-ai.git
   git push -u origin main
   ```
2. **Deploy on Streamlit Cloud:**
   * Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
   * Click **New app**.
   * Select your repository (`<your-github-username>/vitalflow-ai`).
   * Set Branch to `main`.
   * Set Main file path to `app.py`.
   * Click **Deploy!**
3. Your application will be live worldwide with a public URL (e.g., `https://vitalflow-ai.streamlit.app`)!

---

## 📂 Repository File Structure
```
AI_MSPA/
├── app.py                      # Main Streamlit SaaS application dashboard
├── requirements.txt            # Python package dependencies
├── README.md                   # Comprehensive project documentation
├── VIVA_PREPARATION_GUIDE.md   # Complete 30+ Viva Q&A & theory guide
├── DEMO_SCRIPT.md              # 5-minute step-by-step presentation script
├── test_core.py                # Automated unit testing suite
│
├── core/                       # Pure algorithmic implementations from first principles
│   ├── __init__.py
│   ├── search_planner.py      # A*, Greedy Best-First, and Dijkstra graph search
│   ├── reflex_agents.py        # Model-Based vs Simple Reflex patient telemetry agents
│   ├── csp_scheduler.py        # CSP formulation & Min-Conflicts local search solver
│   ├── logic_triage.py         # Horn-clause forward chaining & FOL unification
│   └── partial_order_plan.py   # Partial order planning with causal links
│
├── data/                       # Spatial networks & clinical dataset scenarios
│   ├── __init__.py
│   ├── hospital_network.py     # Nagpur urban healthcare nodes & road graph
│   ├── patient_cases.py        # Streaming patient vitals (Sepsis, Hypoxia, ICP, Anxiety)
│   └── staff_resources.py      # Doctors, specialties, shifts, and ward constraints
│
└── ui/                         # Modern SaaS design system & Plotly charts
    ├── __init__.py
    ├── styles.py               # Custom CSS (Inter font, cards, status pills, dark/light)
    ├── components.py           # Metric cards, alert strips, syllabus badges
    └── visualizers.py          # Plotly network maps, telemetry charts, Gantt timelines
```

---

## 🏆 Key Academic Differentiators
* **Pure First-Principles Implementation:** Every algorithm (A*, Min-Conflicts, Horn-Clause Forward Chaining, Model-Based Agent, Partial Order Planning) is written cleanly in standard Python without relying on opaque black-box libraries.
* **Direct Syllabus Mapping:** Directly fulfills Course Outcomes CO1, CO2, CO3, and CO4 for Course 23ADS1502.
* **Visible AI Decision Making:** The application features interactive priority-queue logs, conflict reduction curves, and causal-link dependency tables so examiners can see the algorithms reasoning step-by-step.
* **Modern SaaS UI/UX:** Elevated cards, responsive metrics, custom gradients, interactive Plotly charts, and dark-mode polished aesthetics make the project stand out as a genuine product.

---

## 📄 License
This project is released under the **MIT License**. Free for academic and research purposes.
