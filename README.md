# 🛡️ EnvGuard

**EnvGuard** is a lightweight CLI tool designed to audit your environment variables. It helps developers identify unused variables in `.env` files and detects variables used in the source code that are missing from the environment configuration.

## 🚀 Features

- **Unused Variable Detection**: Scans your `.env` files and compares them with your codebase.
- **Missing Variable Alerts**: Identifies where your code expects an environment variable that isn't defined.
- **Multi-language Support**: Scans Python, JavaScript, TypeScript, Go, and more.
- **Zero Dependencies**: Built using only Python standard libraries.

## 📦 Installation

Simply clone the repository and run the script:

```bash
git clone https://github.com/yourusername/envguard.git
cd envguard
```

## 🛠️ Usage

Run EnvGuard in your project root:

```bash
python3 envguard.py /path/to/your/project
```

## 📊 Example Output

```text
--- EnvGuard Audit for ./my-awesome-project ---

[+] Env files found: ['.env', '.env.example']

[!] Unused variables in .env files (2):
  - DEBUG_OLD_KEY
  - TEMP_API_URL

[!] Variables used in code but missing from .env (1):
  - NEW_STRIPE_KEY

--- End of Audit ---
```

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

MIT License.
