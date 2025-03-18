import os
import subprocess
import sys
from colorama import Fore, Style, init
import yaml

# Load default configuration from file to use for default scanner options
with open('config.yaml') as f:
    default_config = yaml.safe_load(f)

# Define default options using values from config.yaml
default_options = {
    "target": default_config.get("target", ""),
    "threads": default_config.get("threads", 10),
    "processes": default_config.get("processes", 4),
    "timeout": default_config.get("timeout", 5),
    "delay": default_config.get("delay", 1),
    "output": default_config.get("output", "html"),
    "wordlist_path": default_config.get("wordlist_path", "/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt"),
    "auth_type": default_config.get("auth", {}).get("type", "none"),
    "auth_username": default_config.get("auth", {}).get("username", ""),
    "auth_password": default_config.get("auth", {}).get("password", ""),
    "cors_origin": default_config.get("cors_origin", "http://evil.com"),
    "user_agents": default_config.get("user_agents", []),
    "check_headers": True,
    "test_ssrf": True,
    "fuzz_params": True,
    "cvss_threshold": 6.0,
    "run_bruteforce": True  # New option for brute-force
}

# Import the AdvancedScanner from webscan.py
from webscan import AdvancedScanner

# Initialize colorama
init(autoreset=True)

class PentestFramework:
    def __init__(self):
        self.scanners = {
            "webscan": {
                "description": "Advanced Web Vulnerability Scanner",
                "options": default_options.copy()  # Each scanner maintains its own settings
            }
        }
        self.encoders = ["Base64", "URL Encoding", "Hex Encoding"]

    def show_banner(self):
        banner = f"""
{Fore.CYAN} ▄████▄  {Fore.GREEN}▓█████   {Fore.YELLOW}██████ 
{Fore.CYAN}▒██▀ ▀█  {Fore.GREEN}▓█   ▀ {Fore.YELLOW}▒██    ▒ 
{Fore.CYAN}▒▓█    ▄ {Fore.GREEN}▒███   {Fore.YELLOW}░ ▓██▄            
{Fore.CYAN}▒▓▓▄ ▄██▒{Fore.GREEN}▒▓█  ▄ {Fore.YELLOW}  ▒   ██▒ {Fore.RED} cogito ergo sum framework 
{Fore.CYAN}▒ ▓███▀ ░{Fore.GREEN}░▒████▒{Fore.YELLOW}▒██████▒▒ {Fore.RED} made by tuerleprince
{Fore.CYAN}░ ░▒ ▒  ░{Fore.GREEN}░░ ▒░ ░{Fore.YELLOW}▒ ▒▓▒ ▒ ░
{Fore.CYAN}  ░  ▒   {Fore.GREEN}░ ░  ░{Fore.YELLOW}░ ░▒  ░ ░
{Fore.CYAN}░        {Fore.GREEN}  ░   {Fore.YELLOW}░  ░  ░  
{Fore.CYAN}░ ░      {Fore.GREEN}   ░  ░{Fore.YELLOW}      ░  
{Fore.CYAN}░        {Fore.GREEN}      {Fore.YELLOW}         
---------------------------------------------------------------------------------------------------
COMMANDS: show modules , show encoders , show scanners, ai , use ,exit
        """
        print(banner)

    def show_scanners(self):
        print(f"{Fore.BLUE}Available Scanners:{Style.RESET_ALL}")
        for name, info in self.scanners.items():
            print(f"{Fore.GREEN} - {name}: {info['description']}{Style.RESET_ALL}")

    def show_encoders(self):
        print(f"{Fore.BLUE}Available Encoders:{Style.RESET_ALL}")
        for encoder in self.encoders:
            print(f"{Fore.GREEN} - {encoder}{Style.RESET_ALL}")

    def ai_command(self):
        venv_path = "/path/to/venv/bin/activate" 
        script_path = "AMAI.py" 

        if not os.path.exists(venv_path):
            print(f"{Fore.RED}Error: Virtual environment not found at {venv_path}{Style.RESET_ALL}")
            return

        if not os.path.exists(script_path):
            print(f"{Fore.RED}Error: Script not found at {script_path}{Style.RESET_ALL}")
            return

        command = f"bash -c 'source {venv_path}; python3 {script_path}; exec bash'"

        try:
            subprocess.Popen(
                ["xterm", "-e", command],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            print(f"{Fore.GREEN}AI script started in a new terminal window. You can continue working in the main framework.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error starting AI script in new terminal: {e}{Style.RESET_ALL}")

    def scanner_menu(self, scanner_name):
        scanner = self.scanners.get(scanner_name)
        if not scanner:
            print(f"{Fore.RED}Scanner {scanner_name} not found.{Style.RESET_ALL}")
            return

        options = scanner["options"]
        print(f"{Fore.BLUE}Entered {scanner_name} configuration mode. Type 'help' for available commands.{Style.RESET_ALL}")
        while True:
            user_input = input(f"{Fore.MAGENTA}{scanner_name} > {Style.RESET_ALL}").strip()
            if user_input.lower() in ["show options", "options"]:
                print(f"{Fore.BLUE}Options for {scanner_name}:{Style.RESET_ALL}")
                for key, value in options.items():
                    print(f"{Fore.GREEN}{key}: {value}{Style.RESET_ALL}")
            elif user_input.lower().startswith("set "):
                parts = user_input.split()
                if len(parts) >= 3:
                    key = parts[1]
                    value = " ".join(parts[2:])
                    if key in options:
                        # Handle boolean values
                        if key == "run_bruteforce":
                            if value.lower() in ["true", "yes", "1"]:
                                value = True
                            elif value.lower() in ["false", "no", "0"]:
                                value = False
                            else:
                                print(f"{Fore.RED}Invalid boolean value for {key}. Use 'true' or 'false'.{Style.RESET_ALL}")
                                continue
                    
                        elif isinstance(default_options.get(key), int):
                            try:
                                value = int(value)
                            except ValueError:
                                print(f"{Fore.RED}Invalid integer for {key}.{Style.RESET_ALL}")
                                continue
                        elif isinstance(default_options.get(key), float):
                            try:
                                value = float(value)
                            except ValueError:
                                print(f"{Fore.RED}Invalid float for {key}.{Style.RESET_ALL}")
                                continue
                        options[key] = value
                        print(f"{Fore.GREEN}Set {key} to {value}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Unknown option '{key}'. Available options: {', '.join(options.keys())}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Usage: set <option> <value>{Style.RESET_ALL}")
            elif user_input.lower() == "run":
                if scanner_name == "webscan":
                    target = options.get("target")
                    if not target:
                        print(f"{Fore.RED}Target not set. Use 'set target <url>' to set the target.{Style.RESET_ALL}")
                        continue
                    print(f"{Fore.BLUE}Starting webscan on {target} with options:{Style.RESET_ALL}")
                    for key, value in options.items():
                        print(f"{Fore.GREEN}{key}: {value}{Style.RESET_ALL}")
                    try:
                        
                        if options.get("run_bruteforce", False):
                         
                            cmd = [
                                'xterm',
                                '-e',
                                'python',
                                'webscan.py',  
                                target,
                                '--output', options.get("output", "html"),
                                '--processes', str(options.get("processes", 4)),
                                '--threads', str(options.get("threads", 10)),
                                '--bruteforce'
                            ]
                            subprocess.Popen(cmd)
                            # Run main scan without brute-force
                            scanner_options = options.copy()
                            scanner_options["run_bruteforce"] = False
                            webscanner = AdvancedScanner(target, options=scanner_options)
                            webscanner.run()
                        else:
                            # Normal scan
                            webscanner = AdvancedScanner(target, options=options)
                            webscanner.run()
                    except Exception as e:
                        print(f"{Fore.RED}Error running webscan: {e}{Style.RESET_ALL}")
            elif user_input.lower() == "help":
                print(f"{Fore.YELLOW}Available commands in {scanner_name} mode:")
                print("  show options       - Display current scanner options")
                print("  set <option> <val> - Set an option (e.g., set target http://example.com)")
                print("  run                - Run the scanner with current options")
                print("  back               - Return to the main menu")
                print(f"{Style.RESET_ALL}")
            elif user_input.lower() == "back":
                break
            else:
                print(f"{Fore.RED}Unknown command in {scanner_name} mode. Type 'help' for available commands.{Style.RESET_ALL}")

    def run(self):
        self.show_banner()
        while True:
            user_input = input(f"{Fore.BLUE}CES@user#{Style.RESET_ALL} ").strip().lower()

            if user_input == "show scanners":
                self.show_scanners()
            elif user_input == "show encoders":
                self.show_encoders()
            elif user_input == "ai":
                self.ai_command()
            elif user_input.startswith("use "):
                scanner_name = user_input.split(" ", 1)[1]
                self.scanner_menu(scanner_name)
            elif user_input == "exit":
                print(f"{Fore.RED}Exiting the framework...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Unknown command. Available commands: show scanners, show encoders, ai, use <scanner>, exit{Style.RESET_ALL}")

if __name__ == "__main__":
    framework = PentestFramework()
    framework.run()
