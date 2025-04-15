# ghostenv (chmod +x or ghostenv.py with entrypoint setup)

import argparse
import sys
from pathlib import Path
from loader import main as loader_main

def main():
    parser = argparse.ArgumentParser(description="Ghostenv: venv in RAM")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a script in an sandbox")
    run_parser.add_argument("script", help="Path to Python script")
    run_parser.add_argument("--requirements", help="requirements.txt path")
    run_parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments for script")

    args = parser.parse_args()

    if args.command == "run":
        sys.argv = ["loader.py", args.script]
        if args.requirements:
            sys.argv.append(args.requirements)
        sys.argv += args.script_args
        loader_main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
