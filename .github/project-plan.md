# Project Plan for XOLO Pipeline

This document defines the complete roadmap, task breakdown, and progress tracking structure for the development of the **XOLO Pipeline**, a lightweight and user-friendly pipeline for animation, VFX, and commercials.

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

### Issue: Research Katana vs Gaffer integration
**Description:**
Evaluate pros and cons of integrating Katana vs Gaffer in the pipeline. Include compatibility with OCIO and 3Delight.

### Issue: Authentication system for production tracker
**Description:**
Define and implement login mechanism (JWT-based) to access the web UI of the production tracker.

### Issue: Server deployment strategy (local vs cloud)
**Description:**
Define hosting strategy and requirements for running the backend locally or on studio servers.

### Issue: Implement publishing MP4 previews via ffmpeg
**Description:**
Convert image sequences or stills to low-resolution MP4s during publishing for preview on the web UI. Integrate `ffmpeg-python`.

### Issue: Create plugin base structure for Houdini
**Description:**
Set up a directory and module for Houdini integration. Include sample launch file and UI placeholder.

### Issue: Create plugin base structure for Nuke
**Description:**
Prepare directory structure for Nuke integration with a simple panel UI and publishing hook.

### Issue: Create plugin base structure for Gaffer
**Description:**
Implement starter plugin code for Gaffer with metadata ingestion and environment hooks.

### Issue: Add thumbnail generation script
**Description:**
Create utility function to extract a thumbnail from MP4 using ffmpeg and store it next to the publish.

### Issue: Full ingest tool integration with Nuke Studio / Hero
**Description:**
Enable ingesting sequence and shot structure directly from the Nuke Studio / Hero timeline. Allow artist to select clips, define handles (default 10 frames), convert media to EXR, and auto-create shot folders. Published EXRs and metadata must be updated in the frontend/backend.

### Issue: Create internal documentation website with MkDocs
**Description:**
Generate developer and user documentation from docstrings and Markdown files using MkDocs and Material theme.

### Issue: Implement async task queue for publishing
**Description:**
Queue publishing jobs and run in background using Python async or Celery for scalability.

---

## ✅ To Do

### Issue: Implement `xolo init` command
**Description:**
Create CLI command to initialize a new project. Prompt user for project name, root path, and global asset directory.

### Issue: Configure global settings YAML
**Description:**
Store default paths, OCIO configuration, and metadata in a central YAML file that is editable via CLI.

### Issue: Implement `xolo launch` command
**Description:**
Allow users to launch a DCC (e.g., Nuke, Maya) from the CLI with the appropriate environment variables preloaded.

### Issue: Define backend API structure with FastAPI
**Description:**
Plan and scaffold the backend endpoints: `/projects`, `/shots`, `/tasks`, `/users`, etc.

### Issue: Create web UI skeleton with placeholder pages
**Description:**
Implement basic layout in `frontend/` using a modern frontend framework. Include pages: Dashboard, Shots, Settings.

### Issue: CLI option to create shots manually
**Description:**
Add support in CLI to manually create sequences and shots, with automatic folder creation and metadata tracking.

### Issue: Add CLI option to choose Nuke Studio or manual ingest
**Description:**
Let user decide whether to ingest timeline automatically or create manually when running `xolo ingest` command.

### Issue: Implement API endpoint to receive publishes
**Description:**
Create FastAPI route to receive publish metadata and store it in the database with thumbnail.

### Issue: Display publishes and thumbnails in frontend
**Description:**
Render list of published versions and show embedded thumbnails or preview video.

### Issue: Assign task status (in progress, done, approved)
**Description:**
Enable setting status per task or shot in the frontend, synced with backend.

---

## 🚧 In Progress

### Issue: Set up monorepo structure
**Description:**
Implement the proposed monorepo layout with `cli/`, `core/`, `dcc/`, `backend/`, and `frontend/` modules.

### Issue: Define pyproject.toml and sync with `uv`
**Description:**
Configure project metadata, dependencies, dev tools and `xolo` script entry point. Test build and sync.

---

## ✅ Done

### Issue: Create GitHub organization `xololab`
**Description:**
Set up new GitHub organization to host pipeline codebase and future plugins.

### Issue: Move existing repository and restructure layout
**Description:**
Transferred original repository to new organization and reorganized folder structure into modular format.

---

## 📝 Next Steps
- Set up GitHub Project board using this structure.
- Convert each item here into a GitHub Issue and link them to the board.
- Define a `CONTRIBUTING.md` and open the project to collaboration.

---

*Maintained by [@ronnyascencio](https://github.com/ronnyascencio) at [XOLO Lab](https://github.com/xololab)*
