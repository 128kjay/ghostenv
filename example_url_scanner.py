import sys
import socket
import requests
from ipwhois import IPWhois
from rich.console import Console
from rich.table import Table
from urllib.parse import urlparse


VT_API_KEY = ""  # vt key
if not VT_API_KEY:
    print("[!] Warning: No VirusTotal API key found. Skipping VT scans.")

console = Console()

def resolve_hostname(url):
    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        return domain, ip
    except Exception:
        return None, None

def whois_lookup(ip):
    try:
        obj = IPWhois(ip)
        return obj.lookup_rdap()["network"]["name"]
    except Exception:
        return "Unknown"

def geolocate_ip(ip):
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{resp['country']}, {resp['regionName']}"
    except:
        return "Unknown"

def vt_scan(domain):
    if not VT_API_KEY:
        return "[!] Skipped (no API key)"
    headers = {"x-apikey": VT_API_KEY}
    resp = requests.get(f"https://www.virustotal.com/api/v3/domains/{domain}", headers=headers)
    if resp.status_code == 200:
        return resp.json()["data"]["attributes"]["reputation"]
    return "Error"

def main():
    if len(sys.argv) < 2:
        print("Usage: example_url_scanner.py <url1> <url2> ...")
        # testing args 
        #print("[!] No URLs provided. Using test URLs.")
        #sys.argv = ["https://example.com", "https://malicious.biz"]
        return

    urls = sys.argv[1:]
    table = Table(title="URL Threat Analysis")

    table.add_column("URL", style="cyan", no_wrap=True)
    table.add_column("IP", style="green")
    table.add_column("Region", style="yellow")
    table.add_column("Org", style="magenta")
    table.add_column("VT Score", style="red")

    for url in urls:
        domain, ip = resolve_hostname(url)
        if not ip:
            table.add_row(url, "N/A", "N/A", "N/A", "N/A")
            continue
        org = whois_lookup(ip)
        region = geolocate_ip(ip)
        vt = str(vt_scan(domain))
        table.add_row(url, ip, region, org, vt)

    console.print(table)

if __name__ == "__main__":
    main()
