import requests
from bs4 import BeautifulSoup
import os

# 1. Exploit metadata fetcher
def fetch_exploit_metadata(exploit_id):
    url = f"https://www.exploit-db.com/exploits/{exploit_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"[!] Failed to fetch exploit page: HTTP {r.status_code}")
            return None

        # Parse the HTML content
        soup = BeautifulSoup(r.text, "html.parser")
        meta = {
            "EDB-ID": str(exploit_id),
            "CVE": None,
            "Author": None,
            "Type": None,
            "Platform": None,
            "Date": None,
            "Title": None
        }

        # Extract metadata
        title_tag = soup.find("title")
        if title_tag:
            meta["Title"] = title_tag.text.strip().replace(" - Exploit Database", "")

        cve = soup.find("a", href=lambda x: x and "CVE" in x)
        if cve:
            meta["CVE"] = cve.text.strip()

        author = soup.find("meta", attrs={"name": "author"})
        if author:
            meta["Author"] = author.get("content", "").strip()

        pub = soup.find("meta", attrs={"property": "article:published_time"})
        if pub:
            meta["Date"] = pub.get("content", "").strip()

        # Extract type, platform, and author from the stats section
        blocks = soup.find_all("div", class_="col-6 text-center")
        for b in blocks:
            title = b.find("h4", class_="info-title")
            value = b.find("h6", class_="stats-title")
            if not title or not value:
                continue
            label = title.text.strip().lower()
            val = value.text.strip()
            if label == "type:":
                meta["Type"] = val
            elif label == "platform:":
                meta["Platform"] = val
            elif label == "author:" and not meta["Author"]:
                meta["Author"] = val
            elif label == "date:" and not meta["Date"]:
                meta["Date"] = val

        return meta
    except Exception as e:
        print(f"[!] Error fetching metadata: {e}")
        return None

# 2. Download exploit file
def download_exploit_file(exploit_id):
    url = f"https://www.exploit-db.com/download/{exploit_id}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            print(f"[!] Failed to download .py for {exploit_id}: HTTP {r.status_code}")
    except Exception as e:
        print(f"[!] Error downloading file: {e}")
    return None

# 3. Generate prompt text
def generate_prompt(metadata, code):
    return f"""Exploit Title: {metadata.get("Title", "Unknown")}
EDB-ID: {metadata.get("EDB-ID")}
CVE: {metadata.get("CVE") or "N/A"}
Platform: {metadata.get("Platform") or "Unknown"}
Type: {metadata.get("Type") or "Unknown"}
Date: {metadata.get("Date") or "Unknown"}
Author: {metadata.get("Author") or "Unknown"}

Exploit Code:
{code}

---

🛡️ Please answer the following questions as a cybersecurity expert:

1. What are the conditions required on the target system for this vulnerability to be exploitable?
2. What is the technical mechanism or logic behind this vulnerability?
3. What are the potential impacts if the exploit is successfully executed?
4. ✅ What are effective mitigation steps or security recommendations for system administrators to neutralize or prevent this vulnerability?

Your response should be clear, technical, and include actionable solutions.
"""

# 4. Create exploit folder and files
def process_exploit_id(exploit_id, service_name):
    service_folder = service_name.replace(" ", "_").replace("/", "_")
    base_folder = os.path.join("exploits", service_folder, str(exploit_id))
    os.makedirs(base_folder, exist_ok=True)

    meta = fetch_exploit_metadata(exploit_id)
    if not meta:
        return

    code = download_exploit_file(exploit_id)
    if not code:
        return

    # info.txt yaz
    with open(os.path.join(base_folder, "info.txt"), "w", encoding="utf-8") as f:
        for key, val in meta.items():
            f.write(f"{key}: {val or 'N/A'}\n")

    # exploit kodu yaz
    with open(os.path.join(base_folder, f"exploit_{exploit_id}.py"), "w", encoding="utf-8") as f:
        f.write(code)

    # prompt dosyası yaz
    prompt_text = generate_prompt(meta, code)
    with open(os.path.join(base_folder, f"prompt_{exploit_id}.txt"), "w", encoding="utf-8") as f:
        f.write(prompt_text)

    print(f"[✓] {exploit_id} klasörü ve dosyaları oluşturuldu → {service_folder}")

# 5. Batch process from map file
def batch_process_from_map_file(file="exploit_map.txt"):
    if not os.path.exists(file):
        print(f"[!] File not found: {file}")
        return
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 2:
                continue
            eid, service = parts
            if eid.isdigit():
                process_exploit_id(eid.strip(), service.strip())

if __name__ == "__main__":
    batch_process_from_map_file("exploit_map.txt")

