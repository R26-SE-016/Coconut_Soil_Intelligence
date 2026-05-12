import subprocess
import time
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def run_system():
    print("Starting Coconut Soil Intelligence System...")
    
    #Start Backend
    print("Starting Backend API on http://localhost:5000...")
    backend_proc = subprocess.Popen([sys.executable, "src/app.py"], cwd=ROOT_DIR)
    
    time.sleep(2)
    
    print("Starting Dashboard Frontend...")
    try:
        frontend_proc = subprocess.Popen(["npm", "run", "dev"], cwd=ROOT_DIR / "dashboard", shell=True)
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down system...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    run_system()
