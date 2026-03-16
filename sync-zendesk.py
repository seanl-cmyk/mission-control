#!/usr/bin/env python3
"""
Sync Zendesk tickets to Mission Control dashboard.
Fetches all tickets assigned to Sean and updates index.html with accurate counts.
"""

import json
import subprocess
import os
import re
from datetime import datetime

def run_mcporter(query):
    """Run mcporter zendesk search and return results."""
    env = os.environ.copy()
    env['ZENDESK_MCP_TOKEN'] = os.getenv('ZENDESK_MCP_TOKEN', '')
    
    result = subprocess.run(
        ['mcporter', 'call', 'zendesk.search', f'query={query}', 'per_page=100'],
        capture_output=True, text=True, env=env
    )
    
    if result.returncode != 0:
        print(f"Error running mcporter: {result.stderr}")
        return []
    
    try:
        data = json.loads(result.stdout)
        return data.get('results', [])
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {result.stdout[:200]}")
        return []

def get_ticket_counts():
    """Get ticket counts by status."""
    counts = {}
    for status in ['open', 'pending', 'hold']:
        env = os.environ.copy()
        env['ZENDESK_MCP_TOKEN'] = os.getenv('ZENDESK_MCP_TOKEN', '')
        
        result = subprocess.run(
            ['mcporter', 'call', 'zendesk.search_count', f'query=type:ticket assignee:sean status:{status}'],
            capture_output=True, text=True, env=env
        )
        
        try:
            data = json.loads(result.stdout)
            counts[status] = data.get('count', 0)
        except:
            counts[status] = 0
    
    return counts

def fetch_zendesk_tickets():
    """Fetch all tickets assigned to Sean that aren't solved/closed."""
    tickets = run_mcporter("type:ticket assignee:sean status<solved")
    
    formatted = []
    for t in tickets:
        formatted.append({
            "id": t.get("id"),
            "subject": t.get("subject", "")[:80],
            "status": t.get("status", "open"),
            "priority": t.get("priority", "normal"),
            "customer": "",  # Would need org lookup
            "category": "voice",  # Default
            "created_at": t.get("created_at", ""),
            "updated_at": t.get("updated_at", "")
        })
    
    return formatted

def update_index_html(tickets, counts):
    """Update the zendeskTickets array in index.html."""
    index_path = os.path.expanduser("~/mission-control/index.html")
    
    with open(index_path, 'r') as f:
        content = f.read()
    
    # Build new tickets array
    tickets_js = "    // Zendesk tickets from query (will be merged with cases.json)\n"
    tickets_js += "    const zendeskTickets = [\n"
    
    for i, t in enumerate(tickets):
        tickets_js += f"""      {{
        id: {t['id']},
        subject: "{t['subject'].replace('"', '\\"')}",
        status: "{t['status']}",
        priority: "{t['priority'] or 'normal'}",
        customer: "{t['customer']}",
        category: "{t['category']}",
        created_at: "{t['created_at']}",
        updated_at: "{t['updated_at']}"
      }}"""
        if i < len(tickets) - 1:
            tickets_js += ","
        tickets_js += "\n"
    
    tickets_js += "    ];\n"
    
    # Replace the zendeskTickets array
    pattern = r'    // Zendesk tickets from query.*?const zendeskTickets = \[.*?\];\n'
    content = re.sub(pattern, tickets_js, content, flags=re.DOTALL)
    
    with open(index_path, 'w') as f:
        f.write(content)
    
    print(f"Updated index.html with {len(tickets)} tickets")
    print(f"Counts: Open={counts.get('open',0)}, Pending={counts.get('pending',0)}, Hold={counts.get('hold',0)}")

def main():
    print(f"Syncing Zendesk tickets at {datetime.now().isoformat()}")
    
    # Load env vars
    env_path = os.path.expanduser("~/.openclaw/workspace/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    os.environ[key] = val.strip('"').strip("'")
    
    counts = get_ticket_counts()
    tickets = fetch_zendesk_tickets()
    
    if tickets:
        update_index_html(tickets, counts)
        print("Done!")
    else:
        print("No tickets found or error fetching")

if __name__ == "__main__":
    main()
