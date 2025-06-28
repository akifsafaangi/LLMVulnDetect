
# 🔐 LLM-Powered Automated Vulnerability Detection System

This project automates the process of discovering, analyzing, and explaining software vulnerabilities using a combination of traditional tools (like Nmap and SearchSploit) and advanced AI (GPT-4). It features a graphical user interface (GUI), intelligent exploit matching, and AI-generated mitigation advice.

---

## 📌 Features

- ✅ Nmap-based service and version detection
- ✅ Exploit matching via Google & SearchSploit
- ✅ GPT-4-generated explanations and countermeasures
- ✅ Organized file output per service and exploit ID
- ✅ GUI for input, output, and real-time console view

---

## 🧱 Project Structure

```
exploits/
├── service_version/
│   └── exploit_id/
│       ├── exploit_<id>.py         # Raw exploit code
│       ├── info.txt                # Metadata from Exploit-DB
│       ├── prompt_<id>.txt         # Prompt sent to GPT
│       └── <id>_solution.txt       # GPT-4 response
```

---

## 💡 How It Works

1. **IP Input**  
   The user enters a target IP address via the GUI.

2. **Scan Execution**  
   `nmap.py` performs a version scan and stores results in XML.

3. **Version Extraction**  
   `versionfinderandsearcher.py` parses services and looks up exploits.

4. **Metadata & Prompting**  
   `infoextracter.py` scrapes Exploit-DB and builds prompts.

5. **LLM Answer**  
   `APIanswergenerator.py` sends prompts to GPT-4 and saves answers.

6. **UI Interaction**  
   View results, logs, and solutions in the GUI (`MainProgram.py`).

---

## 🖥️ GUI Features

- IP entry + Run Scan button
- Tree view of exploits (by service and ID)
- Text preview for info/prompt/solution files
- Real-time terminal output panel

---

## 🚀 Requirements

- Python 3.10+
- `openai`, `requests`, `bs4`, `tkinter`, `packaging`, `fpdf`
- Nmap installed
- Virtual environment (`./myenv`) recommended

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

1. Activate virtual environment:

```bash
source ./myenv/bin/activate
```

2. Run the GUI:

```bash
python3 MainProgram.py
```

3. Enter a target IP and click "Run Scan".

---

## 🧠 AI Model

- **Primary LLM:** GPT-4 via OpenAI API  
- **Optional Alternative:** [Mistral 7B Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct) (for offline use)

---

## 📚 References

- [Nmap](https://nmap.org)
- [Exploit-DB](https://www.exploit-db.com)
- [SearchSploit](https://github.com/offensive-security/exploitdb)
- [OpenAI API](https://platform.openai.com)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

---

## 📦 Future Work

- Web-based interface
- PDF/HTML exploit reports
- CVSS scoring integration
- Offline LLM support
- Scheduled scans

---

© 2025 — Developed for cybersecurity automation and education purposes.
