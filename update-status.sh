#!/bin/bash
# Update Sensei activity status
# Usage: ./update-status.sh <state> <message> [ticketId]
# States: idle, thinking, analyzing, researching, drafting, processing

STATE="${1:-idle}"
MESSAGE="${2:-Ready}"
TICKET_ID="${3:-null}"
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ "$STATE" = "idle" ]; then
  STARTED="null"
else
  STARTED="\"$NOW\""
fi

if [ "$TICKET_ID" != "null" ]; then
  TICKET_ID="\"$TICKET_ID\""
fi

cat > /home/telnyx-user/mission-control/status.json << EOF
{
  "state": "$STATE",
  "message": "$MESSAGE",
  "ticketId": $TICKET_ID,
  "startedAt": $STARTED,
  "updatedAt": "$NOW"
}
EOF

# Push to GitHub for remote viewing
cd /home/telnyx-user/mission-control
git add status.json
git commit -m "Status: $STATE - $MESSAGE" --quiet
git push --quiet 2>/dev/null &

echo "Status updated: $STATE - $MESSAGE"
