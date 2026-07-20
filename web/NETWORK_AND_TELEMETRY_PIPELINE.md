# Network Overlay & Telemetry Pipeline Specification

**Document Standard:** `260720_0818_001`  
**Core Technologies:** WireGuard VPN, Eclipse Mosquitto MQTT, Cloudflare Tunnels

---

## 🔒 1. WireGuard Overlay Network Topology

To connect heterogeneous hardware labs (`Core12` WSL2, `jason-lab.dev` Acme Lab silicon test rigs, and OCI/GCP cloud instances) into a secure, encrypted peer-to-peer fabric, `edge-ai` utilizes **WireGuard**.

```text
                               ┌───────────────────────────────┐
                               │  Oracle Cloud Always Free VM  │
                               │  (WireGuard Hub: 10.8.0.1)    │
                               │  - Mosquitto Broker (1883)    │
                               │  - WebSockets Proxy (9001)    │
                               └───────────────┬───────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
┌───────────────────────────────────────────┐     ┌───────────────────────────────────────────┐
│     Core12 Workstation (WSL2 / Linux)     │     │      Acme Lab (jason-lab.dev Rigs)       │
│      (WireGuard Peer: 10.8.0.2)           │     │       (WireGuard Peer: 10.8.0.3)          │
│ - Runs builds & telemetry sync            │     │ - Silicon validation telemetry            │
│ - Publishes MQTT telemetry events         │     │ - Historical log archives                 │
└───────────────────────────────────────────┘     └───────────────────────────────────────────┘
```

### Key Advantages of WireGuard Overlay:
- **Zero Firewall Port Opening**: Workstations behind NAT/WSL2 establish outbound WireGuard tunnels to the OCI static IP hub (`10.8.0.1`).
- **High Throughput & Low Latency**: Kernel-level UDP encryption (ChaCha20-Poly1305) ensures minimal CPU overhead during telemetry streaming.

---

## 📡 2. Eclipse Mosquitto MQTT Telemetry Pipeline

The telemetry pipeline uses **Eclipse Mosquitto** as an idempotent, lightweight publish-subscribe broker running on the OCI VM node.

### Topic Namespace Standard

| Topic Pattern | Description | Payload Schema |
| :--- | :--- | :--- |
| `edge-ai/telemetry/builds` | Build status & matrix execution logs | `{"status": "PASS", "target": "sycl", "timestamp_id": "260720_0818_001"}` |
| `edge-ai/telemetry/inference` | SLM token generation metrics | `{"model": "qwen-0.5b", "tokens_per_sec": 42.5, "ttft_ms": 120}` |
| `edge-ai/telemetry/log-diff` | AI Log Diff surface summary | `{"added_errors": 0, "missing_events": 2, "report_url": "..."}` |
| `acme-lab/telemetry/silicon` | Hardware telemetry from `jason-lab.dev` | `{"temp_c": 48.2, "power_w": 15.4, "voltage_v": 1.2}` |

### Web-Friendly Access (MQTT over WebSockets)
- Mosquitto is configured to enable WebSockets on port `9001`.
- The GitHub Pages dashboard (`dash.aomaker.org`) connects directly to `wss://dash.aomaker.org/mqtt` via `cloudflared` tunnel, allowing live browser UI updates without page reloads.
