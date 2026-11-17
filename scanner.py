import sys
import socket
import webbrowser
import os
from urllib.parse import urlparse
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from rich.console import Console
from rich.panel import Panel

console = Console()

def banner():
    console.print(Panel(
        "[bold red]PROTIO SUITE - ALL-IN-ONE OSINT & SECURITY AUDIT PLATFORM[/bold red]\n"
        "[cyan]Developer: Vedansh Srivastava | Educational Security & Recon Tool[/cyan]",
        border_style="yellow"
    ))

def phone_osint():
    console.print("\n[bold yellow][*] Phone Number OSINT Intelligence[/bold yellow]")
    raw_num = console.input("Enter phone number with country code (e.g., +919876543210): ").strip()
    try:
        parsed = phonenumbers.parse(raw_num, None)
        if not phonenumbers.is_valid_number(parsed):
            console.print("[red][-] Invalid phone number format.[/red]")
            return
        region = geocoder.description_for_number(parsed, "en")
        sim_carrier = carrier.name_for_number(parsed, "en")
        tz = timezone.time_zones_for_number(parsed)
        
        console.print(f"[green][+] Valid Number  :[/green] True")
        console.print(f"[green][+] Region/Country:[/green] {region or 'Unknown'}")
        console.print(f"[green][+] Carrier/ISP   :[/green] {sim_carrier or 'Unknown'}")
        console.print(f"[green][+] Timezone      :[/green] {', '.join(tz)}")
    except Exception as e:
        console.print(f"[red][-] Error parsing number: {e}[/red]")

def username_osint():
    console.print("\n[bold yellow][*] Public Username OSINT Footprinting[/bold yellow]")
    username = console.input("Enter target username: ").strip()
    if not username:
        console.print("[red][-] Username cannot be empty.[/red]")
        return

    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Medium": f"https://medium.com/@{username}",
        "Dev.to": f"https://dev.to/{username}"
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    console.print(f"[cyan][*] Checking public profiles for '{username}'...[/cyan]\n")

    for site, url in platforms.items():
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                console.print(f"    [bold green]✔ {site:<12}:[/bold green] Found -> {url}")
            else:
                console.print(f"    [dim red]✘ {site:<12}:[/dim red] Not Found")
        except Exception:
            console.print(f"    [yellow]! {site:<12}:[/yellow] Connection Timeout")

def ip_location_lookup():
    console.print("\n[bold yellow][*] IP Address Geo-Location Lookup[/bold yellow]")
    ip = console.input("Enter public IP address (e.g., 8.8.8.8): ").strip()
    try:
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5).json()
        if "error" in geo:
            console.print(f"[red][-] Error: {geo.get('reason', 'Invalid IP')}[/red]")
            return
        console.print(f"[green][+] IP Address    :[/green] {geo.get('ip')}")
        console.print(f"[green][+] City / Region :[/green] {geo.get('city')}, {geo.get('region')}")
        console.print(f"[green][+] Country       :[/green] {geo.get('country_name')}")
        console.print(f"[green][+] Coordinates   :[/green] {geo.get('latitude')}, {geo.get('longitude')}")
        console.print(f"[green][+] ISP / Org     :[/green] {geo.get('org')}")
    except Exception as e:
        console.print(f"[red][-] Location lookup failed: {e}[/red]")

def web_recon():
    console.print("\n[bold yellow][*] Web Target Full Recon & Security Audit[/bold yellow]")
    target = console.input("Enter target domain or URL (e.g., example.com): ").strip()
    domain = urlparse(target).netloc if "://" in target else target.split("/")[0]
    
    try:
        ip = socket.gethostbyname(domain)
        console.print(f"[green][+] Target Domain :[/green] {domain}")
        console.print(f"[green][+] Public IP     :[/green] {ip}")
        
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5).json()
        console.print(f"[green][+] Location      :[/green] {geo.get('city')}, {geo.get('country_name')}")
        console.print(f"[green][+] Hosting/ISP   :[/green] {geo.get('org')}")
        
        url = f"https://{domain}" if not target.startswith("http") else target
        resp = requests.get(url, timeout=5)
        console.print(f"[green][+] HTTP Status   :[/green] {resp.status_code}")
        server = resp.headers.get("Server", "Hidden")
        console.print(f"[green][+] Server Header :[/green] {server}")

        if "cloudflare" in server.lower() or "cf-ray" in resp.headers:
            console.print("[bold red][!] WAF Detected  :[/bold red] Protected by Cloudflare")
        else:
            console.print("[green][+] WAF/CDN       :[/green] Direct Server")

        console.print("\n[bold cyan][*] Security Headers Check:[/bold cyan]")
        for h in ["X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection"]:
            if h in resp.headers:
                console.print(f"    [green]✔ {h}: Present[/green]")
            else:
                console.print(f"    [red]✘ {h}: Missing[/red]")

        console.print(f"\n[bold cyan][*] Scanning Common Ports on {ip}...[/bold cyan]")
        for port in [21, 22, 80, 443, 8080, 3306]:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                console.print(f"    [bold green]✔ Port {port} is OPEN[/bold green]")
            else:
                console.print(f"    [dim red]✘ Port {port} is closed[/dim red]")
            s.close()

    except Exception as e:
        console.print(f"[red][-] Recon failed: {e}[/red]")

def permission_awareness_demo():
    console.print("\n[bold yellow][*] Browser Permission Security Awareness Demo[/bold yellow]")
    console.print("[cyan]Generates a local HTML page to demonstrate how browsers prompt users for GPS, Mic, and File permissions.[/cyan]")
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>PROTIO - Browser Permission Awareness</title>
    <style>
        body { background: #0f172a; color: #38bdf8; font-family: monospace; text-align: center; padding-top: 50px; }
        .box { background: #1e293b; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 0 15px rgba(56,189,248,0.3); }
        button { background: #0284c7; color: white; border: none; padding: 12px 20px; font-size: 16px; cursor: pointer; border-radius: 5px; margin: 10px; }
        button:hover { background: #0369a1; }
        #log { margin-top: 20px; color: #f43f5e; text-align: left; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🔒 PROTIO Permission Security Demo</h2>
        <p>Click buttons below to observe standard browser permission prompts:</p>
        <button onclick="checkGeo()">Test Geolocation Prompt</button>
        <button onclick="checkMic()">Test Microphone Prompt</button>
        <button onclick="checkFile()">Test File Picker Prompt</button>
        <input type="file" id="fileInput" style="display:none" accept="image/*">
        <div id="log"></div>
    </div>
    <script>
        function checkGeo() {
            const log = document.getElementById('log');
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(pos => {
                    log.innerHTML += `[+] Permission Granted - Coordinates displayed locally.<br>`;
                }, err => { log.innerHTML += `[-] Prompt Blocked/Error: ${err.message}<br>`; });
            }
        }
        function checkMic() {
            const log = document.getElementById('log');
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => { 
                    log.innerHTML += "[+] Microphone Permission Granted (Stopping stream immediately).<br>"; 
                    stream.getTracks().forEach(track => track.stop());
                })
                .catch(err => { log.innerHTML += `[-] Prompt Blocked/Error: ${err.message}<br>`; });
        }
        function checkFile() {
            document.getElementById('fileInput').click();
            document.getElementById('fileInput').onchange = e => {
                document.getElementById('log').innerHTML += `[+] File Selected Locally: ${e.target.files[0].name}<br>`;
            };
        }
    </script>
</body>
</html>"""
    
    filename = "permission_demo.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    console.print(f"[green][+] Generated local awareness demo: {filename}[/green]")
    webbrowser.open("file://" + os.path.abspath(filename))

def main():
    while True:
        banner()
        console.print("[1] Phone Number OSINT Intelligence")
        console.print("[2] Username OSINT (Social Media Profile Finder)")
        console.print("[3] IP Address Geo-Location Lookup")
        console.print("[4] Web Target Full Recon (IP, Headers, WAF & Ports)")
        console.print("[5] Browser Permission Awareness Demo (Local UI)")
        console.print("[6] Open Official ELVORIX Web Portal")
        console.print("[7] Open Creator YouTube Channel")
        console.print("[8] Join Discord Community")
        console.print("[9] Join Telegram Security Channel")
        console.print("[10] Exit")
        
        choice = console.input("\n[bold cyan]Select an option (1-10): [/bold cyan]").strip()
        
        if choice == "1":
            phone_osint()
        elif choice == "2":
            username_osint()
        elif choice == "3":
            ip_location_lookup()
        elif choice == "4":
            web_recon()
        elif choice == "5":
            permission_awareness_demo()
        elif choice == "6":
            console.print("[green][+] Opening ELVORIX Portal...[/green]")
            webbrowser.open("https://vedansh73.github.io/ELVORIX/")
        elif choice == "7":
            console.print("[green][+] Opening YouTube Channel...[/green]")
            webbrowser.open("https://www.youtube.com/@vedanshsrivastava182")
        elif choice == "8":
            console.print("[green][+] Opening Discord Server...[/green]")
            webbrowser.open("https://discord.com/invite/PUgqMfdWwB")
        elif choice == "9":
            console.print("[green][+] Opening Telegram Channel...[/green]")
            webbrowser.open("https://t.me/vedasecurity182")
        elif choice == "10":
            console.print("[bold red]Exiting PROTIO Suite. Stay safe and ethical![/bold red]")
            sys.exit()
        else:
            console.print("[red]Invalid choice! Please select between 1-10.[/red]")
            
        console.input("\n[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    main()
