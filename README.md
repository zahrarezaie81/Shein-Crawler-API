# 🛍️ Shein Product Crawler & FastAPI Project

This project is a web crawler and REST API that collects and serves product data from the Shein website. It uses **Playwright** for browser automation and **FastAPI** for the backend. Data is stored in a **MySQL** database and migrations are handled by **Alembic**.

---

## ⬇️ Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/zahrarezaie81/Shein-Crawler-API.git
cd Shein-Crawler-API
```

---

## 📁 Project Structure

```
Shein-Crawler-API/
├── alembic/
├── output_jsons/
├── project/
│   ├── config/
│   ├── crawler/
│   ├── database/
│   ├── image_processor/
│   ├── loggs/
│   ├── main.py
│   └── __init__.py
├── .gitignore
├── alembic.ini
├── README.md
├── requirements.txt
└── venv/
```

---

## ⚙️ Setup Instructions

### 1. 📦 Create & Activate Virtual Environment

From the `Shein-Crawler-API` root folder:

```bash
python -m venv venv
.env\Scriptsctivate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. 🛠️ Configure the Database

Create a **MySQL** database named `shein_project`.

Then update your DB credentials inside:

```
project/database/database.py
```

Example:

```python
DATABASE_URL = "mysql+pymysql://your_user:your_password@localhost/shein_project"
```

---

### 3. 🧠 Setup Chrome & Authentication

Update the following variables in `project/crawler/auth_fetch.py`:

```python
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
user_data_dir = "C:/Users/yourname/AppData/Local/Google/Chrome/User Data/Profile 3"
```

Make sure you're already logged into [shein.com](https://shein.com) using that Chrome profile.

---

### 4. 🧪 Configure Crawling Categories

Edit the file `project/crawler/config.yaml`:

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

Run from the **root** folder (after activating your venv):

```bash
.env\Scriptsctivate
python -m project.crawler.auth_fetch
```

This will generate `auth_data.json` with valid cookies and headers.

---

### 6. 🚀 Run FastAPI Server

Run from the **project root folder**:

```bash
.env\Scriptsctivate
uvicorn project.main:app --reload
```

Then visit the Swagger docs:  
📎 http://127.0.0.1:8000/docs

---

## 🧬 Alembic Migrations

To generate a new migration:

```bash
alembic revision --autogenerate -m "your message"
```

To apply migrations:

```bash
alembic upgrade head
```

---

## 🧾 License

This project is for educational and testing purposes only.
