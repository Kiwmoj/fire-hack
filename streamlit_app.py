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

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except ImportError:
    HAS_AUTOREFRESH = False

st.set_page_config(
    page_title="SignalSentinel AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: linear-gradient(165deg, #0A0E14 0%, #0D1117 40%, #111820 100%);
        color: #E6EDF3;
    }

    h1, h2, h3, h4 {
        color: #F0F6FC !important;
        letter-spacing: -0.03em;
        font-weight: 700 !important;
    }

    .stMetric {
        background: linear-gradient(180deg, #161B22 0%, #12171E 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    div[data-testid="stMetricValue"] {
        color: #F0F6FC !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8B949E !important;
        font-weight: 500 !important;
    }

    .stButton > button {
        background: linear-gradient(180deg, #238636 0%, #1A7F37 100%);
        color: white !important;
        border: 1px solid #2EA043;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        padding: 0.55rem 1rem;
        box-shadow: 0 2px 8px rgba(35, 134, 54, 0.25);
    }
    .stButton > button:hover {
        background: linear-gradient(180deg, #2EA043 0%, #238636 100%);
        border-color: #3FB950;
        color: white !important;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #010409 0%, #0D1117 100%);
        border-right: 1px solid #21262D;
    }

    .block-container {
        padding-top: 1.75rem;
        padding-bottom: 2.5rem;
        max-width: 1380px;
    }

    [data-testid="stForm"] {
        background: linear-gradient(180deg, #161B22 0%, #12171E 100%);
        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    }

    .ss-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(31,111,235,0.25), rgba(88,166,255,0.12));
        color: #79C0FF;
        border: 1px solid rgba(88,166,255,0.35);
        border-radius: 999px;
        padding: 0.3rem 1rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .ss-role-banner {
        border-left: 3px solid #58A6FF;
        border-radius: 0 10px 10px 0;
        padding: 0.65rem 1rem;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, rgba(88,166,255,0.12), transparent);
    }
    .ss-role-admin { border-left-color: #F85149; background: linear-gradient(90deg, rgba(248,81,73,0.12), transparent); }
    .ss-role-emergency { border-left-color: #D29922; background: linear-gradient(90deg, rgba(210,153,34,0.12), transparent); }
    .ss-role-planner { border-left-color: #58A6FF; background: linear-gradient(90deg, rgba(88,166,255,0.12), transparent); }
    .ss-role-viewer { border-left-color: #8B949E; background: linear-gradient(90deg, rgba(139,148,158,0.1), transparent); }

    hr { border-color: #21262D !important; margin: 1.25rem 0 !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


USERS = {
    "admin": {"password": "admin123", "role": "Admin", "name": "System Administrator"},
    "emergency": {"password": "emergency123", "role": "Emergency", "name": "Emergency Responder"},
    "planner": {"password": "planner123", "role": "Planner", "name": "Urban Planner"},
    "viewer": {"password": "viewer123", "role": "Viewer", "name": "Public Viewer"},
}


def generate_map_points(n=80):
    center_lat, center_lon = 40.7580, -73.9855
    lats = center_lat + np.random.normal(0, 0.04, n)
    lons = center_lon + np.random.normal(0, 0.05, n)
    congestion = np.random.choice(["Free", "Moderate", "Heavy"], n, p=[0.55, 0.30, 0.15])
    size = np.where(congestion == "Heavy", 80, np.where(congestion == "Moderate", 50, 30))
    return pd.DataFrame({"lat": lats, "lon": lons, "congestion": congestion, "size": size})


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.display_name = None


if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, center, _ = st.columns([0.9, 1.4, 0.9])
    with center:
        st.markdown("# 🚦 SignalSentinel AI")
        st.markdown('<div style="text-align:center"><span class="ss-badge">National Traffic Command</span></div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown(
            "<p style='text-align:center;color:#8B949E;font-size:1.05rem;line-height:1.5;'>"
            "AI-powered signal optimization and emergency priority routing<br>"
            "for multi-city traffic networks."
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown("")

        with st.form("login_form"):
            st.markdown("#### Sign in to continue")
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign In →", use_container_width=True)

            if submitted:
                user = USERS.get(username.strip().lower())
                if user and user["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.role = user["role"]
                    st.session_state.username = username.strip().lower()
                    st.session_state.display_name = user["name"]
                    st.success(f"Welcome, {user['name']}")
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.markdown("")
        st.markdown(
            "<p style='text-align:center;color:#8B949E;font-size:0.9rem;font-weight:600;'>Demo accounts</p>",
            unsafe_allow_html=True,
        )
        a, b = st.columns(2)
        with a:
            st.markdown("`admin` / `admin123`  \n<span style='color:#8B949E;font-size:0.8rem;'>Full AI control</span>", unsafe_allow_html=True)
            st.markdown("`emergency` / `emergency123`  \n<span style='color:#8B949E;font-size:0.8rem;'>Green Wave</span>", unsafe_allow_html=True)
        with b:
            st.markdown("`planner` / `planner123`  \n<span style='color:#8B949E;font-size:0.8rem;'>Analytics</span>", unsafe_allow_html=True)
            st.markdown("`viewer` / `viewer123`  \n<span style='color:#8B949E;font-size:0.8rem;'>View only</span>", unsafe_allow_html=True)
    st.stop()


role = st.session_state.role
status_data = simulator.get_status()
s = status_data["status"]
k = status_data["kpis"]

with st.sidebar:
    st.markdown("### 🚦 SignalSentinel")
    st.caption("National Traffic Command")
    st.markdown(f"**{st.session_state.display_name}**")
    st.caption(f"Role · {role}")
    if st.button("Sign Out"):
        for key in ("logged_in", "role", "username", "display_name"):
            st.session_state[key] = False if key == "logged_in" else None
        st.rerun()

    st.divider()
    st.markdown("#### System Health")
    st.metric("Active Sensors", f"{s['active_sensors']:,}")
    st.metric("Signal Nodes", f"{s['signal_nodes']:,}")
    st.metric("AI Latency", f"{s['ai_latency_ms']} ms")
    st.metric("Uptime", f"{s['uptime_pct']}%")

    st.divider()
    if st.button("↻ Refresh Data"):
        st.rerun()
    auto = st.checkbox("Auto-refresh 5s", value=True, key="auto_refresh")
    if auto and HAS_AUTOREFRESH:
        st_autorefresh(interval=5000, key="ss_auto")

    st.divider()
    st.markdown("#### Architecture")
    st.code(
        "IoT Sensors\n    ↓\nAI Optimization Engine\n    ↓\nSignal Controllers\n    ↓\nCommand Dashboard",
        language=None,
    )
    st.caption("Human override always available")


ROLE_META = {
    "Admin": ("🔴 ADMIN ACCESS", "Full system control · AI engine · manual overrides", "ss-role-admin"),
    "Emergency": ("🟠 EMERGENCY ACCESS", "Priority routing · Green Wave corridors", "ss-role-emergency"),
    "Planner": ("🔵 PLANNER ACCESS", "Analytics · policy simulation · impact reports", "ss-role-planner"),
    "Viewer": ("⚪ VIEWER ACCESS", "Read-only dashboard · no control actions", "ss-role-viewer"),
}
badge, blurb, css_cls = ROLE_META.get(role, ("ROLE", "", "ss-role-viewer"))
st.markdown(
    f'<div class="ss-role-banner {css_cls}"><strong>{badge}</strong><br>'
    f'<span style="color:#8B949E;font-size:0.9rem;">{blurb}</span></div>',
    unsafe_allow_html=True,
)

h1, h2 = st.columns([5, 1])
with h1:
    st.markdown("# Command & Control")
    st.caption(f"{st.session_state.display_name}  ·  **{role}**  ·  System Online  ·  IoT Connected")
with h2:
    st.metric("AI Engine", "🟢 AUTO" if s["ai_enabled"] else "🔴 OFF")

st.markdown("### Network KPIs")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Avg Travel Time", f"{k['avg_travel_time_min']} min", f"{k['avg_travel_delta_pct']}%")
k2.metric("Congestion Index", f"{k['congestion_index']:.2f}", f"+{k['congestion_delta_pct']}%")
k3.metric("Signal Efficiency", f"{k['signal_efficiency_pct']}%")
k4.metric("Emergency Response", f"{k['emergency_response_min']} min")

if role in ("Admin", "Planner", "Emergency"):
    st.markdown("### Demo Impact")
    st.caption("Simulated 30-day network window")
    i1, i2, i3, i4 = st.columns(4)
    i1.metric("Delay Hours Saved", "1,847", "+12%")
    i2.metric("Fuel Saved", "42.3k L", "+9%")
    i3.metric("Emergency ETA Cut", "34%", "faster")
    i4.metric("Signals Optimized", "47", "last cycle")
else:
    st.caption("Impact metrics hidden for Viewer accounts.")

st.divider()

st.markdown("### Live Traffic Map")
st.caption("Sensor density · Larger points = heavier congestion")
st.map(generate_map_points(90), size="size", zoom=11, use_container_width=True)

st.markdown("### Live Camera Feeds")
CAMERA_CATALOG = {
    "Iowa": [
        ("I-235 Des Moines", "https://atmsqf.iowadot.gov/SNAPSHOTS/PUBLIC/Metro/dmtv05hd.jpeg"),
        ("I-80 MM 71.7", "https://atmsqf.iowadot.gov/SNAPSHOTS/PUBLIC/Metro/80tv072hd.jpeg"),
        ("I-80 Rest Area", "https://atmsqf.iowadot.gov/snapshots/Public/RestAreas/RA80EB300-01-CENTER.jpg"),
        ("RWIS I-35", "https://atmsqf.iowadot.gov/snapshots/Public/RWIS/RWIS_84-01.jpg"),
    ],
    "Virginia": [
        ("I-64 MM 238.4", "https://snapshot.vdotcameras.com/thumbs/HamptonRoads877.flv.png"),
        ("I-64 MM 237.8", "https://snapshot.vdotcameras.com/thumbs/HamptonRoads878.flv.png"),
        ("I-64 MM 236.4", "https://snapshot.vdotcameras.com/thumbs/HamptonRoads881.flv.png"),
        ("Settlers Landing", "https://snapshot.vdotcameras.com/thumbs/HamptonRoads887.flv.png"),
    ],
}
cam_tabs = st.tabs(list(CAMERA_CATALOG.keys()) + ["All US 511 maps"])
for idx, (state, cams) in enumerate(CAMERA_CATALOG.items()):
    with cam_tabs[idx]:
        cols = st.columns(len(cams))
        _ts = int(time.time())
        for col, (name, url) in zip(cols, cams):
            with col:
                st.caption(name)
                try:
                    st.image(f"{url}?t={_ts}", use_column_width=True)
                except Exception:
                    st.warning("Offline")
with cam_tabs[-1]:
    st.markdown("Official state traffic camera portals")
    states_511 = {
        "California": "https://cwwp2.dot.ca.gov/vm/streamlist.htm",
        "Texas": "https://www.txdot.gov/discover/live-traffic-cameras.html",
        "Florida": "https://fl511.com/",
        "New York": "https://www.511ny.org/",
        "Virginia": "https://www.511virginia.org/",
        "Iowa": "https://511ia.org/",
        "Washington": "https://www.wsdot.com/traffic/cameras/",
        "Illinois": "https://www.gettingaroundillinois.com/",
    }
    c = st.columns(4)
    for i, (name, url) in enumerate(states_511.items()):
        c[i % 4].markdown(f"**[{name}]({url})**")
    st.caption("Open any link for full state camera maps.")

st.divider()

left, right = st.columns([1.55, 1], gap="large")

with left:
    st.markdown("### Sector Heatmap")
    heatmap_data = simulator.get_heatmap(cols=12, rows=8)
    cells = heatmap_data["cells"]
    grid = np.zeros((8, 12))
    for cell in cells:
        val = {"free": 0.25, "moderate": 0.6, "heavy": 0.95}.get(cell["state"], 0.3)
        grid[cell["r"] % 8, cell["c"] % 12] = val
    rows = []
    for r in range(8):
        row = []
        for c in range(12):
            v = grid[r, c]
            row.append("🔴" if v > 0.8 else ("🟡" if v > 0.5 else "🟢"))
        rows.append(row)
    st.dataframe(
        pd.DataFrame(rows, columns=[f"S{c+1}" for c in range(12)]),
        use_container_width=True,
        hide_index=True,
        height=240,
    )
    st.caption("🟢 Free  ·  🟡 Moderate  ·  🔴 Heavy")

    st.markdown("### Active Alerts")
    for a in status_data["alerts"]:
        icon = {"critical": "🔴", "warn": "🟡", "info": "🔵"}.get(a["level"], "⚪")
        st.markdown(f"**{icon} {a['type']}** — {a['title']}  \n`{a['detail']} · {a['timestamp']}`")

with right:
    st.markdown(f"### Controls · {role}")

    if role == "Admin":
        st.error("ADMIN CONTROLS")
        st.markdown("**AI Engine**")
        label = "Disable AI" if s["ai_enabled"] else "Enable AI"
        if st.button(label, type="primary", key="admin_toggle_ai"):
            simulator.toggle_ai()
            st.rerun()
        if st.button("Force Optimization Cycle", key="admin_force"):
            result = simulator.force_cycle()
            st.success(result["last_ai_action"])
            time.sleep(0.3)
            st.rerun()
        st.info(f"**Last action**\n\n{s['last_ai_action']}")
        st.markdown("---")
        st.markdown("**System overrides**")
        st.checkbox("Allow manual signal override", value=True, key="admin_override")
        st.checkbox("Broadcast network alert", value=False, key="admin_broadcast")
        st.caption("Admin-only switches")

    elif role == "Emergency":
        st.warning("EMERGENCY CONTROLS")
        st.markdown("**Priority Routing**")
        route = st.selectbox("Corridor", [
            "Route 7 — Central Hospital Corridor",
            "I-95 Express — Northbound Priority",
            "Downtown Grid — Sector A",
            "Airport Access — Terminal 3",
        ], key="em_route")
        gw = status_data["green_wave"]
        if gw["active"]:
            m, sec = divmod(gw["remaining_seconds"], 60)
            st.success(f"🟢 Green Wave ACTIVE · {m}m {sec:02d}s left")
            st.progress(max(0, 1 - gw["remaining_seconds"] / 252))
        else:
            if st.button("⚡ TRIGGER GREEN WAVE", type="primary", key="em_gw"):
                result = simulator.trigger_green_wave(route)
                if result.get("ok"):
                    st.success("Green Wave started")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error(result.get("message", "Failed"))
        st.markdown("---")
        st.markdown("**Incident notes**")
        st.text_area("Dispatch note", placeholder="Ambulance en route…", key="em_note")
        st.caption("Emergency-only panel")

    elif role == "Planner":
        st.info("PLANNER CONTROLS")
        st.markdown("**Policy Simulator**")
        policy = st.selectbox("Policy", [
            "Peak Hour Aggressive",
            "Nighttime Eco Mode",
            "Event Overflow Protocol",
            "Custom Scenario",
        ], key="pl_policy")
        if st.button("Run Simulation", type="primary", key="pl_run"):
            result = simulator.run_policy_sim(policy)
            level = result["level"]
            if level == "success":
                st.success(result["message"])
            elif level == "warn":
                st.warning(result["message"])
            else:
                st.info(result["message"])
        st.markdown("**24h Congestion trend**")
        chart_df = pd.DataFrame({
            "Hour": ["00", "04", "08", "12", "16", "20", "24"],
            "Congestion": [0.22, 0.18, 0.41, 0.55, 0.48, 0.35, 0.28],
        }).set_index("Hour")
        st.line_chart(chart_df, color="#58A6FF")
        st.markdown("---")
        st.metric("Projected annual delay saved", "22,100 hrs")
        st.caption("Planner-only analytics")

    else:
        st.markdown("**VIEWER — no control panel**")
        st.info(
            "Logged in as **Viewer**.\n\n"
            "• Maps, cameras, KPIs: visible\n"
            "• AI engine: hidden\n"
            "• Green Wave: hidden\n"
            "• Policy simulator: hidden\n\n"
            "Sign out and login as admin / emergency / planner for controls."
        )

st.divider()
if role in ("Admin", "Planner", "Emergency"):
    st.markdown("### AI Actions Log")
    log_df = pd.DataFrame(status_data["ai_log"])
    if not log_df.empty:
        st.dataframe(
            log_df[["time", "title", "detail"]],
            use_container_width=True,
            hide_index=True,
            height=180,
        )
else:
    st.caption("AI action log restricted for Viewer accounts")

st.caption(
    f"SignalSentinel AI  ·  {role}  ·  {s['ai_latency_ms']}ms  ·  "
    f"{s['signal_nodes']:,} nodes  ·  {datetime.utcnow().strftime('%H:%M:%S')} UTC"
)
