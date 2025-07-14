
import subprocess
import sys

if __name__ == "__main__":
    # Run the Streamlit app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "5000"])
