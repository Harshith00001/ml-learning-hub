# Setup & Deployment

This document describes how to run the ML Learning Hub locally and notes for simple deployments.

Prerequisites

- Python 3.11+ (3.10 may work; 3.11 recommended)
- Git (optional)

Local Setup (Windows)

1. Create a virtual environment and activate it (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Launch the app (default port 8502):

```bash
streamlit run app_main.py --server.port 8502
```

4. Open `http://localhost:8502` in your browser.

Notes

- The SQLite file `database/progress.db` is created automatically on first run. Ensure the `database/` folder is writable and persisted if deploying to a hosted environment.
- To reset progress during development, delete `database/progress.db` (note: this removes all saved user progress).

Deployment

- For lightweight hosting consider Streamlit Community Cloud. For production use a containerized approach (Docker) or a managed VM.
- Ensure you persist the `database/progress.db` file across restarts or use a hosted DB for multi-instance deployments.

Creating a `requirements.txt`

Run:

```bash
pip freeze > requirements.txt
```

Then commit `requirements.txt` to the repo.
