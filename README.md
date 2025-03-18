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
    git clone https://github.com/oliviaisntcringe/CES_framework.git && cd CES_framework
 
 2. Install dependencies:
    pip install -r requirements.txt
 
 3. Launch:
    source /path/to/your/venv/
    python3 CES.py
    source /path/to/your/venv/ && python3 CES.py
 
 AI Setup
 ------------
 
 From LocalStorage 
 
 <img width="1150" alt="image" src="https://github.com/user-attachments/assets/b4e11650-3d1b-4638-956a-c67889a9f37e" />
 
 1. Visit [chat.deepseek.com](https://chat.deepseek.com)
 2. Log in to your account
 3. Open browser developer tools (F12 or right-click > Inspect)
 4. Go to Application tab (if not visible, click >> to see more tabs)
 5. In the left sidebar, expand "Local Storage"
 6. Click on "https://chat.deepseek.com"
 7. Find the key named `userToken`
 8. Copy `"value"` - this is your authentication token
 9. Open AMAI.py and put your token here
 
 Basic Usage
 -----------
 Start framework:
    python3 CES.py
 
 Example workflow:
    show scanners /
    use webscan /
    show options / 
    set target http://example.com / 
    set threads 20 / 
    set output json /
    run / 
 
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
 
 target: "http://test.site" /
 threads: 15 /
 processes: 4 /
 timeout: 5 / 
 output: "html" / 
 wordlist_path: "/path/to/wordlist.txt" / 
 auth: / 
   type: "basic" / 
   username: "admin" / 
   password: "password" / 
 
 AI Assistant
 ------------
 Example interaction:
 You: How to test for SQL injection? /
 AM: Try payloads like ' OR 1=1-- and monitor response... /
 
🚀 Roadmap
Our journey has just begun! Upcoming features include:

🔓 Exploitation Module:
Integrate a module to exploit vulnerabilities detected by the scanner.
🗂️ Automated Zero-Day Exploits Repository:
Create a dynamic directory of zero-day exploits.
🤖 AI-Driven Exploit Development:
Utilize AI to write and integrate custom exploits as modules.
🎨 Graphical User Interface (GUI):
Develop an intuitive GUI for simplified control and monitoring.

 Legal Notice
 ------------
 Use only on authorized systems. Developers assume no liability for unauthorized use.
 
 License
 -------
 GNU General Public License v3.0
