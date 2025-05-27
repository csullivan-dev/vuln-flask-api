# vuln-flask-api: Python Vulnerability Scanning Comparison 🛡️

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31017/)

**A Capstone Project for Clover Park Technical College comparing pre-containerization and post-containerization vulnerability scanning for Python applications.**

This repository demonstrates and compares the effectiveness of different vulnerability scanning strategies within an automated CI/CD pipeline. It uses an intentionally vulnerable Python Flask API as a target for these scans.

**⚠️ Security Note:** This application uses intentionally vulnerable dependencies for educational and demonstration purposes. **Do not deploy this configuration in a production environment.**

## Table of Contents

* [Project Overview](#project-overview-)
* [Research Focus](#research-focus-)
* [Intended Audience](#intended-audience-)
* [Key Scanning Stages Investigated](#key-scanning-stages-investigated-)
* [Methodology Summary](#methodology-summary-)
* [Technology Stack](#technology-stack-)
* [Project Structure](#project-structure-)
* [Getting Started](#getting-started-)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
* [Running the Application](#running-the-application-)
    * [Using Python Directly](#1-direct-execution-using-runpy)
    * [Using Flask CLI](#2-using-flask-cli)
    * [Using Docker (Recommended)](#3-using-docker-recommended-for-consistent-environment)
* [Database Management](#database-management-scripts-)
* [API Endpoints](#api-endpoints-)
* [Data Structure Usage](#data-structure-usage-)
* [Vulnerability Scanning Integration](#vulnerability-scanning-integration-)
* [Project Basis and Enhancements](#project-basis-and-enhancements-)

## Project Overview 🎯

Modern web applications often use containers (like Docker) and are deployed to the cloud. While tools exist to scan an application's source code for bugs (Static Application Security Testing, or SAST), vulnerabilities can also hide within the container itself or in the software packages (dependencies) the application relies on. These areas are frequently overlooked in typical development cycles.

This project highlights the individual shortcomings of relying on a single scanning approach and underscores the necessity for a combined, multi-stage strategy to achieve comprehensive vulnerability coverage in containerized applications.

## Research Focus ❓

The core question this project seeks to answer is:

> How does the effectiveness of vulnerability detection (considering the types of vulnerabilities, their severity, and whether they are application vs. OS-level) compare when using a dependency-specific scanner *before* building a container versus using a container image scanner *after* the build, all within an automated CI/CD pipeline?

## Intended Audience 🧑‍

This project is designed for:

* **Developers:** Those looking to understand and compare vulnerability scanning options for their Python projects and how to integrate them.
* **Cybersecurity Students & New Developers:** Individuals seeking a practical understanding of how vulnerability scanners fit into a modern DevOps/DevSecOps workflow.

## Key Scanning Stages Investigated 🔍

This project investigates and demonstrates automating vulnerability scans at two critical stages:

1.  **Pre-Containerization Dependency Scanning:** Checking the application's Python packages (from `requirements.txt`) for known vulnerabilities *before* the application is packaged into a Docker container.
2.  **Post-Containerization Image Scanning:** Scanning the final Docker image for vulnerabilities in *both* the application's Python packages (as installed in the image) *and* the underlying operating system of the container.

## Methodology Summary 

To address the research question, a sample Python Flask API was developed with intentionally vulnerable packages. This application is then containerized using Docker. A GitHub Actions CI/CD pipeline automates the following:

1.  **Testing:** Runs a comprehensive suite of unit, functional, and integration tests using `pytest`.
2.  **Pre-Containerization Scan:** `pip-audit` analyzes the application's Python dependencies based on the OSV database.
3.  **Container Build:** Builds the Docker image.
4.  **Post-Containerization Scan:** `Trivy` (an open-source, multi-faceted scanner) analyzes the built Docker image for vulnerabilities in application packages and the container's OS.
5.  **Analysis:** The results from `pip-audit` and `Trivy` scans are collected as artifacts and summarized to compare their findings, highlighting unique detections, overlaps, and differences (e.g., OS vulnerabilities are only expected from `Trivy`'s image scan).

This comparison demonstrates the capabilities and limitations of each approach, showcasing their complementary nature.

## Technology Stack 🛠️

<div>
  <a href="https://www.gnu.org/software/bash/" title="GNUbash"><img src="https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=GNU%20Bash&logoColor=white" alt="GNUbash" ></a>
  <a href="https://www.python.org/" title="Python"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://flask.palletsprojects.com/" title="Flask"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://www.sqlalchemy.org/" title="SQLAlchemy"><img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"></a>
  <a href="https://www.docker.com/" title="Docker"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://github.com/features/actions" title="GitHub Actions"><img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions"></a>
  <a href="https://www.sqlite.org/" title="SQLite"><img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"></a>
  <a href="https://aquasecurity.github.io/trivy/" title="Trivy"><img src="https://img.shields.io/badge/Trivy-22A7F0?style=for-the-badge&logo=Trivy&logoColor=white" alt="Trivy"></a>
  <a href="https://pypi.org/project/pip-audit/" title="pip-audit"><img src="https://img.shields.io/badge/pip--audit-0073B7?style=for-the-badge&logo=python&logoColor=yellow" alt="pip-audit"></a>
</div>

## Project Structure 📂
```
├── .github/
│   └── workflows/              # GitHub Actions CI/CD pipeline
│       └── ci.yml              # CI Pipeline Setup (Test runs, Containerization, Security Report)
├── app/
│   ├── models/                 # SQLAlchemy models (user.py, blog_post.py)
│   ├── routes/                 # API Blueprints/Views (user_routes.py, blog_post_routes.py)
│   ├── services/               # Business logic
│   │   └── data_structures/    # Custom data structure implementations
│   ├── utils/                  # Utility functions (helpers.py)
│   ├── __init__.py             # App factory
│   └── extensions.py/          # Flask-SQLAlchemy Setup with SQLite Configuration
├── instance/                   # Will contain the sqlite db details (sqlitedb.file)
├── scripts/                    
│   ├── generate_sample_data.py # Script to populate DB with sample data
│   ├── init_db.py              # Script to initialize the database schema
├── tests/                      # Tests to be ran in pipeline using pytest
│   ├── unit/                   # Tests for individual components or modules   
│   │   ├── models/             
│   │   │   ├── test_user.py      
│   │   │   └── test_blog_post.py
│   │   ├── services/           
│   │   │    └── data_structures
│   │   └── utils/              
│   │       └── test_helpers.py 
│   ├── functional/             # Tests to verify the software meets defined user functionality
│   ├── integration/            # Tests to ensure modules or components work together as expected
│   │    └── routes/         
│   └── conftest.py             # Test fixtures and configuration
├── .gitignore
├── config.py                   # Flask configuration settings
├── Dockerfile                  # Containerization instructions
├── entrypoint.sh               # Application entry point shell script
├── README.md                   # This file
├── requirements.txt            # Project dependencies (intentionally includes vulnerabilities)
└── run.py                      # Configuring app accessibility outside of Docker
```

*(Note: Simplified structure diagram for brevity)*

## Getting Started 🚀

### Prerequisites

* Python 3.10.x (using `pyenv` or `conda` for version management is recommended)
* `pip` (Python package installer)
* `venv` (for creating virtual environments)
* Docker (if running the application via Docker)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/csullivan-dev/vuln-flask-api 
    cd vuln-flask-api
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv .venv  # Creates a virtual environment in the .venv folder
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application 🏃

### 1. Direct Execution (using `run.py`)

   * **Default (Development Config):**
       ```bash
       python run.py
       ```
   * **Specify Configuration:** Use the `FLASK_CONFIG` environment variable:
       ```bash
       # Production mode
       FLASK_CONFIG=production python run.py

       # Testing mode
       FLASK_CONFIG=testing python run.py
       ```

### 2. Using Flask CLI

   * Set environment variables (in your current shell session):
       ```bash
       export FLASK_APP=run.py
       export FLASK_ENV=development # Or 'production', 'testing'
       ```
   * Run the server:
       ```bash
       flask run
       ```
   * *(Useful Command)* List all registered routes:
       ```bash
       flask routes
       ```

### 3. Using Docker (Recommended for Consistent Environment)

   * **Build the Docker image:**
       ```bash
       docker build -t capstone-app:latest .
       ```
   * **Run the container:**
       ```bash
       docker run -p 5000:5000 capstone-app:latest
       ```
       This will automatically initialize the database (via `entrypoint.sh`) and start the Flask application.

   * **Run with sample data generation (Optional):**
       After the container is running, you can execute the generation script inside it:
       ```bash
       docker exec -it <container_id_or_name> python generate_sample_data.py
       # To generate with custom options:
       # docker exec -it <container_id_or_name> python generate_sample_data.py --users 50 --posts 50 --clear
       ```
       *(Find `<container_id_or_name>` using `docker ps`)*

The API will typically be available at `http://127.0.0.1:5000/` or `http://localhost:5000/`.

## Database Management Scripts 💾

*(These scripts are primarily for non-Docker local setup or for manual intervention inside a running Docker container.)*

* **Initialize Database Schema:** (Run once initially or if you need to reset the schema)
    ```bash
    python scripts/init_db.py 
    # (Ensure virtual environment is active if running locally)
    ```

* **Generate Sample Data:**
    ```bash
    python scripts/generate_sample_data.py [OPTIONS]
    # (Ensure virtual environment is active if running locally)
    ```
    **Options:**
    * `--users INTEGER`: Number of users (default: 200)
    * `--posts INTEGER`: Number of posts (default: 200)
    * `--batch INTEGER`: DB commit batch size (default: 50)
    * `--clear`: Clear existing data before generating

    **Example:**
    ```bash
    python scripts/generate_sample_data.py --users 50 --posts 100 --clear
    ```

## API Endpoints ↔️

*(Note: Detailed request/response schemas are omitted for brevity. Please refer to the route implementations in `app/routes/` for specifics.)*

**User Management:**

* `POST /user`: Creates a new user.
* `GET /user/descending_id`: Retrieves all users, ordered by ID descending.
* `GET /user/ascending_id`: Retrieves all users, ordered by ID ascending.
* `GET /user/<user_id>`: Retrieves a specific user by ID.
* `DELETE /user/<user_id>`: Deletes a specific user.

**Blog Post Management:**

* `POST /blog_post/<user_id>`: Creates a new blog post for the specified user.
* `GET /blog_post/user/<user_id>`: Retrieves all blog posts for a specific user.
* `GET /blog_post/numeric_body`: Retrieves posts, demonstrating a numeric conversion feature.
* `DELETE /blog_post/user/<user_id>`: Deletes all blog posts for a specific user.

## Data Structure Usage 🧱

This API demonstrates the application of several custom data structures within its logic:

* **LinkedList**: Used in user listing endpoints (`/user/descending_id`, `/user/ascending_id`) for managing and ordering user data.
* **Binary Search Tree (BST)**: Employed in blog post retrieval logic (`/blog_post/user/<user_id>`) for potentially efficient searching/sorting.
* **HashTable**: Used during blog post creation (`/blog_post/<user_id>`) for efficient data handling or lookups.
* **Queue**: Applied in the numeric body conversion endpoint (`/blog_post/numeric_body`) for ordered processing of posts.
* **Stack**: Used internally within the blog post deletion endpoint (`/DELETE /blog_post/user/<user_id>`) for managing the deletion sequence.

## Vulnerability Scanning Integration 🔬

This repository is configured for automated vulnerability scanning using GitHub Actions:

* **`pip-audit`**: Scans `requirements.txt` for Python package vulnerabilities before containerization.
    * Local check: `pip-audit -r requirements.txt`
* **`Trivy`**:
    * Scans the repository filesystem (including `requirements.txt`) pre-containerization.
    * Scans the final Docker image for OS package and application library vulnerabilities post-containerization.
    * Local image check: `docker build -t capstone-app:latest . && trivy image capstone-app:latest`

Scan results (JSON reports) are available as artifacts in the GitHub Actions workflow runs. A summary is also provided in the workflow's summary page.

## Project Basis and Enhancements 💡

The foundational API structure for this project was inspired by the [FlaskDS repository](https://github.com/kantancoding/FlaskDS), associated with [FreeCodeCamp's "Data Structures for Python Developers (with Flask)" tutorial](https://www.freecodecamp.org/news/learn-data-structures-flask-api-python/).

This project builds upon that base with significant enhancements reflecting industry best practices:

* **Improved Route Structure & Modular Architecture:** For better organization and maintainability.
* **Robust Error Handling:** Comprehensive error management for API resilience.
* **Refined Data Structure Implementation:** Enhanced logic and application.
* **Detailed API Responses:** More informative and standardized.
* **Comprehensive Testing Suite:** Unit, functional, and integration tests using `pytest`, integrated into the CI/CD pipeline.

These modifications aim to provide a more advanced, production-relevant example that serves the primary goal of demonstrating vulnerability scanning.