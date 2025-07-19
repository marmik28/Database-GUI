
# 🏐 Montréal Volleyball Club — Full Stack Database GUI

A full-stack web app built with **PostgreSQL**, **Flask**, and **React** to view and interact with club data and predefined queries.

---

## 🎬 Demo

![Demo of the UI](/demo.gif)


## 📁 Project Structure

```
Database-GUI/
├── backend/                # Flask API with predefined queries
│   ├── app.py
│   ├── config.py
│   ├── queries/
│   │   └── predefined.py
│   ├── .env
│   └── requirements.txt
├── frontend/               # React UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── TableViewer.tsx
│   │   │   └── QueryViewer.tsx
│   │   └── api/client.ts
│   └── package.json
└── final_reset.sql         # PostgreSQL schema + seed data
```

---

## 🛠 Requirements

- Python 3.10+
- Node.js + npm
- PostgreSQL (installed + running)
- pgAdmin (for DB import)

---

## ⚙️ Setup Instructions

### 1. 🧩 Database (PostgreSQL)

1. Create a database:

```sql
CREATE DATABASE mvc_db;
```

2. In pgAdmin or psql, run:

```sql
-- Run this file
\i completeDB.sql
```

It will:
- Create all tables
- Insert personnel, members, hobbies, relationships
- Load payments and setup clean state

---

### 2. 🔌 Backend (Flask)

#### 🐍 Setup Python environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### 🔐 Create `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mvc_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

#### ▶ Run backend:

```bash
flask run
```

Backend runs on: [http://localhost:5000](http://localhost:5000)

---

### 3. 💻 Frontend (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs on: [http://localhost:3000](http://localhost:3000)

---

## 🚀 Features

### Table Viewer
- View any database table
- Dropdown to select from:
  - clubmembers, personnel, payments, etc.

### Query Viewer
- Choose from 8 predefined SQL queries
- See results instantly in a styled table

---

## 🧪 API Endpoints

| Endpoint                  | Description                  |
|---------------------------|------------------------------|
| `/api/tables/<name>`     | View data from any table     |
| `/api/query/<1-8>`       | Run one of 8 queries         |

---

## 📝 Predefined Queries Summary

1. Count of members and GMs by location
2. Adult members who are also personnel
3. Members with 3+ hobbies
4. Members with no hobbies
5. Age distribution of members
6. Family-member/child mappings
7. Membership fees vs donations
8. Inactive members with outstanding dues

---

## ✅ License

MIT — open for educational use.
