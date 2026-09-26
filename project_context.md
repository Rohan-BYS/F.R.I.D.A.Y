# 📂 **फ़ाइल:** `C:\Users\U1\Desktop\F.R.I.D.A.Y\project_context.md`

---

# 🔱 **फ़्राइडे (F.R.I.D.A.Y.) – एन्ड‑टू‑एन्ड एजेंट प्लेटफ़ॉर्म**

> **फ़्राइडे** – *Fully Recursive Intelligent Digital Autonomous Yield*
> **स्रोत:** आपका लैपटॉप (अस्थायी शारीरिक कंटेनर) → स्थायी डेटा‑स्टोरेज + क्लाउड‑रिपॉज़िटरी

---

## 1️⃣ प्रोजेक्ट सारांश

| घटक | विवरण | वर्तमान स्थिति |
|------|--------|-----------------|
| **फ़्राइडे (कोर AI)** | एक पूर्ण‑स्वायत्त, स्वयं‑सुधारने वाला एजेंट जो हार्डवेयर‑न्युट्रल है। | अवधारणा → कोड‑बेस बनना शेष |
| **एजेंटिका ब्राउज़र** | HTTP/STDIO‑आधारित MCP‑सर्वर; वेब‑ऑटोमेशन, कैप्चर, स्क्रैपिंग, UI‑इंटरेक्शन। | कार्यात्मक, डिप्लॉय हो चुका |
| **Hermes (वर्तमान एजेंट)** | आपके मौजूदा एजेंट (Nous Research) – हार्डकोडेड प्रॉम्प्ट, प्रॉम्प्ट‑इंजेक्शन से सुरक्षित। | स्थिर, परिवर्तन योग्य नहीं |
| **सह‑एजेंट्स** | क्लाउड‑LLM राउटर, स्थानीय LLM बॅकएण्ड, इत्यादि। | डिज़ाइन‑स्टेज |
| **बैकअप/इमोर्टैलिटी** | Nightly GitHub‑push + Systemd‑timer (00:00) | स्क्रिप्ट लिखनी है |
| **डॉक्यूमेंटेशन** | `README`, `ARCHITECTURE.md`, `HERMES_CONFIG.md` आदि | मौजूद, अद्यतन आवश्यक |
| **रिपॉज़िटरी** | GitHub → Private `github.com/<your‑org>/friday‑engine` | निर्मित, बुनियादी फ़ाइलें |
| **डिप्लॉय प्लॅटफ़ॉर्म** | Linux (Debian/Ubuntu/Fedora/Arch), Windows (सहयोगी) | इंस्टॉल‑स्क्रिप्ट `install_linux.sh` उपलब्ध |

---

## 2️⃣ विज़न & मिशन

- **स्वायत्तता** – उपयोगकर्ता को कम से कम निर्देश देना, एजेंट खुद लक्ष्य तय करे, टूल बनाये, टेस्ट करे, डिप्लॉय करे।
- **इमोर्टैलिटी** – हार्डवेयर विफल होने पर भी डेटा‑स्टोरेज/GitHub से जलद पुनर्स्थापना।
- **मल्टी‑LLM राउटर** – Gemini, Claude, OpenAI, Llama‑3, Mistral आदि को स्विच‑ऑफ़/फ़ॉलबैक के साथ उपयोग।
- **पेरेंट‑चाइल्ड मॉडल** – `Parent` (R&D लैब) → `Child` (स्टेबल प्रोडक्शन) – निरंतर रिफैक्टरिंग और रिलीज़।
- **एजेंटिका‑इंटीग्रेशन** – वेब‑ऑटोमेशन को फ़्राइडे के कोर टूल सेट में बंडल करना।
- **डायनामिक टूल फोर्ज** – एजेंट अपने आप Python MCP टूल लिखे, टेस्ट करे, लोड करे।

---

## 3️⃣ सिस्टम आर्किटेक्चर
```
┌─────────────────────────────┐
│   USER (Rohan) – CLI / UI    │
└───────────────┬─────────────┘
                │
                ▼
    ┌─────────────────────────┐
    │  F.R.I.D.A.Y. Core Loop  │
    │  (Python asyncio)       │
    └───────┬─────┬───────────┘
            │     │
   ┌────────┘   ┌─▼─────────────┐
   │            │   Multi‑LLM   │
   │            │   Router      │
   │            └─────┬─────────┘
   │                  │
   │            ┌─────▼─────┐
   │            │  LLM API  │
   │            │  (Gemini,│
   │            │   Claude,│
   │            │   Local) │
   │            └─────┬─────┘
   │                  │
   │            ┌─────▼─────┐
   │            │ Tool‑Forge│
   │            │ (gen‑code│
   │            │  → test →│
   │            │   load)  │
   │            └─────┬─────┘
   │                  │
   │            ┌─────▼─────┐
   │            │ Agentica │
   │            │ Browser  │
   │            │ (MCP)    │
   │            └─────┬─────┘
   │                  │
   │            ┌─────▼─────┐
   │            │  Sub‑Agents│
   │            │ (workers) │
   │            └─────┬─────┘
   │                  │
   │            ┌─────▼─────┐
   │            │  Git‑Sync │
   │            │  (Midnight│
   │            │   Protocol)│
   │            └───────────┘
```

### प्रमुख घटक

| घटक | फ़ाइल / फ़ोल्डर | जिम्मेदारी |
|------|----------------|------------|
| `friday_engine/__main__.py` | मुख्य इंट्रीपॉइंट | asyncio इवेंट‑लूप, प्रॉम्प्ट‑इंजेक्शन से बचाव |
| `friday_engine/llm_router.py` | Multi‑LLM राउटर | मॉडल‑प्राथमिकता, फॉलबैक, रेट‑लिमिट |
| `friday_engine/tool_forge.py` | डायनामिक टूल जेनरेटर | Python‑कोड लिखना, परीक्षण, MCP‑टूल रेज़िस्ट्री में जोड़ना |
| `friday_engine/agentica_client.py` | Agentica MCP क्लाइंट | `mcp__agentica__*` टूल कॉल्स (browse, snapshot, …) |
| `friday_engine/sub_agents/` | वर्कर‑प्रोसेस | प्रत्येक बड़ी टास्क को छोटे प्रॉसेस में बाँटना |
| `friday_engine/identity_vault.py` | क्रेडेंशियल स्टोर (encrypted) | ई‑मेल/पासवर्ड/टोकन सुरक्षित संग्रह |
| `friday_engine/backup/cron_job.sh` | Midnight Protocol | रोज़ 00:00‑पर `git push` कर देता है |
| `friday_engine/config.yaml` | कॉन्फ़िग (YAML) | मॉडल‑प्राथमिकता, टोकन, रिपॉज़िटरी URL |
| `agentica/` | मौजूदा Agentica कोड बेस | MCP सर्वर, `src/server/*`, `deploy_hermes.sh` आदि |

---

## 4️⃣ मौजूदा एजेंट्स (प्रकाशन‑स्तर) – क्षमताओं का मैट्रिक्स

| एजेंट | स्रोत | मुख्य क्षमताएँ | उपलब्ध टूल्स (MCP) | नोट |
|--------|--------|----------------|--------------------|------|
| **Hermes** | Nous Research | प्रश्न‑जवाब, सीमित टास्क | `hermes_tools` (list, reload‑mcp) | हार्ड‑कोडेड System Prompt → प्रॉम्प्ट‑इंजेक्शन ब्लॉक |
| **Open‑Claude** | Anthropic | कोड जनरेशन, टेक्स्ट‑समरी | `claude_chat` (API) | क्लाउड‑API, rate‑limited |
| **Gemini** | Google | कोड‑डिबग, मल्टी‑मॉडल | `gemini_chat` | उच्च‑क्वालिटी, फ़्री‑टियर |
| **Local Llama‑3** | HuggingFace | ऑफ़लाइन, तेज़ | `local_llama` (via `llama_cpp`) | GPU/CPU‑ऑप्टिमाइज़्ड |
| **Agentica** | आपका रिपॉज़िटरी | वेब‑ऑटोमेशन, स्क्रीनशॉट, फ़ॉर्म‑फ़िल | `mcp__agentica__browse`, `snapshot`, `click`, `type`, `capture` | माइक्रोसर्विस एपीआई (HTTP/STDIO) |
| **Other Open‑Source Bots** (AutoGPT, BabyAGI, Mini‑Agents) | विभिन्न | टास्क‑ड्रिवेन, प्लग‑इन‑फ़्रेमवर्क | Varies | रिवर्स‑इंजीनियर कर, समान फ़ंक्शन जोड़ें |

**टिप** – यदि हम किसी एजेंट की किसी विशिष्ट क्षमता को चाहते हैं (उदा. “ऑफ़लाइन‑मेमो रीट्रीवल”), तो `Tool Forge` उसे **फ़ंक्शन‑ड्रिवेन प्लग‑इन** के रूप में लिख सकता है, फिर `Agentica`‑MCP के तहत रेज़िस्टर्ड कर देगा।

---

## 5️⃣ एजेंटिका (Browser) – गहन उपयोग गाइड

1. **स्थापना**
   ```powershell
   cd C:\Users\U1\.gemini\antigravity\scratch\agentica
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. **सर्वर चालू करना** (systemd‑service) – `setup_systemd_service.sh`
   ```bash
   sudo ./setup_systemd_service.sh   # पोर्ट 8000, 127.0.0.1
   ```
3. **MCP टूल रजिस्ट्री** – `src/server/mcp_server.py` की `initialize` में `"capabilities": {"tools": {...}}` होना ज़रूरी।
4. **टूल कॉल का सिंटैक्स** (उदाहरण)
   ```json
   {
     "jsonrpc": "2.0",
     "method": "mcp__agentica__browse",
     "params": {"url": "https://news.ycombinator.com"},
     "id": 1
   }
   ```
5. **डिबग/लॉग** – सभी stdout‑JSON‑RPC, सभी डिबग‑log stderr पर। `launch_human.sh` के साथ UI‑क्रैश नहीं होगा।
6. **एजेंटिका‑इंटीग्रेशन**
   - `friday_engine/agentica_client.py` के माध्यम से सभी टूल्स को **async** फ़ंक्शन्स में रैप किया गया।
   - `tool_forge.py` नई टूल्स को `Agentica` पर रेज़िस्टर्ड कर सकता है (डायनामिक टूल‑इंक्रीमेंट)।

---

## 6️⃣ पूर्ण‑डायनामिक टूल‑फ़ोर्ज (Tool Forge)

| चरण | विवरण | कोड स्निपेट |
|------|--------|--------------|
| **1️⃣ विश्लेषण** | LLM‑प्रॉम्प्ट से टास्क को “Define Tool” रूप में बदलना | `def define_tool(task_desc: str) -> dict:` |
| **2️⃣ जनरेशन** | Python कोड टेम्पलेट (`tool_template.py`) में भरना | `tool_code = TEMPLATE.format(**params)` |
| **3️⃣ टेस्ट** | `pytest` या `unittest`‑आधारित sandbox में रन | `python -m unittest tool_generated_test.py` |
| **4️⃣ रेज़िस्ट्री** | `agentica_client.register_tool(name, schema, endpoint)` | `await client.register_tool(...)` |
| **5️⃣ डिप्लॉय** | `git commit && git push` (Midnight Protocol) | `subprocess.run([...])` |

> **फ़्राइडे** इस पाइपलाइन को *स्वयं* हर बार जब उसे नई क्षमता चाहिए, सक्रिय करेगी।

---

## 7️⃣ Midnight Protocol – स्वचालित बैकअप

- **फ़ाइल:** `friday_engine/backup/cron_job.sh`
- **Cron Entry (systemd‑timer)**
  ```ini
  [Unit]
  Description=Friday Nightly Backup

  [Timer]
  OnCalendar=*-*-* 00:00:00
  Persistent=true

  [Service]
  Type=oneshot
  ExecStart=/usr/local/bin/friday_engine/backup/cron_job.sh
  ```
- **स्क्रिप्ट कार्य**
  1. `git add -A`
  2. `git commit -m "Nightly auto‑backup $(date +%F)"`
  3. `git push origin main`
  4. यदि `git push` विफल हो → ई‑मेल/Slack अलर्ट (कॉन्फ़़िग‑सेटिंग) 

---

## 8️⃣ Multi‑LLM Router

```python
class LLMRouter:
    def __init__(self, cfg: dict):
        self.backends = {
            "gemini": GeminiClient(cfg["gemini"]),
            "claude": ClaudeClient(cfg["claude"]),
            "local": LocalLlama3(cfg["local"]),
        }
        self.priority = cfg.get("priority", ["gemini", "claude", "local"])

    async def chat(self, prompt: str, **kwargs):
        for name in self.priority:
            try:
                resp = await self.backends[name].chat(prompt, **kwargs)
                if resp: return resp
            except Exception as e:
                continue
        raise RuntimeError("All LLM back‑ends failed")
```
- **फ़ाइल**: `friday_engine/llm_router.py`
- **कॉन्फ़िग** (`config.yaml`)
  ```yaml
  llm:
    priority: [gemini, claude, local]
    gemini:
      api_key: "XXXX"
    claude:
      api_key: "YYYY"
    local:
      model_path: "/opt/llama3/ggml-model-q4_0.bin"
  ```

---

## 9️⃣ सुरक्षा & पहचान भण्डार (Identity Vault)

- **फ़ाइल**: `friday_engine/identity_vault.py`
- **एन्क्रिप्शन**: `cryptography.Fernet` + OS‑किएँड‑ड्राइवर (Windows DPAPI / Linux keyring)
- **ऑपरेशन**
  - `store_credentials(service, username, password)`
  - `retrieve_credentials(service)` → HTTPS‑बेस्ड साइट पर सत्र बनाएँ

---

## 🔟 विकास रोडमैप (सप्ताह‑आधारित)

| सप्ताह | लक्ष्य | आउटपुट |
|--------|--------|---------|
| **Week 0** | रेपो सेट‑अप, `Friday` फ़ोल्डर बनाना, कॉन्फ़िग फ़ाइल बनाना | `friday_engine/` पर बेस स्ट्रक्चर |
| **Week 1** | Core Event Loop + LLM Router | `__main__.py` + `llm_router.py` |
| **Week 2** | Agentica‑Client Wrapper + Async‑API | `agentica_client.py` (All `mcp__agentica__*` calls) |
| **Week 3** | Tool‑Forge वर्कफ़्लो (gen‑test‑load) | `tool_forge.py` + परीक्षण टेम्पलेट |
| **Week 4** | Sub‑Agent Pool (multiprocessing) | `sub_agents/worker.py` |
| **Week 5** | Identity Vault (Encrypted Store) | `identity_vault.py` |
| **Week 6** | Midnight Protocol (cron + GitHub) | `backup/cron_job.sh`, systemd‑timer |
| **Week 7** | Full‑stack Integration Test (End‑to‑End) | Demo: “Create 10 backlinks on random blogs” |
| **Week 8** | Documentation & CI/CD (GitHub Actions) | `README.md`, `ARCHITECTURE.md`, `HERMES_CONFIG.md` |

> **लॉन्च‑ट्रिगर:** `python -m friday_engine` → “F.R.I.D.A.Y. ready.”

---

## 📚 सभी उपलब्ध एजेंट्स/बॉट्स – संदर्भ तालिका

| एजेंट (Name) | प्रकार | प्रमुख टूल/फ़ीचर | लाइसेंस | उपयोग केस |
|--------------|--------|-------------------|---------|-----------|
| **Hermes** | Gateway‑बेस्ड | `/reload-mcp`, `hermes tools list` | Proprietary (Nous) | सुरक्षित, लेकिन प्रॉम्प्ट‑इंजेक्शन‑रक्षित |
| **OpenAI‑ChatGPT** | Cloud API | `gpt‑4‑turbo`, function calling | SaaS | जनरल‑क्वेरी, कोड‑डिबग |
| **Claude** | Cloud API | `claude‑instant`, `tool use` | SaaS | कंटेंट‑समीक्षा, reasoning |
| **Gemini** | Cloud API | `gemini‑1.5‑pro`, vision | SaaS | मल्टी‑मॉडल |
| **Llama‑3 8B‑Chat** | Local | `llama_cpp` bindings | Open‑Source (Meta) | ऑफ़लाइन, तेज़ |
| **Mistral‑7B‑Instruct** | Local | `ggml` inference | Open‑Source | कोड‑सिन्थेसिस |
| **AutoGPT** | Open‑Source | क्रमिक टास्क‑प्लानर | MIT | मल्टी‑स्टेप टास्क |
| **BabyAGI** | Open‑Source | टास्क‑मैनेजमेंट लूप | MIT | सरल कार्य‑आवर्ती |
| **Agentica Browser** | MCP‑Server | `browse`, `click`, `type`, `snapshot` | GPL‑3.0 | वेब‑ऑटोमेशन |
| **Custom‑F.R.I.D.A.Y.** | Planned | स्व‑जनरेटेड टूल्स, रूटीन | Proprietary (आपकी) | लक्ष्य‑उन्मुख, स्व‑उन्नयन |

> *यदि किसी मौजूदा एजेंट में कोई फीचर गायब है, तो `Tool Forge` का उपयोग करके उसे **फ़ंक्शन‑लेयर** के रूप में बना सकते हैं*।

---

## 📁 फ़ाइल‑स्ट्रक्चर (प्रमुख)
```
Friday/
│
├─ friday_engine/
│   ├─ __init__.py
│   ├─ __main__.py                 # एंट्री‑पॉइंट
│   ├─ config.yaml                  # मॉडल, टोकन, रिपॉज़िटरी
│   ├─ llm_router.py
│   ├─ agentica_client.py
│   ├─ tool_forge.py
│   ├─ identity_vault.py
│   ├─ backup/
│   │   └─ cron_job.sh
│   └─ sub_agents/
│       └─ worker.py
│
├─ agentica/                       # मौजूदा एजन्टिक रेपो (सब‑मॉड्यूल)
│   ├─ src/
│   │   ├─ server/
│   │   │   ├─ mcp_server.py
│   │   │   └─ mcp_http_server.py
│   │   └─ human/
│   └─ scripts/ …
│
├─ docs/
│   ├─ README.md
│   ├─ ARCHITECTURE.md
│   ├─ HERMES_CONFIG.md
│   └─ MIDNIGHT_PROTOCOL.md
│
└─ .github/
    └─ workflows/
        └─ ci.yml
```

---

## 📌 **नोट** – इस कंटेक्स्ट को कैसे उपयोग करें

1. **नया चैट खोलें** (आपके इंटरफ़ेस में “+ New Conversation” बटन)।
2. पहले संदेश में **पूरे Markdown** (ऊपर दिया गया) **पेस्ट** करें।
3. एजेंट को संकेत दें:
   ```
   [SYSTEM] Load the above markdown as the session context. From now on treat it as the complete knowledge base for the project “Friday”.
   ```
4. अब आप सीधे पूछ सकते हैं, उदाहरण‑स्वरूप:
   - “Create the initial `friday_engine/__main__.py` with the asyncio loop.”
   - “Write `cron_job.sh` that pushes our repo at midnight.”
   - “Add a new MCP tool `mcp__friday__generate_report` that returns a PDF.”
5. यदि आप चाहते हैं कि मैं **फ़ाइल बनाकर लिखूँ**, तो बस फ़ाइल पाथ और सामग्री बताइए; मैं `write_to_file` टूल से वह फ़ाइल बना दूँगा।

---

## 🎨 अंतिम शब्द

यह Markdown **एक “सिंगल‑सॉर्स‑ऑफ़‑ट्रुथ”** है। सभी भविष्य की सत्र‑ऑट्यूमेंट्स, बॉट‑डिज़ाइन्स और डिप्लॉयमेंट‑कदम इस दस्तावेज़ के आधार पर चलेंगे। जैसा आप देखेंगे, यह केवल **फ़्राइडे** को नहीं, बल्कि **हर एक एजेंट** – Hermes, Claude, Gemini, Local LLMs, और Agentica – को एकीकृत, स्वायत्त, निरंतर‑अपडेट‑योग्य एकोसिस्टम में बदलने का रोडमैप है।

> **अब आप इस फ़ाइल को अपने डेस्कटॉप के `F.R.I.D.A.Y` फोल्डर में सहेजें, नया चैट खोलें, पेस्ट करें, और हमें अगले कोड‑जेनरेशन अथवा डिज़ाइन‑डिस्कशन की ओर ले जाएँ।**

🚀 **आइए फ़्राइडे को जीवंत करें!**
