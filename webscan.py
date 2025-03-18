import requests
import re
import time
import threading
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from bs4 import BeautifulSoup
from html import escape
import json
import csv
import yaml
import random
import argparse
from concurrent.futures import ThreadPoolExecutor
from http import cookiejar
import hashlib
import multiprocessing
import subprocess

# Load default configuration from file
with open('config.yaml') as f:
    config = yaml.safe_load(f)

def is_valid_response(response):
    """Determine if response contains meaningful content (standalone function)"""
    valid_codes = [200, 301, 302, 403, 401]
    content_indicators = ['<html', 'DOCTYPE', '<body', '<head', 'http-equiv']
    text = response.text.lower()
    return (response.status_code in valid_codes and 
            any(indicator in text for indicator in content_indicators))

def process_chunk_worker(chunk, config):
    """Process a subset of the wordlist with given config (standalone function)"""
    session = requests.Session()
    session.headers.update(config['headers'])
    
    # Apply cookies
    for name, value in config['cookies'].items():
        session.cookies.set(name, value)
    
    # Handle authentication
    auth_config = config['auth_config']
    auth_type = auth_config.get('type', 'none')
    
    if auth_type == 'basic':
        session.auth = (
            auth_config.get('username', ''),
            auth_config.get('password', '')
        )
    elif auth_type == 'cookie':
        cookie_name = auth_config.get('cookie_name')
        cookie_value = auth_config.get('cookie_value')
        if cookie_name and cookie_value:
            session.cookies.set(cookie_name, cookie_value)
    elif auth_type == 'bearer':
        token = auth_config.get('token')
        if token:
            session.headers['Authorization'] = f'Bearer {token}'
    
    discovered = []
    for path in chunk:
        url = f"{config['target'].rstrip('/')}/{path.lstrip('/')}"
        try:
            response = session.get(url, timeout=config['timeout'])
            if is_valid_response(response):
                discovered.append(url)
                print(f"[{response.status_code}] {url} ({len(response.text)} bytes)")
        except Exception as e:
            pass
    return discovered

class AdvancedScanner:
    def __init__(self, target, options=None):
        self.target = target
        options = options if options is not None else {}
        
        # Configuration parameters
        self.threads = int(options.get("threads", config.get("threads", 10)))
        self.processes = int(options.get("processes", config.get("processes", 4)))
        self.timeout = int(options.get("timeout", config.get("timeout", 5)))
        self.delay = float(options.get("delay", config.get("delay", 1)))
        self.output = options.get("output", config.get("output", "html"))
        self.wordlist_path = options.get("wordlist_path", config.get("wordlist_path", "wordlist.txt"))
        self.cors_origin = options.get("cors_origin", config.get("cors_origin", "http://evil.com"))
        self.user_agents = config.get("user_agents", [])
        self.run_bruteforce = options.get("run_bruteforce", False)  # New parameter
        
        # Authentication configuration
        self.auth_config = {
            "type": options.get("auth_type", config.get("auth", {}).get("type", "none")),
            "username": options.get("auth_username", config.get("auth", {}).get("username", "")),
            "password": options.get("auth_password", config.get("auth", {}).get("password", "")),
            "cookie_name": options.get("auth_cookie_name", config.get("auth", {}).get("cookie_name", "")),
            "cookie_value": options.get("auth_cookie_value", config.get("auth", {}).get("cookie_value", "")),
            "token": options.get("auth_token", config.get("auth", {}).get("token", ""))
        }

        # Session setup
        self.session = requests.Session()
        self.session.cookies = cookiejar.CookieJar()
        if self.user_agents:
            self.session.headers.update({'User-Agent': random.choice(self.user_agents)})
        self.session.headers.update({'Origin': self.cors_origin})
        
        # State tracking
        self.vulnerabilities = []
        self.discovered_paths = []
        self.authenticated = False
        self.lock = threading.Lock()

    def check_auth(self):
        """Handle authentication for different types"""
        try:
            auth_type = self.auth_config["type"]
            if auth_type == 'basic':
                self.session.auth = (
                    self.auth_config["username"], 
                    self.auth_config["password"]
                )
                test_res = self.session.get(self.target)
                self.authenticated = test_res.status_code == 200
                print(f"{'✅' if self.authenticated else '❌'} Basic Authentication")

            elif auth_type == 'cookie':
                if self.auth_config["cookie_name"] and self.auth_config["cookie_value"]:
                    self.session.cookies.set(
                        self.auth_config["cookie_name"],
                        self.auth_config["cookie_value"]
                    )
                    test_res = self.session.get(self.target)
                    self.authenticated = test_res.status_code == 200
                    print(f"{'✅' if self.authenticated else '❌'} Cookie Authentication")

            elif auth_type == 'bearer':
                if self.auth_config["token"]:
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.auth_config["token"]}'
                    })
                    test_res = self.session.get(self.target)
                    self.authenticated = test_res.status_code == 200
                    print(f"{'✅' if self.authenticated else '❌'} Bearer Token Authentication")

            if not self.authenticated and auth_type != 'none':
                print("⚠️ Proceeding with unauthenticated scan")

        except Exception as e:
            print(f"🔴 Authentication error: {e}")
            self.authenticated = False

    def load_wordlist(self):
        """Load and return wordlist entries"""
        with open(self.wordlist_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def brute_force_directories(self):
        """Multi-process directory brute-forcing"""
        wordlist = self.load_wordlist()
        chunk_size = len(wordlist) // self.processes or 1
        chunks = [wordlist[i:i+chunk_size] for i in range(0, len(wordlist), chunk_size)]

        # Prepare pickle-safe configuration for workers
        worker_config = {
            'target': self.target,
            'timeout': self.timeout,
            'headers': dict(self.session.headers),
            'cookies': requests.utils.dict_from_cookiejar(self.session.cookies),
            'auth_config': self.auth_config
        }

        with multiprocessing.Pool(processes=self.processes) as pool:
            # Use starmap to pass both chunk and config to each worker
            results = pool.starmap(process_chunk_worker, [(chunk, worker_config) for chunk in chunks])
        
        # Merge results from all processes
        for result in results:
            self.discovered_paths.extend(result)

    def detect_tech_stack(self):
        """Identify web technologies in use"""
        try:
            response = self.session.get(self.target)
            tech = {
                'server': response.headers.get('Server', ''),
                'framework': self.detect_framework(response),
                'cookies': [c.name for c in response.cookies]
            }
            print(f"🛠️ Detected Tech Stack: {tech}")
            return tech
        except Exception as e:
            print(f"🔴 Tech detection error: {e}")
            return {}

    def detect_framework(self, response):
        """Detect specific web frameworks"""
        if 'wp-content' in response.text:
            return 'WordPress'
        if 'X-Drupal-Cache' in response.headers:
            return 'Drupal'
        if 'X-Powered-By' in response.headers:
            return response.headers['X-Powered-By']
        return 'Unknown'

    def sql_injection(self):
        """Test for SQL injection vulnerabilities"""
        payloads = [
            ("' AND SLEEP(5)--", 5),
            ("'; WAITFOR DELAY '0:0:5'--", 5),
            ("' OR 1=1-- -", None)
        ]
        for payload, sleep_time in payloads:
            try:
                start = time.time()
                response = self.session.get(f"{self.target}?test={payload}", timeout=self.timeout)
                elapsed = time.time() - start
                
                if (sleep_time and elapsed >= sleep_time) or ('error' in response.text.lower()):
                    self.log_vuln(f"SQLi Vulnerability detected: {payload}", 'High')
            except Exception as e:
                print(f"🔴 SQLi test error: {e}")

    def xss(self):
        """Test for Cross-Site Scripting vulnerabilities"""
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "%3Cscript%3Ealert(1)%3C/script%3E"
        ]
        for payload in payloads:
            try:
                url = f"{self.target}?q={payload}"
                response = self.session.get(url)
                if payload in response.text:
                    self.log_vuln(f"XSS Vulnerability detected: {payload}", 'High')
            except Exception as e:
                print(f"🔴 XSS test error: {e}")

    def check_business_logic(self):
        """Check for business logic flaws"""
        if any('/cart' in path for path in self.discovered_paths):
            payload = {'items': [{'id': 1, 'price': 0.01}]}
            try:
                response = self.session.post(f"{self.target}/cart", json=payload, timeout=self.timeout)
                if response.status_code == 200 and 'total' in response.json() and response.json()['total'] < 1:
                    self.log_vuln("Business Logic Flaw: Price Manipulation", 'High')
            except Exception as e:
                print(f"🔴 Business logic test error: {e}")

    def api_scan(self):
        """Scan for API vulnerabilities"""
        if any('/graphql' in path for path in self.discovered_paths):
            payload = {"query": "{__schema{types{name}}}"}
            try:
                response = self.session.post(f"{self.target}/graphql", json=payload, timeout=self.timeout)
                if 'data' in response.json():
                    self.log_vuln("GraphQL Introspection Enabled", 'Medium')
            except Exception as e:
                print(f"🔴 GraphQL introspection error: {e}")

    def generate_report(self, format='html'):
        """Generate vulnerability report"""
        if format == 'html':
            template = f"""<html>
                <head><title>Security Report - {escape(self.target)}</title></head>
                <body>
                    <h1>Scan Report for {escape(self.target)}</h1>
                    <p>Date: {time.ctime()}</p>
                    <h2>Vulnerabilities ({len(self.vulnerabilities)})</h2>
                    <ul>{"".join(f"<li>{escape(v)}</li>" for v in self.vulnerabilities)}</ul>
                </body>
            </html>"""
            with open('report.html', 'w') as f:
                f.write(template)
        elif format == 'json':
            report = {
                "target": self.target,
                "timestamp": time.time(),
                "vulnerabilities": self.vulnerabilities,
                "paths_found": self.discovered_paths
            }
            with open('report.json', 'w') as f:
                json.dump(report, f, indent=2)
        elif format == 'csv':
            with open('report.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "Details"])
                for vuln in self.vulnerabilities:
                    writer.writerow([vuln.split(':')[0], vuln.split(':')[1]])

    def log_vuln(self, message, severity='Medium'):
        """Log vulnerabilities with severity"""
        with self.lock:
            entry = f"[{severity}] {message}"
            self.vulnerabilities.append(entry)
            print(f"🔥 {entry}")

    def run(self):
        """Main scanning workflow"""
        self.check_auth()
        print(f"🚀 Starting scan on {self.target}")
        
        steps = [
            self.detect_tech_stack,
            self.sql_injection,
            self.xss,
            self.check_business_logic,
            self.api_scan
        ]
        
        # Conditionally add brute_force step
        if self.run_bruteforce:
            steps.insert(1, self.brute_force_directories)
        
        for step in steps:
            try:
                step()
                time.sleep(self.delay)
            except Exception as e:
                print(f"🔴 Error in {step.__name__}: {e}")
        
        self.generate_report(self.output)
        print(f"✅ Scan completed! Found {len(self.vulnerabilities)} vulnerabilities")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Advanced Web Vulnerability Scanner')
    parser.add_argument('target', help='URL to scan')
    parser.add_argument('--output', choices=['html', 'json', 'csv'], default='html')
    parser.add_argument('--processes', type=int, default=4, help='Number of parallel processes')
    parser.add_argument('--threads', type=int, default=10, help='Number of threads per process')
    parser.add_argument('--bruteforce', action='store_true', help='Run directory bruteforce')
    args = parser.parse_args()

    options = {
        'processes': args.processes,
        'threads': args.threads,
        'output': args.output,
        'run_bruteforce': args.bruteforce
    }

    if args.bruteforce:
        # Run only brute-force
        scanner = AdvancedScanner(args.target, options)
        scanner.run()
    else:
        # Launch brute-force in Xterm and run main scan
        cmd = [
            'xterm',
            '-e',
            'python',
            __file__,
            args.target,
            '--output', args.output,
            '--processes', str(args.processes),
            '--threads', str(args.threads),
            '--bruteforce'
        ]
        subprocess.Popen(cmd)
        scanner = AdvancedScanner(args.target, options)
        scanner.run()