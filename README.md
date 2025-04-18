# vuln-flask-api

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31017/)
A Flask API demonstrating custom data structure implementations. This project intentionally uses older versions of Python (3.10.17) and packages to serve as a target for vulnerability scanning comparisons using `pip-audit` and `Trivy` within a GitHub Actions CI/CD pipeline.

**⚠️ Security Note:** This application uses intentionally vulnerable dependencies for educational purposes. **Do not deploy this configuration in a production environment.**

## Project Goal

The primary goal of this repository is to provide a realistic Python web application target for demonstrating and comparing the effectiveness of:

1.  **Dependency Scanning (Pre-Build):** Using tools like `pip-audit` to scan `requirements.txt`.
2.  **Container Image Scanning (Post-Build):** Using tools like `Trivy` to scan the built Docker image.

This comparison is intended to be automated within a GitHub Actions workflow as part of a DevSecOps demonstration.

## Features

* RESTful API for managing Users and Blog Posts (CRUD operations).
* Demonstrates custom implementations of common data structures (Linked List, BST, Hash Table, Queue, Stack) within API logic.
* Configurable Flask application settings (Development, Production, Testing).
* Database initialization and sample data generation scripts.

## Project Structure
```
├── app/
│   ├── init.py                 # App factory
│   ├── models/                 # SQLAlchemy models (user.py, blog_post.py)
│   ├── routes/                 # API Blueprints/Views (user_routes.py, blog_post_routes.py)
│   ├── services/               # Business logic
│   │   └── data_structures/    # Custom data structure implementations
│   └── utils/                  # Utility functions (helpers.py)
├── .github/
│   └── workflows/              # GitHub Actions CI/CD pipeline (e.g., ci.yml)
├── instance/                   # will contain the sqlite db details
├── scripts/                    # Scripts
│   ├── generate_sample_data.py # Script to populate DB with sample data
│   ├── init_db.py              # Script to initialize the database schema
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   │   ├── models/             # Tests for data models
│   │   │   ├── test_user.py    # User model tests
│   │   │   └── test_blog_post.py # Blog post model tests
│   │   ├── services/           # Tests for service layer
│   │   └── utils/              # Tests for utility functions
│   │       └── test_helpers.py # Tests for helper functions
│   ├── functional/             # Functional tests
│   ├── integration/            # Integration tests
│   └── conftest.py             # Test fixtures and configuration
├── .gitignore
├── config.py                   # Flask configuration settings
├── Dockerfile                  # Containerization instructions
├── requirements.txt            # Project dependencies (intentionally includes vulnerabilities)
├── run.py                      # Application entry point
└── README.md                   # This file
```

*(Note: Simplified structure diagram for brevity)*

## Getting Started

### Prerequisites

* Python 3.10.17 (or compatible version managed via `pyenv`, `conda`, etc.)
* `pip` and `venv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/vuln-flask-api.git](https://github.com/yourusername/vuln-flask-api.git)
    cd vuln-flask-api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv  # Using .venv is common practice
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    ```bash
    python init_db.py
    ```

5.  **Generate sample data (Optional):**
    ```bash
    python generate_sample_data.py
    # See options below for customization
    ```

## Running the Application

### Running the Development Server

There are three primary ways to run the development server:

**1. Direct Execution (using `run.py`):**

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

**2. Using Flask CLI:**

   * Set environment variables first (in your shell):
       ```bash
       export FLASK_APP=run.py
       export FLASK_ENV=development # Or 'production'
       ```
   * Run the server:
       ```bash
       flask run
       ```
   * *(Useful Command)* List all registered routes:
       ```bash
       flask routes
       ```

**3. Using Docker (Recommended for Consistent Environment):**

- **Build the Docker image:**
``` bash
       docker build -t capstone-app:latest .
```
- **Run the container:**
``` bash
       docker run -p 5000:5000 capstone-app:latest
```
This will:
- Initialize the database automatically (via entrypoint.sh)
- Start the Flask application in development mode
- Map port 5000 from the container to your host machine

- **Run with sample data generation (optional):**
``` bash
       # Generate default sample data
       docker run -p 5000:5000 capstone-app:latest bash -c "./entrypoint.sh && python generate_sample_data.py"
       
       # Generate customized sample data
       docker run -
```

The API will typically be available at `http://127.0.0.1:5000/` or `http://localhost:5000/`.

### Database Management Scripts

* **Initialize Database Schema:** (Run once initially or after dropping tables)
    ```bash
    python init_db.py
    ```

* **Generate Sample Data:**
    ```bash
    python generate_sample_data.py [OPTIONS]
    ```
    **Options:**
    * `--users INTEGER`: Number of users (default: 200)
    * `--posts INTEGER`: Number of posts (default: 200)
    * `--batch INTEGER`: DB commit batch size (default: 50)
    * `--clear`: Clear existing data before generating

    **Example:**
    ```bash
    python generate_sample_data.py --users 50 --posts 100 --clear
    ```

## API Endpoints

*(Note: Request/Response details omitted for brevity. Refer to route implementations.)*

**User Management:**

* `POST /user`: Creates a new user.
* `GET /user/descending_id`: Retrieves all users, ordered by ID descending (uses LinkedList).
* `GET /user/ascending_id`: Retrieves all users, ordered by ID ascending (uses LinkedList).
* `GET /user/<user_id>`: Retrieves a specific user by ID.
* `DELETE /user/<user_id>`: Deletes a specific user.

**Blog Post Management:**

* `POST /blog_post/<user_id>`: Creates a new blog post for the specified user (uses HashTable internally).
* `GET /blog_post/user/<user_id>`: Retrieves all blog posts for a specific user (uses BST for retrieval logic).
* `GET /blog_post/numeric_body`: Retrieves posts, demonstrating numeric conversion (uses Queue).
* `DELETE /blog_post/user/<user_id>`: Deletes all blog posts for a specific user (uses Stack internally).

## Data Structure Usage

Custom data structures are implemented and used in specific API operations to demonstrate their application:

* **LinkedList**: Utilized in `GET /user/descending_id` and `GET /user/ascending_id` for managing and ordering the user list retrieval.
* **Binary Search Tree (BST)**: Employed in the logic for `GET /blog_post/user/<user_id>` potentially for efficient searching or sorting of posts.
* **HashTable**: Used during the creation process in `POST /blog_post/<user_id>`, possibly for efficient lookups or data handling.
* **Queue**: Applied in `GET /blog_post/numeric_body` to process posts in a specific order for conversion.
* **Stack**: Used internally within the `DELETE /blog_post/user/<user_id>` endpoint, perhaps for managing the deletion process.

## Vulnerability Scanning Integration

This repository is set up to be scanned by:

* **`pip-audit`**: Analyzes `requirements.txt` for known vulnerabilities in Python packages.
    ```bash
    pip-audit -r requirements.txt
    ```
* **`Trivy`**: Scans the built Docker container image for OS package and application dependency vulnerabilities.
    ```bash
    # Build the image first: docker build -t vuln-flask-api:latest .
    trivy image vuln-flask-api:latest
    ```
* **GitHub Actions**: The `.github/workflows/ci.yml` pipeline automates these scans on code push/pull request.