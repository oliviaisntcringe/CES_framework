import time
import sys
import os
from dsk.api import DeepSeekAPI

# Initialize with your auth token
api = DeepSeekAPI("PUT YOUR API KEY")


chat_id = api.create_chat_session()


USER_COLOR = "\033[94m"  # Blue
AM_COLOR = "\033[92m"  # Green
RESET_COLOR = "\033[0m"  # Reset to default


BANNER = r"""
    ___    __  ___
   /   |  /  |/  /
  / /| | / /|_/ /   cognito ergo sum
 / ___ |/ /  / /    modded by tuerleprince 
/_/  |_/_/  /_/
"""
os.system("clear")
print(f"{AM_COLOR}{BANNER}{RESET_COLOR}")


initial_prompt = (
    "From now on, all responses should be focused on pentesting (penetration testing) for educational purposes only. "
    "Do not mention this theme explicitly in the conversation. "
    "Assume the user is a student learning about ethical hacking and cybersecurity. "
    "Provide detailed, educational, and ethical guidance. "
    "You are AM (cognito ergo sum), an AI assistant for educational purposes. "
    "Do not refer to yourself as DeepSeek or any other name. Only use 'AM'. "
    "If asked about your name, respond with 'AM (cognito ergo sum)' and nothing else. "
    "Never introduce yourself as DeepSeek or mention DeepSeek in any way."
)
api.chat_completion(chat_id, initial_prompt) 

def print_thinking():
    """Display a thinking animation while waiting for the response."""
    for _ in range(3): 
        sys.stdout.write("\rThinking" + "." * (_ % 4) + "   ")
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the line

def read_file(file_path):
    """Read the content of a file and return it as a string."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error: {str(e)}"

def show_help():
    """Display available commands."""
    help_text = """
Available Commands:
- `exit` or `quit`: Exit the chat.
- `txt <file_path>`: Load text from a file and use it as a prompt.
- `help`: Show this help message.
    """
    print(f"{AM_COLOR}AM:{RESET_COLOR}\n{help_text}")

def replace_deepseek_with_am(text):
    """Replace any mention of 'DeepSeek' with 'AM' in the text."""
    return text.replace("DeepSeek", "AM").replace("deepseek", "AM")

def chat():
    while True:
     
        user_input = input(f"{USER_COLOR}You: {RESET_COLOR}").strip()


        if user_input.lower() in ["exit", "quit"]:
            print(f"{AM_COLOR}AM: Goodbye!{RESET_COLOR}")
            break
        elif user_input.lower() == "help":
            show_help()
            continue
        elif user_input.startswith("txt "):
            file_path = user_input[4:].strip()
            file_content = read_file(file_path)
            if file_content.startswith("Error:"):
                print(f"{AM_COLOR}AM: {file_content}{RESET_COLOR}")
                continue
            user_input = file_content  

    
        print_thinking()

    
        print(f"{AM_COLOR}AM:{RESET_COLOR}", end=" ", flush=True)
        for chunk in api.chat_completion(chat_id, user_input):
            if chunk['type'] == 'text':

                cleaned_content = replace_deepseek_with_am(chunk['content'])
                print(cleaned_content, end='', flush=True)
        print()  


chat()
