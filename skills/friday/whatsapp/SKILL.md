---
name: whatsapp_messaging
description: Send and manage WhatsApp messages and bulk campaigns using open-whatsapp MCP server or local bridge.
category: automation
---

# WhatsApp Automation Skill

## Overview
F.R.I.D.A.Y. can interact with WhatsApp via the `open-whatsapp` MCP server or direct headless bridge powered by `@open-wa/wa-automate-nodejs`.

## Capabilities
1. `send_whatsapp_message(phone, message, typingDelaySeconds)`:
   - Sends a single direct message to a user.
   - Includes simulated human typing to prevent bans.
   
2. `start_bulk_campaign(contactsPath, template)`:
   - Initiates a background broadcast campaign from a CSV file.
   - Supports jitter pacing, batch resting, and spintax (`{Hi|Hello}`).

3. `get_campaign_status()`:
   - Returns real-time progress (sent, failed, remaining).

4. `get_whatsapp_status()`:
   - Checks if the WhatsApp session is connected or awaiting QR login.

## Usage Guidelines
- Verify WhatsApp connection state before running bulk actions.
- Ensure phone numbers include country code without '+' (e.g., `919876543210`).
- Documentation: https://docs.openwa.dev/
