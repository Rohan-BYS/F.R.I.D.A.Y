---
name: whatsapp_messaging
description: Send and manage WhatsApp messages and bulk campaigns using the open-whatsapp MCP server.
category: automation
---

# WhatsApp Automation Skill

## Overview
F.R.I.D.A.Y. can interact with WhatsApp via the `open-whatsapp` MCP server, which interfaces with the `@open-wa/wa-automate-nodejs` library. This server is already configured in `mcp_servers.json`.

## Capabilities (MCP Tools)
The following tools are automatically loaded by the MCP Hub and available to F.R.I.D.A.Y.:

1. **`send_whatsapp_message(phone: str, message: str, typingDelaySeconds: int)`**: 
   - Sends a single direct message to a user.
   - Includes simulated human typing to prevent bans.
   
2. **`start_bulk_campaign(contactsPath: str, template: str, ...)`**: 
   - Initiates a background broadcast campaign from a CSV file (e.g., `contacts_sample.csv`).
   - Supports anti-ban safeguards: jitter pacing, batch resting, and spintax (`{Hi|Hello}`).

3. **`get_campaign_status()`**: 
   - Returns real-time progress (sent, failed, remaining).

4. **`pause_campaign()`**: 
   - Gracefully pauses an ongoing campaign.

5. **`get_whatsapp_status()`**: 
   - Checks if the WhatsApp session is connected or awaiting QR login.

## Usage Guidelines
- Always verify the WhatsApp status using `get_whatsapp_status()` before attempting to send messages. If it's awaiting login, the user must run `npm start` in `C:\Users\U1\Desktop\open-whatsapp-mcp` to scan the QR code.
- When sending a single message, use `send_whatsapp_message`.
- Ensure phone numbers include the country code without the '+' (e.g., `919876543210`).
- For bulk marketing, format a CSV and use `start_bulk_campaign` rather than looping `send_whatsapp_message` to leverage built-in anti-ban protections.

## Upstream Project & Latest Updates
The backend is powered by [open-wa/wa-automate-nodejs](https://github.com/open-wa/wa-automate-nodejs). It is an unofficial automation wrapper and is subject to WhatsApp's anti-spam algorithms, hence the reliance on built-in jitter and typing simulation.

### Versioning Context
- **v4 (Current Stable):** The stable branch (e.g., 4.76.0) recommended for mature production systems. 
- **v5 (Alpha):** The project is transitioning to a v5 monorepo architecture, intended for fresh projects and testing new features. Keep production systems on v4.

### Documentation & APIs
- **Official Docs:** https://docs.openwa.dev/
- **Easy API / Webhooks:** The core library also supports an "Easy API" mode which spins up local endpoints. If F.R.I.D.A.Y. ever runs the engine standalone (outside of the MCP Server), the interactive Swagger documentation can be accessed locally at `http://localhost:8080/api-docs/`.
