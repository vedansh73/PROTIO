# ⚡ PROTIO Suite - All-in-One OSINT & Security Audit Platform

<p align="center">
  <b>Developed by Vedansh Srivastava</b> | Educational Security, OSINT & Reconnaissance Suite
</p>

---

## 🚀 Overview
**PROTIO Suite** is a modular, Python-based cybersecurity and reconnaissance framework designed for security researchers, ethical hackers, and students. It combines powerful OSINT utilities, deep web target auditing, IP geolocation tracking, and a browser-based permission security awareness module into a single interactive CLI interface.

---

## 🛠️ Features Included

1. **Phone Number OSINT Intelligence**
   - Validates international phone number formats.
   - Extracts carrier/ISP information, region/country description, and timezone metadata using `phonenumbers`.

2. **Username OSINT Footprinting**
   - Scans and checks the availability of target usernames across major platforms instantly (**GitHub, Reddit, Instagram, Pinterest, Medium, Dev.to**).

3. **IP Address Geo-Location Lookup**
   - Resolves public IP addresses to estimate geographical data including city, region, country, coordinates, and network ISP/Organization.

4. **Web Target Full Recon & Security Audit**
   - Resolves target domains to public IP addresses and fetches hosting provider details.
   - Inspects HTTP status codes and Server headers.
   - Detects Web Application Firewalls (WAF) such as Cloudflare.
   - Audits critical security headers (`X-Frame-Options`, `Content-Security-Policy`, `X-XSS-Protection`).
   - Scans common vulnerable/service ports (`21, 22, 80, 443, 8080, 3306`).

5. **Browser Permission Security Awareness Demo**
   - Generates a local interactive HTML user interface to demonstrate how modern web browsers prompt users for sensitive device capabilities like **Live GPS Geolocation, Microphone Access, and Gallery File Selection**.

---

## 📦 Requirements
The tool automatically handles its virtual environment, but it relies on these core Python packages:
- `requests` (For network requests and API integrations)
- `rich` (For beautiful colored terminal banners and UI panels)
- `phonenumbers` (For parsing and analyzing phone metadata)

---

## ⚙️ Quick Installation & Usage

Clone the repository and run the setup script with a single command:

```bash
git clone [https://github.com/vedansh73/PROTIO.git](https://github.com/vedansh73/PROTIO.git)
cd PROTIO
bash run.sh
