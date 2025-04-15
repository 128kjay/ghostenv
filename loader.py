import os
import sys
import shutil
import subprocess
import tempfile
import venv
from pathlib import Path

def create_venv(temp_dir):
    print(f"[+] Creating virtual environment in RAM at: {temp_dir}")
    venv.create(temp_dir, with_pip=True)
    python_bin = Path(temp_dir) / ("Scripts" if os.name == "nt" else "bin") / "python"
    return str(python_bin)

def run_in_venv(python_bin, script_path, requirements=None):
    env = os.environ.copy()

    # Redirect cache/temp
    env["TMPDIR"] = str(Path(python_bin).parent.parent)
    env["PYTHONPYCACHEPREFIX"] = str(Path(python_bin).parent.parent / "__pycache__")

    if requirements:
        print(f"[+] Installing dependencies from: {requirements}")
        subprocess.check_call([python_bin, "-m", "pip", "install", "-r", requirements], env=env)

    print(f"[+] Running script: {script_path}")
    subprocess.run([python_bin, script_path], env=env)

def cleanup(temp_dir):
    print(f"[+] Cleaning up temporary environment at: {temp_dir}")
    shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: loader.py <script.py> [requirements.txt]")
        return

    script_path = sys.argv[1]
    requirements = sys.argv[2] if len(sys.argv) > 2 else None

    temp_dir = tempfile.mkdtemp(prefix="ram_venv_")
    try:
        python_bin = create_venv(temp_dir)
        run_in_venv(python_bin, script_path, requirements)
    finally:
        cleanup(temp_dir)

if __name__ == "__main__":
    main()
