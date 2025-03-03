import os
import subprocess
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class PentestFramework:
    def __init__(self):
        self.scanners = ["Nmap", "Nikto", "OpenVAS"]
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
        """
        print(banner)

    def show_scanners(self):
        print(f"{Fore.BLUE}Available Scanners:{Style.RESET_ALL}")
        for scanner in self.scanners:
            print(f"{Fore.GREEN} - {scanner}{Style.RESET_ALL}")

    def show_encoders(self):
        print(f"{Fore.BLUE}Available Encoders:{Style.RESET_ALL}")
        for encoder in self.encoders:
            print(f"{Fore.GREEN} - {encoder}{Style.RESET_ALL}")

    def ai_command(self):
        venv_path = "/path/to/venv/bin/activate"  # Replace with your virtual environment path
        script_path = "AMAI.py"  # Replace with your AI script path

        if not os.path.exists(venv_path):
            print(f"{Fore.RED}Error: Virtual environment not found at {venv_path}{Style.RESET_ALL}")
            return

        if not os.path.exists(script_path):
            print(f"{Fore.RED}Error: Script not found at {script_path}{Style.RESET_ALL}")
            return

        # Command to activate the virtual environment and run the AI script
        command = f"bash -c 'source {venv_path}; python3 {script_path}; exec bash'"

        # Open a new terminal window using xterm (non-blocking)
        try:
            # Use subprocess.Popen with `stdin`, `stdout`, and `stderr` redirected
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

    def run(self):
        self.show_banner()  # Display the banner at the start
        while True:
            user_input = input(f"{Fore.BLUE}CES@user#{Style.RESET_ALL} ").strip().lower()

            if user_input == "show scanners":
                self.show_scanners()
            elif user_input == "show encoders":
                self.show_encoders()
            elif user_input == "ai":
                self.ai_command()
            elif user_input == "exit":
                print(f"{Fore.RED}Exiting the framework...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Unknown command. Available commands: show scanners, show encoders, ai, exit{Style.RESET_ALL}")

if __name__ == "__main__":
    framework = PentestFramework()
    framework.run()
