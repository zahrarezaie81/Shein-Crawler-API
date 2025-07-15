# 🛍️ Shein Product Crawler & FastAPI Project

This project is a web crawler and REST API that collects and serves product data from the Shein website. It uses Playwright for browser automation and FastAPI for building a backend API. Data is stored in a MySQL database and managed through Alembic migrations.

---

## ⬇️ Clone the Repository

Open a terminal and run:

```bash
git clone <REPO_URL>
cd Shein_Project
```

> Replace `<REPO_URL>` with the actual repository URL.

---

## 📁 Project Structure

```
Shein_Project/
├── project/
│   ├── crawler/
│   ├── database/
│   ├── loggs/
│   ├── main.py
├── alembic/
├── alembic.ini
├── requirements.txt
└── venv/
```

---

## ⚙️ Setup Instructions

### 1. 📦 Create & Activate Virtual Environment

Run these commands from the `Shein_Project` root folder:

```bash
python -m venv venv
.env\Scriptsctivate
```

Then install all required packages:

```bash
pip install -r requirements.txt
```

---

### 2. 🛠️ Configure the Database

Create a MySQL database named `shein_project`.

Update your credentials in this file:
```
project/database/database.py
```

Example:

```python
DATABASE_URL = "mysql+pymysql://your_user:your_password@localhost/shein_project"
```

---

### 3. 🧠 Setup Chrome & Auth

Update these variables in `project/crawler/auth_fetch.py`:

```python
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
user_data_dir = "C:/Users/yourname/AppData/Local/Google/Chrome/User Data/Profile 3"
```

Make sure you're logged into [shein.com](https://shein.com) with this profile.

---

### 4. 🧪 Configure Crawling Categories

Edit the YAML config file: `project/crawler/config.yaml`

```yaml
categories:
  - main_category: "Women Clothing"
    sub_category: "Wedding"
    brand: ""
    max_count: 50

  - main_category: "Women Clothing"
    sub_category: "Party Wear"
    brand: "SHEIN"
    max_count: 50
```

---

### 5. 🔐 Fetch Auth Headers

> Must be run from the **root** folder and **after activating venv**.

```bash
.env\Scriptsctivate
python -m project.crawler.auth_fetch
```

This generates `auth_data.json` with your valid cookies and headers.

---

### 6. 🚀 Run FastAPI Server

From the root folder:

```bash
.env\Scriptsctivate
uvicorn project.main:app --reload
```

Visit the Swagger API docs at:  
📎 http://127.0.0.1:8000/docs

---

## 🧬 Alembic Migrations

Generate new migration:

```bash
alembic revision --autogenerate -m "your message"
```

Apply migration:

```bash
alembic upgrade head
```

---

## 🧾 License

This project is for educational and testing purposes only.
