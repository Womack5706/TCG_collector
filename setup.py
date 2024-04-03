import subprocess
import sys

def install_dependencies():
    """Install required dependencies."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies.")
        sys.exit(1)

def update_dependencies():
    """Update installed dependencies."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to update dependencies.")
        sys.exit(1)

def create_executable():
    """Create executable for TCG_collector.py."""
    try:
        subprocess.run(["pyinstaller", "TCG_collector.py", "--onefile", "--windowed", "--icon", "C:/Yu-gi-oh/yugioh.ico"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to create executable.")
        sys.exit(1)


def main():
    print("Installing dependencies...")
    install_dependencies()

    print("Updating dependencies...")
    update_dependencies()

    print("Creating executable...")
    create_executable()

    print("Setup completed successfully.")

if __name__ == "__main__":
    main()
