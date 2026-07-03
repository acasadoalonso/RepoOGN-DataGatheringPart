# RepoOGN-DataGatheringPart
Gathering APRS fixes from Spain
===============================

License
Licensed under the AGPLv3. https://github.com/glidernet/ogn-live/blob/master/LICENSE 


# RepoOGN-DataGatheringPart

RepoOGN-DataGatheringPart is a comprehensive system designed to collect, process, and store telemetry data from OGN (Open Gliding Network), ADS-B, and FLARM sources. It automates the transformation of raw APRS/OGN logs into standardized IGC flight files and maintains a multi-tier database for rapid local access and centralized long-term storage.

## 🚀 Architecture Overview

The system employs a two-tier database architecture to balance performance and persistence:

1.  **Local Tier (SQLite):** A lightweight, high-performance SQLite database (`ogndb/`) resides on the processing node. This tier is used for rapid ingestion, local flight detection, and immediate data availability.
2.  **Central Tier (MySQL/MariaDB):** Processed data is periodically synchronized to a centralized MySQL or MariaDB server. This provides a persistent, shared repository for web interfaces, long-term analysis, and multi-node access.

## 🔄 Data Lifecycle

The data flows through three primary stages:

1.  **Ingestion**: Raw telemetry from OGN (APRS), ADS-B, and FLARM is collected into daily log files (e.g., `DATAyyyymmdd.log`).
2.  **Processing**: 
    *   The core engine, `SARprocessogn.py`, parses these logs.
    *   It extracts coordinates, altitude, speed, and identity from APRS/OGN messages.
    *   It applies heuristics (e.g., speed thresholds) to detect flight boundaries (take-off and landing).
    *   It generates standardized `.IGC` files for every detected flight.
3.  **Storage**: 
    *   Processed records are first written to the local SQLite database.
    *   The `sh/SARpogn.sh` script then synchronizes this data to the central MySQL/MariaDB instance.

## 🛠️ Core Components

### Processing Engine
*   **`SARprocessogn.py`**: The heart of the system. It handles the heavy lifting of parsing raw logs, detecting flights, and generating IGC files.
*   **`ogndb/`**: A specialized module containing the logic for database interaction, message parsing (`parserfuncs.py`), and specialized data handling (ADS-B, FLARM).

### Automation & Scheduling
The system is designed to run autonomously using periodic cycles:
*   **Sunset Cycle (`sh/SARpogn.sh`)**: Triggered shortly after sunset. It cleans up processes, runs the processing engine, updates both database tiers, synchronizes data, and schedules the next run.
*   **Sunrise Cycle (`sh/SARflight_logger.sh`)**: Triggered during the day to ensure continuous and reliable data logging.

### Deployment & Infrastructure
*   **Docker**: A complete, containerized environment is provided via `dockerfiles/`. The `Dockerfile` sets up a reproducible stack including Python, MariaDB, and all necessary dependencies.
*   **Provisioning**: Automated setup for host environments is supported through **Ansible** playbooks (`provisioning/`) and **Vagrant** (`provisioning/Vagrantfile`).

## ⚙️ Configuration

Configuration is managed at multiple levels to ensure flexibility:

*   **Application Defaults**: `RepoOGN-DataGatheringPart/config.py` contains core application constants.
*   **Environment Settings**: The primary configuration for the automation scripts and database connections is located at `/etc/local/SARconfig.ini`. This file is typically provided via a template (`config.template`) or through Docker volumes.
*   **Database Config**: `ogndb/config.py` manages database-specific settings.

## 📂 Project Structure

```text
RepoOGN-DataGatheringPart/
├── adsbfuncs.py           # ADS-B specific utility functions
├── flarmfuncs.py          # FLARM specific utility functions
├── ognddbfuncs.py         # OGN database utility functions
├── SARprocessogn.py       # Main processing engine (Logs -> IGC)
├── install.sh             # Primary installation script
├── requirements.txt       # Python dependencies
├── config.template        # Template for environment configuration
├── dockerfiles/           # Docker-based deployment files
│   └── Dockerfile         # Main container definition
├── flarmdb/               # FLARM database building utilities
├── ogndb/                 # Core OGN database & parsing logic
│   ├── DBcreate.py        # SQLite schema initialization
│   ├── parserfuncs.py     # APRS/OGN message parsing
│   └── ...                # Other DB management tools
├── provisioning/          # Infrastructure as Code (Ansible, Vagrant)
├── sh/                    # Automation & scheduling shell scripts
│   ├── SARpogn.sh         # Main sunset orchestration script
│   └── ...                # Other periodic task scripts
└── doc/                   # Documentation and SQL schemas
```

## 🚀 Installation & Setup

### Using Docker (Recommended)
The easiest way to deploy is using the provided Docker configuration:
1.  Configure your environment using the `config.template`.
2.  Build and run the container using the instructions in `dockerfiles/README.md`.

### Bare Metal Installation
For manual installation on a Linux host:
1.  Install system dependencies (Python, MariaDB, etc.).
2.  Run `./install.sh` or `./commoninstall.sh`.
3.  Configure `/etc/local/SARconfig.ini` with your database and path settings.

## 📄 License
Licensed under the AGPLv3.
