# Infrastructure & Hosting Analysis: Free Tier & Low-Cost Providers

**Document Standard:** `260720_0818_001`  
**Domain Context:** `aomaker.org` & `edge-ai` Telemetry Pipeline

---

## 📊 1. Free-Tier Cloud VM Provider Matrix

| Provider & Tier | CPU & Memory | Storage & Bandwidth | Static Public IP Policy | Best Use Case in `edge-ai` |
| :--- | :--- | :--- | :--- | :--- |
| **Oracle Cloud (OCI) Always Free** | **4 Arm Ampere cores** + 24 GB RAM (or 2 AMD Micro VMs) | 200 GB Block Storage, 10 TB/month outbound | **Free** (Up to 50 reserved IPv4 addresses per region) | **Primary Hub**: WireGuard VPN, Mosquitto MQTT, heavy build runners |
| **Google Cloud (GCP) Always Free** | **1 `e2-micro` instance** (0.25-1 vCPU, 1 GB RAM) | 30 GB Standard Disk, 1 GB/month egress | **Conditional**: Free *only while attached* to a running VM. (Billed if detached) | **Secondary Node**: Light relay, DNS failover, monitoring probe |
| **Cloudflare Free Tier** | Unlimited static requests (Pages), 100k/day (Workers) | Global Edge CDN Cache | Managed via Cloudflare Anycast IP | **Edge CDN**: Site security, DDoS shield, `cloudflared` TCP tunnels |

---

## 🏛️ 2. Detailed Platform Analysis

### 2.1 Oracle Cloud Infrastructure (OCI) Always Free *(Top Recommendation)*
- **Specs**: Up to 4 ARM Ampere vCPUs, 24 GB RAM, 200 GB storage.
- **Static Public IP**: OCI allows reserving static public IPv4 addresses at zero cost.
- **Role in `edge-ai`**: Hosts the persistent WireGuard VPN gateway and Mosquitto MQTT broker. Handles incoming telemetry from local workstation build nodes (`Core12`, `jason-lab.dev`) cleanly.

### 2.2 Google Cloud Platform (GCP) Always Free (`e2-micro`)
- **Specs**: 1 `e2-micro` VM in US regions (us-west1, us-central1, us-east1).
- **Static Public IP Warning**: GCP provides free in-use external IPs for `e2-micro`, but **bills for idle static IPs** if the VM is stopped or deleted while the IP remains reserved.
- **Role in `edge-ai`**: Acts as a lightweight secondary relay or fallback telemetry mirror.

### 2.3 Google Sites (`google.sites.com`) & Google Workspace (`aomaker.org`)
- **Domain Capabilities**: As members of the `aomaker.org` Google Workspace organization:
  - Custom domain mapping (`aomaker.org`, `www.aomaker.org`) points directly to Google Sites.
  - Shared Google Drive for collaborative media and design assets.
- **Integration Strategy**: Use Google Sites to host the main `aomaker.org` public portal (low-code maker community news, events, project showcases) and embed the GitHub Pages dashboard (`dash.aomaker.org`) inside an iframe or direct navigation link.

### 2.4 Cloudflare (Pages, Workers & Tunnels)
- **Cloudflare Pages**: Free deployment of static dashboard frontends with global edge CDN caching.
- **Cloudflare Tunnels (`cloudflared`)**: Allows exposing the OCI/GCP VM Mosquitto MQTT broker (port 1883/8883) to the internet over encrypted TCP/WebSocket tunnels **without opening public firewall ports** or exposing home IPs.

---

## 💶 3. Secondary Low-Cost & Budget-Controlled Options

| Provider | Cost / Month | Hardware Specs | Strengths / Tradeoffs |
| :--- | :--- | :--- | :--- |
| **Hetzner Cloud** | ~€3.80 / mo ($4.15) | 2 vCPU (ARM/x86), 4 GB RAM, 40 GB NVMe, 20 TB Traffic | **Best Low-Cost Paid VPS**: Unmatched performance per dollar, unmetered bandwidth. |
| **Render** | $0 (Free Tier) | 512 MB RAM, Shared vCPU | Good for web services; sleeps after 15 minutes of inactivity. |
| **Fly.io** | $0 (Free Allowance) | Up to 3 micro VMs (256 MB RAM) | Great for global microservices; strict RAM limits on free tier. |
| **Vercel / Netlify** | $0 (Free Tier) | Serverless Functions & Static CDN | Industry standard for Next.js/JAMstack frontends; 100 GB bandwidth. |
| **AWS Lightsail** | $3.50 / mo | 1 vCPU, 512 MB RAM, 20 GB SSD, 1 TB Traffic | Low-cost entry into AWS ecosystem with static public IP. |
