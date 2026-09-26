"""
F.R.I.D.A.Y. Universal Bootstrap Installer.
Cross-platform installation script (Windows, macOS, Linux).
Installs system dependencies, Python packages, and configures environments from 0 to 100.
"""

import os
import sys
import platform
import subprocess
import shutil

def print_step(msg):
    print(f"\n[{'='*50}]")
    print(f"🚀 {msg}")
    print(f"[{'='*50}]\n")

def run_cmd(cmd, shell=True, check=True):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=shell, check=check)

def install_system_dependencies():
    os_name = platform.system().lower()
    print_step(f"Detecting Operating System: {os_name.upper()}")

    if os_name == "linux":
        print("Checking for apt-get...")
        if shutil.which("apt-get"):
            run_cmd("sudo apt-get update")
            run_cmd("sudo apt-get install -y ffmpeg tesseract-ocr portaudio19-dev python3-dev build-essential")
        elif shutil.which("dnf"):
            run_cmd("sudo dnf install -y ffmpeg tesseract portaudio-devel python3-devel")
        else:
            print("⚠️ Package manager not found. Please manually install: ffmpeg, tesseract-ocr, portaudio.")

    elif os_name == "darwin": # macOS
        print("Checking for Homebrew...")
        if shutil.which("brew"):
            run_cmd("brew install ffmpeg tesseract portaudio")
        else:
            print("⚠️ Homebrew not installed. Install it from https://brew.sh to get system dependencies.")

    elif os_name == "windows":
        print("Checking for Winget or Chocolatey...")
        if shutil.which("winget"):
            run_cmd("winget install --exact --accept-package-agreements --accept-source-agreements Gyan.FFmpeg")
            run_cmd("winget install UB-Mannheim.TesseractOCR")
        elif shutil.which("choco"):
            run_cmd("choco install -y ffmpeg tesseract")
        else:
            print("⚠️ Winget/Chocolatey not found. Please manually install FFmpeg and Tesseract for Windows.")

def setup_python_environment():
    print_step("Setting up Python dependencies")
    
    # Upgrade pip
    run_cmd(f"{sys.executable} -m pip install --upgrade pip")
    
    # Install requirements
    if os.path.exists("requirements.txt"):
        run_cmd(f"{sys.executable} -m pip install -r requirements.txt")
    else:
        print("⚠️ requirements.txt not found!")

def install_browser_binaries():
    print_step("Installing Playwright Agentica Browser Binaries")
    try:
        run_cmd(f"{sys.executable} -m playwright install --with-deps chromium")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to install Playwright browser dependencies. You may need to run 'playwright install' manually.")

def install_local_ai_runtime():
    print_step("Installing Local AI Model Runtime (Ollama / llama.cpp)")
    if shutil.which("ollama"):
        print("✅ Ollama is already installed and available on PATH.")
        return

    os_name = platform.system().lower()
    try:
        if os_name == "windows" and shutil.which("winget"):
            print("Installing Ollama via Winget...")
            run_cmd("winget install --exact --accept-package-agreements --accept-source-agreements Ollama.Ollama")
        elif os_name == "linux":
            print("Installing Ollama via official installer...")
            run_cmd("curl -fsSL https://ollama.com/install.sh | sh")
        elif os_name == "darwin" and shutil.which("brew"):
            print("Installing Ollama via Homebrew...")
            run_cmd("brew install --cask ollama")
        else:
            print("⚠️ Notice: To run models 100% locally, download Ollama from https://ollama.com")
    except Exception as e:
        print(f"⚠️ Could not automatically install Ollama: {e}")

def initialize_directories():
    print_step("Initializing F.R.I.D.A.Y. Directories")
    dirs = ["data", "data/models", "logs", "workspace"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✅ Created directory: {d}")

if __name__ == "__main__":
    print("""
    =========================================================
                 F.R.I.D.A.Y. UNIVERSAL INSTALLER
    =========================================================
    This script will configure your entire operating system
    to run F.R.I.D.A.Y. locally.
    """)
    
    try:
        install_system_dependencies()
        setup_python_environment()
        install_browser_binaries()
        install_local_ai_runtime()
        initialize_directories()
        
        print_step("F.R.I.D.A.Y. INITIALIZATION COMPLETE")
        print("You are ready to boot the system.")
        print(f"Run: {sys.executable} friday_engine/core/engine.py")
        
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)
