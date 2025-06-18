# Project Plan for XOLO Pipeline

This document defines the complete roadmap, task breakdown, and progress tracking structure for the development of the **XOLO Pipeline**, a lightweight, modular, and user-friendly pipeline for animation, VFX, and commercials. It is designed to support individual artists and small studios, with scalability toward networked or cloud workflows.

---

## 🔄 Columns

| Backlog | To Do | In Progress | Review | Done |
|--------|-------|-------------|--------|------|
| Ideas and future tasks not yet prioritized | Tasks ready to be picked up | Tasks actively being worked on | Tasks waiting to be validated or tested | Completed tasks |

---

## 🗃️ Backlog

### Issue: Create plugin base structure for Maya  
**Description:**  
Prepare base directory and module layout to integrate a Maya-specific plugin inside the `dcc/` folder. Include entry point and basic UI placeholder.

### Issue: Create plugin base structure for Houdini  
**Description:**  
Set up a directory and module for Houdini integration. Include sample launch file and UI placeholder.

### Issue: Create plugin base structure for Nuke  
**Description:**  
Prepare directory structure for Nuke integration with a simple panel UI and publishing hook.

### Issue: Create plugin base structure for Gaffer  
**Description:**  
Implement starter plugin code for Gaffer with metadata ingestion and environment hooks. Include OCIO and 3Delight support.

### Issue: Research Katana vs Gaffer integration  
**Description:**  
Evaluate pros and cons of integrating Katana vs Gaffer. Assess compatibility with OCIO and 3Delight.

### Issue: Authentication system for production tracker  
**Description:**  
Define and implement JWT-based login mechanism to access the web UI of the production tracker.

### Issue: Server deployment strategy (local vs cloud)  
**Description:**  
Define hosting strategy and requirements for running the backend locally or on studio servers.

### Issue: Implement publishing MP4 previews via ffmpeg  
**Description:**  
Convert image sequences or stills to low-resolution MP4s during publishing for preview on the web UI. Integrate `ffmpeg-python`.

### Issue: Add thumbnail generation script  
**Description:**  
Create utility function to extract a thumbnail from MP4 using `ffmpeg` and store it next to the publish.

### Issue: Full ingest tool integration with Nuke Studio / Hero  
**Description:**  
Enable ingesting sequence and shot structure directly from Nuke Studio or Hero timeline. Convert to EXR, auto-create folders, and update metadata.

### Issue: Create internal documentation website with MkDocs  
**Description:**  
Generate developer and user documentation from docstrings and Markdown using MkDocs with Material theme.

### Issue: Implement async task queue for publishing  
**Description:**  
Queue publishing jobs and run in background using `asyncio` or `Celery` for scalability.

### Issue: Implement Pyblish for all DCC publishes  
**Description:**  
Use Pyblish to manage validation and publishing workflow across DCCs like Nuke, Maya, Houdini, and Gaffer.

### Issue: Evaluate Perforce integration  
**Description:**  
Research integration with Perforce for asset version control and team collaboration.

---

## ✅ To Do

### Issue: Implement `xolo init` command  
**Description:**  
Create CLI command to initialize a new project. Prompt user for project name, root path, and global asset directory.

### Issue: Configure global settings YAML  
**Description:**  
Store default paths, OCIO configuration, project type, resolution, and metadata in a central YAML file editable via CLI.

### Issue: Implement `xolo launch` command  
**Description:**  
Allow users to launch DCCs (e.g., Nuke, Maya, Houdini) from the CLI with correct environment variables.

### Issue: Define backend API structure with FastAPI  
**Description:**  
Design and scaffold backend routes: `/projects`, `/shots`, `/assets`, `/tasks`, `/users`, `/publishes`.

### Issue: Create web UI skeleton with Astro  
**Description:**  
Build basic layout in `frontend/` using Astro (without React). Include: Dashboard, Shots, Versions, Settings.

### Issue: CLI option to create shots manually  
**Description:**  
Add support in CLI to manually create sequences and shots, auto-creating folder structures and metadata YAMLs.

### Issue: Add CLI option to choose Nuke Studio or manual ingest  
**Description:**  
Let user decide whether to ingest timeline automatically or create manually when running `xolo ingest`.

### Issue: Implement API endpoint to receive publishes  
**Description:**  
Create FastAPI route to receive publish metadata and store it in a file-based or future DB system.

### Issue: Display publishes and thumbnails in frontend  
**Description:**  
Render published versions with embedded thumbnails or MP4 preview videos.

### Issue: Assign task status (In Progress, Done, Approved)  
**Description:**  
Enable frontend and backend sync of task/shot status updates with visual indicators.

### Issue: Implement `xolo settings` CLI command  
**Description:**  
Allow user to view or modify global or per-project settings via CLI using `Typer`.

### Issue: Add OCIO config auto-load  
**Description:**  
Auto-load and inject OCIO environment variables when launching a DCC or creating a project.

### Issue: Create `project_type.yaml` templates  
**Description:**  
Define YAML templates for each project type (animation, VFX, commercial, short). Each template includes default folders, resolution, and metadata.

### Issue: Versioned file and folder naming system  
**Description:**  
Standardize `v001`/`v002` naming in both folders and files. Ensure version match between metadata, file, and folder.

### Issue: Use `rich` for CLI formatting  
**Description:**  
Improve terminal output using `rich` for colors, tables, syntax highlighting, and progress bars.

---

## 🚧 In Progress

### Issue: Set up monorepo structure  
**Description:**  
Implement the proposed monorepo layout with `cli/`, `core/`, `dcc/`, `backend/`, and `frontend/`.

### Issue: Define `pyproject.toml` and sync with `uv`  
**Description:**  
Configure project metadata, dependencies, dev tools, and entry points. Ensure `uv` sync works across submodules.

---

## ✅ Done

### Issue: Create GitHub organization `xololab`  
**Description:**  
Set up GitHub org to host the XOLO pipeline and future plugins/tools.

### Issue: Move existing repository and restructure layout  
**Description:**  
Reorganize repo into modular structure for CLI, DCCs, frontend, and backend.

---

## 📝 Next Steps

- Set up GitHub Project board using this document as reference.
- Convert each item into GitHub Issues and link them to the appropriate column.
- Create `CONTRIBUTING.md`, `LICENSE`, and `README.md` for contributors.
- Begin development with core CLI commands and project scaffolding.

---

*Maintained by [@ronnyascencio](https://github.com/ronnyascencio) at [XOLO Lab](https://github.com/xololab)*
