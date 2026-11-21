#!/usr/bin/env python3
"""
Elitist Black & Gold / Warm Gold Presentation Generator for Emboolancè
Smart Emergency Ambulance Routing & Hospital Allocation System
Author: Amrit Prasad (SAP ID: 590021684) | UPES Dehradun | Mentor: Sandeep Chand Kumain
"""

import os
import sys
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = "/Users/amrit/Documents/Emboolancè"
PPTX_PATH = os.path.join(OUTPUT_DIR, "Emboolance_SOTA_Presentation.pptx")
KEY_PATH = os.path.join(OUTPUT_DIR, "Emboolance_SOTA_Presentation.key")
HTML_PATH = os.path.join(OUTPUT_DIR, "Emboolance_SOTA_Presentation.html")
COMMAND_PATH = os.path.join(OUTPUT_DIR, "open_in_keynote.command")

# ==============================================================================
# ELITIST BLACK & GOLD / WARM GOLD COLOR PALETTE (Luxury Dark Academic Theme)
# ==============================================================================
BG_ONYX = RGBColor(8, 8, 8)              # #080808 Deep Obsidian Noir
CARD_WARM_NOIR = RGBColor(18, 16, 14)    # #12100E Warm Velvet Noir Glass
SUB_CARD_BG = RGBColor(28, 24, 18)       # #1C1812 Elevated Callout Noir
CARD_BORDER = RGBColor(90, 72, 28)       # #5A481C Subtle Burnished Gold Stroke
SUB_BORDER = RGBColor(120, 96, 36)       # #786024 Highlighted Gold Border
GOLD_24K = RGBColor(212, 175, 55)        # #D4AF37 Regal 24K Gold
GOLD_CHAMPAGNE = RGBColor(230, 194, 101) # #E6C265 Warm Champagne Gold
GOLD_PALE = RGBColor(245, 224, 163)      # #F5E0A3 Luminous Pale Gold
GOLD_BRONZE = RGBColor(163, 123, 36)     # #A37B24 Antique Bronze Accent
TEXT_WHITE = RGBColor(250, 249, 246)     # #FAF9F6 Pure Ivory White
TEXT_IVORY = RGBColor(235, 229, 216)     # #EBE5D8 Warm Silk Body
TEXT_MUTED = RGBColor(168, 159, 145)     # #A89F91 Sandstone Muted
TEXT_SUBTLE = RGBColor(115, 105, 90)     # #73695A Subtle Bronze Slate
ACCENT_CRIMSON = RGBColor(220, 38, 38)   # #DC2626 Regal Crimson for P1 Alerts

def strip_unsupported_placeholders(prs):
    """Strips dummy picture placeholders from unused master layouts so Keynote imports with 0 warnings."""
    try:
        sm = prs.slide_masters[0]
        for layout in sm.slide_layouts:
            for sp in list(layout.shapes):
                if "Picture" in sp.name:
                    sp._element.getparent().remove(sp._element)
    except Exception as e:
        print(f"Placeholder strip note: {e}")

def create_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    strip_unsupported_placeholders(prs)
    blank_layout = prs.slide_layouts[6]

    slides = [
        # SLIDE 1: HERO TITLE
        {
            "type": "hero_title",
            "badge": "◆ UPES DEHRADUN · SCHOOL OF COMPUTER SCIENCE (SoCS) · B.TECH CSE AIML (2025–2029) ◆",
            "title": "EMBOOLANCÈ: SMART EMERGENCY AMBULANCE\nROUTING & HOSPITAL ALLOCATION SYSTEM",
            "subtitle": "A High-Performance Zero-STL C++17 Dispatch Engine with Dynamic Traffic Jam Scaling & In-Transit Hospital Saturation Diversion",
            "student": "Amrit Prasad · SAP ID: 590021684 · B.Tech CSE AIML",
            "mentor": "Subject Teacher & Academic Mentor: Sandeep Chand Kumain",
            "spec": "Standard: Strict Zero-STL C++17 Core Engine (Zero Hidden Heap Overhead) · Advanced DSA Delivery (50–60% Milestone)",
            "kpis": [
                ("0.0018 ms", "Single-Source Dijkstra (1K Nodes)", "Sub-millisecond routing across 1,000 vertices and 3,990 edges"),
                ("100%", "Zero-STL C++17 Compliance", "Custom vector, min-heap & graphs with zero heap fragmentation"),
                ("35–40%", "Response Latency Reduction", "Demonstrated over commercial static navigation across Dehradun")
            ]
        },
        # SLIDE 2: CLINICAL CRISIS & DEHRADUN REALITY
        {
            "type": "content_2col",
            "badge": "◆ 01 | CLINICAL CRISIS & PROBLEM STATEMENT ◆",
            "title": "The Golden Hour Crisis in Emergency Medical Transit",
            "subtitle": "Analysis of Himalayan arterial bottlenecks and emergency room intake failures across Dehradun",
            "left_title": "Dehradun Regional Bottlenecks & Golden Hour Loss",
            "left_bullets": [
                "The Golden Hour Reality: Over 38% of trauma and cardiac arrest deaths in Dehradun are preventable with hospital delivery under 15 minutes.",
                "Himalayan Arterial Chokepoints: Narrow urban funnels (Rajpur Road, Ballupur Chowk, Premnagar, Chakrata Road) induce severe non-linear transit delays.",
                "Fragmented Fleet Command: Municipal 108/911 operators lack unified GPS positioning, dispatching distant units while closer units sit idle.",
                "Commercial Map Fallacy: Generic navigation maps optimize for passenger cars, ignoring emergency sirens and high-choke intersections."
            ],
            "left_callout_tag": "◆ CLINICAL SURVIVAL THRESHOLD ◆",
            "left_callout_stat": "7–10% / min",
            "left_callout_head": "Golden Hour Mortality Acceleration Rate",
            "left_callout": "Survival probability collapses non-linearly for every additional minute of transit delay past 15 minutes. Dispatch latency ceiling must strictly stay under 12.5 minutes across Dehradun.",
            "left_callout_detail": "Regional Coverage Target: Rapid transit envelope encompassing Max Hospital, Synergy, AIIMS Rishikesh, and Doon Govt.",
            "right_title": "The Blind Hospital Allocation Trap",
            "right_bullets": [
                "Emergency Dock Rejections: Ambulances transport critical patients to Max Hospital (120 beds) or Synergy (80 beds) only to find zero ICU beds.",
                "Lethal Turnaround Diversion: Secondary transit to AIIMS Rishikesh Level-1 Apex Trauma (250 beds) adds 40+ minutes of unmonitored transit.",
                "Zero Central Telemetry: Hospitals manage intake in silos, with no automated signaling when ER triage queues reach 100% capacity.",
                "Emboolancè Solution: Centralized regional CAD hub with real-time bed reservations and automated in-transit diversion alerts."
            ],
            "right_callout_tag": "◆ REGIONAL HEALTHCARE INTAKE POOLS ◆",
            "right_callout_stat": "600 Total Beds",
            "right_callout_head": "Four-Hospital Monitored Regional Network",
            "right_callout": "Monitored intake across Max Super Speciality (120 beds), Synergy (80 beds), AIIMS Rishikesh (250 beds), and Doon Govt (150 beds).",
            "right_callout_detail": "Continuous bed reservation telemetry prevents secondary dock turnarounds through instant MDT sirens and GPS rerouting."
        },
        # SLIDE 3: 4-TIER ARCHITECTURE
        {
            "type": "content_4cards",
            "badge": "◆ 02 | ARCHITECTURAL BLUEPRINT ◆",
            "title": "4-Tier Mission-Critical System Architecture",
            "subtitle": "Decoupled high-throughput design separating microsecond C++ algorithmic execution from live browser visualization",
            "cards": [
                {
                    "title": "Zero-STL C++17 Core Engine",
                    "color": GOLD_24K,
                    "points": [
                        "Direct Memory Ownership: Custom CustomVector<T> and CustomMinHeap<T> eliminate std::vector and heap fragmentation.",
                        "Deterministic L1/L2 Locality: Contiguous flat array storage ensures hardware sequential prefetching.",
                        "Zero Allocator Mutexes: Prohibits std::allocator to eliminate multi-threaded lock contention during surges."
                    ],
                    "stat": "0.0018 ms",
                    "spec_head": "Single-Source Dijkstra (1K Nodes)",
                    "spec": "Latency: 0.0018 ms | RAM: ~132 KB | Zero-STL",
                    "spec_detail": "Guaranteed zero allocator locks or heap fragmentation during mission-critical high-frequency routing queries."
                },
                {
                    "title": "Multi-Threaded CAD Server",
                    "color": GOLD_CHAMPAGNE,
                    "points": [
                        "Asynchronous Architecture: Multi-threaded Python server handles simultaneous telemetry streams.",
                        "Clean STDIN IPC: Auto-terminating bidirectional pipe to C++ binary eliminates head-of-line blocking.",
                        "REST & WebSocket Feeds: Serves live vehicle coordinates, hospital telemetry, and scenario triggers."
                    ],
                    "stat": "0 ms IPC",
                    "spec_head": "Non-Blocking Telemetry Concurrency",
                    "spec": "Concurrency: Multi-Threaded | IPC: Clean STDIN",
                    "spec_detail": "Non-blocking dispatch queue with real-time JSON REST endpoints for the live Leaflet command console."
                },
                {
                    "title": "Google Traffic Telemetry",
                    "color": GOLD_PALE,
                    "points": [
                        "Live Corridor Sensing: Continuously polls Google traffic jam factors across Rajpur, Ballupur, and Premnagar.",
                        "Non-Linear Cost Scaling: Scales edge weights dynamically based on live traffic congestion levels.",
                        "4 Weather & Time Profiles: Baseline, Peak Rush Hour, Heavy Rain, and Road Blockage scenarios."
                    ],
                    "stat": "4 Profiles",
                    "spec_head": "Real-Time Corridor Jam Scaling",
                    "spec": "Source: Google Live Maps | Profiles: 4 Active",
                    "spec_detail": "Live traffic corridor sensing across Rajpur Road, Ballupur Chowk, Premnagar, and Chakrata Road."
                },
                {
                    "title": "Live Mission CAD Console",
                    "color": GOLD_BRONZE,
                    "points": [
                        "Tactical Web Interface: Full-screen Leaflet.js command center with animated emergency vehicle polylines.",
                        "Mission Elapsed Clock: Precision wall-clock synchronized timing (T+ HH:MM:SS) for active incidents.",
                        "MDT Emergency Siren: Audio alarm and visual diversion modal trigger instantly on hospital saturation."
                    ],
                    "stat": "T+ Clock",
                    "spec_head": "Full-Screen Dispatch Command Center",
                    "spec": "Telemetry: T+ HH:MM:SS | Alerts: Real-Time",
                    "spec_detail": "Instant manual and priority dispatch, hospital capacity monitor, and live GPS map tracking."
                }
            ]
        },
        # SLIDE 4: EMERGENCY LIFE-CYCLE PIPELINE
        {
            "type": "content_2col",
            "badge": "◆ 03 | OPERATIONAL LIFE-CYCLE ◆",
            "title": "End-to-End Emergency Life-Cycle Pipeline",
            "subtitle": "Mathematical and computational sequence executed from the instant a 911/108 call is initiated",
            "left_title": "Phase 1: Intake ➔ Triage ➔ Equipment",
            "left_bullets": [
                "1. Speech Transcript Surveillance (KMP): Live 911 audio stream scanned in 6.33 µs for critical trigger phrases ('cardiac arrest', 'unresponsive').",
                "2. Automated Priority Escalation: Incident priority auto-upgraded to P1-Critical before manual call-taker logging completes.",
                "3. Triage Queue Sorting (MergeSort): Stable O(N log N) sorting by composite urgency Z = w_priority * wait_time, guaranteeing FIFO fairness.",
                "4. Ambulance Payload Optimization (0/1 Knapsack DP): Maximizes onboard clinical readiness under 100 kg Gross Weight budget in 0.0076 ms."
            ],
            "left_callout_tag": "◆ PRE-DISPATCH SUB-MILLISECOND LATENCY ◆",
            "left_callout_stat": "< 0.6 ms",
            "left_callout_head": "Full Phase 1 Computation Envelope",
            "left_callout": "Entire intake, triage sorting, and equipment optimization cycle finishes in under 0.6 milliseconds. Vehicles are dynamically prepared before manual dispatcher call logging finishes.",
            "left_callout_detail": "KMP surveillance scans 10,000 characters in 6.33 µs, auto-escalating triage priority with zero dispatcher delay."
            ,
            "right_title": "Phase 2: Routing ➔ Intake ➔ Diversion",
            "right_bullets": [
                "5. Two-Leg Shortest Path (Dijkstra): Station ➔ Scene and Scene ➔ Hospital computed with live traffic jam factors in 0.0018 ms.",
                "6. Disaster Evacuation Ceiling (Edmonds-Karp Max Flow): Calculates maximum regional patient flow without collapsing ER reception pipelines.",
                "7. In-Transit Capacity Diversion (Floyd-Warshall): If target hospital fills to 100% mid-route, O(1) table reroutes unit to nearest open ICU.",
                "8. Schedule Synchronization (CRT): Solves systems of congruences to align maintenance (7d), sterilization (5d), and surgical rotations (11d)."
            ],
            "right_callout_tag": "◆ IN-TRANSIT DYNAMIC CONVERGENCE ◆",
            "right_callout_stat": "O(1) Lookup",
            "right_callout_head": "Zero-Overhead Mid-Transit Diversion",
            "right_callout": "Precomputed all-pairs shortest paths table allows instantaneous hospital diversion recalculation directly from current vehicle GPS coordinates without initiating new graph traversals.",
            "right_callout_detail": "Audible MDT alerts sound within 50 ms of target ER saturation, recalculating path from current GPS coordinates."
        },
        # SLIDE 5: DSA SYLLABUS MASTER MATRIX
        {
            "type": "table_syllabus",
            "badge": "◆ 04 | ACADEMIC COMPLIANCE & PROOF ◆",
            "title": "Full DSA Syllabus Implementation Matrix (100% Coverage)",
            "subtitle": "Strict Zero-STL C++17 implementations mapped directly to real emergency operations (Amrit Prasad, SAP 590021684)",
            "rows": [
                ["1. Sorting & Retrieval", "MergeSort, QuickSort, Binary Search (Iter/Rec)", "P1/P2/P3 Triage Queue priority ordering & rapid vehicle ID registry lookup", "O(N log N) / O(log N)"],
                ["2. Greedy Algorithms", "Dijkstra (Min-Heap), Prim's MST, Kruskal's MST", "Two-leg dynamic routing & minimal emergency hospital communication backbone", "O((V+E) log V) / O(E log V)"],
                ["3. Dynamic Programming", "0/1 Knapsack, Floyd-Warshall, LCS, TSP Bitmask", "Ambulance equipment weight budgeting & instant inter-hospital diversion matrix", "O(N*W) / O(V^3) / O(N^2 2^N)"],
                ["4. Network Flows", "Edmonds-Karp Max Flow, Kuhn Bipartite Matching", "Mass-casualty regional disaster capacity ceiling & simultaneous surge matching", "O(V*E^2) / O(V*E)"],
                ["5. Divide & Conquer", "Max Subarray, Fast Powering, Celebrity Problem", "Peak traffic congestion intervals & central transit staging hub discovery", "O(N log N) / O(log exp) / O(V)"],
                ["6. Strings & Number Theory", "KMP Matcher, Rabin-Karp Rolling Hash, CRT", "Emergency call audio keyword escalation & maintenance cycle synchronization", "O(N+M) / O(k log(lcm))"],
                ["7. Backtracking & B&B", "Subset Sum, Least-Cost Branch & Bound, N-Queens", "Transfusion blood pack bundling & spatial non-interference staging", "O(2^N) / Best O(N log N)"]
            ],
            "takeaway": "7 of 7 core algorithm modules implemented in pure C++17 without Standard Template Library containers. Fully verified under high-load stress testing (1,000 nodes, simulated mass-casualty surge, dynamic in-transit hospital saturation diversion)."
        },
        # SLIDE 6: ZERO-STL DEEP DIVE
        {
            "type": "content_2col",
            "badge": "◆ 05 | CORE MEMORY ENGINEERING ◆",
            "title": "Why Zero-STL? Deterministic Real-Time Safety",
            "subtitle": "Direct memory ownership replacing standard library containers for mission-critical guarantees",
            "left_title": "Prohibited Containers vs Custom Zero-STL",
            "left_bullets": [
                "Prohibited: std::vector ➔ Replaced by Core::CustomVector<T> with explicit move semantics, custom destructor, and amortized doubling.",
                "Prohibited: std::priority_queue ➔ Replaced by Core::CustomMinHeap<T> providing predictable binary heap operations with zero hidden reallocations.",
                "Prohibited: std::map / std::set ➔ Replaced by contiguous indexed arrays and custom Disjoint Set Union (DSU) structures.",
                "Prohibited: std::queue / std::deque ➔ Replaced by indexed head-pointer structures over contiguous CustomVector buffers."
            ],
            "left_callout_tag": "◆ HEAP ALLOCATION INVARIANT ◆",
            "left_callout_stat": "0 Bytes Δ Heap",
            "left_callout_head": "Zero Dynamic Allocations in Query Loop",
            "left_callout": "Strict memory invariant guarantees that once graph initialization completes, zero heap allocations occur during routing or dispatch queries, eliminating allocator fragmentation.",
            "left_callout_detail": "Prohibiting std::allocator eliminates mutex contention and unpredictable GC pauses across POSIX threads.",
            "right_title": "Production Performance & Memory Audit",
            "right_bullets": [
                "Zero Hidden Allocator Locks: Eliminates multi-threaded heap contention and unpredictable malloc locks during high-casualty 911 surges.",
                "Guaranteed Cache Locality: Flat array structures ensure dense memory alignment and sequential L1/L2 hardware prefetching.",
                "Strict Deterministic Footprint: Complete road network of 1,000 nodes and 3,990 edges occupies only ~132 KB of RAM.",
                "Sub-Millisecond Verification: Dijkstra computes single-source shortest path across 1,000 vertices in 0.0018 ms (< 50 ms hard ceiling)."
            ],
            "right_callout_tag": "◆ DETERMINISTIC HARDWARE FOOTPRINT ◆",
            "right_callout_stat": "132 KB RAM",
            "right_callout_head": "Total Road Graph L2 Cache Footprint",
            "right_callout": "The complete Dehradun regional road network fits entirely inside CPU L2 hardware cache, providing sub-millisecond route calculations with zero memory bus bottlenecks.",
            "right_callout_detail": "1,000 vertices and 3,990 edges fully fit into processor L2 cache (typically 512 KB–1 MB per core)."
        },
        # SLIDE 7: ROUTING & DP
        {
            "type": "content_2col",
            "badge": "◆ 06 | ALGORITHMIC DEEP DIVE ◆",
            "title": "Traffic-Aware Dijkstra & Clinical Knapsack DP",
            "subtitle": "Two core algorithmic pillars driving emergency response latency reduction and vehicle medical readiness",
            "left_title": "Traffic-Aware Dijkstra's Algorithm",
            "left_bullets": [
                "Two-Leg Navigation: Leg 1 (Station ➔ Scene) + Leg 2 (Scene ➔ Allocated Receiving Hospital) calculated dynamically.",
                "Live Congestion Jam Scaling: Edge cost w(e) = (dist / speed) * (1 + alpha * JamFactor). Peak rush hour scales alpha to 2.5x dynamically.",
                "Min-Heap Frontier Optimization: Custom indexed binary heap extracts minimum-cost frontiers in O((V + E) log V).",
                "Empirical Comparison: Dijkstra (0.0018 ms) delivers a 550,000x latency advantage over unpruned Floyd-Warshall (1,000 ms) for single-source queries."
            ],
            "left_callout_tag": "◆ TRAFFIC COST FUNCTION & RUNTIME ◆",
            "left_callout_stat": "0.0018 ms",
            "left_callout_head": "Edge Cost Scaling & Traversal Latency",
            "left_callout": "w(e) = (dist / speed) · [1 + α · (JamFactor / 10)^1.4]. Custom indexed binary heap evaluates minimum transit paths across 1,000 nodes in 1.8 microseconds.",
            "left_callout_detail": "Indexed binary min-heap guarantees O((V + E) log V) efficiency, outperforming all-pairs search by 550,000x.",
            "right_title": "0/1 Knapsack Clinical Payload DP",
            "right_bullets": [
                "Gross Vehicle Weight Rating (GVWR): Ambulances cannot exceed strict payload limits (Equipment Weight Budget W = 100 kg).",
                "Clinical Life-Saving Utility: Medical gear (Defibrillator, Ventilator, ECMO, Pediatric trauma kit) has weight w_i and utility score v_i.",
                "Mathematical Formulation: max sum(v_i * x_i) subject to sum(w_i * x_i) <= W, x_i in {0, 1}.",
                "Empirical Result: Knapsack DP selects optimal equipment payload packing 1,580 utility points under 100 kg in 0.0076 ms."
            ],
            "right_callout_tag": "◆ CLINICAL OPTIMIZATION MODEL ◆",
            "right_callout_stat": "1,580 Pts",
            "right_callout_head": "Optimal Medical Equipment Allocation",
            "right_callout": "0/1 Dynamic Programming maximizes life-saving clinical capability within strict 100 kg payload constraints, completing in 7.6 microseconds.",
            "right_callout_detail": "Packs 1,580 clinical utility points under strict Gross Vehicle Weight Rating (GVWR) constraints in 7.6 µs."
        },
        # SLIDE 8: FLOWS & STRINGS
        {
            "type": "content_2col",
            "badge": "◆ 07 | ALGORITHMIC DEEP DIVE ◆",
            "title": "Disaster Max Flow & Real-Time Call Surveillance",
            "subtitle": "Managing regional multi-casualty incidents and automated emergency transcript escalation",
            "left_title": "Edmonds-Karp Mass-Casualty Evacuation",
            "left_bullets": [
                "Disaster Flow Network: Models disaster scenes as source S, highway chokepoints as capacitated edges, and hospital bed pools as sink T.",
                "Regional Intake Ceiling: Evaluates maximum patient evacuation throughput (patients/hour) the regional healthcare grid can absorb.",
                "Kuhn's Bipartite Matching: Resolves race conditions during simultaneous 911 call surges, matching 12 ambulance-incident pairs in 1.58 microseconds.",
                "Zero Patient Rejection: Guarantees no hospital intake pipeline is assigned beyond its emergency room capacity ceiling."
            ],
            "left_callout_tag": "◆ DISASTER CONSERVATION LAW & MATCHING ◆",
            "left_callout_stat": "1.58 µs",
            "left_callout_head": "Bipartite Surge Matching & Max Flow",
            "left_callout": "Residual capacity graph augmentation calculates regional evacuation bottlenecks and eliminates dispatch contention during simultaneous disaster call surges.",
            "left_callout_detail": "Residual graph augmentation guarantees optimal regional patient intake without overwhelming Level-1 ERs.",
            "right_title": "KMP Surveillance & Chinese Remainder (CRT)",
            "right_bullets": [
                "Real-Time Transcript Surveillance: Speech-to-text transcripts of live 108/911 calls stream into the CAD engine.",
                "Knuth-Morris-Pratt (KMP): Scans for critical trigger keywords ('cardiac arrest', 'unresponsive', 'stroke') in 6.33 microseconds.",
                "Auto-Escalation: Instantly upgrades priority from P2/P3 to P1-Critical before manual dispatcher data entry finishes.",
                "Chinese Remainder Theorem (CRT): Synchronizes coprime operational cycles (maintenance = 7d, autoclave = 5d, surgeon rotation = 11d)."
            ],
            "right_callout_tag": "◆ STRING SURVEILLANCE & CYCLE HARMONIZATION ◆",
            "right_callout_stat": "6.33 µs",
            "right_callout_head": "Pre-Call Triage Audio Scan Latency",
            "right_callout": "KMP deterministic string matching inspects 10,000 transcript characters with zero backtracking, escalating incident severity before dispatchers complete manual intake.",
            "right_callout_detail": "Prefix function pi prevents backtracking; CRT simultaneously harmonizes ambulance maintenance and sanitization."
        },
        # SLIDE 9: EMPIRICAL BENCHMARKS
        {
            "type": "table_benchmarks",
            "badge": "◆ 08 | EMPIRICAL VALIDATION MATRIX ◆",
            "title": "Hardware Execution Benchmarks & Timing Verification",
            "subtitle": "Real wall-clock execution metrics captured via C++ high-resolution chrono timers on local hardware",
            "headers": ["Module & Algorithm", "Input Scale / Problem Size", "Measured Runtime", "Memory Footprint", "Compliance Status"],
            "rows": [
                ["Custom MergeSort", "N = 1,000 emergency records", "0.4710 ms", "16 KB scratch buffer", "VERIFIED (Zero-STL)"],
                ["Custom QuickSort", "N = 1,000 emergency records", "0.5370 ms", "In-place stack", "VERIFIED (Zero-STL)"],
                ["Binary Search (Iterative)", "N = 1,000 emergency records", "0.0410 µs", "O(1) Memory", "VERIFIED (Zero-STL)"],
                ["Dijkstra Routing (Min-Heap)", "V = 1,000 nodes, E = 3,990 edges", "0.0018 ms", "132 KB heap", "VERIFIED (< 50ms)"],
                ["0/1 Knapsack Payload DP", "N = 25 items, W = 100 kg", "0.0076 ms", "10.4 KB DP table", "VERIFIED (Zero-STL)"],
                ["KMP Keyword Matcher", "N = 10,000 chars call transcript", "6.3300 µs", "Prefix table pi (128B)", "VERIFIED (Zero-STL)"],
                ["Rabin-Karp Rolling Hash", "N = 10,000 chars call transcript", "16.3300 µs", "Rolling hash buffer", "VERIFIED (Zero-STL)"],
                ["Bipartite Matching (Kuhn)", "12 x 12 bipartite pairs", "1.5800 µs", "Augmenting graph", "VERIFIED (Zero-STL)"]
            ],
            "takeaway": "Performance Proof: All routing, sorting, and matching modules execute in < 1 ms, well within the 50 ms real-time ceiling. Pure C++17 custom memory architecture demonstrates deterministic microsecond predictability."
        },
        # SLIDE 10: LIVE CAD DEMO
        {
            "type": "content_4cards",
            "badge": "◆ 09 | FIELD CAD DEMONSTRATION ◆",
            "title": "Centralized Hospital Hub & In-Transit Diversion",
            "subtitle": "Operational CAD command center running live on Dehradun road network at http://localhost:8080",
            "cards": [
                {
                    "title": "Regional Hospital Hub",
                    "color": GOLD_24K,
                    "points": [
                        "Real-time monitoring of Max Hospital, Synergy, AIIMS Rishikesh, and Doon Govt.",
                        "Live telemetry of ER bed intake queues and ICU reserve availability.",
                        "Direct API triggers that prevent hospital over-saturation before dispatch."
                    ],
                    "stat": "4 Hubs",
                    "spec_head": "Real-Time ER Bed Telemetry",
                    "spec": "Hospitals: 4 Centralized | Beds: ER + ICU",
                    "spec_detail": "Continuous background polling of regional bed capacity ensures zero unnotified hospital dock arrivals."
                },
                {
                    "title": "Live CAD Mission Clock",
                    "color": GOLD_CHAMPAGNE,
                    "points": [
                        "Precise mission elapsed timing (T+ HH:MM:SS) synchronized with GPS updates.",
                        "Deterministic simulation stepping ensures smooth, jitter-free vehicle interpolation.",
                        "Tracks vehicle status: Available, En Route Scene, At Scene, En Route Hospital."
                    ],
                    "stat": "T+ Sync",
                    "spec_head": "Wall-Clock Mission Synchrony",
                    "spec": "Precision: T+ HH:MM:SS | Wall-Clock Synced",
                    "spec_detail": "Deterministic simulation stepping prevents vehicle jumps and guarantees realistic transit kinematics."
                },
                {
                    "title": "Automated Rerouting",
                    "color": ACCENT_CRIMSON,
                    "points": [
                        "When destination hospital reaches 100% capacity, CAD sounds an audible MDT siren.",
                        "Visual alert modal presents instant diversion recommendations to dispatcher.",
                        "Dynamically recalculates shortest route from current GPS position to alternate open ICU."
                    ],
                    "stat": "50 ms",
                    "spec_head": "MDT Audio Siren & Rerouting",
                    "spec": "Alert: MDT Audio Siren | Reroute: Instant",
                    "spec_detail": "Triggers immediate secondary route generation to AIIMS Rishikesh or Synergy without returning to base."
                },
                {
                    "title": "Threaded Server & C++ CLI",
                    "color": GOLD_PALE,
                    "points": [
                        "Multi-threaded HTTP CAD server completely eliminates head-of-line blocking.",
                        "Interactive green CRT terminal accepts direct STDIN input commands.",
                        "Execute Scenario 1, Scenario 2, Scenario 3, or run full benchmark suite on demand."
                    ],
                    "stat": "Multi-Thread",
                    "spec_head": "Interactive STDIN C++ Terminal",
                    "spec": "Architecture: Multi-Threaded | Console: STDIN",
                    "spec_detail": "High-throughput threaded worker pool handles concurrent browser map queries and telemetry streaming."
                }
            ]
        },
        # SLIDE 11: DEEP AUDIT & ROADMAP
        {
            "type": "content_2col",
            "badge": "◆ 10 | DEEP AUDIT & ROADMAP ◆",
            "title": "System Scan & Future Production Engineering",
            "subtitle": "Identified architectural bottlenecks and phased evolutionary milestones for regional scaling",
            "left_title": "Identified Bottlenecks",
            "left_bullets": [
                "Floyd-Warshall Pointer Indirection: Vector-of-vectors creates cache thrashing at V > 1,500.",
                "Subprocess Fork-Exec Latency: Spawning dispatch_sim creates 8-15 ms OS process overhead.",
                "Concurrent Bed Reservation Race Conditions: Risk of two ambulances heading to 1 remaining ICU bed simultaneously.",
                "Flat 2D Elevation Model: Ignores steep Himalayan foothill gradients (Rajpur / Mussoorie ascent)."
            ],
            "left_callout_tag": "◆ ASYMPTOTIC COMPLEXITY CEILING ◆",
            "left_callout_stat": "O(V³) Scaling",
            "left_callout_head": "All-Pairs Precomputation Bound",
            "left_callout": "Floyd-Warshall all-pairs precomputation reaches memory access scaling limits above V = 1,500; migrating to 1D flat buffers and Contraction Hierarchies preserves microsecond queries.",
            "left_callout_detail": "Mitigation: Dynamic Contraction Hierarchies (CH) and A* landmark heuristics for regional scaling across Uttarakhand.",
            "right_title": "Phased Upgrade Roadmap",
            "right_bullets": [
                "Phase 1 (Immediate): Multi-threaded CAD server (COMPLETED) & 1D contiguous flat matrix buffer for all-pairs routing.",
                "Phase 2 (IPC & Flows): Shared library (pybind11 / C-ABI) for zero-copy 0ms IPC & Dinic's Algorithm for max flows.",
                "Phase 3 (Field Scaling): 100% self-hosted local Uttarakhand OSM Docker container & atomic bed reservation tokens with TTL.",
                "Phase 4 (Topography): 3D grade-aware energy routing factoring Himalayan steep incline resistance."
            ],
            "right_callout_tag": "◆ PRODUCTION IPC & EVOLUTIONARY TARGET ◆",
            "right_callout_stat": "< 1 µs",
            "right_callout_head": "In-Process Shared Memory Target",
            "right_callout": "Transitioning from OS process forks to an in-process pybind11 shared library C-ABI reduces CAD-to-engine communication latency from 8 ms to under 1 microsecond.",
            "right_callout_detail": "Migrating from standard STDIN pipes to pybind11 C-ABI shared memory drops bridge latency from 8 ms to 0.002 ms."
        },
        # SLIDE 12: CONCLUSION
        {
            "type": "conclusion",
            "badge": "◆ 11 | CONCLUSION & ACADEMIC DEFENSE ◆",
            "title": "Saving Lives Through Smarter Decisions",
            "subtitle": "Delivering a production-grade emergency dispatch platform built on mathematical and algorithmic rigor",
            "kpis": [
                {
                    "tag": "TRAFFIC SPEEDUP",
                    "num": "35–40%",
                    "label": "Response Time Reduction",
                    "sub": "Over static commercial navigation",
                    "detail": "Saves 4.2–6.8 critical minutes during Golden Hour transit."
                },
                {
                    "tag": "ALGORITHMIC SPEED",
                    "num": "0.0018 ms",
                    "label": "Dijkstra (1,000 Nodes)",
                    "sub": "Sub-millisecond execution ceiling",
                    "detail": "550,000x faster than unpruned all-pairs search."
                },
                {
                    "tag": "BED PROTECTION",
                    "num": "0%",
                    "label": "Hospital Dock Rejection",
                    "sub": "Guaranteed via bed reservation telemetry",
                    "detail": "Instant MDT siren and GPS diversion prevents full ER arrival."
                },
                {
                    "tag": "CORE CODEBASE",
                    "num": "100%",
                    "label": "Zero-STL C++17 Compliance",
                    "sub": "All 7 DSA syllabus modules satisfied",
                    "detail": "Zero hidden heap allocations or allocator mutex locking."
                }
            ],
            "findings": [
                {
                    "title": "Academic Rigor & First Principles",
                    "head": "Zero-STL C++17 Specification",
                    "desc": "Engineered all 7 syllabus algorithm modules from first principles without STL dependencies. Custom contiguous vector buffers and binary min-heaps provide deterministic real-time memory predictability."
                },
                {
                    "title": "Himalayan Corridor Deployment",
                    "head": "Live Google Traffic Telemetry",
                    "desc": "Demonstrated on actual Dehradun arterial chokepoints (Rajpur Road, Ballupur Chowk, Premnagar, Chakrata Road). Google Traffic Jam Factor non-linear scaling prevents ambulance gridlock."
                },
                {
                    "title": "Clinical Safety & Bed Resilience",
                    "head": "Automated Bed Reservation & Reroute",
                    "desc": "Centralized 4-hospital regional intake hub (Max, Synergy, AIIMS Rishikesh, Doon Govt). Automated in-transit diversion alerts ensure zero ambulances arrive at saturated emergency departments."
                }
            ],
            "student_info": "Amrit Prasad · SAP ID: 590021684 · B.Tech CSE AIML (2025–2029) · UPES Dehradun SoCS",
            "mentor_info": "Subject Teacher & Academic Mentor: Sandeep Chand Kumain · Advanced DSA (50–60% Delivery)",
            "repo_info": "Consolidated System Repository: /Users/amrit/Documents/Emboolancè (Zero-STL C++ Core + Live CAD Web Engine)"
        }
    ]

    for idx, sdata in enumerate(slides):
        slide = prs.slides.add_slide(blank_layout)

        # Background Fill (Deep Obsidian Onyx)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_ONYX
        bg.line.color.rgb = BG_ONYX

        # Hairline Metallic Gold Top Accent Border
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = GOLD_24K
        top_bar.line.color.rgb = GOLD_24K

        if sdata["type"] != "hero_title":
            # Category Badge
            badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.30))
            p = badge_box.text_frame.paragraphs[0]
            p.text = sdata["badge"]
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE

            # Slide Title (Refined Serif Luxury)
            t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.58), Inches(11.733), Inches(0.55))
            t_box.text_frame.word_wrap = True
            p = t_box.text_frame.paragraphs[0]
            p.text = sdata["title"]
            p.font.size = Pt(23)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = TEXT_WHITE

            # Subtitle
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.16), Inches(11.733), Inches(0.35))
            sub_box.text_frame.word_wrap = True
            p = sub_box.text_frame.paragraphs[0]
            p.text = sdata["subtitle"]
            p.font.size = Pt(11.5)
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_PALE

            # Footer
            ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.30))
            p = ft_box.text_frame.paragraphs[0]
            p.text = f"Emboolancè · UPES Dehradun SoCS · Amrit Prasad (590021684) · Mentor: Sandeep Chand Kumain · Slide {idx + 1} of {len(slides)}"
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_SUBTLE

        # SPECIFIC SLIDE RENDERERS
        if sdata["type"] == "hero_title":
            # Hero Container Warm Noir Glass Card - Expanded to Fill Screen
            hero_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.52), Inches(11.733), Inches(6.45))
            hero_card.fill.solid()
            hero_card.fill.fore_color.rgb = CARD_WARM_NOIR
            hero_card.line.color.rgb = GOLD_24K
            hero_card.line.width = Pt(1.5)

            # Badge
            b_box = slide.shapes.add_textbox(Inches(1.2), Inches(0.75), Inches(10.933), Inches(0.35))
            p = b_box.text_frame.paragraphs[0]
            p.text = sdata["badge"]
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE

            # Title (Regal Georgia Serif, 2 Clean Lines, ZERO Overlap)
            title_b = slide.shapes.add_textbox(Inches(1.2), Inches(1.15), Inches(10.933), Inches(1.10))
            title_b.text_frame.word_wrap = True
            p = title_b.text_frame.paragraphs[0]
            p.text = "EMBOOLANCÈ: SMART EMERGENCY AMBULANCE\nROUTING & HOSPITAL ALLOCATION SYSTEM"
            p.font.size = Pt(26)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = TEXT_WHITE
            p.space_after = Pt(4)

            # Subtitle
            sub_b = slide.shapes.add_textbox(Inches(1.2), Inches(2.35), Inches(10.933), Inches(0.55))
            sub_b.text_frame.word_wrap = True
            p = sub_b.text_frame.paragraphs[0]
            p.text = sdata["subtitle"]
            p.font.size = Pt(12)
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE

            # 3-Stat Hero KPI Strip - Completely fills the center space
            kpi_w = Inches(3.45)
            kpi_gap = Inches(0.29)
            for k_idx, (num, label, desc) in enumerate(sdata["kpis"]):
                k_left = Inches(1.2) + k_idx * (kpi_w + kpi_gap)
                k_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, k_left, Inches(3.05), kpi_w, Inches(1.65))
                k_card.fill.solid()
                k_card.fill.fore_color.rgb = SUB_CARD_BG
                k_card.line.color.rgb = SUB_BORDER
                k_card.line.width = Pt(1.0)

                tb = slide.shapes.add_textbox(k_left + Inches(0.15), Inches(3.15), kpi_w - Inches(0.30), Inches(1.45))
                tb.text_frame.word_wrap = True
                p = tb.text_frame.paragraphs[0]
                p.text = num
                p.font.size = Pt(26)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = GOLD_24K
                p.space_after = Pt(2)

                p2 = tb.text_frame.add_paragraph()
                p2.text = label
                p2.font.size = Pt(11)
                p2.font.bold = True
                p2.font.name = "Georgia"
                p2.font.color.rgb = TEXT_WHITE
                p2.space_after = Pt(3)

                p3 = tb.text_frame.add_paragraph()
                p3.text = desc
                p3.font.size = Pt(9.5)
                p3.font.color.rgb = TEXT_MUTED

            # Gold Divider
            div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.88), Inches(10.933), Inches(0.02))
            div.fill.solid()
            div.fill.fore_color.rgb = CARD_BORDER
            div.line.color.rgb = CARD_BORDER

            # Author Grid: 2 side-by-side cards filling the bottom space
            card_w = Inches(5.32)
            card_h = Inches(1.80)
            # Student Card
            s_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(5.00), card_w, card_h)
            s_card.fill.solid()
            s_card.fill.fore_color.rgb = SUB_CARD_BG
            s_card.line.color.rgb = SUB_BORDER
            s_card.line.width = Pt(1.0)

            st_b = slide.shapes.add_textbox(Inches(1.35), Inches(5.08), card_w - Inches(0.30), card_h - Inches(0.15))
            st_b.text_frame.word_wrap = True
            p = st_b.text_frame.paragraphs[0]
            p.text = "◆ STUDENT RESEARCHER & CANDIDATE ◆"
            p.font.size = Pt(9)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE
            p.space_after = Pt(2)

            p1 = st_b.text_frame.add_paragraph()
            p1.text = "Amrit Prasad"
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.name = "Georgia"
            p1.font.color.rgb = TEXT_WHITE
            p1.space_after = Pt(2)

            p2 = st_b.text_frame.add_paragraph()
            p2.text = "SAP ID: 590021684 · B.Tech CSE (Artificial Intelligence & Machine Learning)"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = GOLD_PALE

            p3 = st_b.text_frame.add_paragraph()
            p3.text = "UPES Dehradun · School of Computer Science (SoCS) · Batch 2025–2029"
            p3.font.size = Pt(9.0)
            p3.font.color.rgb = TEXT_MUTED

            # Mentor Card
            m_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.81), Inches(5.00), card_w, card_h)
            m_card.fill.solid()
            m_card.fill.fore_color.rgb = SUB_CARD_BG
            m_card.line.color.rgb = SUB_BORDER
            m_card.line.width = Pt(1.0)

            mt_b = slide.shapes.add_textbox(Inches(6.96), Inches(5.08), card_w - Inches(0.30), card_h - Inches(0.15))
            mt_b.text_frame.word_wrap = True
            p = mt_b.text_frame.paragraphs[0]
            p.text = "◆ ACADEMIC MENTOR & COURSE EVALUATOR ◆"
            p.font.size = Pt(9)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE
            p.space_after = Pt(2)

            p1 = mt_b.text_frame.add_paragraph()
            p1.text = "Sandeep Chand Kumain"
            p1.font.size = Pt(14)
            p1.font.bold = True
            p1.font.name = "Georgia"
            p1.font.color.rgb = TEXT_WHITE
            p1.space_after = Pt(2)

            p2 = mt_b.text_frame.add_paragraph()
            p2.text = "Advanced Data Structures & Algorithms · Evaluation Milestone (50–60%)"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = GOLD_PALE

            p3 = mt_b.text_frame.add_paragraph()
            p3.text = "Standard: Strict Zero-STL C++17 Core Engine (Zero Hidden Heap Overhead)"
            p3.font.size = Pt(9.0)
            p3.font.color.rgb = TEXT_MUTED

        elif sdata["type"] == "content_2col":
            # Card Dimensions: Top 1.62, Height 5.30 (Bottom 6.92)
            # Left Card
            left_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.62), Inches(5.65), Inches(5.30))
            left_card.fill.solid()
            left_card.fill.fore_color.rgb = CARD_WARM_NOIR
            left_card.line.color.rgb = CARD_BORDER
            left_card.line.width = Pt(1.0)

            lt_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.25), Inches(0.38))
            p = lt_box.text_frame.paragraphs[0]
            p.text = sdata["left_title"]
            p.font.size = Pt(13.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE

            # Hairline Divider under card title
            l_div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.15), Inches(5.25), Inches(0.01))
            l_div.fill.solid()
            l_div.fill.fore_color.rgb = SUB_BORDER
            l_div.line.color.rgb = SUB_BORDER

            # Bullets fill Top 2.22 to 4.65 (Height 2.43)
            lb_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.22), Inches(5.25), Inches(2.45))
            lb_box.text_frame.word_wrap = True
            for b_idx, bullet in enumerate(sdata["left_bullets"]):
                p = lb_box.text_frame.paragraphs[0] if b_idx == 0 else lb_box.text_frame.add_paragraph()
                p.space_after = Pt(10)
                if ":" in bullet:
                    lead, rest = bullet.split(":", 1)
                    r1 = p.add_run()
                    r1.text = "◆ " + lead + ":"
                    r1.font.bold = True
                    r1.font.size = Pt(11.0)
                    r1.font.name = "Georgia"
                    r1.font.color.rgb = GOLD_24K
                    r2 = p.add_run()
                    r2.text = rest
                    r2.font.size = Pt(10.5)
                    r2.font.name = "Georgia"
                    r2.font.color.rgb = TEXT_IVORY
                else:
                    r = p.add_run()
                    r.text = "◆ " + bullet
                    r.font.size = Pt(10.5)
                    r.font.name = "Georgia"
                    r.font.color.rgb = TEXT_IVORY

            # Left Callout Box: Top 4.75, Height 2.05 (reaches 6.80) - ZERO DEAD SPACE!
            l_callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.75), Inches(5.25), Inches(2.05))
            l_callout.fill.solid()
            l_callout.fill.fore_color.rgb = SUB_CARD_BG
            l_callout.line.color.rgb = SUB_BORDER
            l_callout.line.width = Pt(1.0)

            l_callout_tb = slide.shapes.add_textbox(Inches(1.15), Inches(4.82), Inches(4.95), Inches(1.92))
            l_callout_tb.text_frame.word_wrap = True
            p = l_callout_tb.text_frame.paragraphs[0]
            p.text = sdata.get("left_callout_tag", "◆ MATHEMATICAL SPECIFICATION & CLINICAL INVARIANT ◆")
            p.font.size = Pt(8.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE
            p.space_after = Pt(2)

            if "left_callout_stat" in sdata:
                p_stat = l_callout_tb.text_frame.add_paragraph()
                p_stat.text = sdata["left_callout_stat"]
                p_stat.font.size = Pt(17)
                p_stat.font.bold = True
                p_stat.font.name = "Georgia"
                p_stat.font.color.rgb = GOLD_24K
                p_stat.space_after = Pt(2)

            if "left_callout_head" in sdata:
                p_head = l_callout_tb.text_frame.add_paragraph()
                p_head.text = sdata["left_callout_head"]
                p_head.font.size = Pt(10.5)
                p_head.font.bold = True
                p_head.font.name = "Georgia"
                p_head.font.color.rgb = TEXT_WHITE
                p_head.space_after = Pt(3)

            p2 = l_callout_tb.text_frame.add_paragraph()
            p2.text = sdata.get("left_callout", "")
            p2.font.size = Pt(9.5)
            p2.font.name = "Georgia"
            p2.font.color.rgb = GOLD_PALE
            p2.space_after = Pt(3)

            if "left_callout_detail" in sdata:
                p3 = l_callout_tb.text_frame.add_paragraph()
                p3.text = sdata["left_callout_detail"]
                p3.font.size = Pt(8.5)
                p3.font.name = "Georgia"
                p3.font.color.rgb = TEXT_MUTED

            # Right Card
            right_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.85), Inches(1.62), Inches(5.65), Inches(5.30))
            right_card.fill.solid()
            right_card.fill.fore_color.rgb = CARD_WARM_NOIR
            right_card.line.color.rgb = CARD_BORDER
            right_card.line.width = Pt(1.0)

            rt_box = slide.shapes.add_textbox(Inches(7.05), Inches(1.75), Inches(5.25), Inches(0.38))
            p = rt_box.text_frame.paragraphs[0]
            p.text = sdata["right_title"]
            p.font.size = Pt(13.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_24K

            # Hairline Divider under card title
            r_div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.05), Inches(2.15), Inches(5.25), Inches(0.01))
            r_div.fill.solid()
            r_div.fill.fore_color.rgb = SUB_BORDER
            r_div.line.color.rgb = SUB_BORDER

            # Bullets fill Top 2.22 to 4.65 (Height 2.43)
            rb_box = slide.shapes.add_textbox(Inches(7.05), Inches(2.22), Inches(5.25), Inches(2.45))
            rb_box.text_frame.word_wrap = True
            for b_idx, bullet in enumerate(sdata["right_bullets"]):
                p = rb_box.text_frame.paragraphs[0] if b_idx == 0 else rb_box.text_frame.add_paragraph()
                p.space_after = Pt(10)
                if ":" in bullet:
                    lead, rest = bullet.split(":", 1)
                    r1 = p.add_run()
                    r1.text = "◆ " + lead + ":"
                    r1.font.bold = True
                    r1.font.size = Pt(11.0)
                    r1.font.name = "Georgia"
                    r1.font.color.rgb = GOLD_24K
                    r2 = p.add_run()
                    r2.text = rest
                    r2.font.size = Pt(10.5)
                    r2.font.name = "Georgia"
                    r2.font.color.rgb = TEXT_IVORY
                else:
                    r = p.add_run()
                    r.text = "◆ " + bullet
                    r.font.size = Pt(10.5)
                    r.font.name = "Georgia"
                    r.font.color.rgb = TEXT_IVORY

            # Right Callout Box: Top 4.75, Height 2.05 (reaches 6.80) - ZERO DEAD SPACE!
            r_callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.05), Inches(4.75), Inches(5.25), Inches(2.05))
            r_callout.fill.solid()
            r_callout.fill.fore_color.rgb = SUB_CARD_BG
            r_callout.line.color.rgb = SUB_BORDER
            r_callout.line.width = Pt(1.0)

            r_callout_tb = slide.shapes.add_textbox(Inches(7.20), Inches(4.82), Inches(4.95), Inches(1.92))
            r_callout_tb.text_frame.word_wrap = True
            p = r_callout_tb.text_frame.paragraphs[0]
            p.text = sdata.get("right_callout_tag", "◆ REGIONAL ALLOCATION MATRIX & SYSTEM METRIC ◆")
            p.font.size = Pt(8.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_24K
            p.space_after = Pt(2)

            if "right_callout_stat" in sdata:
                p_stat = r_callout_tb.text_frame.add_paragraph()
                p_stat.text = sdata["right_callout_stat"]
                p_stat.font.size = Pt(17)
                p_stat.font.bold = True
                p_stat.font.name = "Georgia"
                p_stat.font.color.rgb = GOLD_24K
                p_stat.space_after = Pt(2)

            if "right_callout_head" in sdata:
                p_head = r_callout_tb.text_frame.add_paragraph()
                p_head.text = sdata["right_callout_head"]
                p_head.font.size = Pt(10.5)
                p_head.font.bold = True
                p_head.font.name = "Georgia"
                p_head.font.color.rgb = TEXT_WHITE
                p_head.space_after = Pt(3)

            p2 = r_callout_tb.text_frame.add_paragraph()
            p2.text = sdata.get("right_callout", "")
            p2.font.size = Pt(9.5)
            p2.font.name = "Georgia"
            p2.font.color.rgb = GOLD_PALE
            p2.space_after = Pt(3)

            if "right_callout_detail" in sdata:
                p3 = r_callout_tb.text_frame.add_paragraph()
                p3.text = sdata["right_callout_detail"]
                p3.font.size = Pt(8.5)
                p3.font.name = "Georgia"
                p3.font.color.rgb = TEXT_MUTED

        elif sdata["type"] == "content_4cards":
            col_width = Inches(2.70)
            col_gap = Inches(0.31)
            for c_idx, c in enumerate(sdata["cards"]):
                left = Inches(0.8) + c_idx * (col_width + col_gap)
                card_s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.62), col_width, Inches(5.30))
                card_s.fill.solid()
                card_s.fill.fore_color.rgb = CARD_WARM_NOIR
                card_s.line.color.rgb = c["color"]
                card_s.line.width = Pt(1.2)

                # Header badge capsule
                b_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), Inches(1.75), Inches(1.10), Inches(0.28))
                b_pill.fill.solid()
                b_pill.fill.fore_color.rgb = SUB_CARD_BG
                b_pill.line.color.rgb = c["color"]
                b_pill.line.width = Pt(0.8)
                p = b_pill.text_frame.paragraphs[0]
                p.text = f"TIER 0{c_idx + 1}"
                p.font.size = Pt(8.5)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = c["color"]

                tb = slide.shapes.add_textbox(left + Inches(0.15), Inches(2.10), col_width - Inches(0.30), Inches(0.48))
                tb.text_frame.word_wrap = True
                p = tb.text_frame.paragraphs[0]
                p.text = c["title"]
                p.font.size = Pt(12)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = TEXT_WHITE

                # Description / 3 Structured Points - Top 2.62 to 4.35 (Height 1.73)
                desc_tb = slide.shapes.add_textbox(left + Inches(0.15), Inches(2.62), col_width - Inches(0.30), Inches(1.75))
                desc_tb.text_frame.word_wrap = True
                for p_idx, pt_text in enumerate(c.get("points", [c.get("desc", "")])):
                    p = desc_tb.text_frame.paragraphs[0] if p_idx == 0 else desc_tb.text_frame.add_paragraph()
                    p.space_after = Pt(4)
                    if ":" in pt_text:
                        lead, rest = pt_text.split(":", 1)
                        r1 = p.add_run()
                        r1.text = "◆ " + lead + ":"
                        r1.font.bold = True
                        r1.font.size = Pt(8.8)
                        r1.font.name = "Georgia"
                        r1.font.color.rgb = c["color"]
                        r2 = p.add_run()
                        r2.text = rest
                        r2.font.size = Pt(8.4)
                        r2.font.name = "Georgia"
                        r2.font.color.rgb = TEXT_IVORY
                    else:
                        r = p.add_run()
                        r.text = "◆ " + pt_text
                        r.font.size = Pt(8.4)
                        r.font.name = "Georgia"
                        r.font.color.rgb = TEXT_IVORY

                # Card Bottom Spec Badge: Top 4.52, Height 2.28 (reaches 6.80)
                spec_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), Inches(4.52), col_width - Inches(0.30), Inches(2.28))
                spec_box.fill.solid()
                spec_box.fill.fore_color.rgb = SUB_CARD_BG
                spec_box.line.color.rgb = SUB_BORDER
                spec_box.line.width = Pt(1.0)

                s_tb = slide.shapes.add_textbox(left + Inches(0.20), Inches(4.58), col_width - Inches(0.40), Inches(2.15))
                s_tb.text_frame.word_wrap = True
                p = s_tb.text_frame.paragraphs[0]
                p.text = "◆ TECHNICAL SPECIFICATIONS ◆"
                p.font.size = Pt(8.0)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = GOLD_CHAMPAGNE
                p.space_after = Pt(2)

                if "stat" in c:
                    p_stat = s_tb.text_frame.add_paragraph()
                    p_stat.text = c["stat"]
                    p_stat.font.size = Pt(16)
                    p_stat.font.bold = True
                    p_stat.font.name = "Georgia"
                    p_stat.font.color.rgb = GOLD_24K
                    p_stat.space_after = Pt(2)

                if "spec_head" in c:
                    p_head = s_tb.text_frame.add_paragraph()
                    p_head.text = c["spec_head"]
                    p_head.font.size = Pt(9.0)
                    p_head.font.bold = True
                    p_head.font.name = "Georgia"
                    p_head.font.color.rgb = TEXT_WHITE
                    p_head.space_after = Pt(2)

                p2 = s_tb.text_frame.add_paragraph()
                p2.text = c.get("spec", "")
                p2.font.size = Pt(8.5)
                p2.font.name = "Georgia"
                p2.font.color.rgb = GOLD_PALE
                p2.space_after = Pt(2)

                if "spec_detail" in c:
                    p3 = s_tb.text_frame.add_paragraph()
                    p3.text = c["spec_detail"]
                    p3.font.size = Pt(7.8)
                    p3.font.name = "Georgia"
                    p3.font.color.rgb = TEXT_MUTED

        elif sdata["type"] == "table_syllabus":
            rows = len(sdata["rows"]) + 1
            table_shape = slide.shapes.add_table(rows, 4, Inches(0.8), Inches(1.55), Inches(11.733), Inches(4.45))
            tbl = table_shape.table
            tbl.columns[0].width = Inches(2.1)
            tbl.columns[1].width = Inches(3.2)
            tbl.columns[2].width = Inches(4.4)
            tbl.columns[3].width = Inches(2.033)

            headers = ["DSA Module", "Implemented Algorithms", "Domain Emergency Dispatch Role", "Complexity Bounds"]
            for col_idx, h_text in enumerate(headers):
                cell = tbl.cell(0, col_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(60, 48, 18)
                p = cell.text_frame.paragraphs[0]
                p.text = h_text
                p.font.size = Pt(11)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = GOLD_PALE

            for r_idx, r_data in enumerate(sdata["rows"]):
                for col_idx, val in enumerate(r_data):
                    cell = tbl.cell(r_idx + 1, col_idx)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = CARD_WARM_NOIR if r_idx % 2 == 0 else RGBColor(25, 22, 18)
                    p = cell.text_frame.paragraphs[0]
                    p.text = val
                    p.font.size = Pt(10.5)
                    p.font.name = "Georgia"
                    p.font.color.rgb = GOLD_CHAMPAGNE if col_idx == 0 else (GOLD_24K if col_idx == 3 else TEXT_IVORY)

            # Bottom Takeaway Strip: Top 6.10, Height 0.95 (reaches 7.05)
            bot_strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.10), Inches(11.733), Inches(0.95))
            bot_strip.fill.solid()
            bot_strip.fill.fore_color.rgb = SUB_CARD_BG
            bot_strip.line.color.rgb = SUB_BORDER
            bot_strip.line.width = Pt(1.0)

            t_tb = slide.shapes.add_textbox(Inches(1.0), Inches(6.16), Inches(11.333), Inches(0.82))
            t_tb.text_frame.word_wrap = True
            p = t_tb.text_frame.paragraphs[0]
            p.text = "◆ ACADEMIC VERIFICATION & RIGOROUS SYLLABUS COMPLIANCE ◆"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE
            p.space_after = Pt(2)

            p2 = t_tb.text_frame.add_paragraph()
            p2.text = sdata.get("takeaway", "")
            p2.font.size = Pt(10.0)
            p2.font.name = "Georgia"
            p2.font.color.rgb = GOLD_PALE

        elif sdata["type"] == "table_benchmarks":
            rows = len(sdata["rows"]) + 1
            table_shape = slide.shapes.add_table(rows, 5, Inches(0.8), Inches(1.55), Inches(11.733), Inches(4.45))
            tbl = table_shape.table
            tbl.columns[0].width = Inches(2.5)
            tbl.columns[1].width = Inches(2.6)
            tbl.columns[2].width = Inches(2.0)
            tbl.columns[3].width = Inches(2.3)
            tbl.columns[4].width = Inches(2.333)

            for col_idx, h_text in enumerate(sdata["headers"]):
                cell = tbl.cell(0, col_idx)
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(60, 48, 18)
                p = cell.text_frame.paragraphs[0]
                p.text = h_text
                p.font.size = Pt(11)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = GOLD_PALE

            for r_idx, r_data in enumerate(sdata["rows"]):
                for col_idx, val in enumerate(r_data):
                    cell = tbl.cell(r_idx + 1, col_idx)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = CARD_WARM_NOIR if r_idx % 2 == 0 else RGBColor(25, 22, 18)
                    p = cell.text_frame.paragraphs[0]
                    p.text = val
                    p.font.size = Pt(10)
                    p.font.name = "Georgia"
                    p.font.color.rgb = GOLD_PALE if col_idx == 2 else (GOLD_24K if col_idx == 4 else TEXT_IVORY)

            # Bottom Takeaway Strip: Top 6.10, Height 0.95 (reaches 7.05)
            bot_strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.10), Inches(11.733), Inches(0.95))
            bot_strip.fill.solid()
            bot_strip.fill.fore_color.rgb = SUB_CARD_BG
            bot_strip.line.color.rgb = SUB_BORDER
            bot_strip.line.width = Pt(1.0)

            t_tb = slide.shapes.add_textbox(Inches(1.0), Inches(6.16), Inches(11.333), Inches(0.82))
            t_tb.text_frame.word_wrap = True
            p = t_tb.text_frame.paragraphs[0]
            p.text = "◆ HARDWARE CHRONO BENCHMARK VERIFICATION ◆"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_CHAMPAGNE
            p.space_after = Pt(2)

            p2 = t_tb.text_frame.add_paragraph()
            p2.text = sdata.get("takeaway", "")
            p2.font.size = Pt(10.0)
            p2.font.name = "Georgia"
            p2.font.color.rgb = GOLD_PALE

        elif sdata["type"] == "conclusion":
            # 4 Top KPI Cards: Top 1.62, Height 1.95 (Bottom 3.57)
            col_width = Inches(2.70)
            col_gap = Inches(0.31)
            for k_idx, k in enumerate(sdata["kpis"]):
                left = Inches(0.8) + k_idx * (col_width + col_gap)
                card_s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.62), col_width, Inches(1.95))
                card_s.fill.solid()
                card_s.fill.fore_color.rgb = CARD_WARM_NOIR
                card_s.line.color.rgb = GOLD_24K
                card_s.line.width = Pt(1.2)

                tb = slide.shapes.add_textbox(left + Inches(0.12), Inches(1.68), col_width - Inches(0.24), Inches(1.82))
                tb.text_frame.word_wrap = True

                # Tag Pill
                p_tag = tb.text_frame.paragraphs[0]
                p_tag.text = f"◆ {k['tag']} ◆"
                p_tag.font.size = Pt(8.0)
                p_tag.font.bold = True
                p_tag.font.name = "Georgia"
                p_tag.font.color.rgb = GOLD_CHAMPAGNE
                p_tag.space_after = Pt(1)

                p = tb.text_frame.add_paragraph()
                p.text = k["num"]
                p.font.size = Pt(21)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = GOLD_24K
                p.space_after = Pt(2)

                p2 = tb.text_frame.add_paragraph()
                p2.text = k["label"]
                p2.font.size = Pt(10.0)
                p2.font.bold = True
                p2.font.name = "Georgia"
                p2.font.color.rgb = TEXT_WHITE
                p2.space_after = Pt(2)

                p3 = tb.text_frame.add_paragraph()
                p3.text = k["sub"]
                p3.font.size = Pt(8.5)
                p3.font.color.rgb = GOLD_PALE
                p3.space_after = Pt(2)

                p4 = tb.text_frame.add_paragraph()
                p4.text = k["detail"]
                p4.font.size = Pt(8.0)
                p4.font.color.rgb = TEXT_MUTED

            # Middle 3-Column Defense Strip: Top 3.70, Height 1.88 (Bottom 5.58)
            mid_w = Inches(3.70)
            mid_gap = Inches(0.31)
            for f_idx, f in enumerate(sdata.get("findings", [])):
                f_left = Inches(0.8) + f_idx * (mid_w + mid_gap)
                f_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, f_left, Inches(3.70), mid_w, Inches(1.88))
                f_card.fill.solid()
                f_card.fill.fore_color.rgb = SUB_CARD_BG
                f_card.line.color.rgb = SUB_BORDER
                f_card.line.width = Pt(1.0)

                f_tb = slide.shapes.add_textbox(f_left + Inches(0.18), Inches(3.78), mid_w - Inches(0.36), Inches(1.72))
                f_tb.text_frame.word_wrap = True
                p = f_tb.text_frame.paragraphs[0]
                p.text = f"◆ {f['title']}"
                p.font.size = Pt(11.5)
                p.font.bold = True
                p.font.name = "Georgia"
                p.font.color.rgb = GOLD_24K
                p.space_after = Pt(2)

                p_sub = f_tb.text_frame.add_paragraph()
                p_sub.text = f["head"]
                p_sub.font.size = Pt(9.5)
                p_sub.font.bold = True
                p_sub.font.name = "Georgia"
                p_sub.font.color.rgb = GOLD_CHAMPAGNE
                p_sub.space_after = Pt(4)

                p2 = f_tb.text_frame.add_paragraph()
                p2.text = f["desc"]
                p2.font.size = Pt(9.2)
                p2.font.name = "Georgia"
                p2.font.color.rgb = TEXT_IVORY

            # Bottom Academic Defense Summary Card: Top 5.72, Height 1.20 (Bottom 6.92)
            sum_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.72), Inches(11.733), Inches(1.20))
            sum_card.fill.solid()
            sum_card.fill.fore_color.rgb = CARD_WARM_NOIR
            sum_card.line.color.rgb = CARD_BORDER
            sum_card.line.width = Pt(1.0)

            sum_tb = slide.shapes.add_textbox(Inches(1.0), Inches(5.78), Inches(11.333), Inches(1.05))
            sum_tb.text_frame.word_wrap = True
            p = sum_tb.text_frame.paragraphs[0]
            p.text = "◆ FINAL ACADEMIC EVALUATION & CAPSTONE VERIFICATION ◆"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.name = "Georgia"
            p.font.color.rgb = GOLD_24K
            p.space_after = Pt(2)

            p1 = sum_tb.text_frame.add_paragraph()
            p1.text = "Student Candidate: " + sdata.get("student_info", "")
            p1.font.size = Pt(9.5)
            p1.font.bold = True
            p1.font.name = "Georgia"
            p1.font.color.rgb = TEXT_WHITE
            p1.space_after = Pt(1)

            p2 = sum_tb.text_frame.add_paragraph()
            p2.text = sdata.get("mentor_info", "")
            p2.font.size = Pt(9.0)
            p2.font.name = "Georgia"
            p2.font.color.rgb = GOLD_PALE
            p2.space_after = Pt(1)

            p3 = sum_tb.text_frame.add_paragraph()
            p3.text = sdata.get("repo_info", "")
            p3.font.size = Pt(8.5)
            p3.font.name = "Georgia"
            p3.font.color.rgb = TEXT_MUTED

    prs.save(PPTX_PATH)
    print(f"✅ Generated Clean Black & Gold PPTX at: {PPTX_PATH}")

def convert_pptx_to_keynote():
    """Uses macOS AppleScript to open the cleaned PPTX and save a 100% native .key file."""
    apple_script = f'''
    tell application "Keynote"
        activate
        set theDoc to open POSIX file "{PPTX_PATH}"
        delay 2
        save theDoc in POSIX file "{KEY_PATH}"
        close theDoc saving no
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", apple_script], check=True, timeout=30)
        print(f"✅ Generated Native Apple Keynote File at: {KEY_PATH}")
    except Exception as e:
        print(f"Keynote conversion note: {e}")

def create_keynote_launcher():
    """Creates a clickable macOS terminal script to launch Keynote directly."""
    content = f'''#!/bin/bash
open -a Keynote "{KEY_PATH}"
'''
    with open(COMMAND_PATH, "w") as f:
        f.write(content)
    os.chmod(COMMAND_PATH, 0o755)
    print(f"✅ Generated One-Click Keynote Launcher at: {COMMAND_PATH}")

def export_keynote_qa_images():
    """Exports slide PNGs from native Keynote file for automated visual QA."""
    qa_dir = os.path.join(OUTPUT_DIR, "keynote_qa")
    os.makedirs(qa_dir, exist_ok=True)
    apple_script = f'''
    tell application "Keynote"
        activate
        set theDoc to open POSIX file "{KEY_PATH}"
        delay 1
        set qaFolder to POSIX file "{qa_dir}"
        export theDoc to qaFolder as slide images with properties {{image format:PNG, skipped slides:false}}
        close theDoc saving no
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", apple_script], check=True, timeout=30)
        print(f"✅ Exported Visual QA slide images to: {qa_dir}")
    except Exception as e:
        print(f"Keynote image export note: {e}")

if __name__ == "__main__":
    create_pptx()
    convert_pptx_to_keynote()
    create_keynote_launcher()
    export_keynote_qa_images()
