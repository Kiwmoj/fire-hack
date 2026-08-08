# SignalSentinel AI

**AI-powered traffic signal optimization and emergency priority routing for multi-city networks.**

Built for hackathon demo · Pure Python · Streamlit

---

## Problem

Urban congestion wastes time and fuel. Emergency vehicles lose critical minutes waiting at red lights. Static signal timing cannot adapt to live traffic.

## Solution

SignalSentinel AI uses simulated IoT sensor data and an AI engine to:

1. **Optimize signal timing** dynamically across the network  
2. **Trigger Green Wave corridors** for emergency vehicles  
3. **Give planners** policy simulation and impact metrics  
4. **Keep humans in control** with role-based admin overrides  

## Architecture

```
IoT Sensors  →  AI Optimization Engine  →  Signal Controllers
                                              ↓
                                      Command Dashboard
```

Human operators (Admin / Emergency / Planner) can always override.

## Demo accounts

| Username   | Password       | Role       | What you can do                          |
|------------|----------------|------------|------------------------------------------|
| `admin`    | `admin123`     | Admin      | Toggle AI, force optimization cycles     |
| `emergency`| `emergency123` | Emergency  | Trigger Green Wave priority routing       |
| `planner`  | `planner123`   | Planner    | Run policy sims, view impact metrics     |
| `viewer`   | `viewer123`    | Viewer     | View-only maps, cameras, KPIs, alerts    |

## Suggested 2-minute demo path

1. Login as **`emergency` / `emergency123`**  
2. Trigger **Green Wave** on a corridor → show countdown + alert  
3. **Sign out** → login as **`admin` / `admin123`**  
4. **Force Optimization Cycle** → show AI action log update  
5. Open **Planner** account → show impact metrics (delay/fuel saved)

## Run locally

```bash
git clone https://github.com/Kiwmoj/fire-hack.git
cd fire-hack
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

## Features

- Secure login with role-based access  
- Live KPI strip + demo impact metrics  
- Interactive traffic map  
- Public DOT camera snapshots (Iowa / Virginia) + US 511 links  
- Sector congestion heatmap  
- Admin AI engine controls  
- Emergency Green Wave routing  
- Planner policy simulator  
- Optional auto-refresh every 5 seconds  

## Tech stack

- Python 3  
- Streamlit  
- Pandas / NumPy  
- In-memory traffic simulator (`services/simulator.py`)  

## Note on cameras

Public government cameras are **snapshot images** (updated on the server every ~30–60s), not continuous video streams. Click **Refresh** or enable auto-refresh to load the latest frame. For full state camera maps, use the **All US 511 maps** tab.

---

**SignalSentinel AI** — hybrid human + AI traffic command for safer, faster cities.
