import aiohttp
import asyncio
import socket
import ssl
import nmap
import whois
from datetime import datetime
from urllib.parse import urlparse

# Extract domain from URL
def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc if parsed_url.netloc else url

# Asynchronous SQL Injection check
async def check_sql_injection(session, url):
    sql_payloads = ["'", '"', "OR 1=1 --", "' OR '1'='1"]
    tasks = []
    for payload in sql_payloads:
        target_url = f"{url}{payload}"
        tasks.append(session.get(target_url, timeout=3))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for response in results:
        if isinstance(response, Exception):
            continue
        try:
            text = await response.text()
            if "SQL" in text or "syntax" in text:
                return f"⚠️ **Potential SQL Injection Found!**"
        except:
            continue
    return "✅ **No SQL Injection detected.**"

# Asynchronous XSS check
async def check_xss(session, url):
    xss_payloads = ['<script>alert("XSS")</script>', '" onmouseover="alert(1)"']
    tasks = []
    for payload in xss_payloads:
        target_url = f"{url}{payload}"
        tasks.append(session.get(target_url, timeout=3))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for response in results:
        if isinstance(response, Exception):
            continue
        try:
            text = await response.text()
            if any(payload in text for payload in xss_payloads):
                return f"⚠️ **Potential XSS Found!**"
        except:
            continue
    return "✅ **No XSS detected.**"

# Enumerate subdomains
async def enumerate_subdomains(session, domain):
    subdomains = ["admin", "test", "mail", "dev", "secure", "api"]
    tasks = []
    for sub in subdomains:
        url = f"http://{sub}.{domain}"
        tasks.append(session.head(url, timeout=3))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    found = []
    for idx, response in enumerate(results):
        if isinstance(response, Exception):
            continue
        if response.status < 400:
            found.append(f"http://{subdomains[idx]}.{domain}")

    return found if found else "✅ **No subdomains found.**"

# Scan open ports using Nmap (threaded)
async def scan_ports(target):
    def run_nmap():
        scanner = nmap.PortScanner()
        scanner.scan(target, arguments='-T4 -F')  # Faster scan (-T4 Fast, -F few ports)
        open_ports = []
        for host in scanner.all_hosts():
            open_ports.extend(scanner[host]['tcp'].keys())
        return open_ports if open_ports else "✅ **No open ports detected.**"
    return await asyncio.to_thread(run_nmap)

# Check SSL Certificate details (threaded)
async def check_ssl(domain):
    def run_ssl():
        try:
            context = ssl.create_default_context()
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
            conn.settimeout(3)
            conn.connect((domain, 443))
            cert = conn.getpeercert()
            return cert if cert else "⚠️ **No SSL Certificate Found.**"
        except Exception as e:
            return f"⚠️ **SSL Check Error:** {str(e)}"
    return await asyncio.to_thread(run_ssl)

# Get WHOIS info (threaded)
async def get_whois_info(domain):
    def run_whois():
        try:
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date)
            }
        except Exception as e:
            return f"⚠️ **WHOIS Lookup Error:** {str(e)}"
    return await asyncio.to_thread(run_whois)

# Scan for sensitive files
async def scan_sensitive_files(session, url):
    sensitive_files = ["/.git", "/.env", "/config.php", "/backup.sql"]
    tasks = []
    for file in sensitive_files:
        tasks.append(session.head(url + file, timeout=3))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    found = []
    for idx, response in enumerate(results):
        if isinstance(response, Exception):
            continue
        if response.status == 200:
            found.append(url + sensitive_files[idx])

    return found if found else "✅ **No sensitive files exposed.**"

# Run all security scans asynchronously
async def full_security_scan(target):
    domain = extract_domain(target)
    
    try:
        ip_address = socket.gethostbyname(domain)
    except socket.gaierror:
        ip_address = "Unresolvable Domain"

    async with aiohttp.ClientSession() as session:
        tasks = [
            check_sql_injection(session, target),
            check_xss(session, target),
            enumerate_subdomains(session, domain),
            scan_sensitive_files(session, target),
            scan_ports(domain),
            check_ssl(domain),
            get_whois_info(domain)
        ]
        results = await asyncio.gather(*tasks)

    return {
        "target": domain,
        "ip_address": ip_address,
        "sql_injection": results[0],
        "xss": results[1],
        "subdomains": results[2],
        "sensitive_files": results[3],
        "open_ports": results[4],
        "ssl": results[5],
        "whois": results[6]
    }
