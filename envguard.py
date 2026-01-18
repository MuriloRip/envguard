import os
import re
import sys
import argparse
from pathlib import Path

class EnvGuard:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.env_vars = set()
        self.found_vars = set()
        self.secrets_patterns = {
            "AWS Key": r"AKIA[0-9A-Z]{16}",
            "Generic Secret": r"(?i)secret|password|token|key",
            "IPv4 Address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        }

    def load_env_files(self):
        env_files = list(self.project_path.glob("*.env*"))
        for env_file in env_files:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key = line.split("=")[0].strip()
                        self.env_vars.add(key)
        return env_files

    def scan_code(self):
        extensions = [".py", ".js", ".ts", ".go", ".java", ".cpp"]
        for ext in extensions:
            for path in self.project_path.rglob(f"*{ext}"):
                if "node_modules" in str(path) or ".git" in str(path):
                    continue
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
                    # Look for common env access patterns
                    patterns = [
                        r"os\.environ\.get\(['\"](\w+)['\"]\)",
                        r"os\.getenv\(['\"](\w+)['\"]\)",
                        r"process\.env\.(\w+)",
                        r"env\(['\"](\w+)['\"]\)"
                    ]
                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        self.found_vars.update(matches)

    def audit(self):
        print(f"--- EnvGuard Audit for {self.project_path} ---")
        env_files = self.load_env_files()
        self.scan_code()

        unused = self.env_vars - self.found_vars
        missing = self.found_vars - self.env_vars

        print(f"\n[+] Env files found: {[f.name for f in env_files]}")
        
        if unused:
            print(f"\n[!] Unused variables in .env files ({len(unused)}):")
            for var in unused:
                print(f"  - {var}")
        else:
            print("\n[✓] No unused variables found in .env files.")

        if missing:
            print(f"\n[!] Variables used in code but missing from .env ({len(missing)}):")
            for var in missing:
                print(f"  - {var}")
        
        print("\n--- End of Audit ---")

def main():
    parser = argparse.ArgumentParser(description="EnvGuard: Audit your environment variables.")
    parser.add_argument("path", nargs="?", default=".", help="Path to the project to audit")
    args = parser.parse_args()

    guard = EnvGuard(args.path)
    guard.audit()

if __name__ == "__main__":
    main()
