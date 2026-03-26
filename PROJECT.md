# Mission Control Dashboard

## Overview
Personal NOC dashboard for tracking Zendesk tickets and current work status. Displays real-time activity state (working/idle/offline) and ticket queue.

## Files
| File | Purpose |
|------|---------|
| `index.html` | Main dashboard UI (dark theme, responsive) |
| `sync-zendesk.py` | Fetches tickets via mcporter, updates index.html |
| `cases.json` | Manual/historical case data |
| `status.json` | Current activity state (working/idle/offline) |
| `update-status.sh` | Updates status.json |
| `serve-local.sh` | Local dev server |
| `cors-server.py` | CORS proxy for API calls |

## Current State
- **Last sync:** 2026-03-25 23:30 UTC (EOD)
- **Status:** offline
- **Sync script:** Functional — queries Zendesk for tickets assigned to Sean, updates index.html

## How to Use
```bash
# Update status
./update-status.sh working "Investigating ticket #12345"
./update-status.sh idle
./update-status.sh offline

# Sync Zendesk tickets
source ~/.openclaw/workspace/.env
python3 sync-zendesk.py

# Local dev
./serve-local.sh
```

## TODO / Ideas
- [ ] Auto-sync via cron?
- [ ] Add wireless ticket category detection
- [ ] Customer name lookup from org data
- [ ] Hosted version (GitHub Pages?)

## Recent Changes
- 2026-03-25: End-of-day sync
- 2026-03-19: Added sync-zendesk.py script
- 2026-03-12: Initial dashboard setup

---
*Updated: 2026-03-26*
