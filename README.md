Cogito Ergo Sum Pentest Framework
==================================

An advanced penetration testing framework with AI integration and web vulnerability scanning.

Features
--------
- Multi-module architecture:
  * Web vulnerability scanner (SQLi, XSS, Business Logic flaws)
  * Directory brute-forcer with multi-process support
  * AI-powered pentesting assistant
  * Multiple output formats (HTML, JSON, CSV)
  
- Advanced scanning capabilities:
  * Customizable wordlists
  * Parallel scanning with process/thread control
  * Technology stack detection
  * API security testing (GraphQL introspection)

Installation
------------
1. Clone repository:
   git clone https://github.com/oliviaisntcringe/CES_framework.git
   cd CES_framework

2. Install dependencies:
   pip install -r requirements.txt

3. Launch:
   source /path/to/your/venv/
   python3 CES.py

Basic Usage
-----------
Start framework:
   python3 CES.py

Example workflow:
   show scanners
   use webscan
   set target http://example.com
   set threads 20
   set output json
   run

Key Commands
------------
Main interface:
   show scanners    - List available scanners
   show encoders   - Show encoding schemes
   use <scanner>   - Enter scanner config
   ai              - Launch AI assistant
   exit            - Quit framework

Scanner commands:
   set <option> <value> - Configure parameters
   show options        - View current config
   run                 - Start scanning

Configuration
-------------
Edit config.yaml for default settings:

target: "http://test.site"
threads: 15
processes: 4
timeout: 5
output: "html"
wordlist_path: "/path/to/wordlist.txt"
auth:
  type: "basic"
  username: "admin"
  password: "password"

AI Assistant
------------
Example interaction:
You: How to test for SQL injection?
AM: Try payloads like ' OR 1=1-- and monitor response...

Legal Notice
------------
Use only on authorized systems. Developers assume no liability for unauthorized use.

License
-------
GNU General Public License v3.0