import xml.etree.ElementTree as ET
from googlesearch import search
import subprocess
import time
import requests
from bs4 import BeautifulSoup
import re
from packaging import version

# versionfinderandsearcher.py
def version_matches(service_name, page_text):
    page_text = page_text.lower()
    # Split the service name into parts
    name_parts = service_name.lower().split()

    if len(name_parts) < 2:
        return False

    product = " ".join(name_parts[:-1])
    v_str = name_parts[-1]

    if product not in page_text:
        return False

    try:
        ver = version.parse(v_str)
    except:
        return False

    # Define regex patterns for version matching
    patterns = [
        (r"<\s*([0-9]+\.[0-9]+\.[0-9]+)", lambda x: ver < version.parse(x)),
        (r"<=\s*([0-9]+\.[0-9]+\.[0-9]+)", lambda x: ver <= version.parse(x)),
        (r">=\s*([0-9]+\.[0-9]+\.[0-9]+)", lambda x: ver >= version.parse(x)),
        (r">\s*([0-9]+\.[0-9]+\.[0-9]+)", lambda x: ver > version.parse(x)),
        (r"\b([0-9]+\.[0-9]+)\.x\b", lambda x: v_str.startswith(x)),
    ]

    # Check for exact version match
    for pattern, comparator in patterns:
        matches = re.findall(pattern, page_text)
        for match in matches:
            try:
                if comparator(match):
                    return True
            except:
                continue

    return service_name.lower() in page_text

# Extracts services from Nmap XML output
def extract_services_from_nmap(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    services = []

    for port in root.findall(".//port"):
        service = port.find("service")
        if service is None:
            continue

        product = service.get("product")
        version_str = service.get("version")
        extrainfo = service.get("extrainfo")

        if product and version_str:
            services.append(f"{product} {version_str}")
        elif product and extrainfo:
            services.append(f"{product} {extrainfo}")

    return list(set(services))

# Searches Google for exploit links related to the service name
def google_search_exploit_links(service_name, max_results=3):
    headers = {"User-Agent": "Mozilla/5.0"}
    valid_links = []

    try:
        for url in search(f"{service_name} exploit site:exploit-db.com", num_results=max_results):
            if not re.match(r"^https?://(www\.)?exploit-db\.com/exploits/\d+/?$", url):
                continue
            try:
                # Fetch the page content
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    text = soup.get_text().lower()
                    # Check if the service name and version match
                    if version_matches(service_name, text):
                        valid_links.append(url)
                        print(f"[✓] Google match: {url}")
                    else:
                        print(f"[✗] Google irrelevant: {url}")
            except Exception as e:
                print(f"[!] Fetch error: {e}")
    except Exception as e:
        print(f"[!] Google search error: {e}")

    return valid_links

# Searches Searchsploit for exploit links related to the service name
def searchsploit_links(service_name):
    links = []
    try:
        result = subprocess.run(
            ["searchsploit", "-w", service_name],
            capture_output=True,
            text=True
        )
        output = result.stdout
        matches = re.findall(r"https://www\.exploit-db\.com/exploits/(\d+)", output)
        for eid in set(matches):
            link = f"https://www.exploit-db.com/exploits/{eid}"
            links.append(link)
            print(f"[✓] Searchsploit match: {link}")
    except Exception as e:
        print(f"[!] searchsploit error: {e}")
    return links

# Combines Google and Searchsploit searches for each service
def perform_combined_search(services):
    with open("exploit_links_google.txt", "w", encoding="utf-8") as g_out, \
         open("exploit_links_searchsploit.txt", "w", encoding="utf-8") as s_out, \
         open("exploit_map.txt", "w", encoding="utf-8") as map_out:

        for service in services:
            g_out.write(f"\n=== {service} ===\n")
            g_links = google_search_exploit_links(service)
            for link in g_links:
                g_out.write(link + "\n")
                eid = link.strip("/").split("/")[-1]
                map_out.write(f"{eid},{service}\n")
            time.sleep(10)

            s_out.write(f"\n=== {service} ===\n")
            s_links = searchsploit_links(service)
            for link in s_links:
                s_out.write(link + "\n")
                eid = link.strip("/").split("/")[-1]
                map_out.write(f"{eid},{service}\n")

if __name__ == "__main__":
    xml_file = "nmap_output.xml"
    services = extract_services_from_nmap(xml_file)

    with open("services.txt", "w", encoding="utf-8") as f:
        for s in services:
            f.write(s + "\n")
    print(f"[✓] Services extracted: {len(services)}")

    perform_combined_search(services)
    print("\n✅ All links and exploit_map.txt have been created.")

