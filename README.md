# SignalSentinel AI

**Hybrid traffic management & analytics system** for national / multi-city networks.

Pure **Python** implementation using **Streamlit**.

Real-time IoT sensor data + AI/ML signal optimization with human-in-the-loop controls for administrators, emergency services, and urban planners.

## Features

| Role | Capabilities |
|------|--------------|
| **System Administrator** | Full access, AI engine control, manual overrides, system health |
| **Emergency Services** | Trigger **Green Wave** priority routing |
| **Urban Planner** | Performance reports, policy simulation |

### Core Flows
1. Live traffic heatmaps + system status dashboard
2. AI detects congestion → automatically adjusts signal timings
3. Emergency services trigger Green Wave priority corridors
4. Planners review analytics and test optimization policies

## Tech Stack

- **Language**: Python 3.12
- **UI**: Streamlit (pure Python, no HTML/JS required)
- **Data**: pandas + numpy
- **Simulation**: Custom Python traffic & AI engine

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Kiwmoj/fire-hack.git
cd fire-hack

# 2. Create virtualenv
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (usually **http://localhost:8501**)

## Project Structure

```
fire-hack/
├── streamlit_app.py        # Main Streamlit dashboard (pure Python)
├── services/
│   └── simulator.py        # Traffic / AI / Green Wave simulation
├── requirements.txt
├── .gitignore
└── README.md
```

## Design

Dark Command & Control aesthetic:
- Background `#0D1117`
- Cards `#1F2937`
- Accent `#3B82F6`

## License

MIT
