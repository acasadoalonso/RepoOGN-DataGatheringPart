# Copilot instructions for RepoOGN-DataGatheringPart

Purpose: brief, actionable repository guidance so Copilot sessions can find build/test/lint commands, understand high-level architecture, and respect conventions used here.

---

## 1) Build, test, and lint commands

Python environment (CI uses Python 3.9):
- Install deps (local):
  - python3 -m pip install --upgrade pip
  - python3 -m pip install -r requirements.txt
- Lint (same flags as CI):
  - flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  - flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
- Lint a single file:
  - flake8 path/to/file.py --max-line-length=127

Tests:
- Run full suite: pytest
- Run a single test (example): pytest tests/test_mod.py::test_function_name
  - or run by keyword: pytest -k "keyword"

C/autotools (calcelestial):
- Build: cd calcelestial && ./configure && make
- Install (if needed): sudo make install or run provided sh/calcelestial.sh which bundles build+install

Docker:
- Build (example): docker build -f dockerfiles/Dockerfile -t sarogn:local .
- Many docker helper scripts are under dockerfiles/ and provisioning/.

Installation helper scripts:
- ./install.sh and provisioning/* are used for bare-metal or VM setup. Review install.sh before running.

CI:
- GitHub Actions workflow .github/workflows/python-app.yml installs flake8 and pytest, then runs the same lint/test commands above.

---

## 2) High-level architecture (concise)

- Purpose: collect APRS/OGN/ADSB/FLARM telemetry, detect flights, generate .IGC files, and store records locally and centrally.

- Main components:
  - SARprocessogn.py: core processor. Reads daily DATAyyyymmdd.log files, parses messages, detects flights, writes .IGC and DB entries.
  - ogndb/: database utilities, parserfuncs.py (OGN/APRS parsing), DBcreate.py, and DBschema.sql for SQLite/MySQL schemas.
  - sh/: orchestration/scheduling scripts (SARpogn.sh runs at sunset, SARflight_logger.sh at sunrise, etc.).
  - dockerfiles/: containerized deployment (Python + MariaDB etc.).
  - provisioning/: Ansible/Vagrant playbooks for host provisioning.
  - calcelestial/: bundled C utility (autotools); used for sunrise/sunset calculations and scheduling.

- Data flow (simple): ingestion (DATA*.log) → SARprocessogn parses/fights detection → local SQLite (ogndb/SAROGN.db) → periodic sync to central MySQL/MariaDB via sh/SARpogn.sh.

- Configuration locations:
  - Primary runtime config: /etc/local/SARconfig.ini (template: config.template)
  - Application constants: config.py (reads CONFIGDIR env var or /etc/local/)
  - DB schema: ogndb/DBschema.sql
  - Local data path normally under config.DBpath (config.py reads SARconfig.ini).

---

## 3) Key conventions and repo-specific patterns

- Runtime config precedence:
  - ENV: set CONFIGDIR to point to alternative config directory (config.py honors this).
  - Otherwise config file is /etc/local/SARconfig.ini — Copilot should prefer reading config.template and ogndb/config.py for defaults, not assume hard-coded paths.

- Database: the code expects a local SQLite DB (SAROGN.db) for fast processing; synchronisation scripts expect a MySQL/MariaDB central DB. DB schema and creation are in ogndb/DBschema.sql and DBcreate.py.

- Scheduling and orchestration:
  - sh/* scripts are the operational entrypoints (SARpogn.sh, SARflight_logger.sh, SARfcst.sh). Many invocations use at/cron and calcelestial for timed scheduling.

- Naming and layout:
  - Shell helpers and scheduled tasks start with SAR (SARpogn.sh, SARfcst.sh).
  - Data files: DATAyyMMdd.log naming convention; SARprocessogn expects config.DBpath + DATA<date>.log by default.

- Python path assumptions:
  - Some scripts augment sys.path with /nfs/OGN/src/funcs and /nfs/OGN/src/SARsrc. When running locally, ensure PYTHONPATH or working dir matches expectations, or run from repo root.

- Python version and packaging:
  - CI uses Python 3.9. requirements.txt pins key libs (geopy, ogn_client, etc.). package.json exists but is a placeholder for Node tooling and is not relevant to Python processing.

- Safety / operational notes for automation:
  - install.sh and provisioning scripts perform system-wide actions (apt-get, mysql config, htpasswd). Review and run on dedicated/test hosts only.
  - Many scripts expect to run as specific users (ogn/www-data) and create /nfs/OGN/DIRdata and system cron entries.

---

## Useful file pointers for programmatic agents
- Main processor: SARprocessogn.py
- Parsers & DB helpers: ogndb/parserfuncs.py, ogndb/DBcreate.py, ogndb/DBopen_db.py
- DB schema: ogndb/DBschema.sql
- Configuration template: config.template
- Install scripts: install.sh, provisioning/*, sh/*
- CI: .github/workflows/python-app.yml

---

If this file already exists in a future revision, keep it focused: prefer exact commands, precise locations of configuration and schema, and any non-obvious syscall/privilege expectations.

