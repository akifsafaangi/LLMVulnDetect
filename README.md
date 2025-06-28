
# 🔐 LLM-Powered Automated Vulnerability Detection System

This project automates the process of discovering, analyzing, and explaining software vulnerabilities using a combination of traditional tools (like Nmap and SearchSploit) and advanced AI (GPT-4). It features a graphical user interface (GUI), intelligent exploit matching, and AI-generated mitigation advice.

---

## 📖 Project Description

This system scans a given target IP using Nmap, extracts services and versions, searches for matching exploits in Exploit-DB and SearchSploit, and generates a solution for each exploit using GPT-4. The results are displayed in a GUI with tree navigation and text previews.

---

## 🛠️ Installation Instructions

1. Clone the repository.
2. Create and activate a virtual environment:
```bash
python3 -m venv myenv
source myenv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Ensure `nmap` is installed and accessible from your shell.

---

## ▶️ Usage

Start the GUI:

```bash
python3 MainProgram.py
```

Enter a target IP (e.g., `192.168.56.101`) and click "Run Scan".  
Results will be stored in `exploits/{service}_{version}/{exploit_id}/`.

---

## 🧩 Troubleshooting

- **Error: 'nmap' not found** → Make sure Nmap is installed and added to system PATH.
- **Permission Denied** → Run with appropriate permissions.
- **API Key Error** → Ensure your OpenAI API key is correctly set in `APIanswergenerator.py`.
- **Rate Limits** → Google search may return 429; consider using a proxy or SerpAPI.

---

## 📁 File Overview

| File Name                | Purpose                                                  | Key Functions/Classes               |
|-------------------------|----------------------------------------------------------|-------------------------------------|
| `MainProgram.py`        | GUI interface for scanning and viewing results           | `ExploitViewer` (Tkinter GUI)       |
| `nmap.py`               | Runs Nmap on given IP and saves results as XML           | `run_nmap()`                        |
| `versionfinderandsearcher.py` | Extracts service versions and finds related exploits     | `extract_services_from_nmap()`, `searchsploit_links()` |
| `infoextracter.py`      | Scrapes metadata and downloads exploit code              | `fetch_exploit_metadata()`, `download_exploit_file()` |
| `APIanswergenerator.py` | Sends exploit prompt to GPT-4 and saves explanation      | `generate_solution_from_prompt()`   |
| `exploit_links_*.txt`   | Stores found exploit links from Google/SearchSploit      | N/A                                 |
| `exploits/`             | Main output folder for all results                       | N/A                                 |
| `exploit_map.txt`       | Maps services to their corresponding exploit IDs         | N/A                                 |
| `requirements.txt`      | Python dependency file                                   | N/A                                 |

---

## 🖥️ GUI Features

- Target IP input + Start Scan button
- Exploit tree view by service and ID
- Text area for displaying file content
- Console output panel for log/debug information

---

## 📦 Project Structure

```
exploits/
├── vsftpd_2.3.4/
│   └── 49757/
│       ├── exploit_49757.py
│       ├── info.txt
│       ├── prompt_49757.txt
│       └── 49757_solution.txt
```

---

## 🧠 AI Model

- **Main Model:** GPT-4 (OpenAI API)

---

## 🤝 Acknowledgements

- **Course:** Network And Information Security (2025)
- **Instructor:** Dr. Salih Sarp
- **Collaborators:** ChatGPT by OpenAI and tools like Nmap, Exploit-DB, SearchSploit

---

## 📚 References

- [Nmap](https://nmap.org)
- [Exploit-DB](https://www.exploit-db.com)
- [SearchSploit](https://github.com/offensive-security/exploitdb)
- [OpenAI API](https://platform.openai.com)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
