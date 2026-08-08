"""
SignalSentinel AI - Traffic & System Simulator
Simulates IoT sensor data, congestion, AI decisions, and Green Wave state.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from threading import Lock
from typing import Any


@dataclass
class SystemStatus:
    active_sensors: int = 12847
    total_sensors: int = 13102
    signal_nodes: int = 4291
    ai_latency_ms: float = 18.0
    data_refresh_s: float = 1.2
    uptime_pct: float = 99.97
    ai_enabled: bool = True
    last_ai_action: str = "Adjusted 47 signals on I-95 S4"


@dataclass
class NetworkKPIs:
    avg_travel_time_min: float = 14.2
    avg_travel_delta_pct: float = -8.0
    congestion_index: float = 0.38
    congestion_delta_pct: float = 3.0
    signal_efficiency_pct: float = 91.4
    emergency_response_min: float = 2.1


@dataclass
class Alert:
    id: str
    level: str  # critical | warn | info
    type: str
    title: str
    detail: str
    timestamp: str


@dataclass
class AIAction:
    time: str
    title: str
    detail: str


@dataclass
class GreenWaveState:
    active: bool = False
    route: str = ""
    remaining_seconds: int = 0
    started_at: float | None = None


class TrafficSimulator:
    """Thread-safe in-memory simulator for the dashboard."""

    def __init__(self) -> None:
        self._lock = Lock()
        self.status = SystemStatus()
        self.kpis = NetworkKPIs()
        self.green_wave = GreenWaveState()
        self.alerts: list[Alert] = [
            Alert(
                id="a1",
                level="critical",
                type="CONGESTION",
                title="I-95 Sector 4 — Queue 1.8km",
                detail="AI adjusting 12 signals",
                timestamp=self._now_str(),
            ),
            Alert(
                id="a2",
                level="warn",
                type="SENSOR OFFLINE",
                title="Node TX-882 Downtown East",
                detail="Last ping 4m ago",
                timestamp=self._now_str(),
            ),
            Alert(
                id="a3",
                level="info",
                type="GREEN WAVE",
                title="Route 7 Hospital Corridor",
                detail="Priority active",
                timestamp=self._now_str(),
            ),
        ]
        self.ai_log: list[AIAction] = [
            AIAction("14:22", "Signal timing adjusted", "I-95 S4 • 47 nodes • −18s delay"),
            AIAction("14:19", "Green Wave initiated", "Route 7 • Priority Level 1"),
            AIAction("14:15", "Predictive cycle complete", "Metro-wide • Efficiency +2.1%"),
            AIAction("14:08", "Congestion forecast", "Downtown Grid • Peak in 22min"),
            AIAction("14:01", "Manual override released", "Admin • Sector 2 signals"),
        ]
        self._heatmap_seed = random.randint(0, 9999)

    def _now_str(self) -> str:
        return datetime.now(timezone.utc).strftime("%H:%M")

    def get_status(self) -> dict[str, Any]:
        with self._lock:
            self._tick_green_wave()
            # Live-looking jitter every poll so dashboard never freezes
            self.status.ai_latency_ms = round(16 + random.uniform(0, 8), 1)
            self.status.active_sensors = 12800 + random.randint(0, 80)
            self.status.signal_nodes = 4291 + random.randint(-5, 5)
            self.kpis.avg_travel_time_min = round(13.5 + random.uniform(0, 1.8), 1)
            self.kpis.avg_travel_delta_pct = round(-10 + random.uniform(0, 5), 1)
            self.kpis.congestion_index = round(0.30 + random.uniform(0, 0.18), 2)
            self.kpis.congestion_delta_pct = round(1 + random.uniform(0, 5), 1)
            self.kpis.signal_efficiency_pct = round(89 + random.uniform(0, 4), 1)
            self.kpis.emergency_response_min = round(1.8 + random.uniform(0, 0.6), 1)
            return {
                "status": asdict(self.status),
                "kpis": asdict(self.kpis),
                "green_wave": asdict(self.green_wave),
                "alerts": [asdict(a) for a in self.alerts],
                "ai_log": [asdict(a) for a in self.ai_log[:12]],
                "server_time": datetime.now(timezone.utc).isoformat(),
            }

    def get_heatmap(self, cols: int = 16, rows: int = 12) -> dict[str, Any]:
        with self._lock:
            self._heatmap_seed = (self._heatmap_seed + 1) % 100000
            random.seed(self._heatmap_seed)
            cells = []
            heavy = {(3, 5), (3, 6), (4, 5), (4, 6), (5, 5), (8, 8), (8, 9), (9, 8), (2, 10), (3, 10)}
            moderate = {(6, 3), (7, 3), (7, 4), (10, 2), (11, 2), (11, 3), (1, 7), (2, 7), (12, 6), (13, 6)}

            for r in range(rows):
                for c in range(cols):
                    level = random.random()
                    if (c, r) in heavy or level > 0.92:
                        intensity = 0.55 + random.random() * 0.35
                        color = f"rgba(239, 68, 68, {intensity:.2f})"
                        state = "heavy"
                    elif (c, r) in moderate or level > 0.75:
                        intensity = 0.40 + random.random() * 0.35
                        color = f"rgba(245, 158, 11, {intensity:.2f})"
                        state = "moderate"
                    else:
                        intensity = 0.15 + random.random() * 0.35
                        color = f"rgba(16, 185, 129, {intensity:.2f})"
                        state = "free"
                    cells.append({"c": c, "r": r, "color": color, "state": state})
            random.seed()  # restore
            return {"cols": cols, "rows": rows, "cells": cells, "updated_at": self._now_str()}

    def toggle_ai(self) -> dict[str, Any]:
        with self._lock:
            self.status.ai_enabled = not self.status.ai_enabled
            state = "ENABLED" if self.status.ai_enabled else "DISABLED"
            self._push_log("AI Optimization toggled", f"Admin • Now {state}")
            return {"ai_enabled": self.status.ai_enabled}

    def force_cycle(self) -> dict[str, Any]:
        with self._lock:
            now = self._now_str()
            self.status.last_ai_action = f"Forced cycle completed — {now}"
            self._push_log("Manual optimization forced", "Admin • Network-wide rebalance")
            self.kpis.congestion_index = max(0.15, self.kpis.congestion_index - 0.02)
            return {"last_ai_action": self.status.last_ai_action}

    def trigger_green_wave(self, route: str) -> dict[str, Any]:
        with self._lock:
            if self.green_wave.active:
                return {"ok": False, "message": "Green Wave already active"}
            self.green_wave = GreenWaveState(
                active=True,
                route=route,
                remaining_seconds=252,
                started_at=time.time(),
            )
            self._push_log("Green Wave triggered", f"Emergency • {route.split('—')[0].strip()}")
            self.alerts = [a for a in self.alerts if a.type != "GREEN WAVE"]
            self.alerts.insert(
                0,
                Alert(
                    id="gw",
                    level="info",
                    type="GREEN WAVE",
                    title=route,
                    detail="Priority active",
                    timestamp=self._now_str(),
                ),
            )
            return {"ok": True, "green_wave": asdict(self.green_wave)}

    def _tick_green_wave(self) -> None:
        if not self.green_wave.active or self.green_wave.started_at is None:
            return
        elapsed = int(time.time() - self.green_wave.started_at)
        remaining = max(0, 252 - elapsed)
        self.green_wave.remaining_seconds = remaining
        if remaining <= 0:
            self.green_wave = GreenWaveState()
            self.alerts = [a for a in self.alerts if a.type != "GREEN WAVE"]

    def _push_log(self, title: str, detail: str) -> None:
        self.ai_log.insert(0, AIAction(self._now_str(), title, detail))
        self.ai_log = self.ai_log[:20]

    def run_policy_sim(self, policy: str) -> dict[str, Any]:
        with self._lock:
            results = {
                "Peak Hour Aggressive": ("−11% peak delay, +6% throughput. Confidence 87%.", "success"),
                "Nighttime Eco Mode": ("−4% energy use, travel time +1.2%. Confidence 91%.", "success"),
                "Event Overflow Protocol": ("+14% capacity near venues. Confidence 78%.", "warn"),
                "Custom Scenario": ("Baseline maintained. No significant change. Confidence 95%.", "info"),
            }
            msg, level = results.get(policy, ("Simulation complete.", "info"))
            self._push_log("Policy simulation run", f"Planner • {policy}")
            return {"message": msg, "level": level}


simulator = TrafficSimulator()
