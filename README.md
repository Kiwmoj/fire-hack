# SignalSentinel AI

**Hybrid traffic management & analytics system** for national / multi-city networks.

Real-time IoT sensor data + AI/ML signal optimization with human-in-the-loop controls for administrators, emergency services, and urban planners.

![Design](https://img.shields.io/badge/UI-Command%20%26%20Control%20Dark-0D1117?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Flask-3B82F6?style=flat-square)

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

- **Backend**: Python 3.12 + Flask
- **Frontend**: Vanilla JS + custom CSS (no Tailwind CDN)
- **Charts**: Chart.js
- **Design**: Dark Command & Control (`#0D1117` / `#1F2937` / `#3B82F6`)

## Quick Start

```bash
git clone https://github.com/Kiwmoj/fire-hack.git
cd fire-hack

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000**

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/status` | Full system status, KPIs, alerts, AI log |
| `GET`  | `/api/heatmap` | Live traffic heatmap cells |
| `POST` | `/api/ai/toggle` | Enable / disable AI optimization |
| `POST` | `/api/ai/force-cycle` | Force an optimization cycle |
| `POST` | `/api/green-wave` | Trigger Green Wave |
| `POST` | `/api/policy/simulate` | Run policy simulation |
| `GET`  | `/api/health` | Health check |

## Project Structure

```
fire-hack/
├── app.py
├── requirements.txt
├── services/
│   └── simulator.py
├── templates/
│   └── dashboard.html
├── static/
│   └── css/
│       └── app.css
├── .gitignore
└── README.md
```

## License

MIT
