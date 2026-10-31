# VITALFLOW AI: 5-Minute Project Demonstration Script
## Step-by-Step Viva & Lab Evaluation Walkthrough

Follow this exact walkthrough when presenting VitalFlow AI to your professor or external examiner. It is structured to take 5 to 7 minutes, showcase all core AI algorithms, and demonstrate total command over your syllabus concepts.

---

### Phase 1: The Hook & Introduction (60 Seconds)
1. **Open the Streamlit Application** in your browser (`http://localhost:8501`).
2. **Point to the Hero Banner at the top:**
   > *"Good morning, respected professors. Today, I am presenting **VitalFlow AI**, an Autonomous Hospital Operations and Emergency Logistics Command System developed for our 5th-Semester B.Tech AI & Data Science Minor Project."*
3. **Connect directly to the Syllabus:**
   > *"Rather than building common college projects like Tic-Tac-Toe or a basic chatbot, VitalFlow AI implements five foundational AI paradigms directly from our AI Lab practical syllabus—including A\* Search (P4), Greedy Best-First Search (P3), Model-Based Reflex Agents (P2), Constraint Satisfaction with Min-Conflicts (P5), Propositional Forward Chaining (P7), and Partial Order Planning (P10)—unified to solve the real-world healthcare crisis of emergency response and hospital resource bottlenecks."*

---

### Phase 2: Emergency Ambulance Route Planner (90 Seconds)
1. **Navigate to:** `🚑 Emergency Ambulance Route Planner` in the sidebar.
2. **Show the Map & Controls:**
   > *"Here in Module 1, an emergency ambulance must reach AIIMS Nagpur from Sitabuldi during peak rush hour. The network represents real Nagpur healthcare nodes."*
3. **Explain the Search Algorithms:**
   * Point to the metric cards showing **A\* Search** (25.23 min), **Greedy Best-First** (27.88 min), and **Dijkstra** (25.23 min).
   > *"Notice the difference between A\* and Greedy Best-First. A\* uses $f(n) = g(n) + h(n)$ with an admissible Euclidean heuristic divided by max road speed. It guarantees the mathematically optimal path of 25.23 minutes.*
   > *Greedy Best-First, however, uses only $f(n) = h(n)$ and ignores path cost $g(n)$. It was lured into a local shortcut through congested central roads, resulting in a suboptimal detour of 27.88 minutes."*
4. **Live Interactive Feature:**
   * Toggle **"Simulate Wardha Road Construction Closure"** in the sidebar.
   * Click **🚀 Calculate Emergency Routes**.
   * Show how the map dynamically turns the road red and A\* reroutes through alternative arterial corridors without failing!
5. **Open the Expander:**
   * Expand **"Step-by-Step Search Decision Log"** to show the exact priority queue evaluation order and $g(n)$, $h(n)$, $f(n)$ values.

---

### Phase 3: ICU Patient Telemetry Monitor (60 Seconds)
1. **Navigate to:** `🩺 ICU Patient Telemetry Agent` in the sidebar.
2. **Select Patient Case:** Choose **P-101 (Rajesh Sharma - Post-Cholecystectomy / Sepsis)**.
3. **Move the Inspection Slider to Time Step 3 (08:30):**
   > *"In Module 2, we compare the Simple Reflex Agent from Practical 1 with the Model-Based Reflex Agent from Practical 2."*
4. **Point to the Side-by-Side Comparison:**
   > *"Notice what happens at 08:30: The patient is developing early septic shock. The Simple Reflex Agent looks only at the immediate reading with no memory ($S_t = \emptyset$) and merely issues a mild caution.*
   > *However, our Model-Based Reflex Agent maintains an internal state representation across rolling time intervals ($S_{t+1} = \text{UpdateState}(S_t, P_{t+1})$). It calculates that the Shock Index (Heart Rate divided by Systolic BP) has climbed above 1.0, detects a multi-interval downward deterioration vector, and immediately triggers a Tier-3 Code Blue alert 30 minutes earlier than the threshold-based monitor."*
5. **Show False Alarm Handling:**
   * Select **P-103 (Anil Deshmukh)**.
   * Show how a temporary anxiety spike at 08:15 tricked the Simple Reflex Agent into alarming, while the Model-Based Agent recognized it as a transient spike and suppressed alarm fatigue.

---

### Phase 4: Medical Staff & Bed CSP Allocator (60 Seconds)
1. **Navigate to:** `🧩 Medical Staff & Bed CSP Allocator` in the sidebar.
2. **Explain the Formulation:**
   > *"Module 3 formulates hospital shift scheduling as a formal Constraint Satisfaction Problem $(X, D, C)$, directly mapping to Practical 5.*
   > *Variables $X$ are the 10 emergency shift slots; Domains $D$ are available specialists; Constraints $C$ prevent concurrent double-booking, enforce specialty requirements, and restrict consecutive night shift fatigue."*
3. **Click "⚡ Solve Schedule with Min-Conflicts":**
   * Point to the interactive **Plotly convergence curve**.
   > *"The Min-Conflicts local search algorithm begins with a random assignment of high conflicts and heuristically repairs the most conflicted variable in each iteration, driving total constraint violations down to zero within milliseconds."*
   * Show the resulting clean duty roster table below with zero double-bookings!

---

### Phase 5: Clinical Triage & Proof Engine (45 Seconds)
1. **Navigate to:** `⚖️ Clinical Triage & Proof Engine` in the sidebar.
2. **Select Scenario Preset:** Choose **"Acute ST-Elevation Myocardial Infarction (STEMI)"**.
3. **Show the Deduction Trace:**
   > *"In Module 4, we implement Propositional Horn-Clause Forward Chaining (Practical 7). When chest pain, diaphoresis, and unstable vitals are asserted, Modus Ponens fires Rule R5 to deduce acute coronary syndrome, which triggers Rule R6 to deduce ESI Level 2 Emergent and routes the patient directly to the Critical Care Bay.*
   > *In the second tab, we implement the First-Order Logic Unification algorithm (Practical 8) to find the Most General Unifier (MGU $\theta$) matching patient care needs with attending doctor attributes."*

---

### Phase 6: Trauma Protocol Partial Order Planner (45 Seconds)
1. **Navigate to:** `⏱️ Trauma Protocol Partial Order Planner` in the sidebar.
2. **Explain the Difference from Linear Planning:**
   > *"In Practical 10, we studied Partial Order Planning. In emergency trauma surgery, forcing all actions into a single linear sequence causes fatal delays.*
   > *Our POP planner identifies causal links and open preconditions. Notice the Gantt chart: Stage 2 executes IV line placement and surgical instrument sterilization simultaneously in parallel streams by different clinical teams, compressing the overall resuscitation timeline to just 58 minutes."*

---

### Phase 7: Benchmarks & Viva Guide (30 Seconds)
1. **Navigate to:** `📊 Algorithmic Benchmarks & Complexity`.
   * Point out the asymptotic time and space complexity comparison table ($O(b^d)$, admissibility, completeness).
2. **Navigate to:** `🎓 Viva Preparation & Project Guide`.
   * Show the embedded **Architecture Diagram** and the **Top 25 Viva Questions & Answers** accordion ready inside the app.
3. **Concluding Statement:**
   > *"Every single algorithm in VitalFlow AI was implemented cleanly in Python from first principles, verified with automated unit tests, and packaged into a deployable Streamlit application. Thank you, professors. I am now open to your questions."*
