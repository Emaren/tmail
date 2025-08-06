📬 TMAIL_SNAPSHOT.md
Last updated: 2025-08-06

🔧 Overview
This snapshot documents the current development state of the Tmail Project, including both tmail-app (frontend) and tmail-api (backend). The project enables tracked email interactions through embedded pixel URLs, providing read receipts and stats via a custom dashboard.

✅ Git State
tmail-app
✅ Commit: 22884d0 — "0.1 dashboard basic"

✅ Branch: main

✅ Remote: Emaren/tmail-app

✅ Local status: Clean

✅ VPS status: Matched and pulled

tmail-api
✅ Repo Restored: git init → fetch → checkout

✅ Branch: main

✅ Remote: Emaren/tmail-api

🟡 Status: Dirty (renamed llama-scripts → bin/, not yet committed)

✅ Ready for: Dashboard API integration

🌐 Ports & Services
Service	Port	Status	Notes
tmail-app	3009	✅ Online	Next.js frontend (Dashboard)
tmail-api	8009	✅ Online	Flask API serving /api/stats
track_server.py	8010	✅ Online	Pixel tracking server + open_log.txt appender
track.tokentap.ca	HTTPS	✅ Working	Nginx → port 8010 (pixel URL endpoint)

All apps managed by PM2 using ecosystem.config.js.
HTTPS via Let’s Encrypt, reverse proxy handled by Nginx.

🧱 Current Feature Work
🎯 Focus: DashboardPage in tmail-app

plaintext
Copy
Edit
<DashboardPage>
  ├─ <StatCard />
  ├─ <ChartCard>
  │    ├─ <OpensPerUserChart />    ← planned
  │    └─ <OpensOverTimeChart />   ← planned
  ├─ <PlaceholderTable />          ← replace w/ recent opens
  └─ AI Agent Toggle               ← future: <AgentChat />
📌 Next Steps
✅ Confirm /api/stats working and served from tmail-api

🔜 Implement /api/logs to return recent pixel open records

🔜 Parse and deduplicate entries from open_log.txt

🔜 Populate <StatCard /> with live API metrics

🔜 Replace placeholders with <OpensOverTimeChart />, <OpensPerUserChart />, and real table

🔜 Finalize llama-scripts → bin/ rename and commit

🔜 Add localStorage support for agent toggle (future)

📈 Runtime Notes
useStats.ts fetches GET /api/stats every 10s via NEXT_PUBLIC_API_URL

Polling is light: zero strain on CPU/memory

Pixel events from https://track.tokentap.ca/track?id=... are being logged correctly

Logs confirmed active in PM2: 🎯 Incoming Request and 🎯 Pixel Tracked events appear regularly

System is safe to run 24/7, extremely low-resource (RAM usage ~30MB)

📁 Directory Structure Preview
bash
Copy
Edit
projects/
├── tmail-app/
│   └── app/
│       └── dashboard/
│           └── page.tsx         ← Current focus
├── tmail-api/
│   ├── bin/                     ← Formerly llama-scripts
│   ├── track_server.py          ← Pixel + log API server
│   ├── open_log.txt             ← Append-only read log
│   └── app.py                   ← Stats API `/api/stats`
✅ Changes Made
🟢 Additions:
Added port 8010 reverse proxy via Nginx → track.tokentap.ca

Integrated track_server.py with logging and pixel serve logic

PM2 ecosystem.config.js updated: correct cwd, watch: false, Bash interpreter

Live pixel URL confirmed: https://track.tokentap.ca/track?id=ping

Frontend now polls /api/stats via useStats.ts

🟡 Changes:
Updated llama-scripts/ → bin/ note (rename pending commit)

Clarified runtime logging behavior in track_server.py + app.py

🔴 Removed:
Nothing removed — only expanded and clarified existing project details