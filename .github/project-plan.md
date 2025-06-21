# 🛠️ Project Plan for XOLO Pipeline

This document defines the complete roadmap, task breakdown, and progress tracking structure for the development of the **XOLO Pipeline**, a lightweight, modular, and user-friendly pipeline for animation, VFX, and commercials. It is designed to support individual artists and small studios, with scalability toward networked or cloud workflows.

---

## 🔄 Columns

| Column        | Description                                      |
|---------------|--------------------------------------------------|
| **Backlog**   | Ideas and future tasks not yet prioritized       |
| **To Do**     | Tasks ready to be picked up                      |
| **In Progress** | Tasks actively being worked on                |
| **Review**    | Tasks waiting to be validated or tested          |
| **Done**      | Completed tasks                                  |


### Create plugin base structure for Maya
**Labels:** `dcc`  
Prepare base directory and module layout to integrate a Maya-specific plugin inside the `dcc/` folder. Include entry point, basic UI placeholder (using PyQt/PySide), and example environment setup.

### Create plugin base structure for Houdini
**Labels:** `dcc`  
Set up a directory and module for Houdini integration. Include sample launch file, UI placeholder, and environment hooks.

### Research Katana vs Gaffer integration
**Labels:** `dcc`, `enhancement`  
Evaluate pros and cons of integrating Katana vs Gaffer. Assess compatibility with OCIO and 3Delight, focusing on ease of setup and cost for small studios.

### Authentication system for production tracker
**Labels:** `backend`, `enhancement`, `security`  
Define and implement JWT-based login mechanism to access the web UI. Requires backend user management and frontend login/registration flow.

### Server deployment strategy (local vs cloud)
**Labels:** `backend`, `deployment`  
Define hosting strategy and requirements for local and cloud deployment.

### Implement publishing MP4 previews via ffmpeg
**Labels:** `backend`, `frontend`, `media`  
Convert EXR or stills to MP4 for web UI preview using `ffmpeg`. Trigger post-publish in backend.

### Add thumbnail generation script
**Labels:** `backend`, `frontend`, `media`, `enhancement`  
Generate thumbnails from MP4 or frames using `ffmpeg` for quick visual reference.

### Implement async task queue for publishing
**Labels:** `backend`, `enhancement`  
Use asyncio or Celery to queue publishing tasks and avoid blocking API threads.

### Implement Pyblish for all DCC publishes
**Labels:** `dcc`  
Develop Pyblish collectors, validators, and extractors for all supported DCCs.

### Evaluate Perforce integration
**Labels:** `enhancement`, `version_control`  
Assess Perforce integration for asset versioning and team collaboration.

### Asset Type Definition and Management
**Labels:** `core`, `backend`, `enhancement`  
Define `core/asset_types.yaml` with default folder structures and naming for each asset type.

### Pipeline Configuration Schema Validation
**Labels:** `core`, `cli`, `backend`, `enhancement`  
Use Pydantic to validate YAML files like `global_settings.yaml` and `project_type.yaml`.

### Implement Health Check Endpoint for Backend
**Labels:** `backend`, `monitoring`  
Add `/health` FastAPI route to validate backend and DB status.

### Add Basic CLI Testing Framework (Pytest)
**Labels:** `cli`, `testing`  
Setup unit/integration tests for CLI commands.

### Add Basic Backend API Testing Framework (Pytest)
**Labels:** `backend`, `testing`  
Setup testing framework using `httpx` or `TestClient`.

### Implement Basic Cache Management for DCCs (Optional)
**Labels:** `dcc`, `enhancement`, `performance`  
Add caching for frequently used data in DCC plugins.



### Core Data Model Definition (Pydantic/DB Schema)
**Labels:** `backend`, `core`, `priority: high`  
Design Pydantic models and DB schema for Project, Task, Asset, Version, and User.

### Basic User Authentication in Backend
**Labels:** `backend`, `security`, `priority: high`  
Add simple API key/session-based auth for dev phase.

### Implement `xolo init` command
**Labels:** `cli`, `priority: high`  
Create project structure from YAML template and register with backend.

### Configure global settings YAML
**Labels:** `cli`, `core`  
Store OCIO paths, executable paths, and pipeline defaults in YAML config.

### Implement `xolo launch` command
**Labels:** `cli`, `dcc`, `priority: high`  
Launch DCCs with environment setup using CLI and backend config.

### Define backend API structure with FastAPI
**Labels:** `backend`, `priority: high`  
Create routes for `/projects`, `/tasks`, `/assets`, `/versions`, `/users`, `/config`.

### Create web UI skeleton with Astro
**Labels:** `frontend`  
Design basic Astro layout with dashboard, projects, shots, tasks, and settings.

### Implement `xolo settings` CLI command
**Labels:** `cli`  
View and edit global/project settings via CLI.

### Add OCIO config auto-load
**Labels:** `cli`, `core`, `priority: high`  
Automatically set OCIO env var when launching DCCs or creating projects.

### Create `project_type.yaml` templates
**Labels:** `core`  
Template default folders, resolutions, metadata for each project type.

### Versioned file and folder naming system
**Labels:** `core`, `priority: high`  
Design consistent naming system like `asset_v001`, `shot_v003`.

### Ingest tool with Nuke Studio / Hero (Phase 1: OTIO Parsing)
**Labels:** `dcc`, `enhancement`, `priority: high`  
Parse OTIO to extract sequence/shot info for ingesting.

### Implement API endpoint to receive publishes
**Labels:** `backend`, `priority: high`  
Add `POST /publishes` to register versions and metadata from DCCs.

### Create plugin base structure for Nuke
**Labels:** `dcc`  
Directory for Nuke panel UI and publishing hook.

### Base DCC Python Library
**Labels:** `dcc`, `core`, `priority: high`  
Create `core/dcc_utils.py` with shared DCC helper functions.



### Set up monorepo structure
**Labels:** `core`, `cli`, `backend`, `frontend`, `dcc`  
Organize codebase into `cli/`, `backend/`, `frontend/`, `dcc/`, `core/`.

### Define `pyproject.toml` and sync with `uv`
**Labels:** `core`, `cli`  
Setup dependencies, dev tools, and CLI entry point in `pyproject.toml`.





### Create GitHub organization `xololab`
**Labels:** `documentation`  
Set up GitHub org to host XOLO pipeline and future tools/plugins.

### Move existing repository and restructure layout
**Labels:** `core`, `cli`, `backend`, `frontend`, `dcc`  
Restructure into monorepo with proper modular layout.



**Maintained by [@ronnyascencio](https://github.com/ronnyascencio) at XOLO Lab**
