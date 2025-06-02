# 🚀 Getting Started with Xolo Pipeline

This guide helps you set up and run your first project using Xolo Pipeline.

## 🛠️ Requirements

- [`uv`](https://github.com/astral-sh/uv)
- `git`

## 📥 Installation

```bash
git clone https://github.com/ronnyascencio/xolo-pipeline.git
cd xolo-pipeline
uv venv --python=python3.11
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
uv sync

```
🧰 Running the CLI

Once installed:
```
xolo --help
```
Example:
```
xolo create-project my_project
```
More commands and functionality will be available as the CLI grows.


🧠 Philosophy

    Minimal setup and infrastructure

    No database, no web server required

    Modular and extensible for future tools and integrations

Need Help?

Feel free to open an Issue or start a Discussion.