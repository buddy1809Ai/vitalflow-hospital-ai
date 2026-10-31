# VITALFLOW AI: 5-Minute Presentation & Demo Script
## Clean Walkthrough for College Viva & Lab Evaluation

Follow this walkthrough when demonstrating VitalFlow AI to your professor or external examiner. It is structured to take 5 minutes, highlight all core AI algorithms, and demonstrate total command over your syllabus concepts.

---

### Step 1: Executive Overview (60 Seconds)
1. **Open the Application** in your browser (`http://localhost:8501`).
2. **Point to the Header and KPI Cards:**
   > *"Good morning, respected professors. Today, I am demonstrating **VitalFlow AI**, an Autonomous Hospital Operations and Emergency Logistics Platform."*
   > *"Rather than building common toy projects like Tic-Tac-Toe or a basic chatbot, VitalFlow AI implements five foundational AI paradigms directly from our AI Lab syllabus to solve urban emergency healthcare challenges during the critical **Golden Hour**."*
3. **Show the Map Overview:**
   > *"Our dashboard models 14 interconnected healthcare facilities and transit nodes across Nagpur with 371 total ICU beds and dynamic traffic multipliers."*

---

### Step 2: Emergency Route Planner (90 Seconds)
1. **Click on:** `Emergency Route Planner` in the sidebar.
2. **Explain the Search Algorithms:**
   * Origin: `Sitabuldi` $\to$ Destination: `AIIMS_Nagpur`.
   * Point to the metric cards showing **A\* Search** (25.23 min), **Greedy Best-First** (27.88 min), and **Dijkstra** (25.23 min).
   > *"Here in Module 1, an ambulance must reach AIIMS Nagpur. We compare A\* with Greedy Best-First Search.*
   > *A\* uses $f(n) = g(n) + h(n)$ with an admissible Euclidean time heuristic ($h(n) \le h^*(n)$). It guarantees the optimal path of 25.23 minutes.*
   > *Greedy Best-First uses only $f(n) = h(n)$ and ignores path cost $g(n)$. It was lured into a local shortcut through congested central roads, resulting in a suboptimal detour of 27.88 minutes."*
3. **Demonstrate Dynamic Obstacle Avoidance:**
   * Check **"Simulate Wardha Road Closure"** in the sidebar.
   * Click **Calculate Optimal Routes**.
   * Show how the map highlights the road closure in red, and A\* automatically reroutes via the Outer Ring Road in 25.97 minutes!

---

### Step 3: Hospital Operations (2 Minutes)
Click on `Hospital Operations` in the sidebar. It contains 3 clear operational modules:

#### Tab 1: ICU Patient Monitoring (Practical 2 & 1)
* Select **P-101 (Rajesh Sharma - Sepsis Progression)**.
* Move the slider to **Step 3 (08:30)**.
> *"Here we compare the Simple Reflex Agent from Practical 1 with the Model-Based Reflex Agent from Practical 2.*
> *At 08:30, the patient's vitals are drifting. The Simple Reflex Agent acts only on current percepts without memory ($S = \emptyset$) and merely issues a mild caution.*
> *Our Model-Based Reflex Agent maintains an internal state representation across rolling time windows ($S_{t+1} = \text{UpdateState}(S_t, P_{t+1})$). It calculates that the Shock Index (Heart Rate / Systolic BP) has climbed above 1.0, detects a downward deterioration vector, and triggers a Code Blue alert 30 minutes earlier than standard threshold monitors."*
* Quickly switch to **P-103 (Anil Deshmukh)** to show how the Model-Based Agent recognizes a temporary anxiety spike and suppresses false alarms!

#### Tab 2: Staff Duty Scheduling (Practical 5)
* Explain: Variables = Shift Slots, Domains = Doctors, Constraints = No Double Booking, Specialty Eligibility.
* Click **"Solve Roster with Min-Conflicts"**.
* Point out the convergence curve driving violations down to zero within milliseconds, outputting a conflict-free roster table!

#### Tab 3: Emergency Triage & Surgical Protocol (Practical 7 & 10)
* Select preset: **Acute STEMI Heart Attack**.
* Show the forward-chaining proof trace: Modus Ponens firing Horn clauses to deduce **ESI Level 2 Emergent** and routing to the Critical Care Bay.
* Point to the **Partial Order Planning Gantt Timeline**:
> *"In trauma surgery, linear planning ($A_1 \to A_2 \to A_3$) causes fatal delays. POP identifies causal links and open preconditions: Resuscitation nurses place IV lines while scrub technicians simultaneously sterilize instruments in parallel stages, compressing the critical path to 58 minutes."*

---

### Step 4: Closing Statement (30 Seconds)
> *"Every algorithm in VitalFlow AI was implemented cleanly in standard Python from first principles, tested with 100% automated test coverage, and structured as a clean SaaS interface. Thank you, professors. I am ready for your questions."*
