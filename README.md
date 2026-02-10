# Chemical Equipment Parameter Visualizer  
### Hybrid Web + Desktop Application

A hybrid application built as part of the **Intern Screening Task**, designed to visualize and analyze chemical equipment parameters using a **common Django backend**, with both **Web (React)** and **Desktop (PyQt5)** frontends.

The **Chemical Equipment Parameter Visualizer** allows users to upload a CSV file containing chemical equipment data. The backend parses and analyzes the data and exposes REST APIs consumed by:

- 🌐 **Web Application (React + Chart.js)**
- 🖥️ **Desktop Application (PyQt5 + Matplotlib)**

Both frontends provide consistent data tables, charts, and summary statistics.

The application expects a CSV file with the following columns:
Equipment Name, Type, Flowrate, Pressure, Temperature


A sample dataset is included:  
📄 `sample_equipment_data.csv`

---

## Tech Stack

| Layer | Technology | Purpose |
|------|-----------|---------|
| Frontend (Web) | React.js + Chart.js | Tables & charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Desktop visualization |
| Backend | Django + Django REST Framework | REST APIs |
| Data Handling | Pandas | CSV parsing & analytics |
| Database | SQLite | Store last 5 datasets |
| Version Control | Git & GitHub | Source control |

---

## Key Features

- 📂 **CSV Upload** from both Web and Desktop applications  
- 📊 **Data Summary API**  
  - Total equipment count  
  - Average flowrate, pressure, temperature  
  - Equipment type distribution  
- 📈 **Visualizations**
  - Chart.js (Web)
  - Matplotlib (Desktop)
- 🕘 **History Management**
  - Stores last 5 uploaded datasets with summaries
- 📄 **PDF Report Generation**
- 🔐 **Basic Authentication**
- ✅ Uses provided sample CSV for demo & testing

---


---

## Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/BhagyaSriRao/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

### 2️⃣ Backend Setup (Django)

Navigate to the backend folder, create a virtual environment, install dependencies, and start the Django server:

```bash
cd backend
python -m venv venv
```

# Activate virtual environment

# On Windows:
```bash
venv\Scripts\activate
```

# On Linux/Mac:
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

This includes:  

- Heading for clarity (`### 2️⃣ Backend Setup (Django)`)  
- Code block with all commands  
- Notes for Windows and Linux/Mac activation  
- Server URL displayed nicely  

---
### 3️⃣ Web Frontend Setup (React)

Navigate to the web-frontend folder, install dependencies, and start the development server:

```bash
cd web-frontend
npm install
npm start
```

---
### 4️⃣ Desktop App Setup (PyQt5)

Navigate to the desktop-app folder, install dependencies, and run the desktop application:

```bash
cd desktop-app
pip install -r requirements.txt
python main.py
```

### API Endpoints

. POST /api/upload/ – Upload CSV file

. GET /api/summary/ – Equipment statistics

. GET /api/history/ – Last 5 uploads



// identity fix
