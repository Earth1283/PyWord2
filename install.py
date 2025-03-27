import subprocess
import sys
import urllib.request
import importlib

# Function to check if PyQt5 is installed
def check_pyqt5_installed():
    try:
        importlib.import_module('PyQt5')
        print("PyQt5 is already installed.")
        return True
    except ImportError:
        return False

# Function to install PyQt5
def install_pyqt5():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
        print("PyQt5 successfully installed using pip3.")
    except subprocess.CalledProcessError:
        print("pip3 installation failed, trying pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
            print("PyQt5 successfully installed using pip.")
        except subprocess.CalledProcessError:
            print("Failed to install PyQt5. Exiting.")
            sys.exit(1)

# Function to download the main.py script
def download_main_py():
    url = "https://raw.githubusercontent.com/Earth1283/PyWord2/main/main.py"
    local_filename = "main.py"
    try:
        urllib.request.urlretrieve(url, local_filename)
        print(f"{local_filename} downloaded successfully.")
    except Exception as e:
        print(f"Failed to download {local_filename}. Error: {e}")
        sys.exit(1)

# Main function to run the steps
def main():
    if not check_pyqt5_installed():
        install_pyqt5()
    download_main_py()

if __name__ == "__main__":
    main()
