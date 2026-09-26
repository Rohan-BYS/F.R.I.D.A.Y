# 🛡️ Hermes Agent Integration & MCP Configuration

> **Hermes Agent** (Nous Research)  
> Role in Ecosystem: Stable execution bot with hardened system prompt protection against prompt injection.

---

## 1. Overview
Hermes is deployed alongside F.R.I.D.A.Y. to handle critical, prompt-injection-sensitive tasks where system prompt immutability is required. F.R.I.D.A.Y. acts as the upstream Parent Forge that generates tools and provides them to Hermes via the Model Context Protocol (MCP).

---

## 2. Configuration & MCP Tool Exposure

Hermes interacts with external tools via standard JSON-RPC MCP calls. F.R.I.D.A.Y.'s `ToolForge` and `Agentica` expose tools that Hermes can discover and execute.

### Reloading MCP Tools in Hermes
When F.R.I.D.A.Y. completes the synthesis of a new tool via `ToolForge`:
```bash
# Triggers tool reload inside Hermes
hermes tools list
hermes tools reload-mcp
```

### Prompt-Injection Defense Architecture
Hermes enforces a strict boundary between user inputs and system instructions:
1. **Instruction Quarantine:** User queries are parsed as data payloads rather than executable system instructions.
2. **Deterministic Tool Schema:** MCP tools exposed to Hermes enforce strict JSON schema validation, discarding extraneous or malicious properties.
3. **Audit Trail:** All Hermes tool executions are logged into `logs/friday_engine.log` for continuous monitoring.
