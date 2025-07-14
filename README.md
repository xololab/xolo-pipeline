<p align="center">
  <img src="docs/assets/logo.png" alt="Xolo Logo" width="200"/>
</p>

<p align="center">
  <strong>Xolo Pipeline</strong><br>

</p>


**Xolo Pipeline** is a modular, cross-platform, open source pipeline framework built with Python and [`uv`](https://github.com/astral-sh/uv). It’s designed for **freelancers**, **solo artists**, and **small studios** working in VFX, animation, and digital content creation.

Inspired by [Prism Pipeline](https://prism-pipeline.com/) and [TikManager](https://github.com/masqu3rad3/tik_manager4), Xolo Pipeline is built from the ground up to be lightweight, easy to install, and extensible.

---

## ✨ Features

- ✅ Cross-platform: works on **Windows**, **Linux**, and **macOS** (not tested yet)
- 🔌 Modular CLI powered by [`typer`](https://typer.tiangolo.com/)
- ☁️ Compatible with local disk, cloud sync (Google Drive, Dropbox), or NAS
- 🧪 Simple local development using only `uv` (no global Python installation required)

---

## 🚀 Installation

To get started, you only need:

- [`uv`](https://github.com/astral-sh/uv)
- `git`

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/ronnyascencio/xolo-pipeline.git
cd xolo-pipeline

# Create and activate a virtual environment with Python 3.11
uv venv --python=python3.11
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies (if any are listed in pyproject.toml)
uv pip install -r requirements.txt  # or just `uv pip install .` if packaged
uv sync # this works too
```
🧰 Usage

Once installed, you can run the CLI from anywhere inside the environment using:
```bash

xolo
```
For example:
``` bash
xolo [COMMAND]
```
More commands will be available as the pipeline evolves.

💡 Project Philosophy

Xolo Pipeline is built to:

    Reduce the technical barrier for solo creators

    Provide intuitive CLI tooling without complex infrastructure

    Avoid database or server dependencies

    Be extensible as your team or needs grow

☁️ Storage Support

    ✅ Local disk (default)

    🔄 Cloud-sync folders (Google Drive, Dropbox, OneDrive)

    🗃️ NAS/shared network storage

    Planned: centralized config via remote JSON/YAML

📈 Roadmap Highlights

CLI scaffold with typer

Project initialization command

Versioning system for assets and shots

Maya, Nuke, Gaffer and Blender integration modules

Task tracking and review tools

    Optional frontend (web or Qt)

Track progress on GitHub Projects.
🆚 Why Xolo Pipeline?

    🎯 Simple setup — uv handles Python + virtualenv in one step

    🧳 Ideal for freelancers/small studios — no pipeline engineer required

    🔧 Modular structure — easy to extend and customize

    ☁️ Flexible storage — works locally or in the cloud

    📦 Open Source — MIT licensed, no lock-in

    🌍 Cross-platform — works on all major OSs

🤝 Contributing

You can help by:

    Submitting issues or feature ideas

    Improving the docs

    Building integration modules

    Testing on other OSs or setups

Steps to contribute:

    Fork this repo

    Create a feature branch

    Commit your changes

    Open a pull request

📄 License

MIT License — free for commercial or personal use. See LICENSE for full details.
👨‍💻 Author

Ronny Ascencio
Python developer & digital artist
GitHub: @ronnyascencio
Website: ronnyascencio.com
