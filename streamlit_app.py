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

# Clean dark theme
st.markdown("""
<style>
    .stApp { background-color: #0D1117; color: #E5E7EB; }
    h1, h2, h3, h4 { color: #E5E7EB !important; }
    .stMetric {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 10px 14px;
    }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.4rem !important; }
    .stButton > button {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { background-color: #2563EB; color: white; }
    div[data-testid="stSidebar"] { background-color: #161B22; }
    .block-container { padding-top: 1.2rem; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.title("🚦 SignalSentinel AI")
    st.caption("National Traffic Command")

    role = st.radio(
        "Operator Role",
        ["Admin", "Emergency", "Planner"],
        index=0
    )

    st.divider()

    status_data = simulator.get_status()
    s = status_data["status"]
    k = status_data["kpis"]

    st.subheader("System Health")
    st.metric("Active Sensors", f"{s['active_sensors']:,}")
    st.metric("Signal Nodes", f"{s['signal_nodes']:,}")
    st.metric("AI Latency", f"{s['ai_latency_ms']} ms")
    st.metric("Uptime", f"{s['uptime_pct']}%")

    st.divider()
    if st.button("↻ Refresh Data"):
        st.rerun()


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Command & Control")
    st.caption(f"Role: **{role}**  ·  System Online  ·  IoT Connected")
with col2:
    ai_label = "🟢 AUTO" if s["ai_enabled"] else "🔴 OFF"
    st.metric("AI Engine", ai_label)


# ──────────────────────────────────────────────
# KPIs
# ──────────────────────────────────────────────
st.subheader("Network KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Travel Time", f"{k['avg_travel_time_min']} min", f"{k['avg_travel_delta_pct']}%")
c2.metric("Congestion Index", f"{k['congestion_index']:.2f}", f"+{k['congestion_delta_pct']}%")
c3.metric("Signal Efficiency", f"{k['signal_efficiency_pct']}%")
c4.metric("Emergency Response", f"{k['emergency_response_min']} min")

st.divider()


# ──────────────────────────────────────────────
# Main area
# ──────────────────────────────────────────────
left, right = st.columns([2, 1])

with left:
    st.subheader("Live Traffic Heatmap")

    # Build simple heatmap without matplotlib
    heatmap_data = simulator.get_heatmap(cols=12, rows=8)
    cells = heatmap_data["cells"]

    grid = np.zeros((8, 12))
    for cell in cells:
        val = {"free": 0.25, "moderate": 0.6, "heavy": 0.95}.get(cell["state"], 0.3)
        grid[cell["r"] % 8, cell["c"] % 12] = val

    # Show as a simple table with emoji intensity
    rows = []
    for r in range(8):
        row = []
        for c in range(12):
            v = grid[r, c]
            if v > 0.8:
                row.append("🔴")
            elif v > 0.5:
                row.append("🟡")
            else:
                row.append("🟢")
        rows.append(row)

    df_heat = pd.DataFrame(rows, columns=[f"S{c+1}" for c in range(12)])
    st.dataframe(df_heat, use_container_width=True, hide_index=True, height=280)
    st.caption("🟢 Free   🟡 Moderate   🔴 Heavy congestion")

    # Alerts
    st.subheader("Active Alerts")
    for a in status_data["alerts"]:
        icon = {"critical": "🔴", "warn": "🟡", "info": "🔵"}.get(a["level"], "⚪")
        st.markdown(f"**{icon} {a['type']}** — {a['title']}  \n`{a['detail']} · {a['timestamp']}`")

with right:
    if role == "Admin":
        st.subheader("AI Engine")
        label = "Disable AI" if s["ai_enabled"] else "Enable AI"
        if st.button(label, type="primary"):
            simulator.toggle_ai()
            st.rerun()
        if st.button("Force Optimization Cycle"):
            result = simulator.force_cycle()
            st.success(result["last_ai_action"])
            time.sleep(0.4)
            st.rerun()
        st.info(f"**Last Action**\n\n{s['last_ai_action']}")

    elif role == "Emergency":
        st.subheader("Priority Routing")
        st.warning("EMERGENCY MODE")
        route = st.selectbox("Corridor", [
            "Route 7 — Central Hospital Corridor",
            "I-95 Express — Northbound Priority",
            "Downtown Grid — Sector A",
            "Airport Access — Terminal 3",
        ])
        gw = status_data["green_wave"]
        if gw["active"]:
            m, sec = divmod(gw["remaining_seconds"], 60)
            st.success(f"🟢 Green Wave ACTIVE\n\n{m}m {sec:02d}s remaining")
            st.progress(max(0, 1 - gw["remaining_seconds"] / 252))
        else:
            if st.button("⚡ TRIGGER GREEN WAVE", type="primary"):
                result = simulator.trigger_green_wave(route)
                if result.get("ok"):
                    st.success("Green Wave started!")
                    time.sleep(0.6)
                    st.rerun()
                else:
                    st.error(result.get("message", "Failed"))

    elif role == "Planner":
        st.subheader("Policy Simulator")
        policy = st.selectbox("Policy", [
            "Peak Hour Aggressive",
            "Nighttime Eco Mode",
            "Event Overflow Protocol",
            "Custom Scenario",
        ])
        if st.button("Run Simulation", type="primary"):
            result = simulator.run_policy_sim(policy)
            if result["level"] == "success":
                st.success(result["message"])
            elif result["level"] == "warn":
                st.warning(result["message"])
            else:
                st.info(result["message"])

        st.subheader("Performance (24h)")
        chart_df = pd.DataFrame({
            "Hour": ["00", "04", "08", "12", "16", "20", "24"],
            "Congestion": [0.22, 0.18, 0.41, 0.55, 0.48, 0.35, 0.28]
        }).set_index("Hour")
        st.line_chart(chart_df, color="#3B82F6")
        m1, m2 = st.columns(2)
        m1.metric("Delay Saved", "1,847 hrs")
        m2.metric("Fuel Saved", "42.3k L")


# ──────────────────────────────────────────────
# AI Log
# ──────────────────────────────────────────────
st.divider()
st.subheader("AI Actions Log")
log_df = pd.DataFrame(status_data["ai_log"])
if not log_df.empty:
    st.dataframe(
        log_df[["time", "title", "detail"]],
        use_container_width=True,
        hide_index=True,
        height=200
    )

st.caption(
    f"SignalSentinel AI v2.4.1  ·  Latency {s['ai_latency_ms']}ms  ·  "
    f"{s['signal_nodes']:,} nodes  ·  {datetime.utcnow().strftime('%H:%M:%S')} UTC"
)
