# 📡 Enterprise Telco Reporting System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.7-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

<img width="1438" height="775" alt="Screenshot 2026-01-15 230753" src="https://github.com/user-attachments/assets/bb279e38-5d32-4dd6-86c7-7c38c0ac546b" />

> **Architected by:** Aryaguna Abi Rafdi Yasa

## 📋 Executive Summary

The **Enterprise Telco Reporting System** is a robust, end-to-end Data Engineering solution designed to automate the ingestion, transformation, and visualization of telecommunication product data.

By integrating **Django** as the orchestration layer and **dbt (data build tool)** for complex SQL transformations, this system replaces manual data processing with a scalable ELT (Extract, Load, Transform) pipeline. It features an intelligent ingestion engine capable of handling unstructured filenames via Regex, applying complex business logic (segmentation), and presenting actionable insights through a modern, interactive dashboard.

---

To make your project look truly **Enterprise-Grade**, you need a **Data Pipeline Architecture Diagram**. This visualizes how data travels from the user's CSV file all the way to the final dashboard.

This is exactly what potential employers or clients want to see: **Logic and Architecture.**

Here is a professional breakdown of the **Data Flow** and **User Interface (UI) Flow** for your system.

---

### 1. High-Level Data Pipeline Architecture (For README)

You can copy this **Mermaid** code into your `README.md` (GitHub supports Mermaid diagrams natively). It renders a beautiful flowchart.

```mermaid
graph TD
    %% Styles
    classDef user fill:#f9f,stroke:#333,stroke-width:2px;
    classDef app fill:#667eea,stroke:#333,stroke-width:2px,color:white;
    classDef db fill:#4169E1,stroke:#333,stroke-width:2px,color:white;
    classDef dbt fill:#FF694B,stroke:#333,stroke-width:2px,color:white;

    subgraph "Frontend Layer (Glassmorphism UI)"
        User((User / Engineer)):::user
        UploadUI[📂 Upload Interface]:::app
        DashboardUI[📊 Analytics Dashboard]:::app
    end

    subgraph "Orchestration Layer (Django)"
        Ingest[⚙️ Ingestion Service]:::app
        BatchLogic{Batch Logic}:::app
        Trigger[⚡ dbt Trigger]:::app
    end

    subgraph "Data Warehouse (PostgreSQL)"
        RawTable[(Raw Data Tables)]:::db
        StagingView[(Staging Views)]:::db
        FinalTable[(Reporting Marts)]:::db
    end

    subgraph "Transformation Layer (dbt)"
        dbt_run(dbt run):::dbt
        Regex[Regex Extraction]:::dbt
        BizLogic[Business Rules]:::dbt
    end

    %% Flow Connections
    User -->|Drag & Drop CSV| UploadUI
    UploadUI -->|POST Request| Ingest
    Ingest -->|Generate Suffix| BatchLogic
    BatchLogic -->|Save data_raw_150126| RawTable
    
    Ingest -->|On Success| Trigger
    Trigger -->|Execute Subprocess| dbt_run
    
    dbt_run -->|Read| RawTable
    dbt_run -->|Clean & Extract| Regex
    Regex -->|Apply Segmentation| BizLogic
    BizLogic -->|Materialize| FinalTable
    
    DashboardUI -->|Query (SQL)| FinalTable
    FinalTable -->|Return Data| DashboardUI
    DashboardUI -->|Download CSV| User

```

### What to do next?

1. **Copy the Mermaid Code** above.
2. **Edit your `README.md**` file again.
3. Paste the code inside the README under a new section called `## 🔄 Data Architecture`.

This diagram is what separates "Coding Exercises" from **"System Engineering"**. It shows you understand the *big picture*.

## 🚀 Key Features

### 1. Intelligent Data Ingestion
* **Smart Batching Mechanism:** Implements an auto-incrementing suffix logic (e.g., `batch_150126_1`) to prevent data collisions and ensure data integrity across multiple daily uploads.
* **Regex-Powered Extraction:** Utilizes advanced Regular Expressions within SQL to extract metadata (dates, cities) from non-standard filenames (e.g., parsing `20260102` correctly regardless of its position in the string).
* **Asynchronous Processing:** Handles large CSV bulk uploads efficiently with visual feedback.

### 2. Advanced ELT Transformation (dbt)
* **Automated Triggers:** Django signals automatically trigger `dbt run` commands upon successful raw data ingestion.
* **Complex Business Logic:**
    * **Price Segmentation:** Categorizes products into *High/Medium/Low* tiers based on dynamic thresholds.
    * **Validity Normalization:** Standardizes validity periods into *Daily, Weekly, Monthly,* and *>30Days*.
    * **JSON Restructuring:** Reconstructs raw JSON description formats for backend compatibility while maintaining human-readable data for the frontend.

### 3. Modern Interactive Dashboard
* **Glassmorphism UI:** Aesthetically pleasing interface designed for high usability and modern web standards.
* **Human-in-the-Loop Validation:** Features an editable data grid allowing authorized users to correct data anomalies directly within the UI, with real-time database updates.
* **Report Generation:** One-click export functionality to generate standardized CSV reports for stakeholders.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core logic and scripting |
| **Orchestration** | Django 4.2 | Web framework, process management, and UI backend |
| **Warehouse** | PostgreSQL | Relational database for raw and transformed data |
| **Transformation** | dbt (data build tool) | Modular SQL transformation and testing |
| **Frontend** | Bootstrap 5, JS | Responsive UI with DataTables and SweetAlert2 |
| **Version Control** | Git & GitHub | Source code management |

---

## 📂 Project Structure

```bash
Enterprise-Reporting-System/
├── Django_apps/             # Core Application Logic
│   ├── config/              # Project configuration and settings
│   ├── upload/              # App handling ingestion, views, and services
│   ├── templates/           # HTML5 templates (Glassmorphism UI)
│   └── static/              # CSS, JavaScript, and assets
├── dbt_project/             # Transformation Layer
│   ├── models/
│   │   ├── staging/         # Cleaning and standardization views
│   │   ├── intermediate/    # Regex logic and business rule application
│   │   └── marts/           # Final production-ready tables
│   ├── dbt_project.yml      # dbt configuration
│   └── profiles.yml         # Database connection settings
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

```

---

## ⚡ Installation & Setup Guide

Follow these instructions to set up the development environment locally.

### Prerequisites

* Python 3.8 or higher
* PostgreSQL installed and running
* Git

### 1. Clone the Repository

```bash
git clone [https://github.com/rafdi03/Enterprise-Reporting-System.git](https://github.com/rafdi03/Enterprise-Reporting-System.git)
cd Enterprise-Reporting-System

```

### 2. Set Up Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Database

Create a PostgreSQL database (e.g., `telco_db`) and update the `Django_apps/config/settings.py` file with your credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'telco_db',
        'USER': 'your_postgres_user',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```

### 5. Configure dbt Profile

Ensure your `~/.dbt/profiles.yml` or the project-local `profiles.yml` is configured to point to the same PostgreSQL database.

### 6. Run Migrations & Start Server

```bash
cd Django_apps
python manage.py migrate
python manage.py runserver

```

### 7. Access the Application

Open your browser and navigate to:
**`http://127.0.0.1:8000/`**

---

## 📖 Usage Workflow

1. **Ingest:** Navigate to the upload page. Drag and drop your raw Telco CSV files. The system will automatically assign a unique batch ID.
2. **Process:** Watch the real-time loader. The system extracts specific metadata (dates, cities) using Regex and applies `dbt` transformations.
3. **Analyze:** Click "Access Dashboard" to view the transformed data.
4. **Refine:** Double-click any cell in the table to perform manual data corrections if necessary.
5. **Export:** Use the "Download CSV" button to retrieve the final, clean dataset for downstream reporting.

---

## 👨‍💻 Author

**Aryaguna Abi Rafdi Yasa**

* *System Architect & Data Engineer*
* [GitHub Profile]([https://www.google.com/search?q=https://github.com/rafdi03](https://github.com/rafdi03))

---

> *Built with precision for scalable data operations.*

---

### **Step 2: Update `requirements.txt` (Crucial)**
Since the README instructs users to install from `requirements.txt`, you must ensure this file exists and is up to date.

Run this command in your terminal (make sure your virtual environment is active):

```bash
pip freeze > requirements.txt

```

### **Step 3: Commit and Push**

Now, upload the README and the updated requirements file to your GitHub repository:

```bash
git add README.md requirements.txt
git commit -m "Docs: Add professional README and update requirements"
git push origin main

```

Now your repository will look like a top-tier engineering project! 🚀
