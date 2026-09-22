# AI-Powered QA Automation

An AI-assisted website QA automation system that uses **Playwright** for browser automation and **Groq LLMs** to generate structured test cases from a website's actual content and links.

The system takes a website URL, analyzes the page, generates QA test cases, executes them automatically, and produces a CSV report containing both the generated test plan and execution results.

## Features

* 🌐 Automated website inspection with Playwright
* 🤖 AI-generated QA test cases using Groq
* 🔗 Link and navigation testing
* 📝 Content verification
* 🔐 Automatic login-system detection
* 👤 Credential-based authentication testing
* 🛑 Authentication failure acts as a gate before normal QA testing
* 📊 CSV test reports
* ⏱️ Timestamped reports for each execution
* 🔒 Environment variables for API keys
* 🧩 Modular Python project structure

## How It Works

```text
Website URL
     ↓
Playwright Browser
     ↓
Website Inspection
     ↓
Login Detection
     ↓
 ┌───────────────┐
 │ Login Exists? │
 └───────┬───────┘
       No│     │Yes
         ↓     ↓
      Normal   Authentication
        QA          ↓
         │      Success?
         │       /   \
         │     Yes    No
         │      ↓      ↓
         │   Continue  Stop QA
         │      ↓
         └──→ AI Test Generation
                    ↓
              Playwright Testing
                    ↓
                PASS / FAIL
                    ↓
                CSV Report
```

## Test Types

The AI currently generates three main types of tests:

### Content Tests

Verifies that expected content exists on the page.

Example:

```text
Verify Customer Support heading is present
```

### Link Tests

Checks that a link exists and verifies its destination.

Example:

```text
Verify Order Now link href
```

### Navigation Tests

Clicks an actual link from the website and verifies that navigation reaches the expected URL.

Example:

```text
Navigate to Business Cards page
```

## Login Handling

The system first checks whether a website appears to contain a login system.

If no login system is detected:

```text
No login system detected
```

The system proceeds directly to normal QA testing.

If a login system is detected, the system requests test credentials through the terminal. The password is entered using Python's hidden password input and is not sent to the LLM or included in the CSV report.

Successful authentication allows the system to continue with QA testing.

If authentication fails, normal QA testing is stopped rather than assuming that the website itself is broken.

> The authentication flow is currently implemented as a prototype and should be tested against an authorized test website before being considered production-ready.

## Project Structure

```text
QA_automation/
│
├── main.py              # Main application flow
├── browser.py           # Browser launching and website inspection
├── auth.py              # Login detection and authentication
├── LLm.py               # AI test generation using Groq
├── test.py            # Playwright test execution
├── report.py          # CSV report generation
├── .gitignore
├── .env                 # Local API credentials (not committed)
└── venv/                # Python virtual environment (not committed)
```

## Technologies

* **Python**
* **Playwright**
* **Groq API**
* **OpenAI GPT-OSS 120B**
* **python-dotenv**
* **CSV**
* **HTML / Web technologies**

## Installation

Clone the repository:

```bash
git clone https://github.com/Wajidmalik12/QA-Automation.git
cd QA-Automation
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```
Install Playwright Chromium:

```bash
playwright install chromium
```

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

## Running the Project

Start the application:

```powershell
python main.py
```

Enter the website URL when prompted:

```text
Enter website URL:
```

The system will then inspect the website, generate test cases, execute them, and create a timestamped CSV report.

## Example

For a website without authentication, the system can generate tests such as:

```text
TEST 1
Name: Verify Customer Support heading is present
Type: content

TEST 2
Name: Verify Business Card price is displayed
Type: content

TEST 3
Name: Verify WhatsApp contact link href
Type: link

TEST 4
Name: Verify Order now link href
Type: link

TEST 5
Name: Navigate to Business Cards page
Type: navigation
```

Execution results are displayed in the terminal:

```text
[PASS] Verify Customer Support heading is present
[PASS] Verify Business Card price is displayed
[PASS] Verify WhatsApp contact link href
[PASS] Verify Order now link href
[PASS] Navigate to Business Cards page
```

## CSV Reports

Every execution generates a new timestamped report:

```text
qa_report_2026-09-22_03-27-24.csv
```

The report contains two sections:

1. **LLM Generated Test Plan**
2. **Playwright Execution Results**

This keeps the AI-generated expectations separate from the actual browser execution results.

## Current Limitations

* Login detection is heuristic-based.
* Authentication success detection is currently prototype-level.
* Login testing requires an authorized test account.
* AI-generated tests depend on the information available on the inspected page.
* The system currently focuses on content, links, and navigation rather than full functional/API/load testing.
* Dynamic websites may require additional handling.

## Future Improvements

* More robust authentication validation
* Positive and negative login test cases
* Form validation testing
* Button interaction testing
* Screenshot capture on failures
* Better handling of dynamic websites
* API testing
* Database-backed test history
* HTML dashboard for test results
* More advanced AI-generated test scenarios

## Purpose

This project explores how **LLMs and browser automation can work together to reduce the manual effort involved in website QA testing**.

Instead of manually writing every basic test case, the system uses the website's actual content and structure to generate test scenarios and then lets Playwright execute them automatically.
