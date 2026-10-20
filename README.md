# Enterprise UI Automation Framework – Books to Scrape

## Project Overview
This repository contains a production-ready UI test automation framework built with **Playwright** and **Pytest** in Python. It validates the core functionality, UI elements, data consistency, hyperlink integrity, image rendering, pagination, and authentication flows across two target sandbox platforms:
* **Books to Scrape:** `https://books.toscrape.com/index.html`,
* **Quotes to Scrape:** `https://quotes.toscrape.com/`,

The framework uses the Page Object Model (POM) pattern, custom Pytest fixtures, containerized execution via Docker, and automated CI/CD execution through GitHub Actions with self-contained HTML and Allure test reporting.

---

## Features
* **Page Object Model (POM) Architecture:** Clean separation between page locators/interactions (`pages/`), test assertions (`tests/`), configuration (`config/`), and helper utilities (`utils/`).
* **Reproducible Random Sampling:** Session-scoped `five_random_books` fixture selects 5 random books using a configurable or auto-generated cryptographic seed (`BOOK_SAMPLE_SEED`), allowing deterministic reproduction of any test run
* **Fast Broken Link Validation:** Extracts and deduplicates all anchor `href` attributes from the DOM and verifies HTTP 200 status codes using Playwright's `APIRequestContext`.
* **Zero Hardcoded Waits:** Uses Playwright's web-first assertions (`expect(...)`) and auto-waiting mechanisms for reliable synchronization.
* **Comprehensive Failure Diagnostics:** Automatically captures screenshots, videos, and Playwright trace files on test failure.
* **Dual Reporting Engine:** Generates both self-contained `pytest-html` reports and interactive Allure reports locally and in CI.
* **Dockerized & CI/CD Ready:** Fully containerized environment using Python 3.12 and GitHub Actions workflow integration.

---

## Tech Stack
| Component | Technology / Version | Purpose |
| :--- | :--- | :--- |
| **Language** | Python `3.12` | Core programming language |
| **Browser Automation** | Playwright `1.64.0` | UI and API request automation |
| **Test Runner** | Pytest `9.1.1` & `pytest-playwright` `0.10.0` | Test discovery, fixtures, and parametrization |
| **HTML Reporting** | `pytest-html` `4.2.0` | Self-contained HTML execution reports |
| **Allure Reporting** | `allure-pytest` `2.16.2` | Rich interactive test analytics and step reporting |
| **Linter / Formatter** | Ruff `0.17.1` | Static code analysis and PEP8 formatting |
| **Containerization** | Docker (`python:3.12-bookworm`) | Consistent execution environment |
| **CI/CD** | GitHub Actions | Automated test execution and artifact publishing |

---

## Installation Guide

### Prerequisites
* **Python:** `3.12+` installed on your system
* **Git:** To clone the repository
* **Docker:** *(Optional)* For containerized test execution
* **Allure CLI:** *(Optional)* Required locally only to render HTML dashboards from `allure-results/`

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/gazimaksudur2/UI-Automation-Testing-toscrap.git
   cd UI-Automation-Testing-toscrap
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   # .venv\Scripts\activate    # Windows
   ```

3. **Install Python dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install Playwright Chromium browser and system dependencies:**
   ```bash
   python -m playwright install chromium
   ```

---

## Environment Setup
Target URLs are centralized in `config/settings.py`:
* `BOOKS_HOME_URL = "https://books.toscrape.com/index.html"`
* `QUOTES_HOME_URL = "https://quotes.toscrape.com/"`

### Optional Environment Variables
* `BOOK_SAMPLE_SEED`: Controls the random selection of the 5 books in `conftest.py`. If omitted, a random 32-bit seed is generated and printed to stdout (`Random seed: <seed>`).
  ```bash
  export BOOK_SAMPLE_SEED=123456789
  ```

---

## Running Tests

### 1. Run All Tests (Default Configuration)
```bash
python -m pytest
```

### 2. Run in Headed Mode (Visible Browser)
```bash
python -m pytest tests/ -v --headed
```

### 3. Run Specific Test Modules
```bash
# Homepage validation
python -m pytest tests/test_homepage.py -v --browser=chromium

# Random book navigation (5 books)
python -m pytest tests/test_book_navigation.py -v --browser=chromium

# Book data consistency (5 books)
python -m pytest tests/test_book_data_consistency.py -v --browser=chromium

# Broken link checker
python -m pytest tests/test_broken_links.py -v --browser=chromium

# Product images & pagination
python -m pytest tests/test_product_images.py -v --browser=chromium

# Quotes login and logout validation
python -m pytest tests/test_quotes_login.py -v --browser=chromium
```

### 4. Run Tests Inside Docker
```bash
docker build -t books-ui-tests .
mkdir -p reports/html allure-results test-results
docker run --rm --init --ipc=host \
  -v "$PWD/reports:/app/reports" \
  -v "$PWD/allure-results:/app/allure-results" \
  -v "$PWD/test-results:/app/test-results" \
  books-ui-tests
```

---

## Project Structure
```text
UI-Automation-Testing-toscrap/
├── .github/
│   └── workflows/
│       └── playwright.yml              # GitHub Actions CI/CD workflow
├── config/
│   ├── __init__.py
│   └── settings.py                     # Centralized base URLs
├── pages/
│   ├── __init__.py
│   ├── book_details_page.py            # POM for book details view
│   ├── books_home_page.py              # POM for Books to Scrape catalog
│   ├── quotes_home_page.py             # POM for Quotes to Scrape home
│   └── quotes_login_page.py            # POM for Quotes to Scrape login
├── tests/
│   ├── conftest.py                     # Session fixtures & random book seeding
│   ├── test_book_data_consistency.py   # TC 3: Homepage vs Details data check
│   ├── test_book_navigation.py         # TC 2: 5 random book navigation tests
│   ├── test_broken_links.py            # TC 4: HTTP 200 hyperlink validation
│   ├── test_homepage.py                # TC 1: Homepage structure & headings
│   ├── test_product_images.py          # TC 5: Image attributes & 5-page pagination
│   └── test_quotes_login.py            # TC 6: Quotes login & logout verification
├── utils/
│   ├── __init__.py
│   └── url_utils.py                    # URL normalization & deduplication helper
├── Dockerfile                          # Container build definition
├── requirements.txt                    # Locked Python dependencies
└── README.md                           # Project documentation
```

---

## Test Case Coverage
| ID | Test Case | Test File | Description |
| :--- | :--- | :--- | :--- |
| **TC 1** | Homepage Validation | `tests/test_homepage.py` | Verifies homepage URL, page title (`All products \| Books to Scrape - Sandbox`), visible headings (`h1–h6`) have non-empty text, and the books section contains items. |
| **TC 2** | Random Book Navigation Validation | `tests/test_book_navigation.py` | Randomly selects 5 books on the homepage, clicks each, verifies the `/catalogue/.../index.html` URL pattern, checks that the `h1` title matches the selected title, verifies the product information table is populated, and navigates back. |
| **TC 3** | Book Data Consistency Validation | `tests/test_book_data_consistency.py` | Captures title and price for 5 randomly selected books on the homepage, opens each details page, verifies exact title and price parity, and returns to the homepage. |
| **TC 4** | Broken Link Validation | `tests/test_broken_links.py` | Collects all `a[href` attributes on the homepage, resolves relative links, strips fragments, deduplicates URLs, and asserts HTTP `200` responses via Playwright's API request context. |
| **TC 5** | Product Image Validation | `tests/test_product_images.py` | Validates that every product image is visible and has a non-empty `src`, non-empty `alt`, and `thumbnail` class across up to 5 paginated pages. |
| **TC 6** | Login & Logout Link Validation | `tests/test_quotes_login.py` | Navigates to `quotes.toscrape.com`, opens the Login page, submits credentials, verifies authenticated redirection, and asserts that the Logout link is visible and enabled. |

---

## Report Generation Guide
Test execution produces three output directories in the project root:
* `reports/html/`: Contains the standalone `report.html` file generated by `pytest-html`.
* `allure-results/`: Contains raw JSON execution metadata for Allure.
* `test-results/`: Stores failure screenshots, videos, and Playwright traces (`trace.zip`).

---

## HTML Report Guide
1. **Generate the HTML Report:**
   ```bash
   python -m pytest tests/ --html=reports/html/report.html --self-contained-html
   ```
2. **View the Report:**
   Open `reports/html/report.html` directly in any web browser:
   ```bash
   xdg-open reports/html/report.html   # Linux
   open reports/html/report.html       # macOS
   ```
   Because `--self-contained-html` is enabled, CSS and assets are embedded inside the single HTML file for easy sharing and CI artifact viewing.

---

## Allure Report Guide
1. **Generate Allure Results:**
   ```bash
   python -m pytest tests/ --alluredir=allure-results --clean-alluredir
   ```
2. **Serve the Interactive Report Locally:**
   *(Requires Allure CLI installed)*
   ```bash
   allure serve allure-results
   ```
3. **Generate a Static Allure HTML Folder:**
   ```bash
   allure generate allure-results -o reports/allure-report --clean
   allure open reports/allure-report
   ```

---

## GitHub Actions Setup
The CI/CD pipeline is defined in `.github/workflows/playwright.yml` and triggers automatically on:
* `push` to the `main` branch
* `pull_request` targeting the `main` branch
* Manual execution via `workflow_dispatch`

### Pipeline Workflow Steps
1. **Checkout repository:** Pulls the source code using `actions/checkout@v4`.
2. **Build Docker image:** Builds `books-ui-tests` from the `Dockerfile` (installing Python dependencies and Playwright Chromium with system libraries).
3. **Prepare report directories:** Creates `reports/html`, `allure-results`, and `test-results` on the runner host
4. **Run Playwright tests:** Executes the Docker container with `--init --ipc=host` (to prevent Chromium shared-memory crashes) and volume-mounts the report directories back to the host workspace.
5. **Upload Artifacts (`if: always()`):** Uploads three artifacts via `actions/upload-artifact@v4` regardless of pass/fail status:
   * `pytest-html-report` (`reports/html/`)
   * `allure-results` (`allure-results/`)
   * `playwright-test-results` (`test-results/` containing screenshots, videos, and traces on failure)

---

## Design Decisions
1. **Session-Scoped Random Sampling with Seed Logging:**
   Instead of re-scraping book titles inside every parametrized test, `five_random_books` in `tests/conftest.py` fetches the catalog once per session and selects 5 unique titles using `random.Random(seed).sample(titles, 5)`. This ensures both **TC 2 (Navigation)** and **TC 3 (Data Consistency)** run as 5 isolated test cases in Pytest reports while remaining reproducible via `BOOK_SAMPLE_SEED`.
2. **Hybrid UI + API Link Checking:**
   Clicking 50+ links sequentially through the browser in **TC 4** is slow and brittle. Instead, the framework extracts all `href` attributes from the live DOM, normalizes/deduplicates them via `utils/url_utils.py`, and validates HTTP 200 status codes using Playwright's `playwright.request.new_context()`.
3. **Containerized CI Execution (`--ipc=host`):**
   Running tests inside Docker guarantees identical browser binaries and OS libraries between local development and GitHub Actions Passing `--ipc=host` and `--init` avoids Chromium `/dev/shm` memory exhaustion and zombie processes in CI
4. **Web-First Assertions Over Explicit Sleeps:**
   All state validations use Playwright's `expect()` API, which automatically retries until the DOM settles or the timeout expires, eliminating timing flakiness.

---

## Known Limitations
* **External Sandbox Availability:** All tests run against live public demo servers (`books.toscrape.com` and `quotes.toscrape.com`). Temporary network latency, DNS issues, or server downtime on those external hosts can impact test execution.
* **Mock Authentication on Quotes to Scrape:** The `quotes.toscrape.com/login` endpoint accepts any non-empty username and password combination by design; therefore, negative authentication scenarios (invalid password rejection) are not enforced by the target backend.
* **Single-Browser Default in Docker:** To optimize Docker image size and CI build times, only `chromium` is installed in the container image (`python -m playwright install --with-deps chromium`). Firefox and WebKit can be run locally by installing them via `playwright install firefox webkit`.