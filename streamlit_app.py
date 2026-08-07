"""
SignalSentinel AI - Pure Python Streamlit Dashboard
Command & Control traffic management system
"""

import time
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np

from services.simulator import simulator

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="SignalSentinel AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom dark theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0D1117;
        color: #E5E7EB;
    }
    .stMetric {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 12px;
    }
    .stMetric label {
        color: #9CA3AF !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
    .stButton > button {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #2563EB;
        color: white;
    }
    h1, h2, h3 {
        color: #E5E7EB !important;
    }
    .block-container {
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Sidebar – Role & Controls
# ──────────────────────────────────────────────
with st.sidebar:
    st.title("🚦 SignalSentinel AI")
    st.caption("National Traffic Command")

    role = st.radio(
        "Operator Role",
        ["Admin", "Emergency", "Planner"],
        index=0,
        help="Switch between System Administrator, Emergency Services, and Urban Planner views"
    )

    st.divider()

    # Live system status
    status_data = simulator.get_status()
    s = status_data["status"]
    k = status_data["kpis"]

    st.subheader("System Health")
    st.metric("Active Sensors", f"{s['active_sensors']:,}", f"/{s['total_sensors']:,}")
    st.metric("Signal Nodes", f"{s['signal_nodes']:,}")
    st.metric("AI Latency", f"{s['ai_latency_ms']} ms")
    st.metric("Uptime", f"{s['uptime_pct']}%")

    st.divider()
    st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")
    if st.button("↻ Refresh Data", use_container_width=True):
        st.rerun()


# ──────────────────────────────────────────────
# Main header
# ──────────────────────────────────────────────
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title("Command & Control Dashboard")
    st.caption(f"Role: **{role}**  |  System Online  |  IoT Stream Connected")

with col_status:
    ai_state = "🟢 AUTO" if s["ai_enabled"] else "🔴 OFF"
    st.metric("AI Engine", ai_state)


# ──────────────────────────────────────────────
# KPI Row
# ──────────────────────────────────────────────
st.subheader("Network KPIs")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Avg Travel Time",
        f"{k['avg_travel_time_min']} min",
        f"{k['avg_travel_delta_pct']}%",
        delta_color="inverse"
    )
with kpi2:
    st.metric(
        "Congestion Index",
        f"{k['congestion_index']:.2f}",
        f"+{k['congestion_delta_pct']}%",
        delta_color="inverse"
    )
with kpi3:
    st.metric("Signal Efficiency", f"{k['signal_efficiency_pct']}%")
with kpi4:
    st.metric("Emergency Response", f"{k['emergency_response_min']} min avg")


st.divider()


# ──────────────────────────────────────────────
# Main content area – depends on role
# ──────────────────────────────────────────────
left, right = st.columns([2, 1])

with left:
    st.subheader("Live Traffic Heatmap")

    # Generate heatmap data
    heatmap_data = simulator.get_heatmap(cols=16, rows=12)
    cells = heatmap_data["cells"]

    # Convert to 2D array for visualization
    grid = np.zeros((12, 16))
    for cell in cells:
        # Map state to numeric value
        val = {"free": 0.2, "moderate": 0.55, "heavy": 0.9}.get(cell["state"], 0.3)
        # Add some noise for visual interest
        val += np.random.uniform(-0.05, 0.05)
        grid[cell["r"], cell["c"]] = np.clip(val, 0, 1)

    df_heat = pd.DataFrame(grid)
    st.dataframe(
        df_heat.style.background_gradient(cmap="RdYlGn_r", vmin=0, vmax=1)
        .format("{:.2f}")
        .set_properties(**{"font-size": "8px"}),
        use_container_width=True,
        height=380,
        hide_index=True,
    )
    st.caption("🟢 Free  ·  🟡 Moderate  ·  🔴 Heavy congestion")

    # Active Alerts
    st.subheader("Active Alerts")
    alerts = status_data["alerts"]
    for a in alerts:
        level_emoji = {"critical": "🔴", "warn": "🟡", "info": "🔵"}.get(a["level"], "⚪")
        st.markdown(
            f"**{level_emoji} {a['type']}** — {a['title']}  \n"
            f"<small>{a['detail']} · {a['timestamp']}</small>",
            unsafe_allow_html=True
        )

with right:
    # ── Admin controls ──
    if role == "Admin":
        st.subheader("AI Engine Controls")

        ai_label = "Disable AI Optimization" if s["ai_enabled"] else "Enable AI Optimization"
        if st.button(ai_label, use_container_width=True, type="primary"):
            simulator.toggle_ai()
            st.rerun()

        if st.button("Force Optimization Cycle", use_container_width=True):
            result = simulator.force_cycle()
            st.success(result["last_ai_action"])
            time.sleep(0.5)
            st.rerun()

        st.info(f"**Last Action**\n\n{s['last_ai_action']}")

    # ── Emergency controls ──
    elif role == "Emergency":
        st.subheader("Priority Routing")
        st.warning("EMERGENCY MODE")

        route = st.selectbox(
            "Select Corridor",
            [
                "Route 7 — Central Hospital Corridor",
                "I-95 Express — Northbound Priority",
                "Downtown Grid — Sector A",
                "Airport Access — Terminal 3",
            ]
        )

        gw = status_data["green_wave"]
        if gw["active"]:
            remaining = gw["remaining_seconds"]
            m, sec = divmod(remaining, 60)
            st.success(f"🟢 Green Wave ACTIVE\n\nETA: {m}m {sec:02d}s remaining")
            st.progress(1 - (remaining / 252))
        else:
            if st.button("⚡ TRIGGER GREEN WAVE", use_container_width=True, type="primary"):
                result = simulator.trigger_green_wave(route)
                if result.get("ok"):
                    st.success("Green Wave initiated!")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error(result.get("message", "Failed"))

    # ── Planner controls ──
    elif role == "Planner":
        st.subheader("Policy Simulator")

        policy = st.selectbox(
            "Select Policy",
            [
                "Peak Hour Aggressive",
                "Nighttime Eco Mode",
                "Event Overflow Protocol",
                "Custom Scenario",
            ]
        )

        if st.button("Run Simulation", use_container_width=True, type="primary"):
            result = simulator.run_policy_sim(policy)
            level = result["level"]
            if level == "success":
                st.success(result["message"])
            elif level == "warn":
                st.warning(result["message"])
            else:
                st.info(result["message"])

        st.subheader("Performance (24h)")
        # Simple synthetic chart data
        chart_data = pd.DataFrame({
            "Hour": ["00", "04", "08", "12", "16", "20", "24"],
            "Congestion": [0.22, 0.18, 0.41, 0.55, 0.48, 0.35, 0.28]
        }).set_index("Hour")
        st.line_chart(chart_data, color="#3B82F6")

        m1, m2 = st.columns(2)
        m1.metric("Delay Saved", "1,847 hrs")
        m2.metric("Fuel Saved", "42.3k L")


# ──────────────────────────────────────────────
# AI Actions Log
# ──────────────────────────────────────────────
st.divider()
st.subheader("AI Actions Log")

log = status_data["ai_log"]
log_df = pd.DataFrame(log)
if not log_df.empty:
    st.dataframe(
        log_df[["time", "title", "detail"]],
        use_container_width=True,
        hide_index=True,
        height=220,
    )


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.caption(
    f"SignalSentinel AI v2.4.1 (Streamlit)  ·  "
    f"Latency: {s['ai_latency_ms']}ms  ·  "
    f"Nodes: {s['signal_nodes']:,} online  ·  "
    f"{datetime.utcnow().strftime('%H:%M:%S')} UTC"
)
