# ML Learning Hub

ML Learning Hub is an interactive Streamlit-based learning platform for practical machine learning, featuring lessons, quizzes, auto-graded coding challenges, streaks, and a project workflow.

Quick start

1. Create and activate a virtual environment:

   Windows (PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
streamlit run app_main.py --server.port 8502
```

Open http://localhost:8502 in your browser.

Files of interest

- `app_main.py`: main Streamlit application
- `database/progress.db`: SQLite DB (auto-created)
- `challenges/`: JSON definitions for quizzes and code tasks
- `docs/SETUP.md`: setup and deployment notes

Contributing

Please create issues or PRs for enhancements, and keep the `requirements.txt` updated for reproducible environments.
