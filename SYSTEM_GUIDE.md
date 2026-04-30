# 🧠 EDRMS — Complete System Guide

**A Plain-English, Step-by-Step Walkthrough for Non-Technical Readers**

> This document explains every part of the Early Dementia Routine Monitoring System: what it does, what tools were used, and how each piece of code works — written so that anyone can follow along and learn to build it themselves.

---

## Table of Contents

1. [What Does This System Do?](#1-what-does-this-system-do)
2. [The Tools & Frameworks Explained](#2-the-tools--frameworks-explained)
3. [Project Folder Structure](#3-project-folder-structure)
4. [Step-by-Step Implementation](#4-step-by-step-implementation)
   - Step 1: Setting Up the Database
   - Step 2: Defining the Data Models
   - Step 3: Creating Validation Schemas
   - Step 4: Building the Security Layer
   - Step 5: Building the API Endpoints
   - Step 6: The Rule-Based Detection Engine
   - Step 7: The Machine Learning Anomaly Detector
   - Step 8: Wiring It All Together
   - Step 9: The Caregiver Dashboard
   - Step 10: The Data Simulation Script
   - Step 11: Writing Automated Tests
5. [How Data Flows Through the System](#5-how-data-flows-through-the-system)
6. [How to Run Everything](#6-how-to-run-everything)
7. [Glossary of Technical Terms](#7-glossary-of-technical-terms)

---

## 1. What Does This System Do?

Imagine a care home where nurses look after elderly patients with early-stage dementia. Every day, patients are supposed to:

- **Eat meals** at regular times (breakfast, lunch, dinner).
- **Take medication** at scheduled times.
- **Sleep** at a consistent time each night.

When dementia begins, patients start **missing meals**, **forgetting medication**, or **sleeping at odd hours**. Nurses try to notice these changes, but they are busy and human observation is unreliable.

**EDRMS solves this by acting as a digital logbook with a built-in brain.** It:

1. **Records** every activity (meal, medication, sleep) for each patient.
2. **Checks rules** immediately — for example, "if medication is missed, raise an alert."
3. **Uses machine learning** to spot unusual patterns that a human might not notice.
4. **Shows everything** on a simple visual dashboard that any caregiver can read.

Think of it like a **smart alarm system for patient routines**.

---

## 2. The Tools & Frameworks Explained

Before diving into the code, here is a plain-English explanation of every tool used and **why** it was chosen.

### 🐍 Python (Programming Language)

Python is the language the entire system is written in. It was chosen because:
- It reads almost like English, making it beginner-friendly.
- It has the largest ecosystem of healthcare, data science, and web libraries.
- It is the industry standard for AI and machine learning work.

### 🌐 FastAPI (Web Framework)

**What it is:** A Python framework for building web APIs (Application Programming Interfaces).

**In plain English:** When a nurse logs a patient's meal on a tablet, that data needs to travel over the internet to our system. FastAPI is the "post office" that receives that data, processes it, and sends back a response. It automatically creates interactive documentation (a web page where you can test the system without writing code).

**Why FastAPI over alternatives like Flask or Django:** FastAPI is modern, extremely fast, and automatically validates incoming data. It also generates its own documentation page.

### 🗄️ SQLite + SQLAlchemy (Database & Database Toolkit)

**SQLite — What it is:** A lightweight database that stores all data in a single file on your computer (called `edrms.db`).

**In plain English:** Think of SQLite as a digital filing cabinet. Every patient record, every activity log, and every alert is stored in neatly organised "drawers" (called tables). Unlike big databases like PostgreSQL or MySQL, SQLite requires zero setup — it just works.

**SQLAlchemy — What it is:** A Python library that lets you interact with the database using Python code instead of writing raw database commands (SQL).

**In plain English:** Instead of writing `INSERT INTO patients (name, age) VALUES ('John', 78)`, you simply write `Patient(name="John", age=78)` in Python. SQLAlchemy translates your Python into database language behind the scenes. This is called an **ORM** (Object-Relational Mapper).

### 📋 Pydantic (Data Validation)

**What it is:** A Python library that checks incoming data is correct before we use it.

**In plain English:** If someone accidentally sends a patient's age as "eighty" (text) instead of `80` (a number), Pydantic catches the mistake immediately and returns a clear error message. It acts as a **quality control inspector** at the front door of our system.

### 🔐 python-jose & passlib (Security)

**python-jose — What it is:** Creates and verifies JWT tokens (JSON Web Tokens).

**In plain English:** When a caregiver logs in, the system gives them a digital "wristband" (a token). Every time they make a request, they show their wristband to prove they are authorised. The token expires after 30 minutes, so a stolen token cannot be used forever.

**passlib — What it is:** Hashes (scrambles) passwords before storing them.

**In plain English:** We never store passwords as plain text. If someone's password is `password123`, passlib converts it into something like `$2b$12$LJ3m5...` — a scrambled string that cannot be reversed. Even if a hacker stole the database, they could not read the passwords.

### 🤖 scikit-learn (Machine Learning)

**What it is:** Python's most popular library for traditional machine learning.

**In plain English:** We use one specific algorithm from scikit-learn called **Isolation Forest**. Imagine you have a flock of sheep and one wolf dressed as a sheep. The Isolation Forest algorithm works by asking: "How easy is it to isolate (separate) this animal from the group?" Normal sheep blend in and are hard to isolate. The wolf behaves differently and is easy to separate. The algorithm finds the "wolves" — the unusual activity patterns.

**Why Isolation Forest specifically:** It is an *unsupervised* algorithm, meaning it does not need labelled examples of "normal" and "abnormal." It learns what "normal" looks like by itself, which is perfect because we do not have pre-labelled dementia data.

### 📊 Streamlit (Dashboard)

**What it is:** A Python framework that turns Python scripts into interactive web dashboards with zero front-end coding.

**In plain English:** Building a traditional web dashboard requires HTML, CSS, and JavaScript — three separate languages. Streamlit lets you build a visual dashboard using only Python. You write `st.title("Hello")` and a title appears on a web page. It is perfect for data-focused applications.

### 📦 pandas (Data Manipulation)

**What it is:** A Python library for working with tabular data (like spreadsheets).

**In plain English:** When the ML model needs to analyse patient activities, pandas organises that data into neat rows and columns (called a DataFrame), just like an Excel spreadsheet. This makes it easy to filter, sort, and feed data into the machine learning model.

### 🧪 pytest (Testing)

**What it is:** A Python framework for writing and running automated tests.

**In plain English:** Instead of manually clicking through the system to check if everything works, we write small test scripts that do it automatically. If someone changes the code and accidentally breaks something, the tests will catch it immediately.

---

## 3. Project Folder Structure

Here is the complete folder layout with an explanation of every file:

```
dementia-routine-monitoring-api/
│
├── app/                          # The main application code
│   ├── main.py                   # 🚪 The front door — starts the server
│   ├── database.py               # 🗄️ Connects to the SQLite database
│   ├── security.py               # 🔐 Password hashing & JWT tokens
│   ├── dashboard.py              # 📊 The Streamlit caregiver dashboard
│   │
│   ├── models/                   # 📦 Database table definitions
│   │   ├── __init__.py           # Registers all models
│   │   ├── user.py               # The "users" table
│   │   ├── patient.py            # The "patients" table
│   │   ├── activity.py           # The "activities" table
│   │   └── alert.py              # The "alerts" table
│   │
│   ├── schemas/                  # ✅ Data validation rules
│   │   ├── __init__.py           # Registers all schemas
│   │   ├── user.py               # Rules for user data
│   │   ├── patient.py            # Rules for patient data
│   │   ├── activity.py           # Rules for activity data
│   │   └── alert.py              # Rules for alert data
│   │
│   ├── api/                      # 🌐 API endpoint handlers
│   │   ├── auth.py               # Login & registration
│   │   ├── patients.py           # Create & view patients
│   │   ├── activities.py         # Log & view activities
│   │   └── alerts.py             # View alerts & trigger ML
│   │
│   ├── services/                 # ⚙️ Business logic
│   │   ├── rule_engine.py        # Rule-based detection
│   │   └── alert_service.py      # Helper to create alerts
│   │
│   └── ml/                       # 🤖 Machine learning
│       └── anomaly_detector.py   # Isolation Forest detector
│
├── data/
│   └── simulate_patient_data.py  # 🧪 Script to generate fake data
│
├── tests/                        # 🧪 Automated tests
│   ├── test_api.py               # Tests for API endpoints
│   └── test_alerts.py            # Tests for alert generation
│
├── requirements.txt              # 📋 List of dependencies
├── .gitignore                    # 🚫 Files to exclude from Git
└── README.md                     # 📖 Project overview
```

**Key Concept — Separation of Concerns:** Notice how the code is split into small, focused folders. Models define *what* the data looks like. Schemas define *how to validate* incoming data. API files define *what URLs are available*. Services contain the *business logic*. This separation makes the code easier to understand, test, and maintain.

---

## 4. Step-by-Step Implementation

This section walks through every file in the order you would build it from scratch.

---

### Step 1: Setting Up the Database — `app/database.py`

**What this file does:** Creates a connection to the SQLite database and provides a reusable way for the rest of the application to talk to it.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./edrms.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Line-by-line explanation:**

| Line | What It Does |
|------|-------------|
| `SQLALCHEMY_DATABASE_URL = "sqlite:///./edrms.db"` | The address of our database. `sqlite:///` means "use SQLite" and `./edrms.db` means "create a file called edrms.db in the current folder." |
| `engine = create_engine(...)` | The engine is the "motor" that powers all database communication. The `check_same_thread=False` setting is required for SQLite to work with web servers. |
| `SessionLocal = sessionmaker(...)` | A session is like opening a conversation with the database. This line creates a factory that can produce new sessions on demand. |
| `Base = declarative_base()` | The foundation class that all our database models will inherit from. Think of it as the blank template for creating tables. |
| `get_db()` | A helper function that opens a database session, lets the caller use it, and then closes it afterwards — no matter what happens. This prevents database connection leaks. |

---

### Step 2: Defining the Data Models — `app/models/`

Models define **what the database tables look like**. Each model is a Python class that maps to a table.

#### `app/models/user.py` — The Users Table

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="caregiver")
```

**In plain English:** This creates a table called `users` with four columns: a unique ID number, an email address (which must be unique), the scrambled password, and a role (either "caregiver" or "admin").

#### `app/models/patient.py` — The Patients Table

```python
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    diagnosis_stage = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
```

**In plain English:** Stores each patient's name, age, their current dementia stage (e.g., "Early", "Mid"), and when their record was created.

#### `app/models/activity.py` — The Activities Table

```python
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    activity_type = Column(String, index=True)   # meal, medication, sleep
    timestamp = Column(DateTime, index=True)
    status = Column(String)                       # completed, missed, delayed
    
    patient = relationship("Patient")
```

**In plain English:** Each row is one activity event. It records *which patient* did it (`patient_id`), *what type* of activity (meal, medication, or sleep), *when* it happened, and *whether* it was completed, missed, or delayed. The `ForeignKey` links each activity back to a specific patient — so you cannot log an activity for a patient that does not exist.

#### `app/models/alert.py` — The Alerts Table

```python
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    alert_type = Column(String, index=True)
    severity = Column(String)     # low, medium, high
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    patient = relationship("Patient")
```

**In plain English:** When the system detects something wrong, it creates an alert. Each alert records which patient it is about, the type of problem (e.g., `medication_missed`), how serious it is (low/medium/high), and a human-readable message explaining what happened.

---

### Step 3: Creating Validation Schemas — `app/schemas/`

Schemas are the **quality control checkpoint**. They define what data is required and in what format.

For example, the patient schema:

```python
class PatientBase(BaseModel):
    name: str
    age: int
    diagnosis_stage: str

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
```

**Why three classes?**

| Class | Purpose |
|-------|---------|
| `PatientBase` | The shared fields that both input and output have in common. |
| `PatientCreate` | What the user sends *in* when creating a patient. Inherits from Base. |
| `PatientResponse` | What the system sends *back* after creating a patient. Includes `id` and `created_at` which the system generates automatically. |

This pattern is repeated for User, Activity, and Alert schemas.

---

### Step 4: Building the Security Layer — `app/security.py`

This file handles two things: **password security** and **login tokens**.

```python
SECRET_KEY = "your-super-secret-key-for-edrms-demo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Password hashing** uses the **bcrypt** algorithm. When a user registers:
1. They send their password (e.g., `password123`).
2. `get_password_hash()` scrambles it into `$2b$12$LJ3m5...`.
3. Only the scrambled version is stored in the database.

When they log in:
1. They send their password again.
2. `verify_password()` scrambles it and compares it to the stored scramble.
3. If they match, the user is genuine.

**JWT tokens** work like digital wristbands:
1. After a successful login, `create_access_token()` creates a token containing the user's email and role.
2. The token is signed with the `SECRET_KEY` so it cannot be forged.
3. The token expires after 30 minutes.

---

### Step 5: Building the API Endpoints — `app/api/`

These files define the URLs that the outside world can call.

#### Authentication — `app/api/auth.py`

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/auth/register` | POST | Creates a new user account. Hashes the password before storing. Rejects duplicate emails. |
| `/auth/login` | POST | Checks email and password. If valid, returns a JWT token. |

#### Patients — `app/api/patients.py`

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/patients/` | POST | Creates a new patient record. |
| `/patients/` | GET | Lists all patients (with optional pagination). |
| `/patients/{id}` | GET | Retrieves a single patient by their ID. |

#### Activities — `app/api/activities.py`

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/activities/` | POST | Logs a new activity. **Crucially, it also triggers the rule engine** to check for problems immediately. |
| `/activities/patient/{id}` | GET | Lists all activities for a specific patient. |

**The critical integration point:** After saving the activity, the code calls `process_activity_rules(db_activity, db)`. This is what makes the system "smart" — every single activity is checked against the detection rules the moment it is logged.

#### Alerts — `app/api/alerts.py`

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/alerts/` | GET | Lists all alerts across all patients. |
| `/alerts/patient/{id}` | GET | Lists alerts for a specific patient. |
| `/alerts/patient/{id}/run-ml-detection` | POST | Manually triggers the ML anomaly detector for a patient. |

---

### Step 6: The Rule-Based Detection Engine — `app/services/rule_engine.py`

This is the **heart of the system**. It contains simple, explainable rules that a doctor or nurse could understand and agree with.

**Rule 1 — Missed Medication → Immediate High Alert**
```
IF activity type is "medication" AND status is "missed"
THEN create an alert with severity "high"
```
Medication is critical for dementia patients. A single missed dose triggers an immediate alert.

**Rule 2 — Two or More Missed Meals in 24 Hours → Medium Alert**
```
IF activity type is "meal" AND status is "missed"
AND there have been 2+ missed meals in the last 24 hours
THEN create an alert with severity "medium"
```
Missing one meal might be normal. Missing two or more suggests confusion or loss of appetite — an early warning sign.

**Rule 3 — Delayed Sleep → Low Alert**
```
IF activity type is "sleep" AND status is "delayed"
THEN create an alert with severity "low"
```
A slightly delayed bedtime is worth noting but is less urgent than missed medication.

**Why rules first, ML second?** In healthcare, decisions must be **explainable**. A doctor needs to understand *why* an alert was raised. "The patient missed their 9am medication" is clear. "The ML model gave a score of -0.73" is not. Rules provide transparency; ML provides depth.

---

### Step 7: The Machine Learning Anomaly Detector — `app/ml/anomaly_detector.py`

The ML component goes beyond simple rules to find **subtle, complex patterns** that rules cannot capture.

**How it works, step by step:**

1. **Fetch Data:** Pull all activities for a given patient from the database.
2. **Extract Features:** Convert each activity into three numbers:
   - `hour_of_day` — What hour did the activity happen? (0–23)
   - `activity_type` — Encoded as: meal=0, medication=1, sleep=2
   - `status` — Encoded as: completed=0, delayed=1, missed=2
3. **Train the Model:** The Isolation Forest examines all activities and learns what "normal" looks like.
4. **Predict:** Each activity is scored. Normal activities get `+1`. Unusual activities get `-1` (anomaly).
5. **Return Results:** The anomalous activities are returned as a list.

**The `contamination=0.1` parameter** tells the algorithm: "Expect roughly 10% of the data to be anomalous." This prevents the model from flagging everything or nothing.

**Minimum data requirement:** The model needs at least 10 activities before it can run. With fewer data points, there is not enough information to distinguish normal from abnormal.

---

### Step 8: Wiring It All Together — `app/main.py`

This is the **entry point** of the entire application. It:

1. Creates all database tables if they do not already exist (`Base.metadata.create_all`).
2. Initialises the FastAPI application with a title and description.
3. Registers all four routers (auth, patients, activities, alerts) so their endpoints become available.
4. Adds CORS middleware (allows the dashboard to communicate with the API from a browser).
5. Defines a simple root endpoint (`/`) that returns a welcome message.

---

### Step 9: The Caregiver Dashboard — `app/dashboard.py`

The Streamlit dashboard provides a **visual interface** so caregivers do not need to use the API directly.

**Page 1 — Patients Overview:**
- Displays a table of all registered patients.
- Lets the caregiver select a patient and view their activity history.

**Page 2 — Alerts & Anomalies:**
- Shows all generated alerts, colour-coded by severity (red for high, orange for medium, blue for low).
- Has a button to manually trigger the ML anomaly detection for any patient.

The dashboard communicates with the FastAPI backend via HTTP requests — the same way a web browser loads a webpage.

---

### Step 10: The Data Simulation Script — `data/simulate_patient_data.py`

Since this is a demonstration system without real patients, this script **generates realistic fake data** to show how the system works.

**What it does, in order:**
1. Registers a doctor user account.
2. Creates a patient named "John Doe", aged 78, early-stage dementia.
3. Logs 3 days of **normal** baseline activity (meals and medication completed on time).
4. Logs **anomalous** activity for today: a missed medication and two missed meals.
5. The rule engine automatically triggers alerts for the anomalous activities.

After running this script, the dashboard will show alerts and the ML detector will have enough data to find patterns.

---

### Step 11: Writing Automated Tests — `tests/`

#### `tests/test_api.py` — API Endpoint Tests

These tests verify that the core API works correctly:
- `test_read_main()` — Checks the root URL returns the welcome message.
- `test_create_patient()` — Creates a patient and verifies the response contains the correct name and an ID.
- `test_log_activity()` — Logs an activity and verifies it was recorded.

**Important detail:** Tests use a *separate* database (`test_edrms.db`) so they never interfere with real data.

#### `tests/test_alerts.py` — Alert Integration Test

This test verifies the **entire chain** works end-to-end:
1. Create a patient.
2. Log a missed medication.
3. Check that the rule engine automatically created a "medication_missed" alert with "high" severity.

---

## 5. How Data Flows Through the System

Here is the complete journey of a single activity through the system:

```
Caregiver logs "Patient 1 missed medication at 9:00 AM"
         │
         ▼
┌─────────────────────────┐
│  API Layer (FastAPI)     │  → Receives the HTTP request
│  activities.py           │  → Validates data using Pydantic schema
│                          │  → Checks patient exists in database
│                          │  → Saves activity to database
│                          │  → Calls rule engine ─────────────────┐
└─────────────────────────┘                                       │
                                                                  ▼
                                               ┌──────────────────────────┐
                                               │  Rule Engine             │
                                               │  rule_engine.py          │
                                               │                          │
                                               │  Checks:                 │
                                               │  ✓ Is it medication?     │
                                               │  ✓ Is status "missed"?   │
                                               │  → YES: Create alert!    │
                                               └──────────┬───────────────┘
                                                          │
                                                          ▼
                                               ┌──────────────────────────┐
                                               │  Alert Service           │
                                               │  alert_service.py        │
                                               │                          │
                                               │  Creates alert record:   │
                                               │  type: medication_missed │
                                               │  severity: high          │
                                               │  Saves to database       │
                                               └──────────────────────────┘
                                                          │
                                                          ▼
                                               ┌──────────────────────────┐
                                               │  Dashboard (Streamlit)   │
                                               │  dashboard.py            │
                                               │                          │
                                               │  Displays alert in RED   │
                                               │  for caregiver to see    │
                                               └──────────────────────────┘
```

---

## 6. How to Run Everything

### Prerequisites
- Install Python 3.10 or newer from [python.org](https://python.org).

### Step-by-step:

```bash
# 1. Clone the repository
git clone https://github.com/ummaruje/dementia-routine-monitoring-api.git
cd dementia-routine-monitoring-api

# 2. Create a virtual environment (an isolated Python workspace)
python -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 4. Install all dependencies
pip install -r requirements.txt

# 5. Start the API server (Terminal 1)
uvicorn app.main:app --reload

# 6. In a NEW terminal, simulate patient data (Terminal 2)
source venv/bin/activate
python data/simulate_patient_data.py

# 7. In another NEW terminal, launch the dashboard (Terminal 3)
source venv/bin/activate
streamlit run app/dashboard.py

# 8. Run the automated tests
source venv/bin/activate
PYTHONPATH=. pytest tests/
```

After step 5, visit **http://127.0.0.1:8000/docs** to see the interactive API documentation.

After step 7, the Streamlit dashboard opens automatically in your web browser.

---

## 7. Glossary of Technical Terms

| Term | Plain English Meaning |
|------|----------------------|
| **API** | A set of URLs that software can call to send or receive data. Like a restaurant menu — you place an order (request) and get food (response). |
| **Endpoint** | A specific URL in the API. For example, `/patients/` is an endpoint for managing patients. |
| **HTTP Methods (GET/POST)** | GET = "give me data." POST = "here is new data, save it." |
| **Database** | An organised digital filing cabinet that stores information permanently. |
| **Table** | A single "drawer" in the filing cabinet. Each table stores one type of data (patients, activities, etc.). |
| **Column** | A specific piece of information in a table — like "name" or "age." |
| **Row/Record** | One complete entry in a table — one patient, one activity, etc. |
| **Foreign Key** | A link between two tables. The `patient_id` in the activities table points back to a specific patient. |
| **ORM** | Object-Relational Mapper. Lets you write Python code instead of database commands. |
| **Schema** | A set of rules defining what data looks like and what format it must be in. |
| **JWT Token** | A digital "wristband" that proves you are logged in. |
| **Hashing** | Scrambling a password into an unreadable string. Cannot be reversed. |
| **Machine Learning** | Teaching a computer to find patterns in data without explicit instructions. |
| **Isolation Forest** | An ML algorithm that finds unusual data points by measuring how easy they are to separate from the group. |
| **Anomaly** | Something that does not fit the normal pattern. |
| **CORS** | Cross-Origin Resource Sharing. A security setting that allows the dashboard (running on one port) to talk to the API (running on a different port). |
| **Virtual Environment** | An isolated Python workspace. Keeps this project's packages separate from other projects on your computer. |
| **Dependencies** | External packages/libraries that the project needs to work (listed in `requirements.txt`). |
| **Middleware** | Code that runs on every request before it reaches your endpoint. CORS middleware is an example. |
| **Router** | A way to group related API endpoints together. The `auth` router handles all `/auth/...` URLs. |

---

> **Author:** Umar Abdulkadir Isa — AI Engineer, Care Sector Portfolio  
> Built with ❤️ for the 900,000 people living with dementia in the UK
