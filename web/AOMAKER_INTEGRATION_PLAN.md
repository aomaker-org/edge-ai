# `aomaker.org` Integration & Web Transformation Plan

**Document Standard:** `260720_0818_001`  
**Target Domain:** `aomaker.org`  
**Associated Sites:** `jason-lab.dev` & `dash.aomaker.org`

---

## 🚀 1. Strategic Goals

Currently, **`aomaker.org`** (Aloha Oregon Makers / STEM community hub) exists as a stub web presence. This plan establishes an actionable roadmap to transform `aomaker.org` into an integrated, professional portal linking community resources, hardware engineering logs, and real-time edge AI dashboards.

---

## 🌐 2. Ecosystem Domain Topology

```text
aomaker.org (Google Sites Public Portal)
├── / (Home / Community News / STEM Maker Projects)
├── /dashboard ───────► Links to dash.aomaker.org (GitHub Pages SPA)
└── /labs ────────────► Links to jason-lab.dev (Acme Lab Silicon Telemetry)
```

1. **`aomaker.org` Primary Portal (Google Sites)**:
   - Hosted on Google Sites via Google Workspace domain mapping.
   - Low-maintenance, zero-cost public landing page featuring maker community news, project showcases, and member directory.
2. **`dash.aomaker.org` Real-Time Dashboard (GitHub Pages)**:
   - Hosted on GitHub Pages via CNAME record.
   - Serves the `edge-ai` interactive build matrix health, SLM inference metrics, and AGY telemetry status.
3. **`jason-lab.dev` Acme Lab Engineering Archives**:
   - Partner silicon validation site featuring 18-year tactical log archives and hardware telemetry.

---

## 📋 3. Action Items & Implementation Milestones

### Phase 1: Domain & Google Workspace Arming
- [ ] Configure `aomaker.org` DNS CNAME & A-records in Google Domains / Cloudflare.
- [ ] Map `aomaker.org` to Google Sites landing page.
- [ ] Set up `dash.aomaker.org` CNAME pointing to `aomaker-org.github.io`.

### Phase 2: GitHub Pages Dashboard Deployment
- [ ] Implement initial React/Vite dashboard SPA in `edge-ai/web/dashboard/`.
- [ ] Configure GitHub Actions workflow (`.github/workflows/deploy_dashboard.yml`) to deploy on push to `main`.
- [ ] Embed `make agy-sync` & `make ai-log-diff-demo` output summaries into the dashboard data feed.

### Phase 3: Telemetry & Overlay Network Coupling
- [ ] Spin up OCI Always Free ARM instance and configure static IPv4.
- [ ] Deploy WireGuard VPN server on OCI VM and connect `Core12` & `jason-lab.dev` peers.
- [ ] Deploy Eclipse Mosquitto broker and expose WebSocket port `9001` via Cloudflare Tunnel (`cloudflared`).
